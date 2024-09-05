from django.shortcuts import render, redirect
from .models import Banner, Produto, ItemEstoque, Cor, Pedido, ItemPedido,Cliente
from .views import *
import uuid 

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

        resposta = redirect('carrinho')

        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            idSessao = request.COOKIES.get("idSessao", str(uuid.uuid4()))
            if not request.COOKIES.get("idSessao"):
                resposta.set_cookie(key="idSessao", value=idSessao)
            cliente, criado = Cliente.objects.get_or_create(idSessao=idSessao)

        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        itemEstoque = ItemEstoque.objects.get(produto__id=idProduto, tamanho=tamanho, cor__id=cor)
        itemPedido, _ = ItemPedido.objects.get_or_create(itemEstoque=itemEstoque, pedido=pedido)
        itemPedido.quantidade += 1
        itemPedido.save()

        return resposta
    else:
        return redirect('loja')




def removerCarrinho(request, idProduto):
    if request.method == "POST" and idProduto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        cor = dados.get("cor")

        if not tamanho:
            return redirect('loja')

        resposta = redirect('carrinho')

        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            idSessao = request.COOKIES.get("idSessao", str(uuid.uuid4()))
            if not request.COOKIES.get("idSessao"):
                resposta.set_cookie(key="idSessao", value=idSessao)
            cliente, criado = Cliente.objects.get_or_create(idSessao=idSessao)

        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        itemEstoque = ItemEstoque.objects.get(produto__id=idProduto, tamanho=tamanho, cor__id=cor)
        itemPedido, _ = ItemPedido.objects.get_or_create(itemEstoque=itemEstoque, pedido=pedido)
        itemPedido.quantidade -= 1
        itemPedido.save()

        return resposta
    else:
        return redirect('loja')

def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("idSessao"):
            idSessao = request.COOKIES.get("idSessao")
            cliente, criado = Cliente.objects.get_or_create(idSessao=idSessao)
        else:
            context = {"cliente": False, "itemPedido": None, "pedido": None}
            return render(request, 'carrinho.html', context)            
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itemPedido = ItemPedido.objects.filter(pedido=pedido)
    context = {"itemPedido": itemPedido, "pedido": pedido}
    return render(request, 'carrinho.html', context)


def checkout(request):
    return render(request, 'checkout.html')
