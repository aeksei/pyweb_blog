from django.contrib import admin

from .models import Note, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...


# # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#inlinemodeladmin-objects
# class CommentInline(admin.TabularInline):
#     model = Comment
#
#     extra = 0
#     min_num = 0


@admin.register(Note)  # связываем админку с моделью
class NoteAdmin(admin.ModelAdmin):
    # Поля в списке
    list_display = (
        'title', 'id', 'public', 'update_at',
        "authors_str", "admin_authors",
    )
    # #
    # # # Группировка поля в режиме редактирования
    fields = (('title', 'public'), 'message', 'authors', 'create_at', 'update_at')
    # Поля только для чтения в режиме редактирования
    readonly_fields = ('create_at', 'update_at')
    # #
    # Поиск по выбранным полям
    search_fields = ['title']
    #
    # Фильтры справа
    list_filter = ('public', )

    # # Widget для удобного поиска записей
    autocomplete_fields = ['authors']  # todo для поиска по автору

    # отображение связи Many-to-one
    # inlines = [
    #     CommentInline
    # ]
    ...

    def admin_authors(self, instance):
        return ", ".join(author.username for author in instance.authors.all())

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset\
            .prefetch_related("authors")
