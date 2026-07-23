from django.db import models
from django.utils import timezone
from companies.models import Company


class PlanDuration(models.TextChoices):
    FREE= "Free" 
    THREE_MONTHS = "3 Months"
    SIX_MONTHS = "6 Months"
    ONE_YEAR = "1 Year"
    LIFETIME = "Lifetime"


class CompanyPlan(models.Model):
    name = models.CharField(max_length=20, choices=PlanDuration.choices, unique=True)
    price = models.PositiveIntegerField(default=0)
    duration_days = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Leave blank for Free/Lifetime - they don't expire on a fixed date.",
    )
    vacancy_limit = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Leave blank for unlimited vacancies.",
    )

    def __str__(self):
        return f"{self.name} - NPR {self.price}"
    class Meta:
        db_table = "subscription_plan"


class SubscriptionStatus(models.TextChoices):
    ACTIVE =  "Active"
    EXPIRED ="Expired"
    CANCELLED= "Cancelled"
    PENDING= "Pending"
    PAUSED = "Paused"
    FAILED = "Failed"



class CompanySubscription(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(CompanyPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=SubscriptionStatus.choices, default=SubscriptionStatus.PENDING)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def is_active(self):
        if self.status != SubscriptionStatus.ACTIVE:
            return False
        if self.end_date is None:
            return True
        return self.end_date >= timezone.now().date()

    def __str__(self):
        return f"{self.company.company_name} - {self.plan.name}"
    class Meta:
        db_table = "company_subscription"


class PaymentMethod(models.TextChoices):
    ESEWA = "esewa"
    KHALTI = "khalti"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"


class PaymentStatus(models.TextChoices):
     PENDING = "pending"
     SUCCESS = "success"
     FAILED = "failed"

class Payment(models.Model):
    subscription = models.ForeignKey(CompanySubscription, on_delete=models.CASCADE, related_name="payments")
    pidx = models.CharField(max_length=100, unique=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.KHALTI)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscription.company.company_name} - {self.pidx}"

    class Meta:
        db_table = "payments"