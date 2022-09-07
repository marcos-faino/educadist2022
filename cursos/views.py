from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Curso, Modulo, Conteudo
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuloFormSet
from django.forms.models import modelform_factory
from django.apps import apps


class HomeView(ListView):
    template_name = 'index.html'
    model = Curso
    context_object_name = 'cursos'


class DonoMixin(object):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(dono=self.request.user)


class DonoEditarMixin(object):
    def form_valid(self, form):
        form.instance.dono = self.request.user
        return super().form_valid(form)


class DonoCursoMixin(DonoMixin,
                     LoginRequiredMixin,
                     PermissionRequiredMixin):
    model = Curso
    fields = ['assunto', 'titulo', 'slug', 'desc_geral', 'icone']
    success_url = reverse_lazy('gerenciar_curso_list')
    context_object_name = 'curso'


class DonoCursoFormMixin(DonoCursoMixin, DonoEditarMixin):
    template_name = 'gerenciar/curso/form.html'


class ListarCursosListView(DonoCursoMixin, ListView):
    template_name = 'gerenciar/curso/listar.html'
    context_object_name = 'cursos'
    permission_required = 'cursos.view_curso'


class CriarCursoCreateView(DonoCursoFormMixin, CreateView):
    permission_required = 'cursos.add_curso'


class AtualizarCursoUpdateView(DonoCursoFormMixin, UpdateView):
    permission_required = 'cursos.change_curso'


class ExcluirCursoDeleteView(DonoCursoMixin, DeleteView):
    template_name = 'gerenciar/curso/excluir.html'
    permission_required = 'cursos.delete_curso'


class ModuloCursoUpdateView(TemplateResponseMixin, View):
    template_name = 'gerenciar/modulo/formset.html'
    curso = None

    def get_formset(self, data=None):
        return ModuloFormSet(instance=self.curso, data=data)

    def dispatch(self, request, pk, *args, **kwargs):
        self.curso = get_object_or_404(Curso, id=pk,
                                       dono=request.user)
        return super().dispatch(request, pk, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('gerenciar_curso_list')
        return self.render_to_response({'curso': self.curso, 'formset': formset})

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'curso': self.curso, 'formset': formset})


class CriarAtualizarConteudoView(TemplateResponseMixin, View):
    modulo = None
    model = None
    obj = None
    template_name = 'gerenciar/conteudo/form.html'

    def get_model(self, model_name):
        if model_name in ['texto', 'video', 'imagem', 'arquivo']:
            return apps.get_model('cursos',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['dono',
                                                 'order',
                                                 'criado',
                                                 'atualizado'])
        return Form(*args, **kwargs)

    def dispatch(self, request, modulo_id, model_name, id=None, *args, **kwargs):
        self.modulo = get_object_or_404(Modulo, id=modulo_id,
                                        curso__dono=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         dono=request.user)
        return super().dispatch(request, modulo_id, model_name, id)

    def get(self, request, modulo_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'conteudo': self.obj,
                                        'model_name': model_name,
                                        'modulo': self.modulo})

    def post(self, request, modulo_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.dono = request.user
            obj.save()
            if not id:
                Conteudo.objects.create(modulo=self.modulo, item=obj)
            return redirect('conteudo_modulo_list', self.modulo.id)
        return self.render_to_response({'form': form,
                                        'conteudo': self.obj,
                                        'modulo': self.modulo})

class ExcluirConteudoView(View):

    def post(self, request, id_cont):
        conteudo= get_object_or_404(Conteudo,
                                    id=id_cont,
                                    modulo__curso__dono = request.user)
        modulo = conteudo.modulo
        conteudo.item.delete()
        conteudo.delete()
        return redirect('conteudo_modulo_list', modulo.id)
