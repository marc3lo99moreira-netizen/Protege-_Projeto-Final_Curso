from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'atividades'
urlpatterns = [
    path('home2/', views.home2, name='home2'),
    path('quiz/', views.quiz, name='quiz'),
    path('proximo_passo/', views.proximo_passo, name='proximo_passo'),
    path('quiz_final/', views.quiz_final, name='quiz_final'),
    path('simulador/', views.simulador, name='simulador'),
    path('proximo_email/', views.proximo_email, name='proximo_email'),
]