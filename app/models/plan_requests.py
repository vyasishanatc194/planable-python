from django.db import models
from planable.models import ActivityTracking
from django.utils.translation import gettext as _


class PlanJoiningRequest(ActivityTracking):
    STATUS_CHOICES = (
        ("PENDING", _("PENDING")),
        ("ACCEPTED", _("ACCEPTED")),
        ("DECLINED", _("DECLINED")),
    )
    user = models.ForeignKey(
        "app.User",
        on_delete=models.CASCADE,
        related_name="Requesting_User",
        null=True,
        blank=True,
    )
    plan = models.ForeignKey(
        "app.Plan",
        on_delete=models.CASCADE,
        related_name="request_for_plan",
        null=True,
        blank=True,
    )
    request_text = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        help_text=_("Request Status"),
        verbose_name=_("request status"),
        default="PENDING",
    )
    response_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Plan Joining Request"
        verbose_name_plural = "Plan Joining Requests"
        ordering = ["-created_at"]
