from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Pais(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Contacto(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre