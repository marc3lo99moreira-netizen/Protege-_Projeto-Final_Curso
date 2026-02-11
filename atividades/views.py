from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def home2(request):
    return render(request, 'atividades/home2.html')

def quiz(request):
    perguntas = [

        {
          "id": 1, "p": "Qual destas senhas é a mais segura?",
          "o": ["123456", "admin", "P@ssw0rd2024!", "marcelo123"], 
          "c": "P@ssw0rd2024!",
          "e": "Para que a tua password seja segura deves misturar letras, numeros e simbolos, e de preferência evitar colocar o teu nome nela."
        },

        {
         "id": 2, "p": "O que é o Phishing?", 
         "o": ["Um desporto", "Um ataque por email", "Um antivírus", "Um tipo de ecrã"],
         "c": "Um ataque por email",
         "e": "O phishing é uma técnica de crime cibernético onde os atacantes enviam mensagens falsas para se fazer passar por entidades confiáveis e roubar os teus dados ou senhas"
         },
        
        {
         "id": 3,
          "p": "Deves partilhar a tua localização nas redes sociais?",
          "o": ["Sim, sempre", "Só com estranhos", "Não, por segurança", "Apenas à noite"], 
          "c": "Não, por segurança",
          "e": "Partilhar a tua localização em real pode revelar onde moras ou onde passas o teu tempo, e permite que pessoas mal intencionadas saibam exatamnete onde estas."
        },
        
        {
         "id": 4, "p": "O que significa o cadeado no navegador?", 
         "o": ["Site lento", "Site perigoso", "Conexão segura", "Site bloqueado"], 
         "c": "Conexão segura",
         "e": "O cadeado indica que a tua ligação ao site é encriptada através de um certificado SSL/TLS. Isso garante que dados sensiveis como passwords ou dados bancarios sejam intercetados por terceiros durante o seu envio."
        },

        {
         "id": 5,
         "p": "De quanto em quanto tempo deves mudar a senha?", 
         "o": ["Nunca", "Anualmente", "Regularmente", "Todos os dias"], 
         "c": "Regularmente",
         "e": "Embora não seja necessario mudar de senha todos os dias, fazê-lo regularmente garante que crendenciais antigas deixem de ser utilidade para os hackers."
        },
        
        {
         "id": 6, 
         "p": "A autenticação de dois fatores (2FA) serve para:", 
         "o": ["Mais velocidade", "Dupla segurança", "Gastar bateria", "Ver vídeos"], 
         "c": "Dupla segurança",
         "e": "O 2FA funciona como uma segunda tranca na tua porta.Mesmo que um hacker descubra a tua password ele não vai conseguir entrar na conta sem o segundo códiog que é enviado para o teu telemovel."
        },       
       
        {"id": 7, 
         "p": "Se receberes um link estranho de um amigo, deves:", 
         "o": ["Clicar logo", "Ignorar e avisá-lo", "Enviar a outros", "Apagar o PC"], 
         "c": "Ignorar e avisá-lo",
         "e": "Muitos virus sao espalhados por mensagens automaticas, caso uma mensagem de um amigo pareça estranha, nao cliques e avisa o de imediato"
        }
    ]

    passo = request.session.get('quiz_step', 0)
    pontuacao = request.session.get('pontuacao', 0)

    if passo >= len(perguntas):
        request.session['quiz_step'] = 0 
        return render(request, 'atividades/quiz_final.html')
    
    pergunta_atual = perguntas[passo]

    if request.method == 'POST':
        resposta_utilizador = request.POST.get('resposta')
        esta_correto = (resposta_utilizador == pergunta_atual['c'])

        if esta_correto:
            request.session['pontuacao'] = request.session.get('pontuacao' , 0) + 1
    
        context = {
            'pergunta': pergunta_atual,
            'numero': passo + 1,
            'mostrar_popup': True,
            'esta_correto': esta_correto,
            'explicacao': pergunta_atual['e'],
            'pontuacao': (passo + 1) * 100 / 7
        }
        return render(request, 'atividades/quiz.html', context)
    
    return render(request, 'atividades/quiz.html', {
            'pergunta': pergunta_atual,
            'numero': passo + 1,
            'mostrar_popup': False,
            'progresso': (passo +1 ) * 100/7
            })

def proximo_passo(request):
    passo = request.session.get('quiz_step', 0)
    novo_passo = passo + 1
    request.session['quiz_step'] = novo_passo
    
    # Se chegou à 7ª resposta, vai para o FINAL
    if novo_passo >= 7:
        return redirect('atividades:quiz_final') # Removido o 'atividades:'
        
    return redirect('atividades:quiz') # Removido o 'atividades:'

def quiz_final(request):
    # 1. Primeiro pegamos o valor da pontuação
    pontuacao_obtida = request.session.get('pontuacao', 0)
    
    # 2. Depois limpamos a sessão para o utilizador poder recomeçar no futuro
    request.session['quiz_step'] = 0
    request.session['pontuacao'] = 0

    context = {
        'pontuacao': pontuacao_obtida,
        'Total': 7
    }
    return render(request, 'atividades/quiz_final.html', context)

def simulador(request):    

    email = [
        {
    "id": 1,
    "remetente": "reembolsos@financas-gov.pt.security.com",
    "assunto": "REEMBOLSO DISPONÍVEL - IRS 2024",
    "corpo": """Caro contribuinte, foi identificado um erro no cálculo do seu IRS e tem um <span class='phishing-trigger' data-info='E-mails governamentais reais nunca usam domínios compostos como .gov.pt.security.com.'>reembolso de 450,20€</span> pendente. 
    Para receber o valor, deve validar o seu IBAN no nosso <span class='phishing-trigger' data-info='As Finanças nunca pedem dados bancários por links diretos em e-mails. Deve fazê-lo sempre no Portal das Finanças oficial.'>portal de pagamentos rápidos</span>. 
    Atenção: Se não validar os dados hoje, o <span class='phishing-trigger' data-info='A urgência é usada para te fazer agir por impulso sem verificar a veracidade da mensagem.'>valor expirará</span>.""",
    },

    {
    "id": 2,
    "remetente": "seguranca@bancoportugal-online.net",
    "assunto": "BLOQUEIO DE CONTA - Verificação Necessária",
    "corpo": """Prezado cliente, detetamos um <span class='phishing-trigger' data-info='Bancos reais tratam o cliente pelo nome oficial e raramente usam termos genéricos como "Prezado cliente".'>acesso suspeito</span> na sua conta bancária a partir de um dispositivo novo. 
    Para sua proteção, as suas transferências foram suspensas. <span class='phishing-trigger' data-info='Bancos nunca enviam links diretos para desbloquear contas. O procedimento seguro é usar a App oficial ou ir ao balcão.'>Clique aqui para reativar</span> o seu acesso agora. 
    Caso não realize a verificação em 2 horas, o seu cartão será <span class='phishing-trigger' data-info='Ameaças de cancelamento imediato são usadas para criar pânico e fazer a vítima agir sem pensar.'>cancelado permanentemente</span>.""",
    "e": ""
}
    ]

    passo = request.session.get('simulador_step', 0)

    if passo >= len(email):
        request.session['simulador_step'] = 0
        return redirect('home2')

    email_atual = email[passo]

    return render(request, 'atividades/simulador.html',{
        'email':email_atual,
        'numero': passo + 1
    })


def proximo_email(request):
    passo = request.session.get('simulador_step', 0)
    request.session['simulador_step'] = passo + 1
    return redirect('simulador')
