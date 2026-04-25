from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Home
    path('', views.home, name='home'),

    # 🔓 Logout
    path('logout/', views.logout_view, name='logout'),

    # ===========================
    # 👤 STAGIAIRE
    # ===========================
    path('stagiaire/signup/', views.signup_stagiaire, name='signup_stagiaire'),
    path('stagiaire/login/', views.login_stagiaire, name='login_stagiaire'),
    
    path('stages/', views.liste_stages, name='liste_stages'),
    path('postuler/<int:id>/', views.postuler_stage, name='postuler_stage'),
    path('annuler/<int:id>/', views.annuler_postulation, name='annuler_postulation'),
    path('profil/', views.profil_stagiaire, name='profil_stagiaire'),
    

    # ===========================
    # 🏢 SOCIETE
    # ===========================
    path('societe/signup/', views.signup_societe, name='signup_societe'),
    path('societe/login/', views.login_societe, name='login_societe'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('ajouter/', views.ajouter_stage, name='ajouter_stage'),
    path('modifier/<int:id>/', views.modifier_stage, name='modifier_stage'),
    path('supprimer/<int:id>/', views.supprimer_stage, name='supprimer_stage'),
    path('candidatures/', views.voir_candidatures, name='candidatures'),
]