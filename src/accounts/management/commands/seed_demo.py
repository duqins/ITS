"""Create synthetic demo data: departments, the nine roles, one user per role, categories and assets.

Run once on an empty database:  python manage.py seed_demo
The demo password comes from DEMO_PASSWORD (default for local use only: dawra-demo-2026).
Everything is synthetic; no real KU people or records.

Besides the records used in the demo script, it adds:
- nine transfers that finished between about five months and one week ago, so the dashboard and its graph
  have months of history (money only comes from monitors, the one category with a cited price);
- more published items for search, and work that is waiting longer than 3 working days (overdue).
The history runs through the real workflow (request, approvals, hold, transfer, receipt); only its dates are
moved back afterwards, so every table tells the same story.
"""

import os
from contextlib import contextmanager
from datetime import date, datetime, time, timedelta
from decimal import Decimal

from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from accounts.models import Department, Role, User, UserRole
from assets.models import Asset, Category, Condition, FurnitureAsset, ITAsset, Listing
from audit.models import AuditLog
from notifications.models import Notification
from resource_requests.models import ResourceRequest
from sustainability.models import SustainabilityImpact
from transfers.models import Approval, Reservation, Transfer

# The time fields the workflow fills in. For the synthetic history they are moved back to the day the step
# "happened". Asset.verified_on is left alone, so no asset suddenly needs verification (FR-06.4).
DATED_FIELDS = [
    (Asset, ["created_at", "updated_at"]),
    (Listing, ["created_at", "published_at"]),
    (ResourceRequest, ["created_at", "submitted_at", "updated_at"]),
    (Approval, ["created_at", "decided_at"]),
    (Reservation, ["created_at"]),  # expires_at is set once the whole story has run (see backdate_hold)
    (Transfer, ["created_at", "handed_over_at", "received_at"]),
    (SustainabilityImpact, ["created_at", "confirmed_at"]),
    (AuditLog, ["created_at"]),
    (Notification, ["sent_at"]),
]

# Transfers that already finished: (days ago the receipt was confirmed, asset type, category, name, description,
# specifications, tags, condition, quantity, value per item in AED, distance km, van trips, transfer cost AED,
# request purpose). All go from Engineering to Computing, the two departments with custodians in the demo.
HISTORY = [
    (160, ITAsset, "Monitor", "Dell P2422H monitors from the old CAD lab",
     "24-inch monitors left after the CAD lab moved to laptops.", "24-inch, HDMI and DisplayPort",
     "monitor, display, 24-inch", Condition.GOOD, 3, "345", "2", 1, "30", "Monitors for the Computing help desk"),
    (133, FurnitureAsset, "Office chair", "Mesh office chairs from the dean's office",
     "Mesh-back chairs replaced during an office refit.", "Adjustable height, armrests", "chair, seating, mesh",
     Condition.FAIR, 2, "380", "2", 1, "30", "Seating for the PhD student room"),
    (118, ITAsset, "Monitor", "Dell P2422H monitor from a staff office",
     "One spare 24-inch monitor after a staff member left.", "24-inch, HDMI", "monitor, display",
     Condition.GOOD, 1, "345", "1.5", 1, "15", "Second screen for the timetabling office"),
    (95, ITAsset, "Monitor", "HP E24 G4 monitors from a closed teaching lab",
     "24-inch monitors from a teaching lab that closed for renovation.", "24-inch, HDMI, USB hub",
     "monitor, display, 24-inch, usb", Condition.GOOD, 4, "345", "5", 1, "50", "Monitors for the networking lab"),
    (75, FurnitureAsset, "Desk", "Height-adjustable desk",
     "Electric sit-stand desk no longer needed after a team moved.", "Electric, 140 x 70 cm", "desk, standing",
     Condition.GOOD, 1, "1100", "2", 1, "30", "Accessible desk for a staff member"),
    (54, ITAsset, "Monitor", "Dell P2422H monitors from the robotics lab",
     "Monitors replaced by larger screens in the robotics lab.", "24-inch, HDMI", "monitor, display",
     Condition.FAIR, 2, "345", "2", 1, "40", "Monitors for the student project room"),
    (34, FurnitureAsset, "Office chair", "Stacking chairs from a seminar room",
     "Stacking chairs left after a seminar room got new furniture.", "Stackable, no wheels", "chair, seating",
     Condition.FAIR, 3, "200", "2", 1, "30", "Seating for the reading corner"),
    (19, ITAsset, "Monitor", "Philips 24-inch monitors",
     "Two monitors from an Engineering meeting room.", "24-inch, HDMI, speakers", "monitor, display, speakers",
     Condition.GOOD, 2, "345", "2", 1, "40", "Monitors for the Computing meeting room"),
    (8, ITAsset, "Monitor", "Dell P2422H monitor (spare)", "A spare monitor kept in Engineering storage.",
     "24-inch, HDMI", "monitor, display", Condition.GOOD, 1, "345", "2", 1, "20", "Monitor for a visiting lecturer"),
]

