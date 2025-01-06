from django.db.models import Max, Min
from django.db.models import Case, When
from django.core.mail import send_mail

def filtrarProdutos(produtos, filtro):
    if filtro:
        print(f"Filtro recebido: {filtro}")
        if "-" in filtro:
            categoria, tipo = filtro.split("-")
            print(f"Categoria: {categoria}, Tipo: {tipo}")
            produtos = produtos.filter(tipo__slug=tipo, categoria__slug=categoria)
            print(f"Produtos após filtro de categoria e tipo: {produtos}")
        else:
            produtos = produtos.filter(categoria__slug=filtro)
            print(f"Produtos após filtro de categoria: {produtos}")
    return produtos

def precoMaximoMinimo(produtos):
    minimo = 0
    maximo = 0
    if len(produtos) > 0:
        maximo = list(produtos.aggregate(Max("preco")).values())[0]
        maximo = round(maximo, 2)
        minimo = list(produtos.aggregate(Min("preco")).values())[0]
        minimo = round(minimo, 2)
    return minimo, maximo

def ordenarProdutos(produtos, ordem):
    if ordem == "menorPreco":
        produtos = produtos.order_by("preco")
    elif ordem == "maiorPreco":
        produtos = produtos.order_by("-preco")
    elif ordem == "maisVendidos":
        listaProdutos = [(produto.totalVendas(), produto.id) for produto in produtos]
        listaProdutos = sorted(listaProdutos, key=lambda x: x[0], reverse=True)
        ordenacao_ids = [produto_id for _, produto_id in listaProdutos]
        print(listaProdutos)
        print(ordenacao_ids)


        # Cria uma ordenação baseada nos IDs dos produtos mais vendidos
        preserva_ordem = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(ordenacao_ids)])
        produtos = produtos.filter(id__in=ordenacao_ids).order_by(preserva_ordem)
        
    return produtos


def enviarEmailCompra(pedido):
    email = pedido.cliente.email
    assunto = f"Pedido Aprovado: {pedido.id}"
    corpo = f""" Parabéns! Pedido aprovado"
    ID PEDIDO: {pedido.id}
    Valor Total: {pedido.precoTotal}"""
    remetente = "mateusfujitaoficial@gmail.com"
    send_mail(assunto,corpo,remetente,[email])