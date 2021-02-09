from django.db import models
from planable.models import ActivityTracking
from django.utils.translation import gettext as _


class Category(ActivityTracking):
    category_name = models.CharField(max_length=155, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-created_at"]


class Plan(ActivityTracking):
    title = models.CharField(max_length=155, blank=True)
    user = models.ForeignKey("app.User", on_delete=models.CASCADE, related_name="User", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    plan_datetime = models.DateTimeField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    city = models.ForeignKey("app.City", on_delete=models.CASCADE, related_name="PlanCity", null=True, blank=True)
    postal_code = models.ForeignKey("app.PostalCode", on_delete=models.CASCADE, related_name="PostalCode", null=True, blank=True) 
    spaces_available = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey("app.Category", on_delete=models.CASCADE, related_name="Category", null=True, blank=True)
    plan_image = models.ImageField(upload_to="plan_images", null=True,  blank=True, verbose_name=_("PlanImages"))
    hashtags = models.TextField(null=True, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["-created_at"]