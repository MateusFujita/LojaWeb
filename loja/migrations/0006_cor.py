# Generated by Django 5.0.6 on 2024-07-11 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0005_itemestoque_cor_alter_banner_imagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
                ('codigo', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
