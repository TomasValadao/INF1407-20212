from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from .models import Plano, PlanoAdquirido, UserProfile, Usuario
from .forms import UsuarioForm
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

#region User Actions

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_url = reverse('subscriptions')

            return redirect(f'{redirect_url}?user_id={request.user.id}')
        else:
            return redirect('account_login')

#endregion

#region Subscription Actions

class SubscriptionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')

        if request.user.is_authenticated and request.user.id == user_id:
            user = UserProfile.objects.get(id=user_id)
            subscriptions = Subscription.objects.filter(usuario=user).all()

            return render(request, 'planos_usuario.html', {'subscriptions': subscriptions})
        else:
            return redirect('account_login')

class SubscriptionDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        subscription = Subscription.objects.get(pk=pk)
        
        return render(request, 'planoadquirido_confirm_delete.html', {'subscription': subscription})

    def post(self, request, pk, *args, **kwargs):
        subscription = Subscription.objects.get(pk=pk)
        subscription.delete()

        return redirect('render_my_plans')

#endregion