import csv
from django.core.management.base import BaseCommand
from projects.models import Projeto, Product  # Substitua 'seu_app' pelo nome do seu app

class Command(BaseCommand):
    help = 'Popula o banco de dados com projetos a partir de um arquivo CSV'

    def handle(self, *args, **kwargs):
        with open('projects/management/commands/projetos.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                produto = Product.objects.get(id=row['produto_id'])  # Certifique-se de que o produto existe
                Projeto.objects.create(
                    titulo=row['titulo'],
                    descricao=row['descricao'],
                    produto=produto
                )
        self.stdout.write(self.style.SUCCESS('Projetos populados com sucesso!'))