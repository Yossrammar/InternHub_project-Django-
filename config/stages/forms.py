from django import forms
from .models import Stage, Stagiaire, Societe


# ===========================
# 📄 STAGE FORM
# ===========================
class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = [
            'titre',
            'description',
            'type_stage',
            'localisation',
            'est_paye',
            'pre_embauche'
        ]


# ===========================
# 👤 STAGIAIRE FORM
# ===========================
class StagiaireForm(forms.ModelForm):
    class Meta:
        model = Stagiaire
        fields = [
            'linkedin',
            'github',
            'date_naissance',
            'telephone',
            'cv'
        ]


# ===========================
# 🏢 SOCIETE FORM
# ===========================
class SocieteForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields = [
            'nom',
            'description',
            'secteur',
            'site_web',
            'telephone'
        ]