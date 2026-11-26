"""Phase 7 unit tests: one function or method at a time, called directly, with no pages.

They are black-box tests. For each function we chose the equivalence classes of its input and
tested one value from each class, plus the values at the boundaries (for example 0.60 for the
classification threshold and AED 5,000 for the Finance threshold).
"""

from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from django.db import IntegrityError, transaction
from django.db.models import F

from accounts.models import Role, User
from ai.classification import ClassificationService
from ai.matching import RankingModel, confidence_label
from ai.report_drafts import unsupported_numbers
from assets.models import Asset, Listing
from audit.lifecycle import BusinessRuleError, TransitionNotAllowed, change_state
from audit.models import AuditLog
from resource_requests.models import ResourceRequest
from transfers.models import Transfer, add_working_days

from .helpers import PASSWORD, DemoTestCase


class SignInUnitTests(DemoTestCase):
    def test_sign_in_lockout_classes(self):
        """User.sign_in: right password, 1 to 4 wrong passwords, the 5th wrong one, and a locked account."""
        user = User.objects.get(username="comp.requester")
        self.assertTrue(user.sign_in(PASSWORD))                      # class 1: the right password
        for attempt in range(1, 5):                                  # class 2: 1 to 4 wrong passwords
            self.assertFalse(user.sign_in("wrong-password"))
            self.assertFalse(user.is_locked(), f"locked after only {attempt} wrong passwords")
        self.assertFalse(user.sign_in("wrong-password"))             # boundary: the 5th wrong password
        self.assertTrue(user.is_locked())
        self.assertFalse(user.sign_in(PASSWORD))                     # class 3: right password, locked account

    def test_role_action_table(self):
        """Role.allows: an action on the role's list, an action not on it, and an action that does not exist."""
        requester = Role.objects.get(code=Role.Code.REQUESTER)
        system_admin = Role.objects.get(code=Role.Code.SYSTEM_ADMINISTRATOR)
        self.assertTrue(requester.allows("request.submit"))
        self.assertFalse(requester.allows("report.view"))
        self.assertTrue(system_admin.allows("role.apply"))
        self.assertFalse(system_admin.allows("role.authorise"))
        self.assertFalse(requester.allows("no.such.action"))


class AssetUnitTests(DemoTestCase):
    def chairs(self):
        return Asset.objects.get(name="Ergonomic office chair")      # 6 units, all available

    def test_reserve_quantity_classes(self):
        """Asset.reserve: fewer units than are free, exactly the free units, and more than are free."""
        asset = self.chairs()
        asset.reserve(4)                                             # class 1: fewer than the 6 free units
        self.assertEqual((asset.available_qty, asset.reserved_qty), (2, 4))
        asset.reserve(2)                                             # boundary: exactly the 2 units left
        self.assertEqual((asset.available_qty, asset.reserved_qty), (0, 6))
        with self.assertRaises(BusinessRuleError):                   # class 2: more than are free
            asset.reserve(1)
        asset.refresh_from_db()
        self.assertEqual((asset.available_qty, asset.reserved_qty), (0, 6))

    def test_database_refuses_more_units_than_exist(self):
        """The check constraint on the asset table: available + reserved + allocated cannot pass the quantity."""
        asset = self.chairs()
        with self.assertRaises(IntegrityError), transaction.atomic():
            Asset.objects.filter(pk=asset.pk).update(reserved_qty=F("quantity") + 1)
        asset.refresh_from_db()
        self.assertEqual(asset.reserved_qty, 0)

    def test_state_table_classes(self):
        """change_state: a move the state diagram allows, a move it does not allow, and the same state again."""
        asset = self.chairs()                                        # In storage (AS-03)
        actor = User.objects.get(username="eng.custodian")
        with self.assertRaises(TransitionNotAllowed):                # not allowed: In storage to Donated
            change_state(asset, Asset.Status.DONATED, actor, "test")
        with self.assertRaises(TransitionNotAllowed):                # the same state again
            change_state(asset, Asset.Status.IN_STORAGE, actor, "test")
        asset.refresh_from_db()
        self.assertEqual(asset.status, Asset.Status.IN_STORAGE)
        entries = AuditLog.for_record(asset).count()
        change_state(asset, Asset.Status.IN_SERVICE, actor, "put into use")   # allowed
        self.assertEqual(asset.status, Asset.Status.IN_SERVICE)
        self.assertEqual(asset.previous_status, Asset.Status.IN_STORAGE)
        self.assertEqual(AuditLog.for_record(asset).count(), entries + 1)

    def test_missing_fields_for_confirmation(self):
        """Asset.missing_for_confirmation: every field filled, one field empty, and several fields empty."""
        asset = self.chairs()
        self.assertEqual(asset.missing_for_confirmation(), [])
        asset.category = None
        self.assertEqual([str(label) for label in asset.missing_for_confirmation()], ["Category"])
        asset.room, asset.value = "", None
        self.assertEqual(len(asset.missing_for_confirmation()), 3)


