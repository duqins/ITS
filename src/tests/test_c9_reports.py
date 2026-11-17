"""C9 Basic report: a table of requests and transfers, with CSV export."""

import csv
from datetime import date
from io import StringIO

from transfers.models import Transfer

from .helpers import DemoTestCase


class ReportTests(DemoTestCase):
    def query(self, report):
        return f"report={report}&date_from={date.today().year}-01-01&date_to={date.today().isoformat()}"

    def test_tables_of_requests_and_transfers(self):
        client = self.sign_in("business.admin")
        self.assertContains(client.get(f"/reports/?{self.query('requests')}"), "Monitors for the new Computing teaching lab")
        response = client.get(f"/reports/?{self.query('transfers')}")
        # Codes come from database ids, which PostgreSQL does not reuse between tests, so look the code up.
        self.assertContains(response, Transfer.objects.get().code)
        self.assertContains(response, "1 transfer · 1 completed")

    def test_csv_contains_filters_records_and_totals(self):
        response = self.sign_in("business.admin").get(f"/reports/?{self.query('transfers')}&format=csv")
        self.assertEqual(response["Content-Type"], "text/csv; charset=utf-8")
        rows = list(csv.reader(StringIO(response.content.decode("utf-8-sig"))))
        self.assertEqual(rows[0], ["Report", "Transfers"])
        self.assertEqual(rows[2], ["Department", "All departments"])
        self.assertIn(Transfer.objects.get().code, [r[0] for r in rows if r])
        self.assertIn(["Total records", "1"], rows)

    def test_representative_reports_on_own_department_only(self):
        response = self.sign_in("eng.rep").get(f"/reports/?{self.query('requests')}")
        self.assertNotContains(response, "Monitors for the new Computing teaching lab")

    def test_requester_cannot_open_reports(self):
        self.assertEqual(self.sign_in("comp.requester").get("/reports/").status_code, 403)

    def test_csv_cells_cannot_run_as_formulas(self):
        from resource_requests.models import ResourceRequest
        ResourceRequest.objects.filter(purpose__startswith="Chairs").update(purpose="=HYPERLINK(1)")
        response = self.sign_in("business.admin").get(f"/reports/?{self.query('requests')}&format=csv")
        self.assertIn("'=HYPERLINK(1)", response.content.decode("utf-8-sig"))
