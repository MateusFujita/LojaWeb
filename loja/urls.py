from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('loja/', loja, name='loja'),
    path('loja/<str:filtro>/', loja, name='loja'),
    path('produtos/<int:idProduto>/',verProduto,name='verProduto'),
    path('produtos/<int:idProduto>/<int:idCor>/',verProduto,name='verProduto'),
    path('carrinho/', carrinho, name='carrinho'),
    path('addCarrinho/<int:idProduto>/', addCarrinho, name='addCarrinho'),
    path('checkout/', checkout, name='checkout'),
    path('removerCarrinho/<int:idProduto>/', removerCarrinho, name='removerCarrinho'),
    path('adicionarEndereco/', adicionarEndereco, name='adicionarEndereco'),

    path('usuarios/minhaconta', minhaconta, name='minhaconta'),
    path('usuarios/fazerLogin', fazerLogin, name='fazerLogin'),
    path('usuarios/criarConta', criarConta, name='criarConta'),
]




