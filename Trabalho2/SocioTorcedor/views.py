from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from .models import Plano
from .forms import UsuarioForm

class PlansView(View):
    def get(self, request, *args, **kwargs):
        plans = Plano.objects.all()

        return render(request, 'planos.html', {'plans': plans})

class UserView(View):
    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST or None)

        if form.is_valid():
            form.save()
            return redirect('render_plans')

        return render(request, 'cadastro.html', {'form': form})