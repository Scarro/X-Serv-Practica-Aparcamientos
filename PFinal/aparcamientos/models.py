from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Aparcamiento(models.Model):
    identidad = models.IntegerField(unique=True)
    slug = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    accesibilidad = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=300)
    likes = models.IntegerField(default=0)
    # Localizacion
    nombrevia = models.CharField(max_length=100, blank=True, null=True)
    clasevial = models.CharField(max_length=100, blank=True, null=True)
    tiponum = models.CharField(max_length=10, blank=True, null=True)
    numero = models.CharField(max_length=10, null=True)
    localidad = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    cpostal = models.IntegerField(blank=True, null=True)
    barrio = models.CharField(max_length=100, blank=True, null=True)
    distrito = models.CharField(max_length=100, blank=True, null=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    latitud = models.FloatField(blank= True, null=True)
    longitud = models.FloatField(blank= True, null=True)
    # Contacto
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Aparcamiento"
        verbose_name_plural = "Aparcamientos"

    def __str__(self):
        return self.nombre

    def save(self, *args,**kwargs):
        self.slug = slugify(self.nombre)
        return super(Aparcamiento, self).save(*args, **kwargs)

class Comentario(models.Model):
    usuario = models.ForeignKey(
        User,
        related_name="comentario_usuario",
        on_delete=models.CASCADE)
    aparcamiento = models.ForeignKey(
        Aparcamiento,
        related_name="comentario_aparcamiento",
        on_delete=models.CASCADE)
    titulo = models.CharField(max_length=300)
    cuerpo = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('aparcamientos:detalle', kwargs={'aparcamiento_identidad':self.aparcamiento.identidad})

class Seleccion(models.Model):
    aparcamiento = models.ForeignKey(
        Aparcamiento,
        related_name="seleccion_aparcamiento",
        on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        User,
        related_name="seleccion_usuario",
        on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Seleccion"
        verbose_name_plural = "Selecciones"

    def __str__(self):
        return self.usuario.username