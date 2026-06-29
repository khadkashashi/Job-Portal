from django.db import models
from django.utils.text import slugify

from companies.models import Company


class Job(models.Model):

    class EmploymentType(models.TextChoices):
        FULL_TIME = "FULL_TIME", "Full Time"
        PART_TIME = "PART_TIME", "Part Time"
        INTERNSHIP = "INTERNSHIP", "Internship"
        CONTRACT = "CONTRACT", "Contract"

    class ExperienceLevel(models.TextChoices):
        ENTRY = "ENTRY", "Entry Level"
        MID = "MID", "Mid Level"
        SENIOR = "SENIOR", "Senior Level"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs",
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField()

    location = models.CharField(max_length=150)

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
    )

    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
    )

    salary_min = models.PositiveIntegerField()

    salary_max = models.PositiveIntegerField()

    vacancies = models.PositiveIntegerField(default=1)

    deadline = models.DateField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title