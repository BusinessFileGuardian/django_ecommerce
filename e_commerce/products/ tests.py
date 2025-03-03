from django.test import TestCase
from django.urls import reverse
from .models import Product, Projeto

class ProductDetailViewTest(TestCase):
    
    def setUp(self):
        """Criar os dados necessários para o teste"""
        # Cria um produto
        self.product = Product.objects.create(
            title="Produto Teste",
            description="Descrição do Produto Teste",
            price=100.00,
            stock=10,
            active=True
        )
        
        # Cria um projeto associado a esse produto
        self.projeto = Projeto.objects.create(
            titulo="Projeto Teste",
            descricao="Descrição do Projeto Teste",
            produto=self.product
        )

    def test_product_detail_view_com_projeto(self):
        """Testa se a view do produto exibe a mensagem de projeto quando há projeto associado"""
        response = self.client.get(reverse('products:detail', kwargs={'pk': self.product.pk}))
        
        # Verifica se o status de resposta é 200
        self.assertEqual(response.status_code, 200)
        
        # Verifica se a mensagem de projeto foi exibida no template
        self.assertContains(response, "Este produto está associado a um projeto!")

    def test_product_detail_view_sem_projeto(self):
        """Testa se a view do produto exibe a mensagem de 'sem projeto' quando não há projeto associado"""
        
        # Remove o projeto do produto
        self.product.projetos.clear()

        response = self.client.get(reverse('products:detail', kwargs={'pk': self.product.pk}))
        
        # Verifica se o status de resposta é 200
        self.assertEqual(response.status_code, 200)
        
        # Verifica se a mensagem de 'sem projeto' foi exibida no template
        self.assertContains(response, "Este produto não está associado a nenhum projeto.")
