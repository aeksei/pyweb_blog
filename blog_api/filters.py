from typing import Optional

from django.db.models.query import QuerySet


def author_id_filter(queryset: QuerySet, author_id: Optional[int]):
    """

    """
    if author_id is not None:
        return queryset.filter(author_id=author_id)
    else:
        return queryset


def author__username_filter(self, queryset):
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#iexact
    ...


def comment__rating_filter(self, queryset):
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#exact
    ...


def comment__rating__gt_filter(self, queryset):
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#gt
    ...


def note_create_at__year_filter(self, queryset):
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#year
    ...


def note_update_at__month__gte_filter(self, queryset):
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#month
    ...