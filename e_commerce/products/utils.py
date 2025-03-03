from .models import Product, Projeto

def verificar_projeto_para_produto(product_id):
    """
    Verifica se um produto tem um projeto relacionado e retorna a informação.
    :param product_id: ID do produto a ser verificado.
    :return: True se o produto tiver um projeto relacionado, caso contrário, False.
    """
    try:
        produto = Product.objects.get(id=product_id)  # Obtém o produto pelo ID
        # Verifica se existe um projeto associado a esse produto
        if produto.projetos.exists():  
            return True
        return False
    except Product.DoesNotExist:
        # Retorna False caso o produto não seja encontrado
        return False
