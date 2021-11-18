from django.urls import path
from . import views

urlpatterns = [
    path('planos/', views.get_plans)
]
