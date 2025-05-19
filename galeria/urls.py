from django.urls import path
from galeria.views import index, biblioteca, alunos, emprestar, livros, questionario, get_livro_details

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('biblioteca/', biblioteca, name='biblioteca'),
    path('alunos/', alunos, name='alunos'),
    path('emprestar/', emprestar, name='emprestar'),
    path('livro-tombo/', livros, name='livro-tombo'),
    path('questionario/', questionario, name='questionario'),
    path('get-livro-details/<int:livro_id>/', get_livro_details, name='get_livro_details'),
]