from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Company(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="company")
    company_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField( upload_to="company_logos/", blank=True, null=True)
    description = models.TextField()
    website = models.URLField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    established_date = models.DateField()
    employee_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.company_name)
            slug = base_slug
            n = 1
            while Company.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

def __str__(self):
        return self.company_name