from django.contrib import admin
from galeria.models import Livro, Aluno, Emprestimo

class ListandoLivros(admin.ModelAdmin):
    list_display = ('id','nome_livro', 'genero','aparecer')
    list_display_links = ('id','nome_livro')
    search_fields = ('nome_livro',)
    list_filter = ('genero',)
    list_editable = ('aparecer',)
    list_per_page = 10

class ListandoAlunos(admin.ModelAdmin):
    list_display = ('id','nome_aluno','matriculado')
    list_display_links = ('id','nome_aluno')
    search_fields = ('nome_aluno',)
    list_filter = ('nome_aluno',)
    list_editable = ('matriculado',)
    list_per_page = 10

class ListandoEmprestimos(admin.ModelAdmin):
    list_display = ('id','id_livro','ra_aluno','status_emprestimo','data_retirada')
    list_display_links = ('id','status_emprestimo')
    search_fields = ('id_livro',)
    list_filter = ('status_emprestimo',)
    list_per_page = 10


admin.site.register(Livro, ListandoLivros)
admin.site.register(Aluno, ListandoAlunos)
admin.site.register(Emprestimo, ListandoEmprestimos)

# Register your models here.
