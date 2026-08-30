# JobPortal AI

A Django-based, multi-role job portal and recruitment platform connecting
Applicants, Recruiters, and Admins — with AI-powered interview scoring,
real payment integration, and automated background tasks.

## Features

### For Applicants
- Register, log in, browse and search jobs (by keyword, location,
  employment type, minimum salary)
- Apply with resume, cover letter, and personal details
- Take an AI-generated interview for each application — questions and
  scoring powered by a locally-run LLM (Ollama)
- Track application status (Pending → Reviewing → Shortlisted →
  Hired/Rejected) with live email notifications on every status change
- Personal dashboard with application stats and recent activity

### For Recruiters
- Create and manage a company profile
- Post, edit, and delete job listings
- Choose a subscription plan: Free (limited job posts) or paid plans
  (3/6/12-month or Lifetime, unlimited posts) via **Khalti** payment
  integration (sandbox)
- Review applications, view AI interview scores, and update candidate
  status
- Dashboard with subscription status, job stats, and application
  breakdowns

### For Admins
- Platform-wide dashboard: user/company/job/application counts, total
  revenue, and live charts (applications by status, companies by plan,
  revenue trend)
- Renew any company's subscription on their behalf, through the same
  real Khalti payment flow
- Quick links into Django's built-in admin panel for full record
  management (Applicants, Recruiters, Companies, Jobs)
- Access gated by Django's real permission system (`is_staff` /
  `is_superuser`) - never a self-registered role

### Platform-wide
- Custom role-based authentication (Applicant / Recruiter / Admin)
- Forgot-password flow with real email delivery
- Scheduled background tasks (Windows Task Scheduler): automatically
  closes job postings past their deadline, and emails companies when a
  deadline arrives

## Tech Stack

- **Backend:** Django 6
- **Database:** SQLite
- **AI:** Ollama (`gemma2:2b`) - local LLM for interview question
  generation and answer scoring
- **Payments:** Khalti Payment Gateway (sandbox)
- **Email:** Gmail SMTP
- **Frontend:** Django templates, Bootstrap, Chart.js
- **Scheduled tasks:** Django management commands + Windows Task
  Scheduler
- **Package management:** uv

## Project Structure

```
Job_Portal/
├── accounts/        # Custom User model, auth, dashboards
├── companies/       # Company profiles
├── jobs/            # Job postings, search/filters, scheduled commands
├── applications/    # Applications, AI interview, status workflow
├── subscriptions/   # Plans, subscriptions, Khalti payment integration
├── landingpage/      # Public landing page
├── api/             # Reserved for future REST API work
└── core/            # Project settings and root URLs
```

## Setup

### Prerequisites
- Python 3.14+
- [uv](https://github.com/astral-sh/uv)
- [Ollama](https://ollama.com/) installed locally, with the `gemma2:2b`
  model pulled

### Installation

```bash
git clone <repo-url>
cd Job_Portal
uv sync
```

### Environment variables

Create a `.env` file in the project root (**never commit this file**):

```
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
KHALTI_SECRET_KEY=your-khalti-sandbox-secret-key
```

- Gmail requires an [App Password](https://myaccount.google.com/apppasswords),
  not your normal login password.
- Khalti sandbox keys are available from the
  [Khalti test merchant dashboard](https://test-admin.khalti.com/).

### Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

Seed the subscription plans (one-time, via `python manage.py shell`):

```python
from subscriptions.models import CompanyPlan
CompanyPlan.objects.get_or_create(name="Free", defaults={"price": 0, "vacancy_limit": 10})
CompanyPlan.objects.get_or_create(name="3 Months", defaults={"price": 5000, "duration_days": 90})
CompanyPlan.objects.get_or_create(name="6 Months", defaults={"price": 8000, "duration_days": 180})
CompanyPlan.objects.get_or_create(name="1 Year", defaults={"price": 10000, "duration_days": 365})
CompanyPlan.objects.get_or_create(name="Lifetime", defaults={"price": 20000})
```

### Run Ollama

```bash
ollama serve
ollama pull gemma2:2b
```

### Run the server

```bash
python manage.py runserver
```

### Scheduled tasks (optional, for deadline automation)

`run_deadline_reminders.bat` runs two management commands
(`close_expired_jobs`, `send_deadline_reminders`) and can be scheduled
daily via Windows Task Scheduler. See the script for the exact commands
if you want to run them manually or adapt them for another OS's
scheduler (e.g. cron on Linux/macOS).

## Roles & Access

| Role | How it's granted | What they can do |
|-----------|-------------------|-----------------------------------|
| Applicant | Self-registration | Apply to jobs, take AI interviews |
| Recruiter | Self-registration | Post jobs, manage a company, subscribe |
| Admin | Manually, by an existing superuser via Django admin | Platform-wide dashboard, subscription management |

Admin access is intentionally **not** self-registrable — it's granted by
promoting an existing, already-vetted user's account via Django's
built-in admin panel, using real permission flags rather than a
selectable role.

## Known Limitations

- The `api` app is currently unused boilerplate, reserved for future
  REST API work.
- AI interview quality depends on the local Ollama model in use;
  `gemma2:2b` is a small model chosen for free, offline testing.
- Scheduled tasks are set up for Windows Task Scheduler; an equivalent
  `cron` setup would be needed on Linux/macOS.
