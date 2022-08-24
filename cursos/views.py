from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Curso


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
    fields = ['assunto', 'titulo', 'slug', 'desc_geral']
    success_url = reverse_lazy('gerenciar_curso_list')


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
