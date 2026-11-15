"""Create synthetic demo data: departments, the nine roles, one user per role, categories and assets.

Run once on an empty database:  python manage.py seed_demo
The demo password comes from DEMO_PASSWORD (default for local use only: dawra-demo-2026).
Everything is synthetic; no real KU people or records.
"""

import os
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Department, Role, User, UserRole
from assets.models import Asset, Category, Condition, FurnitureAsset, ITAsset, Listing
from resource_requests.models import ResourceRequest
from transfers.models import Reservation, Transfer

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
    ("maintenance.staff", "Yousef", "Al Ali", "FM", [("maintenance_staff", "FM")]),
    ("system.admin", "Reem", "Al Kaabi", "ITS", [("system_administrator", "ITS")]),
]

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
            if username == "system.admin":
                user.is_staff = user.is_superuser = True
                user.save()
            if username == "business.admin":
                user.is_staff = True
                user.save()
            for role, role_dept in roles:
                UserRole.objects.create(user=user, role=Role.objects.get(code=role),
                                        department=self.departments[role_dept], status=UserRole.Status.ACTIVE)
            self.users[username] = user

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
