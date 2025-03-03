from django.http import Http404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from analytics.models import ObjectViewed
from analytics.mixin import ObjectViewedMixin
from carts.models import Cart
from .models import Product
from .models import Projeto


def product_redirect_view(request, pk):
    """
    Recupera o produto pelo id (pk) e redireciona para a URL com o slug.
    Exemplo: /products/id/1/ → /products/sistema-de-e-commerce-completo/
    """
    product = get_object_or_404(Product, pk=pk)
    
    # Se o slug for numérico, gera um novo slug a partir do título
    if product.slug.isdigit():
        novo_slug = slugify(product.title)
        product.slug = novo_slug
        product.save(update_fields=['slug'])
    
    return redirect('products:detail', slug=product.slug)

def associar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    detalhes = projeto.detalhes if hasattr(projeto, 'detalhes') else None

    return render(request, 'products/associar_projeto.html', {
        'projeto': projeto,
        'detalhes': detalhes
    })

def confirmar_associacao(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if request.user.is_authenticated:
        # Aqui você pode adicionar a lógica para associar o usuário ao projeto
        projeto.usuarios.add(request.user)  # Exemplo, caso haja uma relação ManyToMany

        messages.success(request, "Você foi associado ao projeto com sucesso!")
        return redirect('products:detail', projeto.produto.id)
    else:
        messages.error(request, "Você precisa estar logado para se associar a um projeto.")
        return redirect('account_login')  # Ajuste para a URL correta do login

def criar_projeto(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    detalhes = projeto.detalhes if hasattr(projeto, 'detalhes') else None

    return render(request, 'products/associar_projeto.html', {
        'projeto': projeto,
        'detalhes': detalhes
    })


class ProductFeaturedListView(ListView):
    """Listagem de produtos destacados."""
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        return Product.objects.featured()


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    """Detalhes de um produto destacado."""
    queryset = Product.objects.featured()
    template_name = "products/featured-detail.html"


class ProductListView(ListView):
    """Listagem de produtos disponíveis."""
    queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


def product_list_view(request):
    """Listagem de produtos usando Function-Based View."""
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    """Detalhes de um produto utilizando slug como identificador."""
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['tem_projeto'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Produto não encontrado!")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()

        # Cria o evento ObjectViewed se o usuário estiver autenticado
        if self.request.user.is_authenticated:
            ObjectViewed.objects.create(
                user=self.request.user,
                content_object=instance
            )
        return instance

# compartilhando se a ou nao projeto associado ao produto
class ProductDetailView(ObjectViewedMixin, DetailView):
    """Detalhes de um produto utilizando o slug como identificador."""
    template_name = "products/detail.html"
    model = Product  # Define o modelo diretamente

    def get_context_data(self, *args, **kwargs):

        
        instance = self.get_object()

        try:
            # Verifica se existe um projeto relacionado a este produto
            Projeto.objects.get(produto=instance)
            tem_projeto = True
        except Projeto.DoesNotExist:
            tem_projeto = False
    
        context = super().get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['tem_projeto'] = tem_projeto 
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')  # Busca pelo slug na URL
        instance = Product.objects.filter(slug=slug).first()
        if instance is None:
            raise Http404("Esse produto não existe!")
        return instance

def product_detail_view(request, pk=None, *args, **kwargs):
    """Detalhes de um produto utilizando Function-Based View."""
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Esse produto não existe!")


    # Adiciona o resultado no contexto
    context = {
        'object': instance,

    }
    return render(request, "products/detail.html", context)



