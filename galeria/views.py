from django.shortcuts import render
from .models import Livro, Aluno, Emprestimo
from django.core.paginator import Paginator

def index(request):
    return render(request, 'galeria/index.html')

def biblioteca(request):
    letra = request.GET.get('letra', '').upper()
    busca = request.GET.get('busca', '')
    
    livros = Livro.objects.filter(aparecer=True)
    
    # Filtro alfabético (só aplica se uma letra foi especificada)
    if letra:
        if letra.isalpha():
            livros = livros.filter(nome_livro__istartswith=letra)
        elif letra == '#':
            livros = livros.exclude(nome_livro__iregex=r'^[a-z]')
    
    # Filtro por busca
    if busca:
        livros = livros.filter(nome_livro__icontains=busca)
    
    paginator = Paginator(livros, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'galeria/biblioteca.html', {
        'page_obj': page_obj,
        'letra_atual': letra if letra else None,  # Alterado para None quando não há filtro
        'busca_atual': busca
    })

def alunos(request):
    alunos = Aluno.objects.filter(matriculado=True)  # Filtra apenas alunos matriculados
    return render(request, 'galeria/alunos.html', {'alunos': alunos})

def emprestar(request):
    # Adicione lógica para empréstimos se necessário
    return render(request, 'galeria/emprestar.html')

def livro_tombo(request):
    # Adicione lógica para livros tombados se necessário
    return render(request, 'galeria/livro-tombo.html')

# Alterei as funções imagem1, imagem2, imagem3, imagem4 pois foram substituídas

