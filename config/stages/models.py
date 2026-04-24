from django.contrib.auth.models import User
from django.db import models

class Stage(models.Model):
    titre = models.CharField(max_length=100)
    type_stage = models.CharField(max_length=20, null=True, blank=True)
    entreprise = models.CharField(max_length=100)
    description = models.TextField()
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titre

class Candidature(models.Model):
    stagiaire = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    date_postulation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stagiaire.username} -> {self.stage.titre}"