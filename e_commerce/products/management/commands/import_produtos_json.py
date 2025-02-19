import csv
from django.core.management.base import BaseCommand
from products.models import Product
from categories.models import Category  # Importando o modelo Category
from django.utils.text import slugify  # Para gerar slugs automaticamente

class Command(BaseCommand):
    help = 'Popula o banco de dados com produtos a partir de um arquivo CSV'

    def handle(self, *args, **kwargs):
        with open('products/management/commands/produtos.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Cria ou obtém a categoria
                category, created = Category.objects.get_or_create(
                    name=row['category'],
                    defaults={
                        'slug': slugify(row['category']),  # Gera um slug automaticamente
                        'description': f"Descrição padrão para {row['category']}",  # Descrição padrão
                        'active': True,  # Define a categoria como ativa
                    }
                )

                # Cria o produto
                Product.objects.create(
                    title=row['title'],
                    description=row['description'],
                    price=row['price'],
                    discount_price=row['discount_price'] if row['discount_price'] else None,
                    stock=int(row['stock']),
                    sku=row['sku'],
                    category=category,  # Associa a categoria ao produto
                    featured=row['featured'].lower() == 'true',
                )
        self.stdout.write(self.style.SUCCESS('Produtos populados com sucesso!'))