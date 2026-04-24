from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Stage
from .forms import StageForm
from django.contrib.auth import authenticate, login


def liste_stages(request):
    stages = Stage.objects.all()
    return render(request, 'stages/liste.html', {'stages': stages})

def ajouter_stage(request):
    if request.method == "POST":
        form = StageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_stages')
    else:
        form = StageForm()

    return render(request, 'stages/ajouter.html', {'form': form})


def modifier_stage(request, id):
    stage = Stage.objects.get(id=id)

    if request.method == "POST":
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            return redirect('liste_stages')
    else:
        form = StageForm(instance=stage)

    return render(request, 'stages/modifier.html', {'form': form})

def supprimer_stage(request, id):
    stage = Stage.objects.get(id=id)
    stage.delete()
    return redirect('liste_stages')


def home(request):
    return render(request, 'home.html')

def dashboard(request):
    stages = Stage.objects.all()
    return render(request, 'stages/dashboard.html', {'stages': stages})



@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    
    stages = Stage.objects.all()
    return render(request, 'stages/dashboard.html', {'stages': stages})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 redirection selon rôle
            if user.is_staff:
                return redirect('dashboard')  # société
            else:
                return redirect('liste_stages')  # stagiaire

    return render(request, 'login.html')

from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Candidature, Stage

@login_required
def postuler_stage(request, id):
    stage = Stage.objects.get(id=id)

    # empêcher double candidature
    if not Candidature.objects.filter(stagiaire=request.user, stage=stage).exists():
        Candidature.objects.create(
            stagiaire=request.user,
            stage=stage
        )
        messages.success(request, "Candidature envoyée ✅")

    else:
        messages.warning(request, "Déjà postulé ❗")

    return redirect('liste_stages')


@login_required
def voir_candidatures(request):
    if not request.user.is_staff:
        return redirect('home')

    candidatures = Candidature.objects.all()
    return render(request, 'stages/candidatures.html', {'candidatures': candidatures})