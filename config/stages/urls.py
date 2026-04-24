from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Stagiaire
    path('stages/', views.liste_stages, name='liste_stages'),
    path('postuler/<int:id>/', views.postuler_stage, name='postuler_stage'),

    # Société
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ajouter/', views.ajouter_stage, name='ajouter_stage'),
    path('modifier/<int:id>/', views.modifier_stage, name='modifier_stage'),
    path('supprimer/<int:id>/', views.supprimer_stage, name='supprimer_stage'),
    path('candidatures/', views.voir_candidatures, name='candidatures'),
]