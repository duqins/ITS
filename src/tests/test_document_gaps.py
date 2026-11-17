"""Parts of the SRS and design that the first Phase 6 build left out: photos and documents (FR-04.1, AI-01.1),
the request description (FR-07.1), the search columns (UI-05), the approval stage tracker (UI-08) and the
role administration of UI-14 (FR-01.3, BR-01, BR-02)."""

from datetime import date, timedelta
from io import BytesIO
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from PIL import Image

from accounts.models import Role, User, UserRole
from assets.models import Asset, AssetFile, Listing
from audit.models import AuditLog
from resource_requests.models import ResourceRequest
from transfers.models import Reservation, Transfer

from .helpers import DemoTestCase, FakeClaude


def photo(name="monitor.png", size=(900, 600), image_format="PNG"):
    out = BytesIO()
    Image.new("RGB", size, (40, 120, 110)).save(out, image_format)
    return SimpleUploadedFile(name, out.getvalue(), content_type="image/png")


def pdf(name="spec-sheet.pdf"):
    return SimpleUploadedFile(name, b"%PDF-1.4\n% synthetic spec sheet\n%%EOF\n", content_type="application/pdf")


ASSET = {"kind": "general", "name": "Dell 24-inch monitor", "description": "small scratch on the frame",
         "condition": "good", "quantity": 1, "campus": "Main campus"}
COMPLETE = {"specifications": "24-inch, HDMI", "building": "Engineering Building", "room": "E2-114",
            "purchase_date": "2023-09-15", "value": "345"}


