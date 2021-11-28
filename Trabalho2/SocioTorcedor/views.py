from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from .models import Plan, Subscription, UserProfile
from .forms import UserProfileCreateForm, RegistrationForm

#region Auth Actions

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'auth_user' : RegistrationForm,
            'user_profile' : UserProfileCreateForm
        }
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        auth_form = RegistrationForm(request.POST)
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

#region User Actions

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_url = reverse('subscriptions')

            return redirect(f'{redirect_url}?user_id={request.user.id}')
        else:
            return redirect('account_login')

#endregion

#region Plan Actions

class PlansView(View):
    def get(self, request, *args, **kwargs):
        plans = Plan.objects.all()

        return render(request, 'planos.html', {'plans': plans})

#endregion

#region Subscription Actions

class SubscriptionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = UserProfile.objects.get(user_id=request.user.id)
            subscriptions = Subscription.objects.filter(user=user).all()

            return render(request, 'planos_usuario.html', {'subscriptions': subscriptions})
        else:
            return redirect('account_login')

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            plan = Plan.objects.get(pk=pk)
            user = UserProfile.objects.get(user_id=request.user.id)

            new_subscription = Subscription(user=user, plan=plan)
            new_subscription.save()

            return redirect('subscriptions')

        else:
            return redirect('account_login')

class SubscriptionDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        subscription = Subscription.objects.get(pk=pk)
        
        return render(request, 'planoadquirido_confirm_delete.html', {'subscription': subscription})

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            subscription = Subscription.objects.get(pk=pk)
            subscription.delete()

            return redirect('subscriptions')

        else:
            return redirect('account_login')

#endregion