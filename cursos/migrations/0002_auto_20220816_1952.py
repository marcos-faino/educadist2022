# Generated by Django 3.2.14 on 2022-08-16 23:52

import cursos.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modulo',
            options={'ordering': ['order'], 'verbose_name': 'Módulo', 'verbose_name_plural': 'Módulos'},
        ),
        migrations.AddField(
            model_name='modulo',
            name='order',
            field=cursos.fields.OrdenaCampos(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('atualizado', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=200, verbose_name='Título')),
                ('caminho', models.URLField()),
                ('dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_relacionados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Texto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('atualizado', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=200, verbose_name='Título')),
                ('conteudo', models.TextField()),
                ('dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='texto_relacionados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Imagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('atualizado', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=200, verbose_name='Título')),
                ('conteudo', models.FileField(upload_to='imagens')),
                ('dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagem_relacionados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Conteudo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('atualizado', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('order', cursos.fields.OrdenaCampos(blank=True)),
                ('content_type', models.ForeignKey(limit_choices_to={'model_in': ('texto', 'imagem', 'video', 'arquivo')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conteudos_modulo', to='cursos.modulo')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateTimeField(auto_now_add=True)),
                ('atualizado', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=200, verbose_name='Título')),
                ('conteudo', models.FileField(upload_to='arquivos')),
                ('dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arquivo_relacionados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
