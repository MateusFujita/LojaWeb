# Generated by Django 5.0.6 on 2024-07-12 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0007_alter_itemestoque_cor'),
    ]

    operations = [
        migrations.AddField(
            model_name='itempedido',
            name='cor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.cor'),
        ),
    ]
