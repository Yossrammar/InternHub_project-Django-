from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_stages, name='liste_stages'),
    path('ajouter/', views.ajouter_stage, name='ajouter_stage'),
    path('modifier/<int:id>/', views.modifier_stage, name='modifier_stage'),
    path('supprimer/<int:id>/', views.supprimer_stage, name='supprimer_stage'),
    
]