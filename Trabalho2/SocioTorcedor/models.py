from django.db import models

# Create your models here.

class Usuario(models.Model):
    name = models.CharField(max_length=40)
    cpf = models.IntegerField(max_length=11, unique=True)

class Plano(models.Model):
    nome = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2)