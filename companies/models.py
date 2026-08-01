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
            base_slug = slugify(self.company_name) #Convert the company name into a URL-friendly slug.
            slug = base_slug
            n = 1
            while Company.objects.filter(slug=slug).exclude(pk=self.pk).exists():  #.exclude(pk=self.pk)-->avoids that problem by ignoring the current object during the duplicate check.
                slug = f"{base_slug}-{n}" #If the slug already exists,create a new one.
                n += 1
            self.slug = slug #Once a unique slug is found,store it in the object.
        super().save(*args, **kwargs) #Call Django's original save() method.

    def __str__(self):
        return self.company_name