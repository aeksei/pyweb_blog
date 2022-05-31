from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


from blog.models import Note, Comment
from . import serializers, filters


class NoteListCreateAPIView(APIView):
    """ Представление, которое позволяет вывести весь список записей и добавить новую запись. """

    def get(self, request: Request):
        objects = Note.objects.all()
        serializer = serializers.NoteSerializer(
            instance=objects,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request: Request):
        # Передаем в сериалайзер (валидатор) данные из запроса
        serializer = serializers.NoteSerializer(data=request.data)

        # Проверка параметров
        if not serializer.is_valid():  # serializer.is_valid(raise_exception=True)
            return Response(
                serializer.errors,  # serializer.errors будут все ошибки
                status=status.HTTP_400_BAD_REQUEST
            )

        # Записываем новую статью и добавляем текущего пользователя как автора
        serializer.save(author=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class NoteDetailAPIView(APIView):
    """ Представление, которое позволяет вывести отдельную запись. """
    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        serializer = serializers.NoteDetailSerializer(
            instance=note,
        )

        return Response(serializer.data)

    def put(self, request, pk):
        ...

    def patch(self, request, pk):
        ...

    def delete(self, request, pk):
        ...


class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NoteFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset \
            .filter(public=True) \
            .order_by("-create_at")\
            .prefetch_related("authors","comment_set")


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def filter_queryset(self, queryset):
        query_params = serializers.QueryParamsCommentFilterSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)

        list_rating = query_params.data.get("rating")
        if list_rating:
            queryset = queryset.filter(rating__in=query_params.data["rating"])

        author = self.request.query_params.get("author")
        if author:
            queryset = queryset.filter(author=author)

        return queryset
