from django.shortcuts import render, redirect
from .models import Stage
from .forms import StageForm

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