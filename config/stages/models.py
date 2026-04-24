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