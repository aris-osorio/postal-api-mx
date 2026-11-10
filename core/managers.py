from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        now = timezone.now()
        return self.update(deleted_at=now, updated_at=now)

    def hard_delete(self):
        return super().delete()


class ActiveObjectsManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """Manager dont show deleted data."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class AllObjectsManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """Manager show all data."""
    pass