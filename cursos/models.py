from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .fields import OrdenaCampos


class Base(models.Model):
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Assunto(Base):
    titulo = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Assunto'
        verbose_name_plural = 'Assuntos'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


class Curso(Base):
    dono = models.ForeignKey(User,
                             related_name='cursos_user',
                             on_delete=models.CASCADE)
    assunto = models.ForeignKey(Assunto,
                                related_name='cursos_assunto',
                                on_delete=models.CASCADE)
    titulo = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=200)
    desc_geral = models.TextField('Descrição')

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['-criado']

    def __str__(self):
        return self.titulo


class Modulo(Base):
    curso = models.ForeignKey(Curso,
                              related_name='modulos_curso',
                              on_delete=models.CASCADE)
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição', blank=True)
    order = OrdenaCampos(blank=True, for_fields=['curso'])

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['order']

    def __str__(self):
        return f'{self.order} - {self.titulo}'


class ItemConteudoBase(Base):
    dono = models.ForeignKey(User,
                             related_name='%(class)s_relacionados',
                             on_delete=models.CASCADE)
    titulo = models.CharField('Título', max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return self.titulo


class Texto(ItemConteudoBase):
    conteudo = models.TextField()


class Arquivo(ItemConteudoBase):
    conteudo = models.FileField(upload_to='arquivos')


class Imagem(ItemConteudoBase):
    conteudo = models.FileField(upload_to='imagens')


class Video(ItemConteudoBase):
    caminho = models.URLField()


class Conteudo(Base):
    modulo = models.ForeignKey(Modulo,
                               related_name='conteudos_modulo',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={
                                         'model_in': (
                                             'texto',
                                             'imagem',
                                             'video',
                                             'arquivo',
                                         )})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrdenaCampos(blank=True, for_fields=['modulo'])

    class Meta:
        ordering = ['order']