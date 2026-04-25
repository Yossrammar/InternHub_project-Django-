from django.contrib import admin
from .models import Stage, Candidature, Stagiaire, Societe


admin.site.register(Stage)
admin.site.register(Candidature)
admin.site.register(Stagiaire)
admin.site.register(Societe)