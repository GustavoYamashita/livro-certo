from django.db import models
from datetime import datetime, timedelta
from pytz import timezone
import re

class Livro(models.Model):
    nome_livro = models.CharField(max_length=100, null=False, blank=False)
    resumo = models.CharField(max_length=400)
    genero = models.CharField(max_length=30, null=False, blank=False)
    autor = models.CharField(max_length=100, null=False, blank=False)
    capa = models.ImageField(upload_to='capas/%Y/%m/%d/', blank=True)
    aparecer = models.BooleanField(default=False)
    quantidade = models.IntegerField(default=1, null=False)
    tags = models.CharField(max_length=200, blank=True)  # Adicione este campo novo

    def get_tags(self):
        return [tag.strip().lower() for tag in self.tags.split(',')] if self.tags else []

    def __str__(self):
        return f"{self.nome_livro} - {self.autor}"


class Aluno(models.Model):
    ra_aluno = models.CharField(max_length=20, null=False, blank=False, unique=True, db_index=True)
    nome_aluno = models.CharField(max_length=100, null=False, blank=False)
    turma = models.CharField(max_length=10, null=True, blank=True)
    matriculado = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.turma:
            self.turma = self.formatar_turma(self.turma)

    @staticmethod
    def formatar_turma(turma):
        turma = turma.strip()
        
        match = re.match(r'^(\d+)\s*º?\s*([a-zA-Z]?)$', turma)
        
        if match:
            numero = match.group(1)
            letra = match.group(2).upper() if match.group(2) else ''
            return f"{numero}º {letra}".strip()
        return turma.upper()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_aluno} ({self.ra_aluno})"
class Emprestimo(models.Model):
    id_livro = models.ForeignKey(Livro, on_delete=models.CASCADE, null=True, blank=True)
    ra_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=True, blank=True, related_name='emprestimos')
    status_emprestimo = models.CharField(max_length=30,editable=False)
    data_retirada = models.DateTimeField(default=datetime.now)
    data_devolucao = models.DateTimeField(default=datetime.now, editable=False)
    devolvido = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_livro} - {self.ra_aluno} - {self.status_emprestimo}"

    def save(self, *args, **kwargs):
        variavel = []
        if not self.data_devolucao:
            self.data_devolucao = self.data_retirada + timedelta(days=14)
        if self.devolvido == True:
            variavel = 'Concluído'
        elif (datetime.now().replace(tzinfo=None) - (self.data_retirada.replace(tzinfo=None) + timedelta(days=14))) > timedelta(days=0):
           variavel = 'Atrasado'
        else: variavel = 'Em andamento'
        self.status_emprestimo = variavel
        super(Emprestimo, self).save(*args, **kwargs)