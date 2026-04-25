from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Stagiaire
from .forms import StagiaireForm
from .models import Stage, Candidature
from .forms import StageForm, StagiaireForm, SocieteForm


# 🏠 HOME
def home(request):
    return render(request, 'home.html')


# ===========================
# 🔐 AUTHENTIFICATION
# ===========================

def login_stagiaire(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            # 🔥 vérifier qu'il est stagiaire
            if Stagiaire.objects.filter(user=user).exists():
                login(request, user)
                return redirect('liste_stages')
            else:
                messages.error(request, "Ce compte n'est pas un stagiaire ❌")
        else:
            messages.error(request, "Identifiants incorrects ❌")

    return render(request, 'stagiaire/login.html')

def login_societe(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Compte invalide pour société ❌")

    return render(request, 'societe/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ===========================
# 📝 SIGNUP
# ===========================
def signup_stagiaire(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username, password=password)

        form = StagiaireForm(request.POST, request.FILES)
        if form.is_valid():
            stagiaire = form.save(commit=False)
            stagiaire.user = user
            stagiaire.save()

        # 🔥 LOGIN DIRECT
        login(request, user)

        return redirect('liste_stages')  # 🔥 direct vers stages

    form = StagiaireForm()
    return render(request, 'stagiaire/signup.html', {'form': form})



def signup_societe(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True
        user.save()

        form = SocieteForm(request.POST)
        if form.is_valid():
            societe = form.save(commit=False)
            societe.user = user
            societe.save()

        # 🔥 LOGIN DIRECT
        login(request, user)

        return redirect('dashboard')

    form = SocieteForm()
    return render(request, 'societe/signup.html', {'form': form})
# ===========================
# 👤 STAGIAIRE
# ===========================


@login_required
def profil_stagiaire(request):

    # 🔒 sécurité : une société ne peut pas accéder
    if request.user.is_staff:
        return redirect('dashboard')

    stagiaire = get_object_or_404(Stagiaire, user=request.user)

    # 🔥 FORMULAIRE (édition)
    form = StagiaireForm(request.POST or None,
                         request.FILES or None,
                         instance=stagiaire)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour ✅")
            return redirect('profil_stagiaire')

    return render(request, 'stagiaire/profil.html', {
        'stagiaire': stagiaire,
        'form': form
    })


@login_required
def liste_stages(request):
    if request.user.is_staff:
        return redirect('dashboard')

    stages = Stage.objects.all()

    candidatures = Candidature.objects.filter(stagiaire=request.user)
    candidatures_ids = [c.stage.id for c in candidatures]

    return render(request, 'stages/liste.html', {
        'stages': stages,
        'candidatures_ids': candidatures_ids
    })

@login_required
def postuler_stage(request, id):
    if request.user.is_staff:
        return redirect('dashboard')

    stage = get_object_or_404(Stage, id=id)

    if not Candidature.objects.filter(stagiaire=request.user, stage=stage).exists():
        Candidature.objects.create(stagiaire=request.user, stage=stage)
        messages.success(request, "Postulation envoyée ✅")

    return redirect('liste_stages')

@login_required
def annuler_postulation(request, id):
    candidature = Candidature.objects.filter(
        stagiaire=request.user,
        stage_id=id
    )

    if candidature.exists():
        candidature.delete()
        messages.info(request, "Postulation annulée ❌")

    return redirect('liste_stages')

# ===========================
# 🏢 SOCIETE
# ===========================

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('liste_stages')

    # 🔥 récupérer les stages de cette société
    stages = Stage.objects.filter(societe=request.user)

    # 🔥 récupérer les candidatures liées à ces stages
    candidatures = Candidature.objects.filter(stage__societe=request.user)

    # 🔥 IMPORTANT : définir les compteurs
    stages_count = stages.count()
    candidatures_count = candidatures.count()

    return render(request, 'stages/dashboard.html', {
        'stages': stages,
        'stages_count': stages_count,
        'candidatures_count': candidatures_count,
    })

@login_required
def voir_candidatures(request):
    if not request.user.is_staff:
        return redirect('home')

    candidatures = Candidature.objects.filter(stage__societe=request.user)
    return render(request, 'stages/candidatures.html', {'candidatures': candidatures})


# ===========================
# 📄 CRUD STAGE
# ===========================

@login_required
def ajouter_stage(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == "POST":
        form = StageForm(request.POST)
        if form.is_valid():
            stage = form.save(commit=False)
            stage.societe = request.user
            stage.save()
            messages.success(request, "Stage ajouté ✅")
            return redirect('dashboard')
    else:
        form = StageForm()

    return render(request, 'stages/ajouter.html', {'form': form})


@login_required
def modifier_stage(request, id):
    if not request.user.is_staff:
        return redirect('home')

    stage = get_object_or_404(Stage, id=id, societe=request.user)

    if request.method == "POST":
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            form.save()
            messages.success(request, "Stage modifié ✅")
            return redirect('dashboard')
    else:
        form = StageForm(instance=stage)

    return render(request, 'stages/modifier.html', {'form': form})


@login_required
def supprimer_stage(request, id):
    if not request.user.is_staff:
        return redirect('home')

    stage = get_object_or_404(Stage, id=id, societe=request.user)
    stage.delete()

    messages.success(request, "Stage supprimé ❌")
    return redirect('dashboard')