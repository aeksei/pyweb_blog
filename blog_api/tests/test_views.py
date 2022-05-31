import unittest

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from blog.models import Note


class TestNoteListCreateAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test@test.ru")

    def test_list_objects(self):
        Note.objects.create(title="Test title", author_id=1)

        test_user = User.objects.get(username="test@test.ru")
        Note.objects.create(title="Test title", author=test_user)

        url = "/notes/"
        resp = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        response_data = resp.data
        self.assertEqual(2, len(response_data))

    def test_empty_list_objects(self):
        url = "/notes/"
        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        response_data = resp.data
        expected_data = []
        self.assertEqual(expected_data, response_data)

    @unittest.skip("Еще не реализовано")
    def test_create_objects(self):
        new_title = "test_title"
        data = {
            "title": new_title
        }
        url = "/notes/"
        resp = self.client.post(url)
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)

        Note.objects.get(title=new_title)  # self.assertTrue(Note.objects.exists(title=new_title))


class TestNoteDetailAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test@test.ru")
        Note.objects.create(title="Test title", author_id=1)

    def test_retrieve_object(self):
        note_pk = 1
        url = f"/notes/{note_pk}"

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        expected_data = {
            "id": 1,
            "title": "Test title",
            "message": "",
            "public": False
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_does_not_exists_object(self):
        does_not_exist_pk = "12312341241234"
        url = f"/notes/{does_not_exist_pk}"

        resp = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, resp.status_code)

    def test_update_object(self):
        ...

    def test_partial_update_object(self):
        ...


class NoteDetailAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create(username="test_username_1", password="fake_password")
        user_2 = User.objects.create(username="test_username_2", password="fake_password")

        cls.token_user_1 = Token.objects.create(user=user_1)
        cls.token_user_2 = Token.objects.create(user=user_2)

        note = Note.objects.create(title="private_user_1_title", public=False)
        user_1.note_set.add(note)
        note = Note.objects.create(title="public_user_1_title", public=True)
        user_1.note_set.add(note)

        note = Note.objects.create(title="private_user_2_title", public=False)
        user_2.note_set.add(note)
        note = Note.objects.create(title="public_user_2_title", public=True)
        user_2.note_set.add(note)

        cls.user_1 = user_1
        cls.user_2 = user_2

    def setUp(self) -> None:
        """Перед каждым тестом логиниться"""
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)

    def test_patch_update(self):
          # пользователь залогинен
        other_user_note_pk = 3
        url = f"/notes/{other_user_note_pk}/"

        resp = self.client.put(url, data={"title":"new_title"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
