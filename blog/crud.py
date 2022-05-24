from django.db.models import Count, Avg, Min, Max, Q

from blog.models import Note, Comment


def notes_count():
    """ Количество записей в блоге. """
    return Note.objects.all().count()


def notes_aggregate_count():
    """ Альтернативный способ получения количество записей в блоге с помощью aggregate. """
    return Note.objects.aggregate(Count("id"))


def all_comments_describe():
    """
    Сводная статистика по всем комментариям.
    Средний, минимальный, максимальный рейтинг и количество комментариев.
    """
    return Comment.objects.aggregate(  # todo add name
        avg=Avg("rating"),
        min=Min("rating"),
        max=Max("rating"),
        count=Count("rating"),
    )


def note_with_count_comments():
    """
    Количество комментариев в каждой статье как дополнительное поле после агрегации.
    https://docs.djangoproject.com/en/4.0/topics/db/aggregation/#following-relationships-backwards
    """
    return Note.objects.annotate(Count("comment"))


def note_only_count_comments():
    """
    Получить только количество комментариев в каждой статье.
    https://docs.djangoproject.com/en/4.0/topics/db/aggregation/#following-relationships-backwards
    """
    return Note.objects\
        .annotate(Count("comment"))\
        .values("id", "comment__count")


def note_avg_comments_rating():
    """
    Количество комментариев в каждой статье как дополнительное поле после агрегации.
    https://docs.djangoproject.com/en/4.0/topics/db/aggregation/#following-relationships-backwards
    """
    return Note.objects.annotate(Avg("comment__rating"))


def notes_published_describe():
    """Вывести сводную информацию об опубликованных и не опубликованных статьях."""
    published = Count("public", filter=Q(public=True))  # количество опубликованных статей
    unpublished = Count("public", filter=Q(public=False))  # количество неопубликованных статей
    return Note.objects\
        .aggregate(
            published=published,
            unpublished=unpublished
        )


def search_in_note_message(first_word, second_word):
    """
    Поиск статей, в сообщении который содержится first_word или second_word.

    https://docs.djangoproject.com/en/4.0/topics/db/queries/#complex-lookups-with-q-objects
    https://docs.djangoproject.com/en/4.0/ref/models/querysets/#std:fieldlookup-icontains
    """
    query = Q(message__icontains=first_word) | \
            Q(message__icontains=second_word)
    return Note.objects.filter(query)
