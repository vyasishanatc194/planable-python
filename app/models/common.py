from django.db import models
from planable.models import ActivityTracking


class City(ActivityTracking):
    city = models.CharField(max_length=55, blank=True)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ["-created_at"]


class PostalCode(ActivityTracking):
    city = models.ForeignKey(
        "app.City",
        on_delete=models.CASCADE,
        related_name="CityCode",
        null=True,
        blank=True,
    )
    postal_code = models.CharField(max_length=55, blank=True)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Postal Code"
        verbose_name_plural = "Postal Codes"
        ordering = ["-created_at"]