class PhotoAndDocumentTests(DemoTestCase):
    def register(self, client, **files):
        return client.post("/assets/register/", {**ASSET, **files}, follow=True)

    def test_a_custodian_adds_photos_and_a_document_when_registering(self):
        client = self.sign_in("eng.custodian")
        self.register(client, photos=[photo(), photo("side.jpg", image_format="JPEG")], documents=[pdf()])
        asset = Asset.objects.get(name=ASSET["name"])
        photos = asset.files.filter(kind=AssetFile.Kind.PHOTO)
        self.assertEqual(photos.count(), 2)
        first = photos.first()
        self.assertEqual(first.content_type, "image/jpeg")
        self.assertLessEqual(max(Image.open(BytesIO(bytes(first.data))).size), 1568)
        self.assertLessEqual(max(Image.open(BytesIO(bytes(first.thumbnail))).size), 480)
        self.assertTrue(AuditLog.objects.filter(action="files changed", record_id=asset.pk).exists())
        page = client.get(f"/assets/{asset.pk}/").content.decode()
        self.assertIn(f"/assets/{asset.pk}/files/{first.pk}/?size=small", page)
        self.assertIn("spec-sheet.pdf", page)
        document = asset.files.get(kind=AssetFile.Kind.DOCUMENT)
        response = client.get(f"/assets/{asset.pk}/files/{document.pk}/")
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(response["Content-Disposition"].startswith("attachment"))

    def test_only_real_jpg_or_png_photos_and_pdf_documents_are_accepted(self):
        client = self.sign_in("eng.custodian")
        fake = SimpleUploadedFile("photo.jpg", b"not really a photo", content_type="image/jpeg")
        response = self.register(client, photos=[fake])
        self.assertContains(response, "photo.jpg is not a JPG or PNG photo.")
        self.assertContains(response, "Please choose your photos and documents again")
        response = self.register(client, documents=[SimpleUploadedFile("notes.pdf", b"plain text")])
        self.assertContains(response, "notes.pdf is not a PDF document.")
        response = self.register(client, photos=[photo(f"p{i}.png") for i in range(6)])
        self.assertContains(response, "An asset can have up to 5 photos.")
        # A small file can still hold a huge image; it is refused before it is decoded.
        response = self.register(client, photos=[photo("huge.png", size=(7000, 7000))])
        self.assertContains(response, "huge.png has too many pixels.")
        big = SimpleUploadedFile("big.jpg", b"x" * (5 * 1024 * 1024 + 1), content_type="image/jpeg")
        self.assertContains(self.register(client, photos=[big]), "big.jpg is larger than 5 MB.")
        big = SimpleUploadedFile("big.pdf", b"%PDF-" + b"x" * (10 * 1024 * 1024), content_type="application/pdf")
        self.assertContains(self.register(client, documents=[big]), "big.pdf is larger than 10 MB.")
        response = self.register(client, documents=[pdf(f"d{i}.pdf") for i in range(6)])
        self.assertContains(response, "An asset can have up to 5 documents.")
        self.assertFalse(Asset.objects.filter(name=ASSET["name"]).exists())
        # A big camera photo, and a phone JPEG with a second picture inside (MPO), are accepted and stored small.
        out = BytesIO()
        Image.new("RGB", (4000, 3000), "navy").save(out, "MPO", save_all=True,
                                                    append_images=[Image.new("RGB", (640, 480), "grey")])
        phone = SimpleUploadedFile("phone.jpg", out.getvalue(), content_type="image/jpeg")
        self.register(client, photos=[photo("camera.jpg", size=(6000, 4000), image_format="JPEG"), phone])
        stored = Asset.objects.get(name=ASSET["name"]).files.order_by("pk")
        self.assertEqual([max(Image.open(BytesIO(bytes(f.data))).size) for f in stored], [1568, 1568])

    def test_panoramas_are_accepted_but_huge_progressive_jpegs_are_not(self):
        client = self.sign_in("eng.custodian")
        out = BytesIO()
        Image.new("RGB", (6000, 5000), "teal").save(out, "JPEG", progressive=True)
        huge = SimpleUploadedFile("huge.jpg", out.getvalue(), content_type="image/jpeg")
        self.assertContains(self.register(client, photos=[huge]), "huge.jpg has too many pixels.")
        self.register(client, photos=[photo("panorama.jpg", size=(12000, 2000), image_format="JPEG")])
        stored = Asset.objects.get(name=ASSET["name"]).files.get()
        self.assertEqual(Image.open(BytesIO(bytes(stored.data))).size, (1568, 261))

    def test_photos_of_a_draft_stay_in_the_department_but_published_items_show_them(self):
        custodian = self.sign_in("eng.custodian")
        self.register(custodian, photos=[photo()])
        draft = Asset.objects.get(name=ASSET["name"]).files.get()
        requester = self.sign_in("comp.requester")
        self.assertEqual(requester.get(f"/assets/{draft.asset_id}/files/{draft.pk}/").status_code, 403)
        listing = Listing.objects.filter(status=Listing.Status.PUBLISHED).first()
        AssetFile.objects.create(asset=listing.asset, kind=AssetFile.Kind.PHOTO, name="chair.jpg",
                                 content_type="image/jpeg", size=3, data=b"abc", thumbnail=b"ab",
                                 uploaded_by=User.objects.get(username="eng.custodian"))
        shown = listing.asset.files.get()
        response = requester.get(f"/assets/{listing.asset_id}/files/{shown.pk}/?size=small")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ab")
        search = requester.get("/assets/search/").content.decode()
        self.assertIn(f"/assets/{listing.asset_id}/files/{shown.pk}/?size=small", search)

    def test_a_draft_edit_can_remove_a_photo(self):
        client = self.sign_in("eng.custodian")
        self.register(client, photos=[photo(), photo("b.png")])
        asset = Asset.objects.get(name=ASSET["name"])
        first = asset.files.first()
        client.post(f"/assets/{asset.pk}/edit/", {**ASSET, "remove_files": [first.pk]})
        self.assertEqual(list(asset.files.values_list("name", flat=True)), ["b.png"])

    def test_the_classification_reads_the_photos(self):
        from ai.classification import ClassificationAnswer
        client = self.sign_in("eng.custodian")
        self.register(client, photos=[photo()], documents=[pdf()])
        asset = Asset.objects.get(name=ASSET["name"])
        seen = []

        class WithDescription(ClassificationAnswer):  # what answer_format asks Claude for
            description: str

        def answer(content):
            seen.append(content)
            return WithDescription(category="IT equipment / Monitor", condition="not_working", tags=["monitor"],
                                   reason="The photo shows a monitor.", missing_details=[],
                                   description="Dell 24-inch monitor with a small scratch on the frame.")

        fake = FakeClaude({ClassificationAnswer: answer})
        with self.settings(ANTHROPIC_API_KEY="test-key"), mock.patch("ai.adapter.anthropic.Anthropic", return_value=fake):
            client.post(f"/ai/assets/{asset.pk}/classify/")
        self.assertEqual(seen[0][0]["type"], "image")
        self.assertEqual(seen[0][0]["source"]["media_type"], "image/jpeg")
        self.assertIn("Dell 24-inch monitor", seen[0][-1]["text"])
        page = client.get(f"/assets/{asset.pk}/").content.decode()
        self.assertIn("The AI also looked at 1 photo.", page)
        self.assertIn("The AI does not read supporting documents (spec-sheet.pdf).", page)
        self.assertIn("Not working", page)  # the condition as people read it, not "not_working"
        self.assertIn("Description: Dell 24-inch monitor with a small scratch on the frame.", page)
        suggestion = asset.ai_suggestions.get()
        client.post(f"/ai/suggestions/{suggestion.pk}/respond/", {"decision": "accept"})
        asset.refresh_from_db()
        self.assertEqual(asset.description, "Dell 24-inch monitor with a small scratch on the frame.")

    def test_only_two_photos_go_to_the_ai_and_the_panel_says_so(self):
        from ai.classification import ClassificationAnswer
        client = self.sign_in("eng.custodian")
        self.register(client, photos=[photo(f"p{i}.png") for i in range(3)])
        asset = Asset.objects.get(name=ASSET["name"])
        seen = []
        fake = FakeClaude({ClassificationAnswer: lambda content: seen.append(content) or ClassificationAnswer(
            category="IT equipment / Monitor", condition="good", tags=["monitor"], reason="A monitor.",
            missing_details=[])})
        with self.settings(ANTHROPIC_API_KEY="test-key"), mock.patch("ai.adapter.anthropic.Anthropic", return_value=fake):
            client.post(f"/ai/assets/{asset.pk}/classify/")
        self.assertEqual([block["type"] for block in seen[0]], ["image", "image", "text"])
        self.assertContains(client.get(f"/assets/{asset.pk}/"), "The AI looked at the first 2 of 3 photos. Check the others yourself: p2.png.")

    def test_confirmation_needs_the_mandatory_fields(self):
        """FR-04.2: a draft can be saved early, but a missing mandatory field keeps it in Draft."""
        self.register(self.sign_in("eng.custodian"))
        asset = Asset.objects.get(name=ASSET["name"])
        mariam = self.sign_in("eng.rep")
        page = mariam.get(f"/assets/{asset.pk}/").content.decode()
        self.assertIn("Complete these fields before confirming: Category, Specifications, Building, Room, "
                      "Purchase date, Estimated value per item (AED).", page)
        response = mariam.post(f"/assets/{asset.pk}/confirm/", {"placement": "in_storage"}, follow=True)
        self.assertContains(response, "Complete these fields before confirming")
        asset.refresh_from_db()
        self.assertEqual(asset.status, Asset.Status.DRAFT)

    def test_a_possible_duplicate_needs_a_second_confirmation(self):
        """FR-04.5: same department, category, name and specifications."""
        client = self.sign_in("eng.custodian")
        self.register(client, **COMPLETE)
        response = self.register(client, **COMPLETE)
        self.assertContains(response, "has the same category, name and specifications")
        self.assertEqual(Asset.objects.filter(name=ASSET["name"]).count(), 1)
        self.register(client, not_duplicate="on", **COMPLETE)
        self.assertEqual(Asset.objects.filter(name=ASSET["name"]).count(), 2)

    def test_a_value_cannot_be_negative(self):
        response = self.register(self.sign_in("eng.custodian"), value="-5")
        self.assertContains(response, "The value cannot be negative.")

    def test_a_partial_transfer_keeps_the_photos_on_the_new_record(self):
        users = {u.username: u for u in User.objects.all()}
        chairs = Listing.objects.get(asset__name__startswith="Ergonomic")
        AssetFile.objects.create(asset=chairs.asset, kind=AssetFile.Kind.PHOTO, name="chair.jpg",
                                 content_type="image/jpeg", size=3, data=b"abc", thumbnail=b"ab",
                                 uploaded_by=users["eng.custodian"])
        request = ResourceRequest.objects.get(purpose__startswith="Chairs")
        request.approve(users["comp.rep"])
        hold = Reservation.request_hold(request, chairs, users["comp.requester"])
        hold.confirm(users["eng.custodian"])
        transfer = Transfer.start(hold, users["comp.requester"], users["comp.custodian"], planned_date=date.today())
        for approver in ("eng.rep", "comp.rep", "finance.officer", "procurement.officer"):
            if transfer.pending_approvals().exists():
                transfer.approve_stage(users[approver])
        transfer.hand_over(users["eng.custodian"], chairs.asset.condition)
        transfer.confirm_receipt(users["comp.custodian"], transfer.quantity, chairs.asset.condition)
        transfer.refresh_from_db()
        self.assertNotEqual(transfer.received_asset_id, chairs.asset_id)  # 4 of 6 chairs: a new record
        self.assertEqual(list(transfer.received_asset.files.values_list("name", flat=True)), ["chair.jpg"])


