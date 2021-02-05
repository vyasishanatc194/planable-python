from django.db import models
from django.utils.translation import ugettext_lazy as _


class ActivityTracking(models.Model):
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    created_at = models.DateTimeField(verbose_name=_('Created At'),
                                      auto_now_add=True, help_text=_("Date when created."), null=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated At'),
                                      auto_now=True, help_text=_("Date when updated."), null=True)

    class Meta:
        abstract = True