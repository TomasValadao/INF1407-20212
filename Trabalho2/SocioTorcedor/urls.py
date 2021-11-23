from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import include, path
from django.urls.base import reverse_lazy
from . import views

urlpatterns = [
    path('planos/', views.PlansView.as_view(), name='render_plans'),
    path('planos/meus_planos', views.UserPlansView.as_view(), name='render_my_plans'),
    path('cadastro/', views.UserView.as_view(), name='create_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='accounts/password_change_form.html', success_url=reverse_lazy('password_change_done')), name='password_change'),
    path('accounts/password_change_done/', PasswordChangeDoneView.as_view( template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html', success_url=reverse_lazy('password_reset_done'), email_template_name='accounts/password_reset_email.html', subject_template_name='accounts/password_reset_subject.txt', from_email='valadaotomas@gmail.com'), name='password_reset'),
    path('accounts/password_reset_done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('accounts/password_reset_complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
