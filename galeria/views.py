from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def imagem(request):
    return render(request, 'src/pages/biblioteca.html')

def imagem(request):
    return render(request, 'src/pages/alunos.html')

def imagem(request):
    return render(request, 'src/pages/emprestar.html')

def imagem(request):
    return render(request, 'src/pages/livro-tombo.html')

