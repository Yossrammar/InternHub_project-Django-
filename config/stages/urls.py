from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.liste_stages, name='liste_stages'),
    path('ajouter/', views.ajouter_stage, name='ajouter_stage'),
    path('modifier/<int:id>/', views.modifier_stage, name='modifier_stage'),
    path('supprimer/<int:id>/', views.supprimer_stage, name='supprimer_stage'),
    path('', views.home, name='home'),
    path('stages/', views.liste_stages, name='liste_stages'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('postuler/<int:id>/', views.postuler_stage, name='postuler_stage'),
    path('candidatures/', views.voir_candidatures, name='candidatures'),
]
