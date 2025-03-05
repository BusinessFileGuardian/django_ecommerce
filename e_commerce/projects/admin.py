from django.contrib import admin
from .models import Projeto, ProjetoDetalhes,SetorAtuacao, TipoSolucao, ProjetoInteresse
# Register your models here.
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

# Administração personalizada para o SetorAtuacao
class SetorAtuacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')  # Exibe as colunas na lista
    search_fields = ('nome',)  # Permite buscar por nome
    list_filter = ('nome',)  # Adiciona filtros por nome

# Administração personalizada para o TipoSolucao
class TipoSolucaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')  # Exibe as colunas na lista
    search_fields = ('nome',)  # Permite buscar por nome
    list_filter = ('nome',)  # Adiciona filtros por nome

# Administração personalizada para o ProjetoInteresse
class ProjetoInteresseAdmin(admin.ModelAdmin):
    list_display = (
        'nome_cliente', 'projeto', 'orcamento', 'email', 'telefone', 'criado_em'
    )
    search_fields = ('nome_cliente', 'email', 'telefone')  # Permite buscar por esses campos
    list_filter = ('projeto', 'criado_em', 'orcamento')  # Filtros para o projeto e data de criação
    filter_horizontal = ('setores_atuacao', 'tipo_solucao')  # Filtro horizontal para os ManyToMany

    # Configura as ações personalizadas, se necessário
    actions = ['marcar_como_concluido']

    def marcar_como_concluido(self, request, queryset):
        # Função de exemplo para marcar projetos como concluídos
        queryset.update(status='concluido')
        self.message_user(request, "Projetos selecionados marcados como concluídos.")
    marcar_como_concluido.short_description = "Marcar como concluído"

# Registro dos modelos no admin
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(ProjetoDetalhes, ProjetoDetalhesAdmin)
admin.site.register(SetorAtuacao, SetorAtuacaoAdmin)
admin.site.register(TipoSolucao, TipoSolucaoAdmin)
admin.site.register(ProjetoInteresse, ProjetoInteresseAdmin)
