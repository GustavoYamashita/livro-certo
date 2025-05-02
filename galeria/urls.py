from django.urls import path
from galeria.views import index, biblioteca, alunos, emprestar, livro_tombo  # Renomeie as imports para nomes mais descritivos

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('biblioteca/', biblioteca, name='biblioteca'),  # Agora aponta para a view 'biblioteca'
    path('alunos/', alunos, name='alunos'),
    path('emprestar/', emprestar, name='emprestar'),
    path('livro-tombo/', livro_tombo, name='livro-tombo'),
]