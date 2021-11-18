from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Plano
from .forms import UsuarioForm

# Create your views here.
def render_plans(request):
    plans = Plano.objects.all()

    return render(request, 'planos.html', {'plans': plans})

def create_user(request):
    form = UsuarioForm(request.POST or None)

    if form.is_valid():
        form.save()
        
        return redirect('render_plans')

    return render(request, 'cadastro.html', {'form': form})