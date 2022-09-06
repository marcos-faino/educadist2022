from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Curso
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuloFormSet


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
    fields = ['assunto', 'titulo', 'slug', 'desc_geral','icone']
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
        self.curso = get_object_or_404(Curso,id=pk,
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