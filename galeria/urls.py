from django.urls import path
from galeria.views import index, imagem

urlpatterns = [
    path('',index),
    path('index.html/',index),
    path('/biblioteca.html/', imagem),
    path('/alunos.html/', imagem),
    path('/emprestar.html/', imagem),
    path('/livro-tombo.html/', imagem),
]