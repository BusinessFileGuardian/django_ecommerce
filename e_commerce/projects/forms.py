from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from .models import SetorAtuacao, TipoSolucao, ProjetoInteresse
from formtools.wizard.views import SessionWizardView

# Formulário para o modelo TipoSolucao
class TipoSolucaoForm(ModelForm):
    class Meta:
        model = TipoSolucao
        fields = ['nome', 'descricao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar'))

# Formulário para o modelo ProjetoInteresse
class ProjetoInteresseForm(ModelForm):
    class Meta:
        model = ProjetoInteresse
        fields = [
            'nome_cliente', 'setores_atuacao', 'tipo_solucao', 'desafios',
            'expectativas', 'orcamento', 'email', 'telefone'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Informações Básicas',
                'nome_cliente',
                'setores_atuacao',  # Campo Many-to-Many
                'tipo_solucao',  # Campo Many-to-Many
            ),
            Fieldset(
                'Detalhes do Projeto',
                'desafios',
                'expectativas',
                'orcamento',
            ),
            Fieldset(
                'Contato',
                'email',
                'telefone',
            ),
            ButtonHolder(
                Submit('submit', 'Enviar', css_class='btn btn-primary')
            )
        )

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if not telefone.isdigit():
            raise ValidationError("O telefone deve conter apenas números.")
        return telefone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise ValidationError("O e-mail deve terminar com '.com'.")
        return email

# Wizard para o formulário de ProjetoInteresse (usando formtools)
class ProjetoInteresseWizard(SessionWizardView):
    form_list = [ProjetoInteresseForm, TipoSolucaoForm]
    template_name = 'projetos/wizard_form.html'

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

        return super().done(form_list, **kwargs)
