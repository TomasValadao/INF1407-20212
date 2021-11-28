from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from .models import Subscription
from .forms import UserProfileCreateForm

#region Auth Actions

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'auth_user' : UserCreationForm,
            'user_profile' : UserProfileCreateForm
        }
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        auth_form = UserCreationForm(request.POST)
        user_profile_form = UserProfileCreateForm(request.POST)

        if auth_form.is_valid() and user_profile_form.is_valid():
            user = auth_form.save()
            user_profile_form.save(user)

            return redirect('account_login')
        else:
            return redirect('create_user')

class OverrideUpdateView(LoginRequiredMixin, UpdateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.id == pk:
            return super().get(request, pk, args, kwargs)
        else:
            return redirect('account_login')

#endregion

#region Subscription Actions

class SubscriptionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')

        if request.user.is_authenticated and user_id is not None and request.user.id == int(user_id):
            subscriptions = Subscription.objects.all()

            context = {
                'subscriptions': subscriptions
            }

            return render(request, 'subscriptions.html', context)
        else:
            return redirect('account_login')

#endregion