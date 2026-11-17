"""C2 Departments and assets, C3 Publish and search."""

from datetime import date

from assets.models import Asset, Category, Listing

from .helpers import DemoTestCase


class AssetTests(DemoTestCase):
    def register(self, client, **extra):
        data = {"kind": "it", "name": "Lenovo 27-inch monitor", "description": "Spare monitor",
                "category": Category.objects.get(subcategory="Monitor").pk, "condition": "good", "quantity": 2,
                "campus": "Main campus", "building": "Engineering Building", "serial_number": "SN-1",
                # FR-04.2: needed before a second person can confirm the record.
                "specifications": "27-inch, HDMI", "room": "E1-101", "purchase_date": "2024-01-15", "value": "900"}
        data.update(extra)
        client.post("/assets/register/", data)
        return Asset.objects.get(name=data["name"])

    def test_register_with_category_condition_department_and_status(self):
        asset = self.register(self.sign_in("eng.custodian"))
        self.assertEqual(asset.status, Asset.Status.DRAFT)
        self.assertEqual(asset.owner_department.code, "ENG")
        self.assertEqual(asset.condition, "good")
        self.assertTrue(hasattr(asset, "itasset"))

    def test_a_second_user_confirms(self):
        custodian, rep = self.sign_in("eng.custodian"), self.sign_in("eng.rep")
        asset = self.register(custodian)
        custodian.post(f"/assets/{asset.pk}/confirm/", {"placement": "in_storage"})
        asset.refresh_from_db()
        self.assertEqual(asset.status, Asset.Status.DRAFT)
        rep.post(f"/assets/{asset.pk}/confirm/", {"placement": "in_storage"})
        asset.refresh_from_db()
        self.assertEqual(asset.status, Asset.Status.IN_STORAGE)

    def test_quantity_must_be_positive(self):
        response = self.sign_in("eng.custodian").post("/assets/register/", {
            "kind": "general", "name": "Nothing", "condition": "good", "quantity": 0, "campus": "Main campus"})
        self.assertContains(response, "positive whole number")

    def test_custodian_of_another_department_cannot_open_the_asset(self):
        asset = Asset.objects.filter(owner_department__code="ENG").first()
        self.assertEqual(self.sign_in("comp.custodian").get(f"/assets/{asset.pk}/").status_code, 403)


class PublishAndSearchTests(DemoTestCase):
    def test_listing_is_released_by_the_department_representative(self):
        custodian, rep = self.sign_in("eng.custodian"), self.sign_in("eng.rep")
        asset = Asset.objects.get(name="Digital oscilloscope")
        Listing.objects.filter(asset=asset).update(status=Listing.Status.WITHDRAWN)
        custodian.post(f"/assets/{asset.pk}/list/", {"quantity": 1, "available_from": date.today().isoformat(),
                                                     "release_reason": "surplus", "submit_for": "release"})
        listing = Listing.objects.filter(asset=asset).latest("created_at")
        self.assertEqual(listing.status, Listing.Status.PENDING_RELEASE)
        rep.post(f"/assets/listings/{listing.pk}/decide/", {"decision": "approve"})
        listing.refresh_from_db()
        self.assertEqual(listing.status, Listing.Status.PUBLISHED)

    def test_search_by_keyword_category_condition_and_department(self):
        client = self.sign_in("comp.requester")
        chair = Category.objects.get(subcategory="Office chair")
        self.assertContains(client.get("/assets/search/?q=chair"), "Ergonomic office chair")
        self.assertContains(client.get(f"/assets/search/?category={chair.pk}"), "Ergonomic office chair")
        self.assertNotContains(client.get(f"/assets/search/?category={chair.pk}"), "Dell P2422H")
        self.assertNotContains(client.get("/assets/search/?q=chair&condition=good"), "Ergonomic office chair")
        self.assertContains(client.get("/assets/search/?q=chair&condition=fair"), "Ergonomic office chair")
        eng = Asset.objects.get(name="Ergonomic office chair").owner_department
        self.assertContains(client.get(f"/assets/search/?department={eng.pk}"), "Ergonomic office chair")

    def test_no_results_offers_a_request(self):
        self.assertContains(self.sign_in("comp.requester").get("/assets/search/?q=submarine"),
                            "Create a request with these criteria")
