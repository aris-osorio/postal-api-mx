from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import ActiveObjectsManager, AllObjectsManager

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

    active_objects = ActiveObjectsManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True
        verbose_name = _('Modelo Base')
        verbose_name_plural = _('Modelos Base')
        
    def delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "updated_at"])

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)