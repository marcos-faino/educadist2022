from django.urls import path
from .views import (HomeView,
                    ListarCursosListView,
                    CriarCursoCreateView,
                    AtualizarCursoUpdateView,
                    ExcluirCursoDeleteView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('meuscursos/',
         ListarCursosListView.as_view(),
         name='gerenciar_curso_list'),
    path('criarcurso/',
         CriarCursoCreateView.as_view(),
         name='criar_curso'),
    path('editarcurso/',
         AtualizarCursoUpdateView.as_view(),
         name='editar_curso'),
    path('excluircurso/',
         ExcluirCursoDeleteView.as_view(),
         name='excluir_curso'),
]