class RequestAndSearchTests(DemoTestCase):
    def test_a_request_can_carry_an_optional_description(self):
        client = self.sign_in("comp.requester")
        request = ResourceRequest.objects.filter(requester__username="comp.requester").first()
        form = client.get("/requests/new/").content.decode()
        self.assertIn('name="description"', form)
        client.post("/requests/new/", {
            "purpose": "Monitor for the teaching assistant desk", "category": request.category_id,
            "specifications": "24-inch", "quantity": 1, "min_condition": "good", "urgency": "normal",
            "delivery_location": "C2-110", "required_by": self.future(), "description": "Near the window, please.",
            "submit_for": "draft"})
        created = ResourceRequest.objects.get(purpose="Monitor for the teaching assistant desk")
        self.assertEqual(created.description, "Near the window, please.")
        self.assertContains(client.get(f"/requests/{created.pk}/"), "Near the window, please.")

    def test_search_shows_restrictions_and_when_the_item_was_last_verified(self):
        listing = Listing.objects.filter(status=Listing.Status.PUBLISHED).first()
        listing.restrictions = "Collection required"
        listing.save()
        page = self.sign_in("comp.requester").get("/assets/search/").content.decode()
        self.assertIn("<th>Restrictions</th>", page)
        self.assertIn("<td>Collection required</td>", page)
        self.assertIn("<th>Last verified</th>", page)
        self.assertIn(timezone.localdate().strftime("%d %b %Y"), page)
        self.assertNotIn("Verification needed", page)

    def test_an_old_check_shows_verification_needed_until_the_custodian_verifies_again(self):
        """FR-06.4, BR-16."""
        listing = Listing.objects.filter(status=Listing.Status.PUBLISHED, asset__owner_department__code="ENG").first()
        Asset.objects.filter(pk=listing.asset_id).update(verified_on=timezone.now() - timedelta(days=120))
        requester = self.sign_in("comp.requester")
        self.assertContains(requester.get("/assets/search/"), "Verification needed")
        self.assertContains(requester.get(f"/assets/listings/{listing.pk}/"), "Verification needed")
        khalid = self.sign_in("eng.custodian")
        khalid.post(f"/assets/{listing.asset_id}/verify/")
        self.assertNotContains(requester.get("/assets/search/"), "Verification needed")
        page = khalid.get(f"/assets/{listing.asset_id}/").content.decode()
        self.assertIn("by Khalid Al Mansoori", page)
        self.assertEqual(self.sign_in("comp.requester").post(f"/assets/{listing.asset_id}/verify/").status_code, 403)

    def test_the_home_page_counts_assets_needing_verification_and_lists_them(self):
        """UI-02: the seeded standing desks were last checked 120 days ago."""
        desks = Asset.objects.get(name="Standing desk")
        fatima = self.sign_in("comp.custodian")
        home = fatima.get("/").content.decode()
        self.assertRegex(home, r'<a class="card has-work" href="/assets/\?verification=needed"><svg[^>]*>.*?</svg>'
                               r'<div class="number" data-count="1">1</div><div class="label">Assets needing '
                               r'verification</div></a>')
        self.assertIn('class="card is-zero"', home)
        listed = fatima.get("/assets/?verification=needed").content.decode()
        self.assertIn(desks.code, listed)
        self.assertIn("Verification needed", listed)
        self.assertEqual(listed.count("<tr><td><a href="), 1)  # only the desks
        fatima.post(f"/assets/{desks.pk}/verify/")
        self.assertIn('<a class="card is-zero" href="/assets/?verification=needed">', fatima.get("/").content.decode())
        self.assertNotIn(desks.code, fatima.get("/assets/?verification=needed").content.decode())


