from django.urls import path
from .views import ProductListView, ProductDetailView,associar_projeto,CriarProjetoWizard,confirmar_associacao,product_redirect_view
from .forms import ProjetoPasso1Form, ProjetoPasso2Form, ProjetoPasso3Form
app_name = "products"

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='category'),
    
    # 🚀 Define "criar-projeto/" ANTES da URL dinâmica "<slug:slug>/"
    path('criar-projeto/', CriarProjetoWizard.as_view([ProjetoPasso1Form, ProjetoPasso2Form, ProjetoPasso3Form]), name="criar_projeto"),
    
    path('associar/<int:projeto_id>/', associar_projeto, name='associar_projeto'),  
    path('confirmar-associacao/<int:projeto_id>/', confirmar_associacao, name='confirmar_associacao'),
    path('id/<int:pk>/', product_redirect_view, name='product_redirect'),
    
    # 🚨 Mantenha essa rota por último para evitar conflitos
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
]