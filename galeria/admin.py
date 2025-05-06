from django.contrib import admin
from django.db import connection
from galeria.models import Livro, Aluno, Emprestimo

def reset_sequence(model):
    if not hasattr(model._meta, 'db_table'):
        return
        
    table_name = model._meta.db_table
    
    with connection.cursor() as cursor:
        if connection.vendor == 'sqlite':
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{table_name}';")
            cursor.execute(f"SELECT MAX(id) FROM {table_name};")
            max_id = cursor.fetchone()[0]
            if max_id is not None:
                cursor.execute(f"INSERT INTO sqlite_sequence (name, seq) VALUES ('{table_name}', {max_id});")
            else:
                cursor.execute(f"INSERT INTO sqlite_sequence (name, seq) VALUES ('{table_name}', 0);")

class ResetSequenceMixin:
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        reset_sequence(obj.__class__)
    
    def delete_queryset(self, request, queryset):
        model = queryset.model
        super().delete_queryset(request, queryset)
        reset_sequence(model)

class ListandoLivros(ResetSequenceMixin, admin.ModelAdmin):
    list_display = ('id', 'nome_livro', 'genero', 'aparecer')
    list_display_links = ('id', 'nome_livro')
    search_fields = ('nome_livro',)
    list_filter = ('genero',)
    list_editable = ('aparecer',)
    list_per_page = 10

class ListandoAlunos(ResetSequenceMixin, admin.ModelAdmin):
    list_display = ('id', 'nome_aluno', 'turma', 'matriculado')
    list_display_links = ('id', 'nome_aluno')
    search_fields = ('nome_aluno',)
    list_filter = ('nome_aluno',)
    list_editable = ('matriculado',)
    list_per_page = 10

class ListandoEmprestimos(ResetSequenceMixin, admin.ModelAdmin):
    list_display = ('id', 'id_livro', 'ra_aluno', 'status_emprestimo', 'data_retirada')
    list_display_links = ('id', 'id_livro', 'status_emprestimo')
    search_fields = ('id_livro',)
    list_filter = ('status_emprestimo',)
    list_per_page = 10

admin.site.register(Livro, ListandoLivros)
admin.site.register(Aluno, ListandoAlunos)
admin.site.register(Emprestimo, ListandoEmprestimos)