class ApprovalStageTests(DemoTestCase):
    def test_a_request_approval_shows_its_stages_and_the_next_one(self):
        pending = ResourceRequest.objects.get(status=ResourceRequest.Status.PENDING_APPROVAL)
        page = self.sign_in("comp.rep").get(f"/transfers/approvals/{pending.approvals.get().pk}/").content.decode()
        self.assertIn('aria-label="Approval stages"', page)
        self.assertIn('<li class="current"><span class="step-dot">2</span>Department review</li>', page)
        self.assertIn("Open (RQ-03): the requester can search for a match and ask for a hold.", page)
        self.sign_in("comp.rep").post(f"/transfers/approvals/{pending.approvals.get().pk}/",
                                      {"decision": "reject", "reason": "No budget"})
        page = self.sign_in("comp.rep").get(f"/transfers/approvals/{pending.approvals.get().pk}/").content.decode()
        self.assertIn(f"This stage is decided. {pending.code} is now Rejected.", page)

    def test_a_transfer_approval_shows_release_receipt_and_approved(self):
        users = {u.username: u for u in User.objects.all()}
        request = ResourceRequest.objects.get(purpose__startswith="Chairs")
        request.approve(users["comp.rep"])
        listing = Listing.objects.get(asset__name__startswith="Ergonomic")
        hold = Reservation.request_hold(request, listing, users["comp.requester"])
        hold.confirm(users["eng.custodian"])
        transfer = Transfer.start(hold, users["comp.requester"], users["comp.custodian"], planned_date=date.today())
        approval = transfer.approvals.get()
        page = self.sign_in("eng.rep").get(f"/transfers/approvals/{approval.pk}/").content.decode()
        self.assertIn('<li class="current"><span class="step-dot">1</span>Release approval</li>', page)
        self.assertIn("Pending receipt approval (TR-02): the Computing representative decides.", page)
        self.assertIn("Approved</li>", page)
        self.assertIn(request.code, page)  # the evidence names the request (mockup 7.4)


