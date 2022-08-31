from django.forms.models import inlineformset_factory
from .models import Curso, Modulo


ModuloFormSet = inlineformset_factory(Curso,
                                      Modulo,
                                      fields=['titulo', 'descricao'],
                                      extra=2,
                                      can_delete=True)
