from .models import Pedido, ItemPedido, Cliente

def carrinho(request):
    quantidadeProdutosCarrinho = 0
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get('idSessao'):
            idSessao = request.COOKIES.get('idSessao')
            cliente, criado = Cliente.objects.get_or_create(idSessao = idSessao)
        else:
            return {"quantidadeProdutosCarrinho": quantidadeProdutosCarrinho}  
    pedido,criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itemPedido = ItemPedido.objects.filter(pedido=pedido)
    for item in itemPedido:
        quantidadeProdutosCarrinho += item.quantidade
    return {"quantidadeProdutosCarrinho": quantidadeProdutosCarrinho}