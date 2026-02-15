import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import QuizPergunta, OpcaoPergunta, ResultadoQuiz, HistoricoQuiz

def home2(request):
    return render(request, 'atividades/home2.html')

@login_required
@require_http_methods(["POST"])
def atualizar_filtros_acessibilidade(request):
    """View para atualizar os filtros de daltonismo e contraste do perfil do usuário"""
    import json
    try:
        data = json.loads(request.body)
        tipo = data.get('tipo')  # 'daltonismo' ou 'contraste'
        valor = data.get('valor')
        
        perfil = request.user.perfil
        
        if tipo == 'daltonismo':
            perfil.filtro_daltonismo = valor
        elif tipo == 'contraste':
            perfil.filtro_contraste = valor
        
        perfil.save()
        return JsonResponse({'status': 'sucesso', 'mensagem': 'Filtros atualizados com sucesso'})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)

@login_required
def quiz(request):

    if 'quiz_indice' not in request.session:
        lingua = request.user.perfil.lingua
        perguntas = list(QuizPergunta.objects.filter(lingua=lingua, nivel_dificuldade=request.user.perfil.nivel_quiz))

        if not perguntas:
            messages.error(request, "Não há perguntas disponíveis para o seu nível e língua.")
            return redirect('atividades:home2')
        
        indice = [p.id for p in random.sample(perguntas, min(len(perguntas), 7))]
        request.session['quiz_indice'] = indice
        request.session['pergunta_atual'] = 0
        request.session['pontuacao'] = 0
        request.session['respostas_utilizador'] = []

    indice = request.session['quiz_indice']
    atual = request.session['pergunta_atual']

    if atual >= len(indice):
        return redirect('atividades:quiz_final')
    
    pergunta = QuizPergunta.objects.get(id=indice[atual])
    opcoes = pergunta.opcoes.all().order_by('id') 

    context = {
        'pergunta': pergunta,
        'opcoes': opcoes,
        'numero': atual + 1,
        'total': len(indice),
        'mostrar_popup': False # Começa sempre como False
    }

    if request.method == 'POST':
        resposta_letra = request.POST.get('resposta')
        print(f"BOTÃO CLICADO! Resposta: {resposta_letra}") 
        
        esta_correto = (resposta_letra == pergunta.resposta_correta)

        # Atualiza o histórico de respostas na sessão
        respostas = request.session.get('respostas_utilizador', [])
        respostas.append({
            'pergunta': pergunta.id,
            'resposta_dada': resposta_letra,
            'correta': esta_correto
        })
        request.session['respostas_utilizador'] = respostas

        # se acertar aumenta a pontuacao
        if esta_correto:
            request.session['pontuacao'] += 1

        #mete o popup a mostrar a explicacao e se ta correto ou errado
        context.update({
            'mostrar_popup': True,
            'esta_correto': esta_correto,
            'explicacao': pergunta.explicacao
        })

        #salva a sessao na bd
        request.session.modified = True

    return render(request, 'atividades/quiz.html', context)

@login_required
def proximo_passo(request):
    
    if 'pergunta_atual' in request.session:
        request.session['pergunta_atual'] += 1
        request.session.modified = True  # Garantir que a sessão é salva

        if request.session['pergunta_atual'] >= len(request.session['quiz_indice']):#verific outravez se ja ta na ultima pergunta
            return redirect('atividades:quiz_final')

    return redirect('atividades:quiz')


@login_required
def quiz_final(request):
    #vai gravar os dados na bd e limpar a sessao
    if 'quiz_indice' not in request.session:
        return redirect('home2')
    
    pontos = request.session['pontuacao'] #pontos do quiz
    total = len(request.session['quiz_indice'])#perguntas do quiz
    percentagem = (pontos / total) * 100

    resultado = ResultadoQuiz.objects.create(
        perfil = request.user.perfil,
        nivel = request.user.perfil.nivel_quiz,
        pontuacao = pontos,
        total_perguntas = total,
        percentagem = percentagem
    )

    #Grava o historico do quiz
    for item in request.session['respostas_utilizador']:
        HistoricoQuiz.objects.create(
            resultado_quiz = resultado,
            pergunta_id = item['pergunta'],
            escolha_utilizador = item['resposta_dada'],
            foi_correta = item['correta']
        )

    perfil = request.user.perfil
    perfil.quizzes_realizados += 1

    perfil.soma_percentagens += percentagem

    subiu  =False

    perfil.pontuacao_total_quiz += pontos
    if perfil.pontuacao_total_quiz >=30:
        perfil.nivel_quiz += 1
        perfil.pontuacao_total_quiz -=30
        subiu = True

    perfil.save()

    #limpa a sessao
    del request.session['quiz_indice']
    del request.session['pergunta_atual']
    del request.session['pontuacao']
    del request.session['respostas_utilizador']

    return render(request, 'atividades/quiz_final.html',{
        'pontos': pontos,
        'total': total,
        'resultado': resultado,
        'xp_atual': perfil.pontuacao_total_quiz,
        'nivel_atual': perfil.nivel_quiz,
        'subiu': subiu
    })

@login_required
def historico_atividades(request):
    # O filtro garante que o utilizador só vê os seus próprios dados
    resultados = ResultadoQuiz.objects.filter(perfil=request.user.perfil).order_by('-data_conclusao')
    
    return render(request, 'atividades/historico.html', {
        'resultados': resultados
    })

@login_required
def detalhe_historico(request, resultado_id):
    # Procura o resultado garantindo que pertence ao utilizador atual
    resultado = ResultadoQuiz.objects.get(id=resultado_id, perfil=request.user.perfil)
    
    respostas = resultado.detalhes.all()

    for item in respostas:
        # opção da pergunta q a letra e igual com a escolha do utilizador
        item.texto_escolha = item.pergunta.opcoes.filter(letra=item.escolha_utilizador).first()
        #opção que é a correta
        item.texto_correta = item.pergunta.opcoes.filter(letra=item.pergunta.resposta_correta).first()
    
    return render(request, 'atividades/detalhe_historico.html', {
        'resultado': resultado,
        'respostas': respostas
    })


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
