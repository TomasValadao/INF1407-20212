from django.urls import path
from . import views

urlpatterns = [
    path('planos/', views.render_plans, name='render_plans'),
    path('cadastro/', views.create_user, name='create_user')
]
