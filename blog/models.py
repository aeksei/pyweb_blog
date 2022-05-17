from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Note(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Заголовок'))
    message = models.TextField(default='', verbose_name='Текст статьи')
    public = models.BooleanField(default=False, verbose_name='Опубликовать')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # todo добавить автора с помощью внешнего ключа

    def __str__(self):
        return f"Запись №{self.id}"

    class Meta:
        verbose_name = _("запись")
        verbose_name_plural = _("записи")


class Comment(models.Model):
    """ Комментарии и оценки к статьям """
    class Ratings(models.IntegerChoices):  # https://docs.djangoproject.com/en/4.0/ref/models/fields/#enumeration-types
        WITHOUT_RATING = 0, _('Без оценки')
        TERRIBLE = 1, _('Ужасно')
        BADLY = 2, _('Плохо')
        FINE = 3, _('Нормально')
        GOOD = 4, _('Хорошо')
        EXCELLENT = 5, _('Отлично')

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/#many-to-one-relationships
    note = models.ForeignKey(Note, on_delete=models.CASCADE,
                             related_name='comments')  # default related_name='comment_set'
    rating = models.IntegerField(default=Ratings.WITHOUT_RATING, choices=Ratings.choices,
                                 verbose_name='Оценка')

    def __str__(self):
        # https://django.fun/docs/django/ru/3.1/ref/models/instances/#django.db.models.Model.get_FOO_display
        return f'{self.get_rating_display()}: {self.author}'
