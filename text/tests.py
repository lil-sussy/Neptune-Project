# tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from .chroma_singleton import ChromaClientSingleton
import json

class DocumentTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chromadb_client = ChromaClientSingleton.get_instance()

    def setUp(self):
        self.save_url = reverse('save_document')
        self.edit_url_template = 'edit_document'
        self.delete_url_template = 'delete_document'
        self.get_url_template = 'get_document'
        
        self.sample_data = {
            "title": "Sample Title",
            "content": "This is a sample content.",
            "tags": ["test", "sample"]
        }
        
        self.updated_data = {
            "title": "Updated Title",
            "content": "This is updated content.",
            "tags": ["update", "sample"]
        }

    def test_save_document(self):
        response = self.client.post(self.save_url, self.sample_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.assertIn('message', response_data)

    def test_edit_document(self):
        self.client.post(self.save_url, self.sample_data, format='json')
        document_id = f"content_Sample Title_{timezone.now().isoformat()}"
        edit_url = reverse(self.edit_url_template, args=[document_id])
        response = self.client.post(edit_url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertIn('message', response_data)

    def test_delete_document(self):
        self.client.post(self.save_url, self.sample_data, format='json')
        document_id = f"content_Sample Title_{timezone.now().isoformat()}"
        delete_url = reverse(self.delete_url_template, args=[document_id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertIn('message', response_data)

    def test_get_document(self):
        self.client.post(self.save_url, self.sample_data, format='json')
        document_id = f"content_Sample Title_{timezone.now().isoformat()}"
        get_url = reverse(self.get_url_template, args=[document_id])
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertIn('document', response_data)
        self.assertIn('metadata', response_data)
