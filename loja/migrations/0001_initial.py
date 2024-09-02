# Generated by Django 5.0.6 on 2024-06-27 18:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemEstoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
                ('tamanho', models.CharField(blank=True, max_length=200, null=True)),
                ('quantidade', models.IntegerField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('telefone', models.CharField(blank=True, max_length=200, null=True)),
                ('idSessao', models.CharField(max_length=200)),
                ('usuario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rua', models.CharField(blank=True, max_length=200, null=True)),
                ('numero', models.IntegerField(default=0)),
                ('complemento', models.CharField(max_length=200, null=True)),
                ('cep', models.CharField(blank=True, max_length=200, null=True)),
                ('cidade', models.CharField(blank=True, max_length=200, null=True)),
                ('estado', models.CharField(blank=True, max_length=200, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finalizado', models.BooleanField(default=False)),
                ('codigoTransacao', models.CharField(blank=True, max_length=200, null=True)),
                ('dataFinalizacao', models.DateTimeField(blank=True, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.cliente')),
                ('endereco', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.endereco')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(blank=True, max_length=200, null=True)),
                ('itemEstoque', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.itemestoque')),
                ('pedido', models.ForeignKey(blank=True, max_length=200, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.CharField(blank=True, max_length=400, null=True)),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ativo', models.BooleanField(default='True')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.categoria')),
                ('tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.tipo')),
            ],
        ),
        migrations.AddField(
            model_name='itemestoque',
            name='produto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.produto'),
        ),
    ]
