from django import forms

class ProjetoPasso1Form(forms.Form):
    nome = forms.CharField(label="Seu Nome", max_length=100, required=True)
    email = forms.EmailField(label="E-mail", required=True)
    telefone = forms.CharField(label="Telefone", required=False)
    ja_enviei_profissionais = forms.ChoiceField(
        label="Já enviou este projeto para outros profissionais?",
        choices=[("sim", "Sim"), ("nao", "Não")],
        widget=forms.RadioSelect,
        required=True
    )

class ProjetoPasso2Form(forms.Form):
    tempo_pretendido = forms.IntegerField(label="Tempo pretendido para o projeto (em meses)", required=True)
    reunioes_disponivel = forms.BooleanField(label="Está disponível para reuniões?", required=False)
    tempo_resposta = forms.IntegerField(label="Tempo máximo de resposta sobre aceitação (em dias)", required=True)
    prazo_flexivel = forms.ChoiceField(
        label="Está disposto a combinar prazos?",
        choices=[("sim", "Sim"), ("nao", "Não")],
        widget=forms.RadioSelect,
        required=True
    )

class ProjetoPasso3Form(forms.Form):
    aceita_termos = forms.BooleanField(
        label="Li e concordo com a ética de projetos e valores da Alcateia.cloud",
        required=True
    )
