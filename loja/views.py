from django.shortcuts import render, redirect
from .models import *
from .views import *
import uuid 
from .utils import *
from django.db.models import Min, Max
from decimal import Decimal
from django.contrib.auth import login,logout, authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from datetime import *
from django.shortcuts import reverse
from .API_MercadoPago import *
from django.core.mail import send_mail

def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context = {"banners": banners}
    return render(request, 'homepage.html', context)

def minhaConta(request):
    erro = None
    alterado = False

    if request.method == "POST":
        dados = request.POST.dict()
        if "senhaAtual" in dados:
            # Modificação de senha
            senhaAtual = dados.get("senhaAtual")
            novaSenha = dados.get("novaSenha")
            senhaConfirmacao = dados.get("senhaConfirmacao")

            if novaSenha == senhaConfirmacao:
                usuario = authenticate(request, username=request.user.email, password=senhaAtual)
                if usuario:
                    usuario.set_password(novaSenha)
                    usuario.save()
                    alterado = True
                else:
                    erro = "senha_incorreta"
            else:
                erro = "senhas_diferentes"

        elif "email" in dados:
            # Modificação de dados pessoais
            email = dados.get("email")
            telefone = dados.get("telefone")
            nome = dados.get("nome")

            if email != request.user.email:
                if User.objects.filter(email=email).exists():
                    erro = "email_existente"

            if not erro:
                cliente = request.user.cliente
                cliente.email = email
                cliente.nome = nome
                cliente.telefone = telefone
                cliente.save()
                request.user.email = email
                request.user.save()
                alterado = True
        else:
            erro = "formulario_invalido"

    context = {"erro": erro, "alterado": alterado}
    return render(request, "usuarios/minhaConta.html", context)

def loja(request, filtro=None):
    produtos = Produto.objects.filter(ativo=True)
    produtos = filtrarProdutos(produtos, filtro)
    if request.method == "POST":
        dados = request.POST.dict()
        produtos = produtos.filter(preco__gte=dados.get("precoMinimo"), preco__lte=dados.get("precoMaximo"))
        if "tamanho" in dados:
            itens = ItemEstoque.objects.filter(produto__in=produtos, tamanho=dados.get("tamanho"))
            ids_produtos = itens.values_list("produto", flat=True).distinct()
            produtos = produtos.filter(id__in=ids_produtos)
        if "tipo" in dados:
            produtos = produtos.filter(tipo__slug=dados.get("tipo"))
        if "categoria" in dados:
            produtos = produtos.filter(categoria__slug=dados.get("categoria"))

    
    ordem = request.GET.get("ordem","menorPreco")
    produtos = ordenarProdutos(produtos,ordem)
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

@login_required
def minhaconta(request):

    return render(request, 'usuarios/minhaconta.html')

@login_required
def meusPedidos(request):
    cliente = request.user.cliente
    pedidos = Pedido.objects.filter(finalizado=True, cliente=cliente).order_by("-dataFinalizacao")


    context = {"pedidos":pedidos}
    return render(request, 'usuarios/meusPedidos.html', context)


def fazerLogin(request):     
    erro = False     
    if request.user.is_authenticated:         
        return redirect('loja')     
    if request.method == "POST":         
        dados = request.POST.dict()         
        if "email" in dados and "senha" in dados:         
            email = dados.get("email")             
            senha = dados.get("senha")
            print(dados)         
            usuario = authenticate(request, username=email, password=senha)  
            if usuario:                 
                login(request, usuario)                 
                return redirect("loja")             
            else:                 
                erro = True         
        else:             
            erro = True 
    context = {"erro": erro}     
    return render(request, 'usuarios/fazerLogin.html', context)

