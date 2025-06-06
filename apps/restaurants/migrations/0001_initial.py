# Generated by Django 5.2.1 on 2025-05-29 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome do Restaurante')),
                ('endereco', models.CharField(max_length=255, verbose_name='Endereço')),
                ('tipo_culinaria', models.CharField(max_length=100, verbose_name='Tipo de Culinária')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Restaurante',
                'verbose_name_plural': 'Restaurantes',
                'ordering': ['nome'],
            },
        ),
    ]
