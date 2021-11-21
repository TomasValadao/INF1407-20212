from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from .models import Plano
from .forms import UsuarioForm

class OverrideUpdateView(LoginRequiredMixin, UpdateView):
    def get(self, request, pk, *args, **kwargs):
        if request.user.id == pk:
            return super().get(request, pk, args, kwargs)
        else:
            return redirect('sec-home')

class PlansView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        plans = Plano.objects.all()

        return render(request, 'planos.html', {'plans': plans})

class UserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {'formulario' : UsuarioForm}
        return render(request, 'cadastro.html', context)

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('render_plans')