# Items published now, so search and the AI search have more to work with. They avoid the office chair and
# projector categories, so the demo's matching for chairs and the projector stays the same.
SUPPLY = [
    ("ENG", ITAsset, "Laptop", "Lenovo ThinkPad T14 laptops",
     "Laptops returned after a research project ended. Batteries hold about four hours.",
     "14-inch, Core i5, 16 GB RAM, 512 GB SSD", "laptop, notebook, portable", Condition.GOOD, 3, "3200",
     dict(stores_data=True)),
    ("ENG", Asset, "Textbook", "Engineering mathematics textbooks",
     "A class set of textbooks from a course that changed its reading list.",
     "Advanced Engineering Mathematics, 10th edition", "book, textbook, mathematics", Condition.FAIR, 12, "120", {}),
    ("ENG", Asset, "Stationery", "Whiteboard markers and stationery boxes",
     "Unopened boxes left after an event.", "Markers, sticky notes, folders", "stationery, markers, office",
     Condition.NEW, 6, "40", {}),
    ("ENG", Asset, "Measurement", "Bench power supplies",
     "Two DC power supplies from an electronics teaching bench.", "0 to 30 V, 3 A, two channels",
     "power supply, lab, electronics", Condition.GOOD, 2, "900", {}),
    ("COMP", FurnitureAsset, "Desk", "Sit-stand desks",
     "Two desks left after the Computing office was rearranged.", "Electric height adjustment, 140 x 70 cm",
     "desk, standing, office", Condition.GOOD, 2, "1100", dict(material="Steel frame, laminate top")),
    ("COMP", ITAsset, "Monitor", "HP E24 G5 monitors",
     "Monitors replaced by docking stations with larger screens.", "24-inch, HDMI, USB-C",
     "monitor, display, usb-c", Condition.GOOD, 2, "345", dict(stores_data=False)),
]

DEPARTMENTS = [
    ("Engineering", "ENG"), ("Computing", "COMP"), ("Facilities Management", "FM"), ("Finance", "FIN"),
    ("Procurement", "PROC"), ("Sustainability Office", "SUS"), ("Business Administration", "BA"),
    ("IT Services", "ITS"),
]

# username, first name, last name, department code, [(role, department code)]
USERS = [
    ("eng.rep", "Mariam", "Al Hosani", "ENG", [("department_representative", "ENG")]),
    ("eng.custodian", "Khalid", "Al Mansoori", "ENG", [("asset_custodian", "ENG")]),
    ("comp.requester", "Aisha", "Al Nuaimi", "COMP", [("requester", "COMP")]),
    ("comp.rep", "Omar", "Al Shamsi", "COMP", [("department_representative", "COMP"), ("requester", "COMP")]),
    ("comp.custodian", "Fatima", "Al Zaabi", "COMP", [("asset_custodian", "COMP")]),
    ("finance.officer", "Hamad", "Al Ketbi", "FIN", [("finance_officer", "FIN")]),
    ("procurement.officer", "Noura", "Al Mazrouei", "PROC", [("procurement_officer", "PROC")]),
    ("sustainability.officer", "Salem", "Al Dhaheri", "SUS", [("sustainability_officer", "SUS")]),
    ("business.admin", "Latifa", "Al Suwaidi", "BA", [("business_administrator", "BA")]),
    # A second Business administrator: a role request needs an independent authoriser (UC-01, BR-02).
    ("business.admin2", "Khalfan", "Al Romaithi", "BA", [("business_administrator", "BA")]),
    ("maintenance.staff", "Yousef", "Al Ali", "FM", [("maintenance_staff", "FM")]),
    ("system.admin", "Reem", "Al Kaabi", "ITS", [("system_administrator", "ITS")]),
]

BUSINESS_SETTINGS = ["accounts.view_department", "accounts.add_department", "accounts.change_department",
                     "assets.view_category", "assets.add_category", "assets.change_category"]
