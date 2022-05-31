from django.db.models.query import QuerySet
from django_filters import rest_framework as filters

from blog.models import Note


def author_id_filter(self, queryset: QuerySet):
    ...


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


class NoteFilter(filters.FilterSet):
    year = filters.NumberFilter(
        field_name="create_at",
        lookup_expr="year",
        help_text="Год статьи",
    )

    class Meta:
        model = Note
        fields = [
            'title',
            'authors',
            'year',
        ]
