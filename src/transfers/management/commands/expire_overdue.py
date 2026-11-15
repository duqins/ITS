"""Expire overdue holds (BR-12) and open requests whose required-by date passed.

The app also does this when the home page, approvals or holds are opened; this command lets a
scheduler (for example a Render cron job) do it every night.
"""

from django.core.management.base import BaseCommand

from transfers.models import expire_overdue


class Command(BaseCommand):
    help = "Expire overdue holds and requests."

    def handle(self, *args, **options):
        expire_overdue()
        self.stdout.write("Overdue holds and requests expired.")
