from .models import Pedido, ItemPedido

def carrinho(request):
    quantidadeProdutosCarrinho = 0
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        return {"quantidadeProdutosCarrinho": quantidadeProdutosCarrinho}
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itemPedido = ItemPedido.objects.filter(pedido=pedido)
    for item in itemPedido:
        quantidadeProdutosCarrinho += item.quantidade
    return {"quantidadeProdutosCarrinho": quantidadeProdutosCarrinho}