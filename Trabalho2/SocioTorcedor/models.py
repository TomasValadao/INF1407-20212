from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=False)
    cpf = models.IntegerField(unique=True)
    USERNAME_FIELD = 'username'

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.SET_NULL)
