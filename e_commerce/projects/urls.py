from django.urls import path
from .views import associar_projeto,confirmar_associacao,product_redirect_view,criar_projeto
from .views import ProjetoInteresseWizardView
from .forms import TipoSolucaoForm, ProjetoInteresseForm
#modelos de componnets Dropdron refatora depois
from . import views

app_name = "projects"
 
urlpatterns = [

      path('wizard/', ProjetoInteresseWizardView.as_view(), name='projeto_interesse_wizard'),
      #path('projeto/sucesso/', TemplateView.as_view(template_name="projetos/sucesso.html"), name='projeto_sucesso'),  # Página de Sucesso
      path("reserva/", ProjetoInteresseWizardView.as_view([TipoSolucaoForm,ProjetoInteresseForm]), name="booking_step"),
      path('criar/', criar_projeto, name='criar_projeto'),
      path('associar/<int:projeto_id>/', associar_projeto, name='associar_projeto'),  
      path('confirmar-associacao/<int:projeto_id>/', confirmar_associacao, name='confirmar_associacao'),
      path('id/<int:pk>/', product_redirect_view, name='product_redirect'),
      #component Dropdrow projects
      path('dropdrow_componnts/<int:projeto_id>/', views.index, name='index'),
      path('buscar/', views.buscar_resultados, name='buscar_resultados'),
      path('adicionar/', views.adicionar_opcao, name='adicionar_opcao'),
      path('remover/', views.remover_opcao, name='remover_opcao'),
   ]