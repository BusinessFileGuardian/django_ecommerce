from django.urls import path
from .views import ProductListView, ProductDetailView,product_redirect_view
from .forms import ProjetoPasso1Form, ProjetoPasso2Form, ProjetoPasso3Form
app_name = "products"

urlpatterns = [
    path('id/<int:pk>/', product_redirect_view, name='product_redirect'),
    path('', ProductListView.as_view(), name='list'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='category'),
    # 🚨 Mantenha essa rota por último para evitar conflitos
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
]