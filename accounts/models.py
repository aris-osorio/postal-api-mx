from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser


from rest_framework.authtoken.models import Token


class User(AbstractUser):

    environment = models.CharField(
        max_length=75,
        choices=(
            ('SANDBOX', "Sandbox"),
            ('PRODUCTION', "Producción"),
        ),
        default='SANDBOX',
        verbose_name = 'Ambiente'
    )

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return str(self.username)

    @property
    def access_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token.key
