from datetime import date
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from jobs.models import Job


class Command(BaseCommand):
    help = "Emails each company whose job posting deadline is today."
    def handle(self, *args, **options):
        today = date.today()
        jobs_due_today = Job.objects.filter(deadline=today, is_active=True)
        if not jobs_due_today.exists():
            self.stdout.write("No job deadlines today.")
            return

        for job in jobs_due_today:
            company_email = job.company.email
            if not company_email:
                self.stdout.write(f"Skipped '{job.title}' - company has no email on file.")
                continue

            send_mail(
                subject=f"Deadline reached: {job.title}",
                message=(
                    f"Hi {job.company.company_name},\n\n"
                    f"The application deadline for '{job.title}' is today ({today}).\n"
                    f"Log in to your dashboard to review applicants and close the posting "
                    f"if you're done hiring.\n\n"
                    f"- JobPortal AI"
                ),
                from_email=None,
                recipient_list=[company_email],
                fail_silently=True,
            )
            self.stdout.write(f"Emailed {company_email} about '{job.title}'.")