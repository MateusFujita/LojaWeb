from django.contrib import admin
from .models import *

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'idSessao', 'usuario')
    search_fields = ('nome', 'email', 'telefone')
    list_filter = ('usuario',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class TipoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'ativo', 'categoria', 'tipo')
    search_fields = ('nome', 'categoria__nome', 'tipo__nome')
    list_filter = ('ativo', 'categoria', 'tipo')
    list_editable = ('ativo',)

class CorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo')
    search_fields = ('nome', 'codigo')

class ItemEstoqueAdmin(admin.ModelAdmin):
    list_display = ('getProduto','getCategoria','getTipo', 'tamanho', 'cor', 'quantidade')
    search_fields = ('produto__nome', 'tamanho', 'cor__nome')
    list_filter = ('cor', 'tamanho')

    def getProduto(self, obj):
        return obj.produto.nome if obj.produto else None
    getProduto.short_description = 'Produto'


    def getCategoria(self, obj):
        return obj.produto.categoria if obj else None
    getCategoria.short_description = 'Categoria'

    def getTipo(self, obj):
        return obj.produto.tipo if obj else None
    getTipo.short_description = 'Tipo'
    
    
    

class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'rua', 'numero', 'cidade', 'estado', 'cep')
    search_fields = ('cliente__nome', 'rua', 'cidade', 'estado')
    list_filter = ('cidade', 'estado')

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('get_cliente', 'get_codigo_transacao', 'get_finalizado', 'endereco', 'dataFinalizacao', 'quantidadeTotal', 'precoTotal')
    search_fields = ('cliente__nome', 'codigo_transacao')
    list_filter = ('finalizado', 'dataFinalizacao')

    def get_cliente(self, obj):
        return obj.cliente.nome if obj.cliente else None

    get_cliente.short_description = 'Cliente'

    def get_codigo_transacao(self, obj):
        return obj.id if obj else None

    get_codigo_transacao.short_description = 'ID do Pedido'

    def get_finalizado(self, obj):
        return obj.finalizado if obj else None
    
    get_finalizado.short_description = 'Finalizado'



class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'itemEstoque', 'cor', 'quantidade', 'precoTotal')
    search_fields = ('pedido__id', 'itemEstoque__produto__nome', 'cor__nome')
    list_filter = ('cor',)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('linkDestino', 'ativo')
    search_fields = ('linkDestino',)
    list_filter = ('ativo',)
    list_editable = ('ativo',)


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Cor, CorAdmin)
admin.site.register(ItemEstoque, ItemEstoqueAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Pedido, PedidoAdmin)
