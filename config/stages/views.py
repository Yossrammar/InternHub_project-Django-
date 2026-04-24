from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Stage, Candidature
from .forms import StageForm


# 🏠 HOME
def home(request):
    return render(request, 'home.html')


# 🔐 LOGIN (redirige selon rôle)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_staff:
                return redirect('dashboard')     # société
            else:
                return redirect('liste_stages')  # stagiaire
        else:
            messages.error(request, "Login invalide ❌")

    return render(request, 'login.html')


# 🔓 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# 👤 STAGIAIRE → voir stages
@login_required
def liste_stages(request):
    if request.user.is_staff:
        return redirect('dashboard')  # sécurité

    stages = Stage.objects.all()
    return render(request, 'stages/liste.html', {'stages': stages})


# 📩 POSTULER
@login_required
def postuler_stage(request, id):
    if request.user.is_staff:
        return redirect('dashboard')

    stage = get_object_or_404(Stage, id=id)

    if not Candidature.objects.filter(stagiaire=request.user, stage=stage).exists():
        Candidature.objects.create(stagiaire=request.user, stage=stage)
        messages.success(request, "Candidature envoyée ✅")
    else:
        messages.warning(request, "Déjà postulé ❗")

    return redirect('liste_stages')


# 🏢 DASHBOARD SOCIÉTÉ
@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('liste_stages')

    stages = Stage.objects.all()
    return render(request, 'stages/dashboard.html', {'stages': stages})


# 📊 VOIR CANDIDATURES
@login_required
def voir_candidatures(request):
    if not request.user.is_staff:
        return redirect('home')

    candidatures = Candidature.objects.all()
    return render(request, 'stages/candidatures.html', {'candidatures': candidatures})


# ➕ AJOUTER STAGE
@login_required
def ajouter_stage(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == "POST":
        form = StageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Stage ajouté ✅")
            return redirect('dashboard')
    else:
        form = StageForm()

    return render(request, 'stages/ajouter.html', {'form': form})


# ✏️ MODIFIER STAGE
@login_required
def modifier_stage(request, id):
    if not request.user.is_staff:
        return redirect('home')

    stage = get_object_or_404(Stage, id=id)

    if request.method == "POST":
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            messages.success(request, "Stage modifié ✅")
            return redirect('dashboard')
    else:
        form = StageForm(instance=stage)

    return render(request, 'stages/modifier.html', {'form': form})


# ❌ SUPPRIMER STAGE
@login_required
def supprimer_stage(request, id):
    if not request.user.is_staff:
        return redirect('home')

    stage = get_object_or_404(Stage, id=id)
    stage.delete()
    messages.success(request, "Stage supprimé ❌")

    return redirect('dashboard')