def criarConta(request):
    erro = None
    if request.user.is_authenticated:
        return redirect("loja")

    if request.method == "POST":
        dados = request.POST.dict()
        print("Dados recebidos:", dados)  # Para depuração, pode remover depois

        # Verificando se os campos essenciais estão presentes
        if "email" in dados and "senha" in dados and "confirmacaoSenha" in dados:
            email = dados["email"]
            senha = dados["senha"]
            confirmacaoSenha = dados["confirmacaoSenha"]

            # Validação do email
            try:
                validate_email(email)
            except ValidationError:
                erro = "emailInvalido"
            
            # Verificando se as senhas são iguais
            if senha != confirmacaoSenha:
                erro = "senhaInvalida"
            
            # Se não houver erro de email ou senha, criamos o usuário
            if erro is None:
                usuario, criado = User.objects.get_or_create(username=email, email=email)
                if not criado:
                    erro = "usuarioExistente"
                else:
                    usuario.set_password(senha)
                    usuario.save()
                    usuario = authenticate(request, username=email, password=senha)
                    login(request, usuario)

                    # Verificando a sessão do cliente
                    idSessao = request.COOKIES.get("idSessao")
                    if idSessao:
                        cliente, criado = Cliente.objects.get_or_create(idSessao=idSessao)
                    else:
                        cliente, criado = Cliente.objects.get_or_create(email=email)
                    
                    cliente.usuario = usuario
                    cliente.email = email
                    cliente.save()

                    return redirect("loja")
        else:
            erro = "preenchimento"

    context = {"erro": erro}
    return render(request, "usuarios/criarConta.html", context)

@login_required
def fazerLogout(request):
    logout(request)
    return redirect("fazerLogin")

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



def finalizarPedido(request, idPedido):
    if request.method == "POST":
        erro = None
        dados = request.POST.dict()

        total = dados.get("total")
        total = float(total.replace(",", "."))
        pedido = Pedido.objects.get(id=idPedido)

        if total != float(pedido.precoTotal):
            erro = "preco"

        if not "endereco" in dados:
            erro = "endereco"
        else:
            idEndereco = dados.get("endereco")
            endereco = Endereco.objects.get(id=idEndereco)
            pedido.endereco = endereco

        if not request.user.is_authenticated:
            email = dados.get("email")
            try:
                validate_email(email)
            except ValidationError:
                erro = "email"
            if not erro:
                clientes = Cliente.objects.filter(email=email)
                if clientes:
                    pedido.cliente = clientes[0]
                else:
                    pedido.cliente.email = email
                    pedido.cliente.save()
        
        codigoTransacao = f"{pedido.id}-{datetime.now().timestamp()}"
        pedido.codigoTransacao = codigoTransacao
        pedido.save()
        if erro:
            enderecos = Endereco.objects.filter(cliente=pedido.cliente)
            context = {"erro": erro, "pedido": pedido, "enderecos": enderecos}
            return render(request, "checkout.html", context)
        else:
            itensPedido = ItemPedido.objects.filter(pedido=pedido)
            link = request.build_absolute_uri(reverse('finalizar_pagamento'))
            link_pagamento, id_pagamento = criarPagamento(itensPedido, link)
            pagamento = Pagamento.objects.create(id_pagamento = id_pagamento, pedido=pedido)
            pagamento.save()
            return redirect(link_pagamento)

    else:
        return redirect("loja")

def finalizar_pagamento(request):
    dados = request.GET.dict()
    status = dados.get("status")
    id_pagamento = dados.get("preference_id")
    if status == "approved":
        pagamento = Pagamento.objects.get(id_pagamento = id_pagamento)
        pagamento.aprovado = True
        pedido = pagamento.pedido
        pedido.finalizado = True
        pedido.dataFinalizacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pedido.save()
        pagamento.save()
        enviarEmailCompra(pedido)
        if request.user.is_authenticated:
            return redirect("meusPedidos")
        else:
            return redirect("pedidoAprovado, pedido.id")
    else:
        return redirect("checkout")




def pedidoAprovado(request, idPedido):
    pedido = Pedido.objects.get(id = idPedido)
    context = {"pedido":pedido}
    return render(request, "pedidoAprovado.html")

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