class RoleAdministrationTests(DemoTestCase):
    def waiting(self):
        return UserRole.objects.get(user__username="maintenance.staff", role__code="requester")

    def test_a_role_needs_a_request_an_independent_authorisation_and_an_application(self):
        self.assertEqual(self.waiting().status, UserRole.Status.REQUESTED)
        latifa = self.sign_in("business.admin")
        page = latifa.get("/accounts/administration/").content.decode()
        self.assertIn("Yousef Al Ali", page)
        self.assertIn('value="authorise"', page)
        latifa.post(f"/accounts/administration/roles/{self.waiting().pk}/", {"decision": "authorise"})
        self.assertEqual(self.waiting().status, UserRole.Status.AUTHORISED)
        reem = self.sign_in("system.admin")
        self.assertIn('value="apply"', reem.get("/accounts/administration/").content.decode())
        reem.post(f"/accounts/administration/roles/{self.waiting().pk}/", {"decision": "apply"})
        self.assertEqual(self.waiting().status, UserRole.Status.ACTIVE)
        self.assertTrue(User.objects.get(username="maintenance.staff").has_role(Role.Code.REQUESTER))
        self.assertEqual(AuditLog.objects.filter(action__in=("role requested", "role authorised", "role applied"))
                         .count(), 3)

    def test_nobody_decides_their_own_role_request_and_application_needs_authorisation(self):
        khalfan = self.sign_in("business.admin2")
        page = khalfan.get("/accounts/administration/").content.decode()
        self.assertIn("Another Business administrator decides this (BR-02).", page)
        khalfan.post(f"/accounts/administration/roles/{self.waiting().pk}/", {"decision": "authorise"})
        self.assertEqual(self.waiting().status, UserRole.Status.REQUESTED)
        self.assertTrue(AuditLog.objects.filter(action="blocked: authorise role").exists())
        self.sign_in("system.admin").post(f"/accounts/administration/roles/{self.waiting().pk}/", {"decision": "apply"})
        self.assertEqual(self.waiting().status, UserRole.Status.REQUESTED)
        # A Business administrator cannot apply, and a System administrator cannot authorise (BR-01).
        response = self.sign_in("business.admin").post(f"/accounts/administration/roles/{self.waiting().pk}/",
                                                      {"decision": "apply"})
        self.assertEqual(response.status_code, 403)
        response = self.sign_in("system.admin").post(f"/accounts/administration/roles/{self.waiting().pk}/",
                                                    {"decision": "authorise"})
        self.assertEqual(response.status_code, 403)

    def test_the_three_steps_are_done_by_three_different_people(self):
        users = {u.username: u for u in User.objects.all()}
        system_admin = Role.objects.get(code="system_administrator")
        # One person holding both administrator roles cannot authorise and then apply the same request.
        UserRole.objects.create(user=users["business.admin"], role=system_admin, department=users["business.admin"]
                                .department, status=UserRole.Status.ACTIVE)
        latifa = self.sign_in("business.admin", role="business_administrator")
        latifa.post(f"/accounts/administration/roles/{self.waiting().pk}/", {"decision": "authorise"})
        latifa = self.sign_in("business.admin", role="system_administrator")
        latifa.post(f"/accounts/administration/roles/{self.waiting().pk}/", {"decision": "apply"})
        self.assertEqual(self.waiting().status, UserRole.Status.AUTHORISED)
        # A System administrator cannot apply a role to their own account.
        own = UserRole.request(users["system.admin"], Role.objects.get(code="business_administrator"),
                               users["system.admin"].department, by=users["business.admin2"])
        own.authorise(users["business.admin"])
        self.sign_in("system.admin").post(f"/accounts/administration/roles/{own.pk}/", {"decision": "apply"})
        own.refresh_from_db()
        self.assertEqual(own.status, UserRole.Status.AUTHORISED)
        # Nobody decides a request for their own account.
        mine = UserRole.request(users["business.admin"], Role.objects.get(code="requester"),
                                users["business.admin"].department, by=users["business.admin2"])
        self.sign_in("business.admin").post(f"/accounts/administration/roles/{mine.pk}/", {"decision": "authorise"})
        mine.refresh_from_db()
        self.assertEqual(mine.status, UserRole.Status.REQUESTED)

    def test_the_requester_can_withdraw_a_role_request(self):
        khalfan = self.sign_in("business.admin2")
        self.assertIn('value="withdraw"', khalfan.get("/accounts/administration/").content.decode())
        self.sign_in("business.admin").post(f"/accounts/administration/roles/{self.waiting().pk}/",
                                            {"decision": "withdraw"})
        self.assertEqual(self.waiting().status, UserRole.Status.REQUESTED)  # only the one who asked
        khalfan.post(f"/accounts/administration/roles/{self.waiting().pk}/", {"decision": "withdraw"})
        self.assertEqual(self.waiting().status, UserRole.Status.REMOVED)

    def test_the_page_shows_the_proposed_thresholds(self):
        page = self.sign_in("business.admin").get("/accounts/administration/").content.decode()
        self.assertIn("AED 5,000", page)
        self.assertIn("90 days", page)
        self.assertIn("Proposed", page)

    def test_a_rejection_needs_a_reason_and_gives_no_role(self):
        latifa = self.sign_in("business.admin")
        latifa.post(f"/accounts/administration/roles/{self.waiting().pk}/", {"decision": "reject", "reason": ""})
        self.assertEqual(self.waiting().status, UserRole.Status.REQUESTED)
        latifa.post(f"/accounts/administration/roles/{self.waiting().pk}/", {"decision": "reject", "reason": "Not needed"})
        self.assertEqual(self.waiting().status, UserRole.Status.REJECTED)
        self.assertFalse(User.objects.get(username="maintenance.staff").has_role(Role.Code.REQUESTER))

    def test_a_business_administrator_requests_a_role_from_the_page(self):
        latifa = self.sign_in("business.admin")
        fatima = User.objects.get(username="comp.custodian")
        latifa.post("/accounts/administration/", {"user": fatima.pk, "role": Role.objects.get(code="requester").pk,
                                                  "department": fatima.department_id})
        assignment = UserRole.objects.get(user=fatima, role__code="requester")
        self.assertEqual((assignment.status, assignment.requested_by.username), ("requested", "business.admin"))

    def test_the_administration_site_cannot_change_roles_or_business_records(self):
        reem = self.sign_in("system.admin")
        self.assertEqual(reem.get("/admin/accounts/user/").status_code, 200)
        self.assertEqual(reem.get("/admin/transfers/approval/").status_code, 403)
        change = reem.get(f"/admin/accounts/user/{User.objects.get(username='comp.requester').pk}/change/")
        self.assertNotContains(change, "is_superuser")
        aisha = User.objects.get(username="comp.requester")
        reem.post(f"/admin/accounts/user/{aisha.pk}/change/", {"username": aisha.username, "is_superuser": "on",
                                                              "is_staff": "on", "account_status": "active"})
        aisha.refresh_from_db()
        self.assertFalse(aisha.is_superuser or aisha.is_staff)
        self.assertEqual(reem.get(f"/admin/accounts/userrole/{self.waiting().pk}/change/").status_code, 200)
        reem.post(f"/admin/accounts/userrole/{self.waiting().pk}/change/", {"status": "active"})
        self.assertEqual(self.waiting().status, UserRole.Status.REQUESTED)
        # An administrator account is out of reach: no password reset, so nobody can act as a Business admin.
        latifa = User.objects.get(username="business.admin")
        self.assertEqual(reem.get(f"/admin/accounts/user/{latifa.pk}/password/").status_code, 403)
        # A rejected administrator request does not lock the System administrator out of an ordinary account.
        fatima = User.objects.get(username="comp.custodian")
        refused = UserRole.request(fatima, Role.objects.get(code="business_administrator"), fatima.department,
                                   by=latifa)
        refused.reject(User.objects.get(username="business.admin2"), "Not needed")
        self.assertEqual(reem.get(f"/admin/accounts/user/{fatima.pk}/password/").status_code, 200)
        reem.post(f"/admin/accounts/user/{latifa.pk}/password/", {"password1": "x-New-pass-42",
                                                                  "password2": "x-New-pass-42"})
        latifa.refresh_from_db()
        self.assertTrue(latifa.check_password("dawra-demo-2026"))

    def test_only_administrators_see_the_menu_entry(self):
        self.assertIn("/accounts/administration/", self.sign_in("system.admin").get("/").content.decode())
        self.assertNotIn("/accounts/administration/", self.sign_in("comp.requester").get("/").content.decode())
        self.assertEqual(self.sign_in("comp.requester").get("/accounts/administration/").status_code, 403)
