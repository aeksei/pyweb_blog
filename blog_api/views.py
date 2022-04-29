from rest_framework.views import APIView
from rest_framework.request import Request


class NoteListCreateAPIView(APIView):
    """ Представление, которое позволяет вывести весь список записей и добавить новую запись. """
    def get(self, request: Request):
        ...

    def post(self, request):
        # todo request.data
        # todo simple serializer
        # todo status code
        ...


class NoteDetailAPIView(APIView):
    """ Представление, которое позволяет вывести отдельную запись. """
    def get(self, request):  # todo path param
        # todo shortcuts
        ...

    def put(self, request):
        # todo shortcuts
        ...

    def patch(self, request):
        # todo shortcuts
        ...
