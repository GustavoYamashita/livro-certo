from django.db import models
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Case, When, Count, Value, CharField
from django.db.models.functions import Lower, Trim
from .models import Livro, Aluno, Emprestimo
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import random

def biblioteca(request):
    letra = request.GET.get('letra', '').upper()
    busca = request.GET.get('busca', '')
    genero = request.GET.get('genero', '')
    
    livros = Livro.objects.filter(aparecer=True).order_by('nome_livro')
    
    if letra and letra != '#':
        livros = livros.filter(nome_livro__istartswith=letra)
    elif letra == '#':
        livros = livros.filter(nome_livro__iregex=r'^[^a-zA-Z]')
    
    if busca:
        livros = livros.filter(nome_livro__icontains=busca)
        
    if genero:
        livros = livros.filter(genero__iexact=genero)
    
    generos = Livro.objects.filter(aparecer=True).values_list('genero', flat=True).distinct().order_by('genero')
    
    paginator = Paginator(livros, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'galeria/biblioteca.html', {
        'page_obj': page_obj,
        'letra_atual': letra if letra else None,
        'busca_atual': busca,
        'generos': generos,
        'genero_atual': genero
    })

def alunos(request):
    order_by = request.GET.get('order_by', '-total_emprestimos')
    direction = request.GET.get('direction', 'desc')

    if order_by == request.GET.get('current_order_by'):
        direction = 'asc' if direction == 'desc' else 'desc'

    if direction == 'asc':
        order_by = order_by.lstrip('-')
    else:
        if not order_by.startswith('-'):
            order_by = '-' + order_by

    alunos = Aluno.objects.filter(matriculado=True).annotate(
        total_emprestimos=Count('emprestimos')
    )

    podio = list(alunos.order_by('-total_emprestimos')[:3])

    turma_filter = request.GET.get('turma')
    nome_search = request.GET.get('nome')

    if turma_filter:
        alunos = alunos.filter(turma__iexact=turma_filter.strip())
    if nome_search:
        alunos = alunos.filter(nome_aluno__icontains=nome_search)

    alunos = alunos.order_by(order_by)

    paginator = Paginator(alunos, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    turmas = sorted(set(Aluno.objects.filter(matriculado=True).values_list('turma', flat=True)))

    return render(request, 'galeria/alunos.html', {
        'podio': podio,
        'page_obj': page_obj,
        'turmas': turmas,
        'order_by': order_by.lstrip('-'),
        'direction': direction,
        'current_params': request.GET.urlencode()
    })

def emprestar(request):
    return render(request, 'galeria/emprestar.html')

def livros(request):
    nome_search = request.GET.get('nome', '')
    genero_filter = request.GET.get('genero', '')
    
    order_by = request.GET.get('order_by', 'nome_livro')
    direction = request.GET.get('direction', 'asc')

    if direction == 'desc':
        order_by = '-' + order_by

    livros = Livro.objects.filter(aparecer=True)
    
    if nome_search:
        livros = livros.filter(nome_livro__icontains=nome_search)
    if genero_filter:
        livros = livros.filter(genero=genero_filter)
    
    livros = livros.annotate(
        disponivel=Case(
            When(quantidade__gt=0, then=Value('Disponível')),
            default=Value('Indisponível'),
            output_field=CharField()
        )
    )
    
    livros = livros.order_by(order_by)
    
    generos = sorted(set(Livro.objects.filter(aparecer=True).values_list('genero', flat=True)))

    paginator = Paginator(livros, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'galeria/livro-tombo.html', {
        'page_obj': page_obj,
        'generos': generos,
        'nome_atual': nome_search,
        'genero_atual': genero_filter,
        'order_by': order_by.lstrip('-'),
        'direction': direction
    })

def index(request):
    total_livros = Livro.objects.filter(aparecer=True).count()
    total_alunos = Aluno.objects.filter(matriculado=True).count()
    total_emprestimos = Emprestimo.objects.count()

    generos_emprestimos = Livro.objects.filter(
        emprestimo__isnull=False
    ).values('genero').annotate(
        total=Count('emprestimo')
    ).order_by('-total')

    top_generos = list(generos_emprestimos[:5])
    total_outros = sum(g['total'] for g in generos_emprestimos[5:])

    generos_data = {
        'labels': [g['genero'] for g in top_generos] + (['Outros'] if total_outros else []),
        'data': [g['total'] for g in top_generos] + ([total_outros] if total_outros else [])
    }

    turmas_emprestimos = Aluno.objects.filter(
        emprestimos__isnull=False,
        matriculado=True
    ).values('turma').annotate(
        total=Count('emprestimos')
    ).order_by('-total')

    top_turmas = list(turmas_emprestimos[:7])
    total_outros_turmas = sum(t['total'] for t in turmas_emprestimos[7:])

    turmas_data = {
        'labels': [t['turma'] for t in top_turmas] + (['Outros'] if total_outros_turmas else []),
        'data': [t['total'] for t in top_turmas] + ([total_outros_turmas] if total_outros_turmas else [])
    }

    return render(request, 'galeria/index.html', {
        'total_livros': total_livros,
        'total_alunos': total_alunos,
        'total_emprestimos': total_emprestimos,
        'generos_data': generos_data,
        'turmas_data': turmas_data
    })

@csrf_protect
def questionario(request):
    
    generos_disponiveis = Livro.objects.values_list('genero', flat=True).distinct()
    
    if request.method == 'POST':
        palavras_chave = []
        
        # 1. Gênero principal
        genero = request.POST.get('genero', '').lower()
        if genero:
            palavras_chave.append(genero)
        
        # 2. Clima de leitura
        clima = request.POST.get('clima', '').lower()
        if clima == 'aventura':
            palavras_chave.extend(['ação', 'aventura', 'emoção', 'perigo', 'desafio'])
        elif clima == 'reflexivo':
            palavras_chave.extend(['reflexão', 'filosofia', 'profundidade', 'contemplação'])
        elif clima == 'emocional':
            palavras_chave.extend(['drama', 'emoção', 'sentimental', 'paixão'])
        elif clima == 'humor':
            palavras_chave.extend(['comédia', 'leveza', 'divertido', 'sátira'])
        elif clima == 'misterio':
            palavras_chave.extend(['mistério', 'suspense', 'investigação', 'crime'])
        
        # 3. Tipo de personagem
        personagem = request.POST.get('personagem', '').lower()
        if personagem == 'heroi':
            palavras_chave.extend(['herói', 'coragem', 'protagonista', 'nobreza'])
        elif personagem == 'antiheroi':
            palavras_chave.extend(['complexo', 'moral ambígua', 'imperfeito', 'cinza'])
        elif personagem == 'vilao':
            palavras_chave.extend(['vilão', 'malvado', 'manipulador', 'poder'])
        elif personagem == 'intelectual':
            palavras_chave.extend(['cientista', 'intelectual', 'sábio', 'conhecimento'])
        elif personagem == 'comum':
            palavras_chave.extend(['cotidiano', 'realista', 'pessoa comum', 'identificação'])
        
        # 4. Ambiente preferido
        ambiente = request.POST.get('ambiente', '').lower()
        if ambiente == 'futurista':
            palavras_chave.extend(['futuro', 'tecnologia', 'ciência', 'avançado'])
        elif ambiente == 'historico':
            palavras_chave.extend(['histórico', 'época', 'passado', 'tradição'])
        elif ambiente == 'cotidiano':
            palavras_chave.extend(['atual', 'realidade', 'cidade', 'moderno'])
        elif ambiente == 'fantasia':
            palavras_chave.extend(['fantasia', 'magia', 'reino', 'medieval'])
        elif ambiente == 'espaco':
            palavras_chave.extend(['espaço', 'universo', 'nave', 'alienígena'])
        
        # Busca os livros correspondentes
        livros_com_pontos = []
        for livro in Livro.objects.filter(aparecer=True):
            pontos = 0
            campos = [
                livro.nome_livro.lower(),
                livro.resumo.lower(),
                livro.genero.lower(),
                livro.tags.lower() if livro.tags else ''
            ]
            
            # Verifica cada palavra-chave em cada campo
            for palavra in palavras_chave:
                for campo in campos:
                    if palavra in campo:
                        pontos += 1
                        break  
            
            if pontos > 0:
                livro.pontos = pontos
                livros_com_pontos.append(livro)
        
        # Ordena por relevância e seleciona até 5
        livros_com_pontos.sort(key=lambda x: x.pontos, reverse=True)
        livros_recomendados = livros_com_pontos[:5]
        
        # Fallback aleatório se nenhum livro for encontrado
        if not livros_recomendados:
            livros_disponiveis = list(Livro.objects.filter(aparecer=True))
            if len(livros_disponiveis) >= 2:
                livros_recomendados = random.sample(livros_disponiveis, 2)
            else:
                livros_recomendados = livros_disponiveis
        
        # Calcula porcentagem de relevância para a barra de progresso
        max_pontos = livros_recomendados[0].pontos if livros_recomendados and hasattr(livros_recomendados[0], 'pontos') else 1
        for livro in livros_recomendados:
            livro.porcentagem_relevancia = (livro.pontos / max_pontos) * 100 if hasattr(livro, 'pontos') else 0
        
        return render(request, 'galeria/resultados.html', {
            'livros': livros_recomendados,
            'palavras_chave': palavras_chave,
            'fallback': len(livros_com_pontos) == 0,
            'generos_disponiveis': generos_disponiveis
        })
    
    # GET request - mostrar formulário
    return render(request, 'galeria/questionario.html', {
        'generos_disponiveis': generos_disponiveis
    })

def get_livro_details(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    
    data = {
        'nome_livro': livro.nome_livro,
        'autor': livro.autor,
        'genero': livro.genero,
        'quantidade': livro.quantidade,
        'resumo': livro.resumo,
        'capa_url': livro.capa.url if livro.capa else None
    }
    
    return JsonResponse(data)