from django.db import models
from django.contrib.auth.models import User

# 👤 STAGIAIRE
class Stagiaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    linkedin = models.URLField()
    github = models.URLField(blank=True, null=True)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)
    cv = models.FileField(upload_to='', null=True, blank=True)

    def __str__(self):
        return self.user.username


# 🏢 SOCIETE
class Societe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    secteur = models.CharField(max_length=100)
    site_web = models.URLField(blank=True, null=True)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom


# 📄 STAGE
class Stage(models.Model):
    societe = models.ForeignKey(User, on_delete=models.CASCADE)

    titre = models.CharField(max_length=100)
    description = models.TextField()

    TYPE_CHOICES = [
        ('PFE', 'PFE'),
        ('ETE', 'ETE'),
    ]
    type_stage = models.CharField(max_length=10, choices=TYPE_CHOICES)

    localisation = models.CharField(max_length=100)

    est_paye = models.BooleanField(default=False)
    pre_embauche = models.BooleanField(default=False)

    def __str__(self):
        return self.titre

# 📩 CANDIDATURE
class Candidature(models.Model):
    stagiaire = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('stagiaire', 'stage')  # 🔥 empêche double postulation

    def __str__(self):
        return f"{self.stagiaire.username} -> {self.stage.titre}"