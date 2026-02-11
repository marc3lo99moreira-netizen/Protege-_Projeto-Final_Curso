from django.db import models
from django.contrib.auth.models import User



class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    instituicao = models.CharField(max_length=200)
    idade = models.IntegerField()
    ano_letivo = models.CharField(max_length=50)

    def __str__(self):
        return f"Perfil de {self.user.username}"