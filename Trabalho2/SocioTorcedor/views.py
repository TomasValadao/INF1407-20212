from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from .models import Plano, PlanoAdquirido, Usuario
from .forms import UsuarioForm

class OverrideUpdateView(LoginRequiredMixin, UpdateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.id == pk:
            return super().get(request, pk, args, kwargs)
        else:
            return redirect('sec-home')

class PlansView(View):
    def get(self, request, *args, **kwargs):
        plans = Plano.objects.all()

        return render(request, 'planos.html', {'plans': plans})

class UserPlansView(View):
    def get(self, request, *args, **kwargs):
        user = Usuario.objects.get(cpf='16592756799')
        plans = PlanoAdquirido.objects.filter(usuario=user).all()

        return render(request, 'planos_usuario.html', {'plans': plans})

class UserView(View):
    def get(self, request, *args, **kwargs):
        context = {'form' : UsuarioForm}
        return render(request, 'cadastro.html', context)

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('render_plans')