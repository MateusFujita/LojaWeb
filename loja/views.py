from django.shortcuts import render, redirect
from .models import *
from .views import *
import uuid 
from .utils import *
from django.db.models import Min, Max
from decimal import Decimal

def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {"banners": banners}
    return render(request, 'homepage.html', context)


def loja(request, filtro=None):
    produtos = Produto.objects.filter(ativo=True)
    produtos = filtrarProdutos(produtos, filtro)
    # aplicar os filtros do formulário
    if request.method == "POST":
        dados = request.POST.dict()
        produtos = produtos.filter(preco__gte=dados.get("preco_minimo"), preco__lte=dados.get("preco_maximo"))
        if "tamanho" in dados:
            itens = ItemEstoque.objects.filter(produto__in=produtos, tamanho=dados.get("tamanho"))
            ids_produtos = itens.values_list("produto", flat=True).distinct()
            produtos = produtos.filter(id__in=ids_produtos)
        if "tipo" in dados:
            produtos = produtos.filter(tipo__slug=dados.get("tipo"))
        if "categoria" in dados:
            produtos = produtos.filter(categoria__slug=dados.get("categoria"))

    itens = ItemEstoque.objects.filter(quantidade__gt=0, produto__in=produtos)
    tamanhos = itens.values_list("tamanho", flat=True).distinct()
    ids_categorias = produtos.values_list("categoria", flat=True).distinct()
    categorias = Categoria.objects.filter(id__in=ids_categorias)
    minimo, maximo = precoMaximoMinimo(produtos)
    context = {"produtos": produtos, "minimo": minimo, "maximo": maximo, "tamanhos": tamanhos, 
               "categorias": categorias}
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

        if itemPedido.quantidade > 1:
            itemPedido.quantidade -= 1
            itemPedido.save()
        else:
            itemPedido.delete()  # Remove o item do carrinho se a quantidade for menor ou igual a 1

        return resposta
    else:
        return redirect('loja')


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
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("idSessao"):
            idSessao = request.COOKIES.get("idSessao")
            cliente, criado = Cliente.objects.get_or_create(idSessao=idSessao)
        else:
            return redirect('loja')
            
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    endereco = Endereco.objects.filter(cliente=cliente)
    context = {"pedido": pedido, "endereco": endereco}
    return render(request, 'checkout.html', context)


def adicionarEndereco(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("idSessao"):
            idSessao = request.COOKIES.get("idSessao")
            cliente, criado = Cliente.objects.get_or_create(idSessao=idSessao)
        else:
            return redirect("loja")

    if request.method == "POST":
        dados = request.POST.dict()
        endereco = Endereco.objects.create(
            cliente=cliente,
            rua=dados.get("rua"),
            numero=int(dados.get("numero")),  
            estado=dados.get("estado"),
            cidade=dados.get("cidade"),
            cep=dados.get("cep"),
            complemento=dados.get("complemento")           

        )
        endereco.save()

        return redirect("checkout")
    else:
        return render(request, 'adicionarEndereco.html')


