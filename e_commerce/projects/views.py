from django.contrib import messages
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from formtools.wizard.views import SessionWizardView
from products.models import Product
from .forms import ProjetoInteresseForm, TipoSolucaoForm
from django.http import HttpResponseRedirect
from .models import Projeto,TipoSolucao,ProjetoInteresse
import json
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


#-------------- component Dropdrow projects


# View para carregar a página
def index(request, projeto_id):

    try:
        # Valida se o projeto existe
        projeto = get_object_or_404(Projeto, id=projeto_id)
        
        # Filtra os tipos de solução associados ao projeto
        opcoes = TipoSolucao.objects.filter(projetointeresse__projeto_id=projeto_id).distinct().order_by('nome')
        # Verifica se há opções disponíveis
        if not opcoes:

            projects = Projeto.objects.filter(produto_id=projeto_id)  
            print(projects)
            return render(request, 'components/mostrar_projetos.html', {'projects': projects})
            
            if not projects:
                return render(request, 'respostas/sem_opcoes_projeto_sem_solucoes.html', {'projects': projects})
        
        # Passa os valores para o template principal
        #return render(request, 'components/dropdrow.html', {'opcoes': opcoes})
        return render(request, 'components/mostrar_projetos.html', {'opcoes': opcoes})

    except Exception as e:
        # Log do erro (opcional)
        produto = get_object_or_404(Product, pk=projeto_id)
        print(f"Erro: {e}")
        # Renderiza uma página de erro personalizada
        return render(request, 'respostas/sem_opcoes_produto_sem_projeto.html', {
            'produto': produto,
            }, status=404)





# View para buscar os resultados no banco de dados
@csrf_exempt
def buscar_resultados(request):
    if request.method == "POST":
        data = json.loads(request.body)
        escolhas = data.get("escolhas", [])
        
        resultados = ProjetoInteresse.objects.filter(nome__in=escolhas)
        
        return JsonResponse({"resultados": [op.nome for op in resultados]})
    
    return JsonResponse({"error": "Método inválido"}, status=400)

# View para adicionar opções dinamicamente
@csrf_exempt
def adicionar_opcao(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nome = data.get("nome")
        if nome:
            opcao, created = ProjetoInteresse.objects.get_or_create(nome=nome)
            return JsonResponse({"success": True, "opcao": opcao.nome})
    return JsonResponse({"error": "Nome inválido"}, status=400)

# View para remover uma escolha
@csrf_exempt
def remover_opcao(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nome = data.get("nome")
        try:
            opcao = ProjetoInteresse.objects.get(nome=nome)
            opcao.delete()
            return JsonResponse({"success": True})
        except Opcao.DoesNotExist:
            return JsonResponse({"error": "Opção não encontrada"}, status=404)