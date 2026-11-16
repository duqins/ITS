"""The 'at a glance' row on the home page (UI-02), added after the TA review on 17 November: savings and items
reused for the roles that may see the dashboard, and late approvals for everyone, green for good and red for bad."""

import re

from .helpers import DemoTestCase


def tiles(html):
    """[(tone, label, value, note)] of the glance row, in order."""
    row = re.search(r'<section class="glance".*?</section>', html, re.S)
    if row is None:
        return []
    found = re.findall(r'class="glance-tile(?: tone-(\w+))?"[^>]*>\s*<div class="label">(.*?)</div>'
                       r'<div class="value">(.*?)</div><small class="tone-text">(.*?)</small>', row.group(0), re.S)
    return [(tone, label, value, note) for tone, label, value, note in found]


class GlanceWithHistoryTests(DemoTestCase):
    with_history = True

    def home(self, username, role=None):
        return tiles(self.sign_in(username, role).get("/").content.decode())

    def test_the_sustainability_officer_sees_campus_savings_in_green_and_late_work_in_red(self):
        row = self.home("sustainability.officer")
        self.assertEqual(row[0], ("good", "Net savings this year (whole campus)", "AED 4,940", "Saving money"))
        self.assertEqual(row[1][0], "good")
        self.assertEqual(row[1][2], "21")
        self.assertEqual(row[2], ("bad", "Late approvals on campus", "2", "Needs attention"))

    def test_a_representative_sees_only_their_department_and_their_own_late_tasks(self):
        row = self.home("comp.rep")
        self.assertIn("(Computing)", row[0][1])
        self.assertEqual(row[-1][1:3], ("Your approvals waiting over 3 working days", "1"))
        engineering = self.home("eng.rep")
        self.assertEqual(engineering[0][0:3], ("", "Net savings this year (Engineering)", "AED 0"))
        self.assertEqual(engineering[0][3], "No savings yet")

    def test_a_requester_sees_no_money_but_sees_requests_held_up(self):
        row = self.home("comp.requester")
        self.assertEqual(len(row), 1)  # no dashboard.view: savings are not shown (access matrix, section 6)
        self.assertEqual(row[0], ("bad", "Your requests held up by a late approval", "2", "Needs attention"))

    def test_finance_and_custodians_see_the_late_items_that_concern_them(self):
        self.assertEqual(self.home("finance.officer")[-1][1:3], ("Your approvals waiting over 3 working days", "1"))
        self.assertEqual(self.home("eng.custodian")[0][1:3], ("Late approvals in Engineering", "1"))
        self.assertEqual(self.home("comp.custodian")[0][1:3], ("Late approvals in Computing", "2"))
        self.assertEqual(self.home("maintenance.staff")[0], ("good", "Late approvals in Facilities Management", "0",
                                                             "Nothing late"))


class GlanceWithoutHistoryTests(DemoTestCase):
    def test_the_worked_example_alone_shows_its_savings_and_nothing_late(self):
        row = tiles(self.sign_in("sustainability.officer").get("/").content.decode())
        self.assertEqual(row[0][2], "AED 650")
        self.assertEqual(row[-1], ("good", "Late approvals on campus", "0", "Nothing late"))

    def test_the_row_is_in_arabic_for_arabic_users(self):
        client = self.sign_in("comp.requester")
        client.post("/accounts/settings/language/", {"language": "ar"})
        html = client.get("/").content.decode()
        self.assertIn("نظرة سريعة", html)
        self.assertIn("لا شيء متأخر", html)
