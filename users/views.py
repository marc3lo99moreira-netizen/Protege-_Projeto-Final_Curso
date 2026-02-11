from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Perfil  # IMPORTANTE: Adicionado para o Django reconhecer a tabela Perfil

def home(request):
    return render(request, 'users/home.html')

def login_view(request):
    return render(request, 'users/login.html')

def registar(request):
    if request.method == 'POST':
        # 1. Recolher os dados do formulário
        email = request.POST.get('email')
        instituicao = request.POST.get('instituicao')
        idade = request.POST.get('idade')
        ano_letivo = request.POST.get('ano_letivo')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 2. Validações
        if password != confirm_password:
            messages.error(request, "As palavras-passe não coincidem!")
            return render(request, 'users/registar.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de utilizador já está em uso.")
            return render(request, 'users/registar.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        
        Perfil.objects.create(
            user=user, 
            instituicao=instituicao, 
            idade=idade, 
            ano_letivo=ano_letivo
        )
        
        messages.success(request, "Conta criada com sucesso! Podes agora entrar.")
        return redirect('login')

    # Se for um pedido GET (abrir a página), mostra o formulário
    return render(request, 'users/registar.html')

def sobrenos(request):
    return render(request, 'users/sobrenos.html')




def perfil(request):
    return render (request, 'users/perfil.html')