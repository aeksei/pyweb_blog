from django.shortcuts import render
from django.views import View, generic

from .models import Note


class HomeView(View):
    def get(self, request):
        # Объект который будет передан в шаблон
        context = {
            'title': 'Добро пожаловать',
            'left': 'генератор списка',
            'right': 'записи из базы данных',
            'data': [{'id': i, 'name': f'Name {i}'} for i in range(3)],
            'notes': Note.objects.all(),
        }

        # Рендеринг шаблона с последующим ответом клиенту
        return render(request, ..., context)  # todo installed app


class HomeTemplateView(generic.TemplateView):
    template_name = ...  # todo set template

    def get_context_data(self, **kwargs):
        ...  # todo context