ADMIN_SITE_PERMISSIONS = {
    "system.admin": ["accounts.view_user", "accounts.add_user", "accounts.change_user", "accounts.view_userrole",
                     "accounts.view_department"],
    "business.admin": BUSINESS_SETTINGS,
    "business.admin2": BUSINESS_SETTINGS,
}

MONITOR_SOURCE = ("Low: UK DESNZ 2024 'IT (primary material production)' 24.86548 kg CO2e/kg x Dell P2422H mass "
                  "5.15 kg (F1 x F3). High: Dell P2422H product carbon footprint 2024, 327 kg CO2e (F2).")
CHAIR_SOURCE = ("Low: FIRA contract-chair average in the Casala Onyx IV EPD, 27 kg CO2e (F4). "
                "High: Steelcase Leap EPD NSF EPD11372, A1-A3, 104 kg CO2e (F5).")

CATEGORIES = [
    dict(name="IT equipment", subcategory="Monitor", emission_factor_low=Decimal("128.057"),
         emission_factor_high=Decimal("327"), factor_source=MONITOR_SOURCE, factor_version="Section 12 v1",
         unit_mass_kg=Decimal("5.15"), replacement_cost_aed=Decimal("345"),
         replacement_cost_source="Dell P2422H price incl. VAT, Phase 2 feasibility study [S15] (F7)"),
    dict(name="IT equipment", subcategory="Laptop"),
    dict(name="IT equipment", subcategory="Projector"),
    dict(name="Furniture", subcategory="Office chair", emission_factor_low=Decimal("27"),
         emission_factor_high=Decimal("104"), factor_source=CHAIR_SOURCE, factor_version="Section 12 v1"),
    dict(name="Furniture", subcategory="Desk"),
    dict(name="Lab equipment", subcategory="Measurement", procurement_controlled=True),
    dict(name="Books", subcategory="Textbook"),
    dict(name="Office materials", subcategory="Stationery"),
]


