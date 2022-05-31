from datetime import datetime

from rest_framework import serializers

from blog.models import Note, Comment


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ("public",)
        read_only_fields = ("author", )


class CommentSerializer(serializers.ModelSerializer):
    # todo serializers.SerializerMethodField
    # rating = serializers.SerializerMethodField('get_rating')
    #
    # def get_rating(self, obj):
    #     return {
    #         'value': obj.rating,
    #         'display': obj.get_rating_display()
    #     }

    class Meta:
        model = Comment
        fields = "__all__"


class NoteDetailSerializer(serializers.ModelSerializer):
    """ Одна статья блога """
    author = serializers.SlugRelatedField(
        slug_field="username",  # указываем новое поле для отображения
        read_only=True  # поле для чтения
    )
    comment_set = CommentSerializer(many=True, read_only=True)  # one-to-many-relationships

    class Meta:
        model = Note
        fields = (
            'title', 'message', 'create_at', 'update_at',  # из модели
            'author', 'comment_set',  # из сериализатора
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


class QueryParamsCommentFilterSerializer(serializers.Serializer):
    rating = serializers.ListField(
        child=serializers.ChoiceField(choices=Comment.Ratings.choices), required=False,
    )
