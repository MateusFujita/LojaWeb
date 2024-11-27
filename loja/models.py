from django.db import models
from django.contrib.auth.models import User

#Cliente
class Cliente(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=200, null=True, blank=True)
    idSessao = models.CharField(max_length=200)
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    


    def __str__(self):
        # Determine o valor a ser retornado
        retorno = self.nome if self.nome else f"Cliente {self.id}"
        return retorno  # Corrigido para retornar uma string


class Categoria(models.Model):
    nome = models.CharField(max_length=200,null=True, blank=True)
    slug = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return self.nome

class Tipo(models.Model):
    nome = models.CharField(max_length=200,null=True, blank=True)
    slug = models.CharField(max_length=200,null=True, blank=True)
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    imagem = models.ImageField()
    nome = models.CharField(max_length=200,null=True, blank=True)
    preco = models.DecimalField(max_digits = 10,decimal_places = 2)
    ativo = models.BooleanField(default='True')
    categoria = models.ForeignKey(Categoria, null=True, blank=True,on_delete=models.SET_NULL)
    tipo = models.ForeignKey(Tipo, null=True, blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return f"Nome: {self.nome}, Categoria: {self.categoria} Tipo: {self.tipo}, ID: {self.id}"

    def totalVendas(self):
        itens = ItemPedido.objects.filter(pedido__finalizado = True, itemEstoque__produto = self.id)
        total = sum([item.quantidade for item in itens])
        return total


class Cor(models.Model):
    nome = models.CharField(max_length=200,null=True,blank=True)
    codigo = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.nome

class ItemEstoque(models.Model):
    produto = models.ForeignKey(Produto, null=True, blank=True,on_delete=models.SET_NULL)
    nome = models.CharField(max_length=200,null=True, blank=True)
    tamanho = models.CharField(max_length=200,null=True, blank=True)
    cor= models.ForeignKey(Cor,null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.nome}, Tamanho: {self.tamanho}, Cor: {self.cor}"
    
class Endereco(models.Model):
    rua = models.CharField(max_length=200,null=True, blank=True)
    numero = models.IntegerField(default=000)
    complemento = models.CharField(max_length=200,null=True)
    cep = models.CharField(max_length=200,null=True, blank=True)
    cidade = models.CharField(max_length=200,null=True, blank=True)
    estado = models.CharField(max_length=200,null=True, blank = True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True,on_delete=models.SET_NULL)
    

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True,on_delete=models.SET_NULL)
    finalizado = models.BooleanField(default=False)
    codigoTransacao = models.CharField(max_length=200,null=True, blank=True)
    endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    dataFinalizacao = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Cliente:{self.cliente.email} - idPedido: {self.id} - Finalizado:{self.finalizado}"
    
    @property    
    def quantidadeTotal(self):
        itemPedido = ItemPedido.objects.filter(pedido__id= self.id)
        qntTotal = sum([item.quantidade for item in itemPedido])
        return qntTotal
    @property    
    def precoTotal(self):
        itemPedido = ItemPedido.objects.filter(pedido__id = self.id)
        preco = sum([item.precoTotal for item in itemPedido])
        return preco
    
    def itens(self):
        itemPedido = ItemPedido.objects.filter(pedido__id = self.id)
        return itemPedido

    
        
class ItemPedido(models.Model):
    itemEstoque = models.ForeignKey(ItemEstoque, null=True, blank=True,on_delete=models.SET_NULL)
    cor = models.ForeignKey(Cor, null=True, blank=True,on_delete=models.SET_NULL)
    quantidade = models.IntegerField(default=0)
    pedido = models.ForeignKey(Pedido,null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"ID Pedido: {self.pedido.id} - Produto: {self.itemEstoque.produto} - Cor: {self.itemEstoque.cor.nome}"

    @property
    def precoTotal(self):
        return self.quantidade * self.itemEstoque.produto.preco

class Banner(models.Model):
    imagem = models.ImageField(upload_to="banners", null = True, blank= True)
    linkDestino = models.CharField(max_length=400, null = True, blank=True)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return self.linkDestino 
    