class Command(BaseCommand):
    help = "Create synthetic demo data for Dawra Campus (only on an empty database)."

    def add_arguments(self, parser):
        parser.add_argument("--without-history", action="store_true",
                            help="Only the records of the demo script and the section 12 worked example (used by "
                                 "the tests); no months of history, extra items or overdue work.")

    def handle(self, *args, **options):
        if Department.objects.exists():
            self.stdout.write("Demo data already exists; nothing was changed.")
            return
        password = os.environ.get("DEMO_PASSWORD", "dawra-demo-2026")
        with transaction.atomic():
            self.create_people(password)
            self.create_categories()
            self.create_assets()
            self.create_requests_and_transfer()
            if not options["without_history"]:
                self.create_history()
                self.create_supply()
                self.create_waiting_work()
        self.stdout.write(self.style.SUCCESS(
            f"Demo data created. Sign in as any of: {', '.join(u[0] for u in USERS)}"
        ))

    def create_people(self, password):
        self.departments = {code: Department.objects.create(name=name, code=code) for name, code in DEPARTMENTS}
        for code in Role.Code.values:
            Role.objects.create(code=code)
        self.users = {}
        for username, first, last, dept, roles in USERS:
            user = User.objects.create_user(
                username=username, password=password, first_name=first, last_name=last,
                email=f"{username}@dawra.example", department=self.departments[dept],
            )
            # The administration site only for what each administrator maintains (FR-01.1, FR-03). Nobody is a
            # superuser, so technical administration never gives business approval rights (BR-01).
            if username in ADMIN_SITE_PERMISSIONS:
                user.is_staff = True
                user.save()
                for name in ADMIN_SITE_PERMISSIONS[username]:
                    app_label, codename = name.split(".")
                    user.user_permissions.add(Permission.objects.get(content_type__app_label=app_label,
                                                                     codename=codename))
            for role, role_dept in roles:
                UserRole.objects.create(user=user, role=Role.objects.get(code=role),
                                        department=self.departments[role_dept], status=UserRole.Status.ACTIVE)
            self.users[username] = user
        # A role request waiting for an independent Business administrator (shown in Administration).
        UserRole.request(self.users["maintenance.staff"], Role.objects.get(code="requester"), self.departments["FM"],
                         by=self.users["business.admin2"])

    def create_categories(self):
        self.categories = {}
        for data in CATEGORIES:
            category = Category.objects.create(**data)
            self.categories[data["subcategory"]] = category

    def make_asset(self, model, owner, custodian, confirmer, in_use=False, **fields):
        asset = model(**fields)
        asset.register(self.users[custodian], self.departments[owner])
        asset.confirm(self.users[confirmer], in_use=in_use)
        return asset

    def create_assets(self):
        today = date.today()
        self.monitors = self.make_asset(
            ITAsset, "ENG", "eng.custodian", "eng.rep", name="Dell P2422H 24-inch monitor",
            description="24-inch office monitors from the old design studio. Small scratch on one stand.",
            category=self.categories["Monitor"], tags="monitor, display, 24-inch, office", condition=Condition.GOOD,
            quantity=4, specifications="24-inch, 1920x1080, HDMI and DisplayPort, height-adjustable stand",
            building="Engineering Building", room="E2-114", value=Decimal("345"), purchase_date=today - timedelta(days=900),
            planned_retirement_date=today + timedelta(days=4 * 365), serial_number="CN-0P2422H-DEMO",
        )
        self.chairs = self.make_asset(
            FurnitureAsset, "ENG", "eng.custodian", "eng.rep", name="Ergonomic office chair",
            description="Mesh-back office chairs with adjustable height. Fabric worn on the armrests.",
            category=self.categories["Office chair"], tags="chair, seating, ergonomic", condition=Condition.FAIR,
            quantity=6, specifications="Adjustable height, armrests, wheels", building="Engineering Building",
            room="E1-020", value=Decimal("450"), purchase_date=today - timedelta(days=1500),
            planned_retirement_date=today + timedelta(days=2 * 365), material="Mesh and steel",
        )
        self.projector = self.make_asset(
            ITAsset, "ENG", "eng.custodian", "eng.rep", name="Epson classroom projector",
            description="Ceiling projector removed during a refit. Bulb is broken; otherwise works.",
            category=self.categories["Projector"], tags="projector, classroom, AV", condition=Condition.POOR,
            quantity=1, specifications="3LCD, 3600 lumens, HDMI", building="Engineering Building", room="E3-201",
            value=Decimal("1800"), purchase_date=today - timedelta(days=6 * 365),
        )
        self.oscilloscope = self.make_asset(
            Asset, "ENG", "eng.custodian", "eng.rep", name="Digital oscilloscope",
            description="Four-channel bench oscilloscope from a closed teaching lab.",
            category=self.categories["Measurement"], tags="oscilloscope, lab, electronics", condition=Condition.GOOD,
            quantity=1, specifications="4 channels, 200 MHz, USB", building="Engineering Building", room="E4-310",
            value=Decimal("7500"), purchase_date=today - timedelta(days=2 * 365),
            planned_retirement_date=today + timedelta(days=5 * 365),
        )
        self.desks = self.make_asset(
            FurnitureAsset, "COMP", "comp.custodian", "comp.rep", in_use=True, name="Standing desk",
            description="Height-adjustable standing desks in use in the Computing office.",
            category=self.categories["Desk"], tags="desk, standing, office", condition=Condition.NEW,
            quantity=3, specifications="Electric height adjustment, 160 x 80 cm", building="Computing Building",
            room="C1-105", value=Decimal("1200"), purchase_date=today - timedelta(days=200),
        )
        # The desks were last checked four months ago, so the Computing home page shows an asset needing
        # verification (UI-02, FR-06.4). They are not listed, so the demo holds are not affected (BR-16).
        Asset.objects.filter(pk=self.desks.pk).update(verified_on=timezone.now() - timedelta(days=120))
        for asset, qty in ((self.monitors, 4), (self.chairs, 6), (self.projector, 1), (self.oscilloscope, 1)):
            listing = Listing.objects.create(asset=asset, quantity=qty, created_by=self.users["eng.custodian"],
                                             release_reason=Listing.ReleaseReason.SURPLUS)
            listing.submit_for_release(self.users["eng.custodian"])
            listing.publish(self.users["eng.rep"])
            setattr(asset, "demo_listing", listing)

    def create_requests_and_transfer(self):
        requester = self.users["comp.requester"]
        # A completed transfer, so history and the dashboard have real figures (the section 12 example).
        req = ResourceRequest.objects.create(
            purpose="Monitors for the new Computing teaching lab", category=self.categories["Monitor"],
            specifications="24-inch, HDMI", quantity=2, min_condition=Condition.FAIR,
            delivery_location="Computing Building C2-210", required_by=date.today() + timedelta(days=30),
            requester=requester, department=self.departments["COMP"],
        )
        req.submit(requester)
        req.approve(self.users["comp.rep"])
        hold = Reservation.request_hold(req, self.monitors.demo_listing, requester)
        hold.confirm(self.users["eng.custodian"])
        transfer = Transfer.start(
            hold, requester, self.users["comp.custodian"], to_building="Computing Building", to_room="C2-210",
            delivery_arrangement=Transfer.Arrangement.DELIVERY, van_trips=1, distance_km=Decimal("10"),
            transfer_cost_aed=Decimal("40"), planned_date=date.today(),
        )
        transfer.approve_stage(self.users["eng.rep"])
        transfer.approve_stage(self.users["comp.rep"])
        transfer.hand_over(self.users["eng.custodian"], Condition.GOOD)
        transfer.confirm_receipt(self.users["comp.custodian"], 2, Condition.GOOD)
        transfer.impact.confirm_avoided_purchase(self.users["comp.rep"])

        # An open request waiting for department approval, and one ready for matching.
        chairs = ResourceRequest.objects.create(
            purpose="Chairs for the robotics lab", category=self.categories["Office chair"],
            specifications="Adjustable height", quantity=4, min_condition=Condition.FAIR,
            delivery_location="Computing Building C3-002", required_by=date.today() + timedelta(days=21),
            requester=requester, department=self.departments["COMP"],
        )
        chairs.submit(requester)
        projector = ResourceRequest.objects.create(
            purpose="Projector for a seminar room", category=self.categories["Projector"],
            specifications="HDMI", quantity=1, min_condition=Condition.POOR,
            delivery_location="Computing Building C1-001", required_by=date.today() + timedelta(days=14),
            requester=requester, department=self.departments["COMP"],
        )
        projector.submit(requester)
        projector.approve(self.users["comp.rep"])

    # Synthetic history -------------------------------------------------------------------------------------

    @staticmethod
    def day(days_ago, hour=10):
        """A moment `days_ago` days back, during working hours (local time)."""
        return timezone.make_aware(datetime.combine(timezone.localdate() - timedelta(days=days_ago), time(hour)))

    @contextmanager
    def happened(self, when):
        """Run workflow steps now, then move every time they wrote back to `when`. Messages from the past are
        marked as read an hour later; impacts, listings and transfers get that day as their date."""
        start = timezone.now()
        newest = {model: model.objects.order_by("-pk").values_list("pk", flat=True).first() or 0
                  for model in (Notification, SustainabilityImpact, Listing, Transfer)}
        yield
        shift = start - when
        for model, fields in DATED_FIELDS:
            for name in fields:
                model.objects.filter(**{f"{name}__gte": start}).update(**{name: F(name) - shift})
        day = timezone.localtime(when).date()
        Notification.objects.filter(pk__gt=newest[Notification]).update(read_at=F("sent_at") + timedelta(hours=1))
        SustainabilityImpact.objects.filter(pk__gt=newest[SustainabilityImpact]).update(occurred_on=day)
        Listing.objects.filter(pk__gt=newest[Listing]).update(available_from=day)
        Transfer.objects.filter(pk__gt=newest[Transfer]).update(planned_date=day)

    def publish_item(self, owner, model, subcategory, name, description, specifications, tags, condition, quantity,
                     value, **extra):
        custodian, rep = {"ENG": ("eng.custodian", "eng.rep"), "COMP": ("comp.custodian", "comp.rep")}[owner]
        asset = self.make_asset(
            model, owner, custodian, rep, name=name, description=description, category=self.categories[subcategory],
            tags=tags, condition=condition, quantity=quantity, specifications=specifications, value=Decimal(value),
            building="Engineering Building" if owner == "ENG" else "Computing Building",
            room="E2-010" if owner == "ENG" else "C1-110", purchase_date=date.today() - timedelta(days=3 * 365),
            planned_retirement_date=date.today() + timedelta(days=3 * 365), **extra)
        listing = Listing.objects.create(asset=asset, quantity=quantity, created_by=self.users[custodian],
                                         release_reason=Listing.ReleaseReason.SURPLUS)
        listing.submit_for_release(self.users[custodian])
        listing.publish(self.users[rep])
        return listing

    def ask(self, purpose, subcategory, specifications, quantity, min_condition, room):
        return ResourceRequest.objects.create(
            purpose=purpose, category=self.categories[subcategory], specifications=specifications, quantity=quantity,
            min_condition=min_condition, delivery_location=f"Computing Building {room}",
            required_by=date.today() + timedelta(days=30), requester=self.users["comp.requester"],
            department=self.departments["COMP"])

    @staticmethod
    def backdate_hold(hold, confirmed):
        """A hold lasts 5 working days from its confirmation (BR-12), also in the history."""
        from transfers.models import add_working_days

        Reservation.objects.filter(pk=hold.pk).update(expires_at=add_working_days(confirmed, 5))

    def run_transfer(self, receipt_days_ago, listing, purpose, specifications, quantity, min_condition, distance,
                     trips, cost, finish=True):
        """One request from Computing for an Engineering item, through every step, dated back in time.
        With finish=False it stops after the receiving side approved (waiting for Finance or Procurement)."""
        u, d = self.users, receipt_days_ago
        with self.happened(self.day(d + 9, 9)):
            req = self.ask(purpose, listing.asset.category.subcategory, specifications, quantity, min_condition,
                           "C2-114")
            req.submit(u["comp.requester"])
        with self.happened(self.day(d + 8, 11)):
            req.approve(u["comp.rep"])
        with self.happened(self.day(d + 7, 10)):
            hold = Reservation.request_hold(req, listing, u["comp.requester"])
            hold.confirm(u["eng.custodian"])
        with self.happened(self.day(d + 6, 13)):
            transfer = Transfer.start(
                hold, u["comp.requester"], u["comp.custodian"], to_building="Computing Building", to_room="C2-114",
                delivery_arrangement=Transfer.Arrangement.DELIVERY, van_trips=trips, distance_km=Decimal(distance),
                transfer_cost_aed=Decimal(cost), planned_date=date.today())
        with self.happened(self.day(d + 5, 10)):
            transfer.approve_stage(u["eng.rep"])
        with self.happened(self.day(d + 4, 12)):
            transfer.approve_stage(u["comp.rep"])
        self.backdate_hold(hold, self.day(d + 7, 10))
        if finish:
            with self.happened(self.day(d + 1, 14)):
                transfer.hand_over(u["eng.custodian"], listing.asset.condition)
            with self.happened(self.day(d, 11)):
                transfer.confirm_receipt(u["comp.custodian"], quantity, listing.asset.condition)
            with self.happened(self.day(max(d - 1, 1), 9)):
                transfer.impact.confirm_avoided_purchase(u["comp.rep"])
        ResourceRequest.objects.filter(pk=req.pk).update(
            required_by=timezone.localtime(self.day(d + 9)).date() + timedelta(days=30))
        return transfer

    def create_history(self):
        """Nine transfers that finished over the last months, so the dashboard has a history to show."""
        for (days_ago, model, subcategory, name, description, specs, tags, condition, quantity, value, distance,
             trips, cost, purpose) in HISTORY:
            with self.happened(self.day(days_ago + 12, 10)):
                listing = self.publish_item("ENG", model, subcategory, name, description, specs, tags, condition,
                                            quantity, value)
            self.run_transfer(days_ago, listing, purpose, specs.split(",")[0], quantity, Condition.FAIR, distance,
                              trips, cost)

    def create_supply(self):
        """More published items for search and the AI search (none are chairs or projectors)."""
        for owner, model, subcategory, name, description, specs, tags, condition, quantity, value, extra in SUPPLY:
            self.publish_item(owner, model, subcategory, name, description, specs, tags, condition, quantity, value,
                              **extra)

    def create_waiting_work(self):
        """Work that has waited longer than 3 working days (TBD-5), so the home pages show something overdue,
        and one more open request that matching can work on."""
        u = self.users
        # A request Omar has not decided for over a week (shown as overdue on his home page).
        with self.happened(self.day(8, 10)):
            desks = self.ask("Desks for the project room", "Desk", "Height-adjustable", 2, Condition.FAIR, "C3-010")
            desks.submit(u["comp.requester"])
        # A transfer over AED 5,000 waiting for Finance for about a week (BR-06; overdue for Hamad).
        with self.happened(self.day(21, 10)):
            laptops = self.publish_item(
                "ENG", ITAsset, "Laptop", "HP EliteBook 840 laptops",
                "Laptops from a finished research grant, wiped and reset.", "14-inch, Core i7, 16 GB RAM",
                "laptop, notebook", Condition.GOOD, 2, "2700", stores_data=True)
        self.run_transfer(3, laptops, "Laptops for teaching assistants", "14-inch", 2, Condition.GOOD, "2", 1, "30",
                          finish=False)
        # An approved request that matching can rank (the engineering textbooks fit it).
        books = self.ask("Textbooks for the AI course", "Textbook", "Mathematics", 10, Condition.FAIR, "C2-001")
        books.submit(u["comp.requester"])
        books.approve(u["comp.rep"])
