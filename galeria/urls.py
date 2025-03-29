from django.urls import path
from galeria.views import index, imagem1, imagem2, imagem3, imagem4

urlpatterns = [
    path('',index),
    path('index/',index, name = 'index'),
    path('biblioteca/', imagem1, name = 'biblioteca'),
    path('alunos/', imagem2, name = 'alunos'),
    path('emprestar/', imagem3, name = 'emprestar'),
    path('livro-tombo/', imagem4, name = 'livro-tombo'),
]