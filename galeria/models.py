from django.db import models
from datetime import datetime, timedelta

class Livro(models.Model):
    nome_livro = models.CharField(max_length=100, null=False, blank=False)
    resumo = models.CharField(max_length=400)
    genero = models.CharField(max_length=30, null=False, blank=False)
    autor = models.CharField(max_length=100, null=False, blank=False)
    capa = models.ImageField(upload_to='capas/%Y/%m/%d/', blank=True)
    aparecer = models.BooleanField(default=False)
    quantidade = models.IntegerField(default=1, null=False)

    def __str__(self):
        return f"{self.nome_livro} - {self.autor}"


class Aluno(models.Model):
    ra_aluno = models.CharField(max_length=20, null=False, blank=False)
    nome_aluno = models.CharField(max_length=100, null=False, blank=False)
    matriculado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome_aluno} ({self.ra_aluno})"


class Emprestimo(models.Model):
    id_livro = models.ForeignKey(Livro, on_delete=models.CASCADE, null=True, blank=True)
    ra_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=True, blank=True)
    STATUS_CHOICES = [
        ('Em andamento', 'Em andamento'),
        ('Concluído', 'Concluído'),
        ('Atrasado', 'Atrasado'),
    ]
    status_emprestimo = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Em andamento')
    data_retirada = models.DateTimeField(default=datetime.now)
    data_devolucao = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.data_devolucao:
            self.data_devolucao = self.data_retirada + timedelta(days=14)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_livro} - {self.ra_aluno} - {self.status_emprestimo}"
    
    def empy(self, *args, **kwargs):
        if self.data_devolucao < datetime.now():
            self.status_emprestimo = 'Atrasado'
            self.save(*args, **kwargs)

