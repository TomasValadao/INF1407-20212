from django.shortcuts import render
from .models import Plano

# Create your views here.
def get_plans(request):
    plans = Plano.objects.all()

    return render(request, 'planos.html', {'plans': plans})

