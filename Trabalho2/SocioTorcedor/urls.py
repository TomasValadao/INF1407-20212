from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import include, path
from django.urls.base import reverse_lazy
from . import views

urlpatterns = [
    path('subscriptions/', views.SubscriptionView.as_view(), name='subscriptions'),
    path('register/', views.RegisterView.as_view(), name='create_user'),
    path('accounts/login/', LoginView.as_view(template_name='accounts/login.html', success_url=reverse_lazy('subscriptions')), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('account_login')), name='account_logout'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='accounts/password_change_form.html', success_url=reverse_lazy('account_password_change_done')), name='account_password_change'),
    path('accounts/password_change_done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='account_password_change_done'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html', success_url=reverse_lazy('account_password_reset_done'), email_template_name='accounts/password_reset_email.html', subject_template_name='accounts/password_reset_subject.txt', from_email='valadaotomas@gmail.com'), name='account_password_reset'),
    path('accounts/password_reset_done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='account_password_reset_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', success_url=reverse_lazy('account_password_reset_complete')), name='account_password_reset_confirm'),
    path('accounts/password_reset_complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='account_password_reset_complete'),
]