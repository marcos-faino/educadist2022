from django.urls import path
from .views import (HomeView,
                    ListarCursosListView,
                    CriarCursoCreateView,
                    AtualizarCursoUpdateView,
                    ExcluirCursoDeleteView,
                    ModuloCursoUpdateView,)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('meuscursos/',
         ListarCursosListView.as_view(),
         name='gerenciar_curso_list'),
    path('criarcurso/',
         CriarCursoCreateView.as_view(),
         name='criar_curso'),
    path('editarcurso/<pk>/',
         AtualizarCursoUpdateView.as_view(),
         name='editar_curso'),
    path('excluircurso/<pk>/',
         ExcluirCursoDeleteView.as_view(),
         name='excluir_curso'),
    path('modulo/<pk>/',
         ModuloCursoUpdateView.as_view(),
         name='modulo_curso_update'),
]
