from django.shortcuts import render

def index(request):
    return render(request, 'galeria/index.html')

def imagem1(request):
    return render(request, 'galeria/biblioteca.html')

def imagem2(request):
    return render(request, 'galeria/alunos.html')

def imagem3(request):
    return render(request, 'galeria/emprestar.html')

def imagem4(request):
    return render(request, 'galeria/livro-tombo.html')

