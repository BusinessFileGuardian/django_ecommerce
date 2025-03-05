from django.contrib import admin
from django.utils.html import format_html  # Import necessário para o método format_html
from .models import Product, ProductImage

# Inline para gerenciar imagens com preview
class ProductImageInline(admin.TabularInline):  # ou admin.StackedInline se preferir
    model = ProductImage
    extra = 1  # Número de campos vazios extras para adicionar
    readonly_fields = ['image_preview']  # Adicionando campo de visualização da imagem

    def image_preview(self, obj):
        """Gera o HTML para exibir o preview da imagem."""
        if obj.image:
            return format_html('<img src="{}" style="width: 150px; height: auto;" />', obj.image.url)
        return "Nenhuma imagem disponível"

    image_preview.short_description = "Preview"  # Nome da coluna no admin

# Configuração do modelo Product no admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['title', 'price', 'stock', 'active']  # Colunas exibidas na listagem
    list_filter = ['active', 'featured']  # Filtros no painel lateral
    search_fields = ['title', 'description']  # Campos para pesquisa
    prepopulated_fields = {"slug": ("title",)}  # Preenchimento automático do campo slug
    ordering = ['-timestamp']  # Ordenação padrão (mais recente primeiro)


# Configuração do admin para o modelo Projeto
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'produto')  # Campos exibidos na lista de projetos
    list_filter = ('produto',)  # Filtros laterais
    search_fields = ('titulo', 'descricao')  # Campos de busca
    raw_id_fields = ('produto',)  # Campo de relacionamento como input de ID (útil para muitos registros)

# Configuração do admin para o modelo ProjetoDetalhes
class ProjetoDetalhesAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'reunioes_previstas', 'interesse_investidor', 'outros_passos')  # Campos exibidos na lista de detalhes
    search_fields = ('projeto__titulo',)  # Busca pelo título do projeto relacionado

