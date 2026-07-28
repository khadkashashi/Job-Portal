from django.contrib import admin
from .models import ( CompanyPlan, CompanySubscription, Payment)

@admin.register(CompanyPlan)
class CompanyPlanAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "duration_days",
        "vacancy_limit",
    )
    search_fields = ("name"),
    ordering = ("price"),


@admin.register(CompanySubscription)
class CompanySubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "plan",
        "status",
        "start_date",
        "end_date",
        "subscription_active",
    )

    list_filter = (
        "status",
        "plan",
    )

    search_fields = (
        "company__company_name",
        "plan__name",
    )

    ordering = (
        "-start_date",
    )

    @admin.display(boolean=True, description="Active")
    def subscription_active(self, obj):
        return obj.is_active()


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "plan",
        "amount",
        "payment_method",
        "status",
        "pidx",
        "transaction_id",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
    )

    search_fields = (
        "subscription__company__company_name",
        "pidx",
        "transaction_id",
    )

    readonly_fields = (
        "pidx",
        "transaction_id",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    @admin.display(description="Company")
    def company(self, obj):
        return obj.subscription.company.company_name

    @admin.display(description="Plan")
    def plan(self, obj):
        return obj.subscription.plan.name