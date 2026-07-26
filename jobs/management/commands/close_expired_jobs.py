from datetime import date

from django.core.management.base import BaseCommand

from jobs.models import Job


class Command(BaseCommand):
    help = "Marks jobs as inactive once their deadline has passed."

    def handle(self, *args, **options):
        today = date.today()

        expired_jobs = Job.objects.filter(is_active=True, deadline__lt=today)
        count = expired_jobs.count()

        if count == 0:
            self.stdout.write("No expired jobs to close.")
            return

        expired_jobs.update(is_active=False)
        self.stdout.write(f"Closed {count} expired job(s).")