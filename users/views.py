from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Perfil, Mensagem  # IMPORTANTE: Adicionado para o Django reconhecer a tabela Perfil
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import EditarPerfilForm



@login_required # Só quem está logado pode ver o perfil
def perfil(request):
    # O Django já coloca o 'user' e o 'user.perfil' no request automaticamente
    return render(request, 'users/perfil.html')
def home(request):
    return render(request, 'users/home.html')

def login_view(request):
    if request.method == 'POST':
        username_login = request.POST.get("username")
        password_login = request.POST.get("password")
        user = authenticate(request, username=username_login, password=password_login)#vai ver se a pass condiz com o username
        if user is not None:
            login(request, user) #faz login
            return redirect('atividades:home2') #redireciona para a home 
        else:
            messages.error(request, "Credenciais inválidas. Tente novamente.") 
            return render(request, 'users/login.html')  
    return render(request, 'users/login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction # Importante para segurança
from .models import Perfil

def registar(request):
    if request.method == 'POST':
        # 1. Recolher os dados
        dados = request.POST
        
        # 2. Validações básicas
        if dados.get('password') != dados.get('confirm_password'):
            messages.error(request, "As palavras-passe não coincidem!")
            return render(request, 'users/registar.html')

        if User.objects.filter(username=dados.get('username')).exists():
            messages.error(request, "Este nome de utilizador já está em uso.")
            return render(request, 'users/registar.html')

        try:
            # 3. Criação Atómica (Tudo ou Nada)
            with transaction.atomic():
                user = User.objects.create_user(
                    username=dados.get('username'),
                    email=dados.get('email'),
                    password=dados.get('password')
                )
                
                Perfil.objects.create(
                    user=user, 
                    instituicao=dados.get('instituicao'), 
                    idade=dados.get('idade'), 
                    ano_letivo=dados.get('ano_letivo')
                )
            
            messages.success(request, "Conta criada com sucesso! Podes agora entrar.")
            return redirect('login') 
        except Exception as e:
            messages.error(request, "Ocorreu um erro ao criar a conta. Tente novamente.")
            return render(request, 'users/registar.html')

    return render(request, 'users/registar.html')

def sobrenos(request):
    if request.method == 'POST':
        # PROTEÇÃO: Verificar autenticação para POST
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Autenticação necessária para enviar mensagens.')
        
        # Recolher dados do formulário
        assunto = request.POST.get('assunto', '').strip()
        mensagem_texto = request.POST.get('mensagem', '').strip()
        
        # Validações básicas
        if not assunto or not mensagem_texto:
            messages.error(request, "Por favor, preenche todos os campos.")
            return render(request, 'users/sobrenos.html')
        
        # Validação adicional de tamanho
        if len(assunto) > 200 or len(mensagem_texto) > 5000:
            messages.error(request, "Mensagem muito longa. Reduz o tamanho.")
            return render(request, 'users/sobrenos.html')
        
        try:
            # Guardar mensagem na BD
            Mensagem.objects.create(
                user=request.user,
                assunto=assunto,
                mensagem=mensagem_texto
            )
            messages.success(request, "✅ Mensagem enviada com sucesso! Obrigado pelo feedback.")
            return redirect('atividades:home2')
        except Exception as e:
            messages.error(request, "❌ Ocorreu um erro ao enviar a mensagem. Tente novamente.")
            return render(request, 'users/sobrenos.html')
    
    return render(request, 'users/sobrenos.html')

@login_required
def perfil(request):
    # O Django já coloca o 'user' e o 'user.perfil' no request automaticamente
    return render(request, 'users/perfil.html')

def logout_view(request):
    # Não resetar os filtros - deixar guardados na BD para próximo login
    logout(request)
    messages.info(request, "Sessão terminada com sucesso.")
    return redirect('home')


@login_required
def salvar_acessibilidade(request):
    tipo  = request.POST.get('tipo')
    valor = request.POST.get('valor')   

    perfil = request.user.perfil
    if tipo == 'daltonismo':
        perfil.daltonismo = valor 
    elif tipo == 'contraste':
        perfil.contraste = valor

    perfil.save()
    return JsonResponse({'status': 'success'})

@receiver(post_save, sender=User)
def criar_perfil_utilizador_social(sender, instance, created, **kwargs):
    if created:
        # Cria o perfil com valores padrão para evitar o erro RelatedObjectDoesNotExist no caso de login com google
        Perfil.objects.get_or_create(
            user=instance,
            defaults={
                'filtro_daltonismo': 'normal',
                'filtro_contraste': 'normal',
                'instituicao': 'Não definida',
                'ano_letivo': 'Não definido',
                'idade': 0
            }
        )

@login_required
def editar_perfil(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil') # Redireciona de volta para o perfil
    else:
        form = EditarPerfilForm(instance=perfil)
    
    return render(request, 'users/editar_perfil.html', {'form': form})