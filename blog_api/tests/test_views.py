import unittest

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

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
