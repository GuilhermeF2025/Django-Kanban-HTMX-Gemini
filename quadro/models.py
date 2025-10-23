from django.db import models
from django.contrib.auth.models import User # Importar o modelo User

class Coluna(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Novo campo
    titulo = models.CharField(max_length=100)
    ordem = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.titulo

class Cartao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Novo campo
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    coluna = models.ForeignKey(Coluna, on_delete=models.CASCADE, related_name='cartoes')
    ordem = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.titulo