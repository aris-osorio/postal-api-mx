from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import ActiveManager

class BaseModel(models.Model):
    """Abstract base model for auditing and soft deletion."""
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Fecha de actualización')
    )
    deleted_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name=_('Fecha de eliminación')
    )

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
        verbose_name = _('Modelo Base')
        verbose_name_plural = _('Modelos Base')