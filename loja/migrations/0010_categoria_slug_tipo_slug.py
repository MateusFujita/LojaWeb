# Generated by Django 5.1.1 on 2024-09-30 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0009_alter_itempedido_quantidade'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='slug',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tipo',
            name='slug',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
