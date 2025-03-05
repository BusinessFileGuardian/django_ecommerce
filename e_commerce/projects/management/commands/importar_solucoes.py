import csv
from django.core.management.base import BaseCommand
from projects.models import TipoSolucao  # Substitua "seu_app" pelo nome do seu app

class Command(BaseCommand):
    help = 'Importa soluções a partir de um arquivo CSV'

    def handle(self, *args, **kwargs):

        with open('projects/management/commands/tipo_solucao.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                TipoSolucao.objects.create(
                    nome=row['nome'],
                    descricao=row['descricao']
                )
        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))