from django.urls import path
from .views import ProductListView, ProductDetailView,associar_projeto,criar_projeto,confirmar_associacao,product_redirect_view

app_name = "products"

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='category'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
    path('associar/<int:projeto_id>/', associar_projeto, name='associar_projeto'),  
    path('confirmar-associacao/<int:projeto_id>/', confirmar_associacao, name='confirmar_associacao'),
    path('id/<int:pk>/', product_redirect_view, name='product_redirect'),
    path('criar-projeto/', criar_projeto, name='criar_projeto'),
]