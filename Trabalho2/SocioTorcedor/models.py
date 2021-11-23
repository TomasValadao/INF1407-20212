from django.db import models

# Create your models here.

class Usuario(models.Model):
    name = models.CharField(max_length=40)
    cpf = models.IntegerField(unique=True)
    email = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name

class Plano(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class PlanoAdquirido(models.Model):
    usuario = models.ForeignKey(Usuario, null=True, on_delete=models.SET_NULL)
    plano = models.ForeignKey(Plano, null=True, on_delete=models.SET_NULL)