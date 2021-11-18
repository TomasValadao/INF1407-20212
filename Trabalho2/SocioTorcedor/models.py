from django.db import models

# Create your models here.

class Usuario(models.Model):
    name = models.CharField(max_length=40)
    cpf = models.IntegerField(unique=True)

class Plano(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)