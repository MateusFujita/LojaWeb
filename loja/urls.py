from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views

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
    path('usuarios/fazerLogout', fazerLogout, name='fazerLogout'),
    path('usuarios/meusPedidos', meusPedidos, name='meusPedidos'),


#URL DO ALTERAR SENHA
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]




