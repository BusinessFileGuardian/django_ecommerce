from django.contrib import messages
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404,redirect
from formtools.wizard.views import SessionWizardView
from .models import Projeto,TipoSolucao,ProjetoInteresse
from products.models import Product
from .forms import ProjetoInteresseForm, TipoSolucaoForm
from django.http import HttpResponseRedirect
# Create your views here.
# A view para o ProjetoInteresseWizard
class ProjetoInteresseWizardView(SessionWizardView):
    FORMS = [
        ("tipoSolucao", TipoSolucaoForm),
        ("projetointeresse", ProjetoInteresseForm),  # Corrigido de ProjetoInteresse para ProjetoInteresseForm
    ]
    form_list = FORMS
    form_list = FORMS
    template_name = 'associar/wizard_form.html'  # O caminho para o seu template

    def done(self, form_list, **kwargs):
        # Processa os dados dos formulários
        projeto_interesse_data = form_list[0].cleaned_data
        tipo_solucao_data = form_list[1].cleaned_data

        # Cria ou atualiza o TipoSolucao
        tipo_solucao, created = TipoSolucao.objects.get_or_create(
            nome=tipo_solucao_data['nome'],
            defaults={'descricao': tipo_solucao_data['descricao']}
        )

        # Cria o ProjetoInteresse
        projeto_interesse = ProjetoInteresse.objects.create(
            nome_cliente=projeto_interesse_data['nome_cliente'],
            desafios=projeto_interesse_data['desafios'],
            expectativas=projeto_interesse_data['expectativas'],
            orcamento=projeto_interesse_data['orcamento'],
            email=projeto_interesse_data['email'],
            telefone=projeto_interesse_data['telefone']
        )

        # Associar os Setores de Atuação e Tipo de Solução ao ProjetoInteresse
        projeto_interesse.setores_atuacao.set(projeto_interesse_data['setores_atuacao'])
        projeto_interesse.tipo_solucao.set(projeto_interesse_data['tipo_solucao'])

        # Redireciona para uma página de sucesso ou onde você desejar
        return HttpResponseRedirect('/projeto/sucesso/')


def criar_projeto(request):
    return render(request, 'criar/criar_projeto.html')



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

    return render(request, 'associar/associar_projeto.html', {
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
