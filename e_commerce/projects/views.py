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
from .models import Projeto,TipoSolucao,ProjetoInteresse,SetorAtuacao
from django.db.models import Q
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

def filtrar_solucoes_e_setores(produto):
    projetos_do_produto = Projeto.objects.filter(produto=produto)
    interesses = ProjetoInteresse.objects.filter(projeto__in=projetos_do_produto)
    solucoes = TipoSolucao.objects.filter(projetointeresse__in=interesses).distinct()
    setores = SetorAtuacao.objects.filter(projetointeresse__in=interesses).distinct()
    return solucoes, setores


@csrf_exempt
@csrf_exempt
def filtrar_projetos(request):
    if request.method == "POST":
        try:
            # Recebe os dados do frontend
            data = json.loads(request.body)
            escolhas = data.get("escolhas", [])
            produto_id = data.get("produto_id")

            # Filtra os projetos associados ao produto
            projetos_filtrados = Projeto.objects.filter(produto=produto_id)

            # Filtros dinâmicos
            filtros_gerais = Q()  # Criamos um filtro único para usar AND

            for escolha in escolhas:
                nome = escolha.get("nome")
                tipo = escolha.get("tipo")

                if tipo == "solucao":
                    filtros_gerais &= Q(interesses__tipo_solucao__nome=nome)  # Adiciona com AND lógico

                elif tipo == "setor":
                    filtros_gerais &= Q(interesses__setores_atuacao__nome=nome)  # Adiciona com AND lógico

            # Aplica os filtros combinados
            if filtros_gerais:
                projetos_filtrados = projetos_filtrados.filter(filtros_gerais)

            # Remove duplicatas
            projetos_filtrados = projetos_filtrados.distinct()

            # Prepara os resultados para o frontend
            resultados = [{"nome": projeto.titulo} for projeto in projetos_filtrados]

            # Se um único projeto é encontrado com todas as características, não será necessário mostrar misturas
            if len(projetos_filtrados) == 1:
                return JsonResponse({"projetos": resultados})
            
            # Caso contrário, você pode mostrar mais projetos ou manipular de outra forma.
            return JsonResponse({"projetos": resultados})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método não permitido"}, status=405)



# View para carregar a página
def index(request, produto_id):
    produto_id=produto_id
    produto = get_object_or_404(Product, id=produto_id)
    print(produto_id)
    solucoes, setores  = filtrar_solucoes_e_setores(produto)
    
    return render(request, 'components/dropdrow.html', {
        'solucoes': solucoes,
        'setores': setores,
        'produto_id': produto_id
    })

def mostrar_projetos_produto(request, produto_id):
    try:
        produto = get_object_or_404(Product, id=produto_id)
        solucoes, setores = filtrar_solucoes_e_setores(produto)
        
        # Filtra os projetos associados ao produto
        projects = Projeto.objects.filter(produto=produto)
        
        return render(request, 'components/mostrar_projetos.html', {
            'projects': projects,
            'solucoes': solucoes,
            'setores': setores,
            'produto_id': produto_id
        })
        
    except Exception as e:
        print(f"Erro: {e}")
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