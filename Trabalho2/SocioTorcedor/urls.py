from django.urls import path
from . import views

urlpatterns = [
    path('planos/', views.PlansView.as_view(), name='render_plans'),
    path('cadastro/', views.UserView.as_view(), name='create_user')
]
