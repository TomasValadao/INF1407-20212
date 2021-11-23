from django.contrib import admin
from .models import Plano, PlanoAdquirido, Usuario

admin.site.register(Plano)
admin.site.register(Usuario)
admin.site.register(PlanoAdquirido)
# Register your models here.