class ThresholdUnitTests(DemoTestCase):
    def test_classification_threshold_classes(self):
        """ClassificationService.can_prefill: no confidence, below 0.60, exactly 0.60, and above 0.60."""
        cases = [(None, False), ("0.333", False), ("0.599", False), ("0.600", True), ("0.667", True), ("1.000", True)]
        for confidence, expected in cases:
            with self.subTest(confidence=confidence):
                suggestion = SimpleNamespace(confidence=None if confidence is None else Decimal(confidence))
                self.assertEqual(ClassificationService.can_prefill(suggestion), expected)

    def test_match_confidence_label_classes(self):
        """confidence_label: no confidence, below 0.50, 0.50 to below 0.75, and 0.75 or above."""
        self.assertIn("unavailable", confidence_label(None))
        self.assertIn("Withheld", confidence_label(0.49))
        self.assertIn("check carefully", confidence_label(0.50))     # boundary
        self.assertIn("check carefully", confidence_label(0.74))
        self.assertEqual(confidence_label(0.75), "Confidence 0.75")  # boundary
        self.assertEqual(confidence_label(0.90), "Confidence 0.90")

    def test_finance_threshold_classes(self):
        """Transfer.needs_finance: below AED 5,000, exactly AED 5,000, above it, and an asset with no value."""
        cases = [("4999.99", 1, False), ("5000.00", 1, True), ("2700.00", 2, True), (None, 3, False)]
        for value, quantity, expected in cases:
            with self.subTest(value=value, quantity=quantity):
                asset = Asset(value=None if value is None else Decimal(value))
                self.assertEqual(Transfer(asset=asset, quantity=quantity).needs_finance(), expected)

    def test_working_days_skip_the_weekend(self):
        """add_working_days: no days, a count that stays inside the week, and counts that cross a weekend."""
        friday, monday = date(2026, 11, 20), date(2026, 11, 23)
        self.assertEqual(add_working_days(monday, 0), monday)
        self.assertEqual(add_working_days(monday, 4), date(2026, 11, 27))     # Monday to Friday
        self.assertEqual(add_working_days(friday, 1), monday)                 # skips Saturday and Sunday
        self.assertEqual(add_working_days(monday, 5), date(2026, 11, 30))     # the hold period of 5 working days


class ScoreUnitTests(DemoTestCase):
    def setUp(self):
        self.request = ResourceRequest.objects.get(purpose="Chairs for the robotics lab")
        self.listing = Listing.objects.get(asset__name="Ergonomic office chair")
        self.ranking = RankingModel()

    def points(self, factor_number, similarity=0.5):
        return self.ranking.score(self.request, self.listing, similarity)[1][factor_number]["points"]

    def test_meaning_points_follow_the_ai_number(self):
        """RankingModel.score, meaning factor: the lowest AI number, a middle one and the highest."""
        for similarity, expected in [(0.0, 0), (0.5, 15), (1.0, 30)]:
            with self.subTest(similarity=similarity):
                self.assertEqual(self.points(0, similarity), expected)

    def test_condition_points_classes(self):
        """RankingModel.score, condition factor: equal to the minimum, one level above, and two or more above."""
        self.listing.asset.condition = "fair"
        for minimum, expected in [("fair", 5), ("poor", 10), ("not_working", 15)]:
            with self.subTest(minimum=minimum):
                self.request.min_condition = minimum
                self.assertEqual(self.points(2), expected)

    def test_total_is_the_sum_of_the_factors(self):
        """RankingModel.score: the total always equals the factor points added up, and stays within 0 to 100."""
        for similarity in (0.0, 0.37, 1.0):
            total, factors = self.ranking.score(self.request, self.listing, similarity)
            self.assertEqual(total, sum(factor["points"] for factor in factors))
            self.assertEqual(sum(factor["max"] for factor in factors), 100)
            self.assertTrue(0 <= total <= 100)


class FiguresCheckUnitTests(DemoTestCase):
    FIGURES = ("Period: 01 Jan 2026 to 24 Nov 2026\nDepartment: All departments\nItems reused: 21\n"
               "Net financial savings (AED): 4,940\nCarbon saved, low estimate (kg CO2e): 253.56")

    def test_figures_check_classes(self):
        """unsupported_numbers: numbers that are in the figures, and four kinds of number that are not."""
        ok = "We reused 21 items and saved AED 4,940 in 2026. About 253.6 kg CO2e was saved."
        self.assertEqual(unsupported_numbers(ok, self.FIGURES), [])              # figures, the year, a rounded figure
        self.assertEqual(unsupported_numbers("We saved AED 9,999.", self.FIGURES), ["9,999"])       # an invented number
        self.assertEqual(unsupported_numbers("We reused 22 items.", self.FIGURES), ["22"])          # a wrong figure
        self.assertEqual(unsupported_numbers("We reused twenty items.", self.FIGURES), ["twenty"])  # a number in words
        self.assertEqual(unsupported_numbers("We saved AED 4,940 in 2025.", self.FIGURES), ["2025"])  # another year
