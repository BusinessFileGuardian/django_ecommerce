import csv
from django.core.management.base import BaseCommand
from projects.models import SetorAtuacao  # Substitua "seu_app" pelo nome do seu app

class Command(BaseCommand):
    help = 'Popula o modelo SetorAtuacao com dados de um arquivo CSV'

    def handle(self, *args, **kwargs):
        with open('projects/management/commands/setores_atuacao.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                SetorAtuacao.objects.create(
                    nome=row['nome'],
                    descricao=row['descricao']
                )
        self.stdout.write(self.style.SUCCESS('Dados populados com sucesso!'))