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