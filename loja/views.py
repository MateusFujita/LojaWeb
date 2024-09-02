from django.shortcuts import render, redirect
from .models import Banner, Produto, ItemEstoque, Cor, Pedido, ItemPedido
from .views import *

def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {"banners": banners}
    return render(request, 'homepage.html', context)

def loja(request, nome_categoria=None):
    produtos = Produto.objects.filter(ativo=True)
    if nome_categoria:
        produtos = produtos.filter(categoria__nome=nome_categoria)
    context = {"produtos": produtos}
    return render(request, 'loja.html', context)

def verProduto(request, idProduto, idCor=None):
    temEstoque = False
    cores = {}
    tamanhos = {}
    produto = Produto.objects.get(id=idProduto)
    itemEstoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)
    corSelecionada = None

    if idCor:
        corSelecionada = Cor.objects.get(id=idCor)
        nomeCor = corSelecionada.id

    if len(itemEstoque) > 0:
        temEstoque = True
        cores = {item.cor for item in itemEstoque}
        if idCor:
            itemEstoque = itemEstoque.filter(produto=produto, cor=idCor, quantidade__gt=0)
            tamanhos = {item.tamanho for item in itemEstoque}
    
    context = {
        "produto": produto,
        "itemEstoque": itemEstoque,
        "temEstoque": temEstoque,
        "cores": cores,
        "tamanhos": tamanhos,
        "corSelecionada": corSelecionada,
    }
    return render(request, "verProduto.html", context)

def minhaconta(request):
    return render(request, 'usuarios/minhaconta.html')

def login(request):
    return render(request, 'usuarios/login.html')

def addCarrinho(request, idProduto):
    if request.method == "POST" and idProduto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        cor = dados.get("cor")
        if not tamanho:
            return redirect('loja')
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            return redirect('loja')
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        itemEstoque = ItemEstoque.objects.get(produto__id=idProduto, tamanho=tamanho, cor__id=cor)
        itemPedido, _ = ItemPedido.objects.get_or_create(itemEstoque=itemEstoque, pedido=pedido)
        itemPedido.quantidade = itemPedido.quantidade + 1
        itemPedido.save()
        return redirect('carrinho')
    else:
        return redirect('loja')



def removerCarrinho(request, idProduto):
    if request.method == "POST" and idProduto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        cor = dados.get("cor")
        if not tamanho:
            return redirect('loja')
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            return redirect('loja')
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        itemEstoque = ItemEstoque.objects.get(produto__id=idProduto, tamanho=tamanho, cor__id=cor)
        itemPedido, _ = ItemPedido.objects.get_or_create(itemEstoque=itemEstoque, pedido=pedido)
        itemPedido.quantidade -= 1
        itemPedido.save()
        if itemPedido.quantidade <= 0:
            itemPedido.delete()
        return redirect('carrinho')
    else:
        return redirect('loja')

def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itemPedido = ItemPedido.objects.filter(pedido=pedido)
    context = {"itemPedido": itemPedido, "pedido": pedido}
    return render(request, 'carrinho.html', context)


def checkout(request):
    return render(request, 'checkout.html')
