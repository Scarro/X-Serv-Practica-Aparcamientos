from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class PerfilUsuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nombre = models.CharField(max_length=200, unique=True)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null =True)
    size = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return self.user.username

