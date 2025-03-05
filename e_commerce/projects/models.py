from django.db import models
from products.models import Product  # Importando Category
import markdown
# Create your models here.
class Projeto(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    produto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='projetos')  # Referência ao modelo Product
    
    def descricao_formatada(self):
        return markdown.markdown(self.descricao)
    
    def __str__(self):
        return f'{self.titulo} - {self.descricao[:50]}...'

# ProjetoDetalhes model
class ProjetoDetalhes(models.Model):
    projeto = models.OneToOneField(Projeto, on_delete=models.CASCADE, related_name='detalhes')
    reunioes_previstas = models.TextField(blank=True, null=True)
    interesse_investidor = models.TextField(blank=True, null=True)
    outros_passos = models.TextField(blank=True, null=True)

    def reunioes_previstas_formatada(self):
        return markdown.markdown(self.reunioes_previstas)
    
    def interesse_investidor_formatada(self):
        return markdown.markdown(self.interesse_investidor)
    
    def outros_passos_formatada(self):
        return markdown.markdown(self.outros_passos)

    def __str__(self):
        return f"Detalhes do projeto {self.projeto.titulo} - {self.reunioes_previstas[:50]}...' - {self.interesse_investidor[:50]}...' - {self.outros_passos[:50]}...'"

#associar projeto
class SetorAtuacao(models.Model):
    nome = models.CharField("Nome do Setor", max_length=100, unique=True)
    descricao = models.TextField("Descrição do Setor", blank=True, null=True)

    def __str__(self):
        return self.nome


# Modelo para os tipos de solução desejada (ex: E-commerce, CRM, Site)
class TipoSolucao(models.Model):
    nome = models.CharField("Nome da Solução", max_length=100, unique=True)
    descricao = models.TextField("Descrição da Solução", blank=True, null=True)

    def __str__(self):
        return self.nome

# Modelo para associar o interesse do cliente no projeto
class ProjetoInteresse(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='interesses')
    nome_cliente = models.CharField("Nome do Cliente/Empresa", max_length=255)
    setores_atuacao = models.ManyToManyField(SetorAtuacao, verbose_name="Setores de Atuação")
    tipo_solucao = models.ManyToManyField(TipoSolucao, verbose_name="Tipo de Solução")
    desafios = models.TextField("Principais Desafios", blank=True)
    expectativas = models.TextField("Expectativas para o Projeto", blank=True)
    orcamento = models.CharField("Faixa de Orçamento", max_length=50, blank=True, null=True)
    email = models.EmailField("E-mail")
    telefone = models.CharField("WhatsApp/Telefone", max_length=20)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_cliente} - {self.projeto.titulo}"