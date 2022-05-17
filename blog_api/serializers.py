from datetime import datetime

from rest_framework import serializers

from blog.models import Note, Comment


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        # exclude = ("public",)  # __all__ без public
        read_only_fields = ("author", )


class CommentSerializer(serializers.ModelSerializer):
    # todo serializers.SerializerMethodField
    rating = serializers.SerializerMethodField('get_rating')

    def get_rating(self, obj: Comment):
        return {
            'value': obj.rating,
            'display': obj.get_rating_display()
        }

    class Meta:
        model = Comment
        fields = "__all__"


class NoteDetailSerializer(serializers.ModelSerializer):
    """ Одна статья блога """
    author = serializers.SlugRelatedField(
        slug_field="email",  # указываем новое поле для отображения
        read_only=True  # поле для чтения
    )
    comments = CommentSerializer(many=True, read_only=True)  # one-to-many-relationships

    class Meta:
        model = Note
        fields = (
            'title', 'message', 'create_at', 'update_at', 'public',  # из модели
            'author', 'comments',  # из сериализатора
        )

    def to_representation(self, instance):
        """ Переопределение вывода. Меняем формат даты в ответе """
        ret = super().to_representation(instance)
        # Конвертируем строку в дату по формату
        create_at = datetime.strptime(ret['create_at'], '%Y-%m-%dT%H:%M:%S.%f')
        # Конвертируем дату в строку в новом формате
        ret['create_at'] = create_at.strftime('%d %B %Y %H:%M:%S')
        return ret


class NoteUpdateSerializer(serializers.ModelSerializer):
    ...  # todo update fields
