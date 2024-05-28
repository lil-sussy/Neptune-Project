from .chroma_singleton import ChromaClientSingleton
import random
import string
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

def generate_random_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

def print_blue(message):
    print(f"\033[94m{message}\033[0m")

def test_save_document(client, url, sample_data):    print_blue("Starting test_save_document")
    response = client.post(url, sample_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED, f"Expected 201, got {response.status_code}"
    response_data = json.loads(response.content)
    assert 'message' in response_data, "'message' not in response_data"
    assert 'title_id' in response_data, "'title_id' not in response_data"
    assert 'content_id' in response_data, "'content_id' not in response_data"
    title_id = response_data['title_id']
    content_id = response_data['content_id']
    print_blue(f"Document saved with title_id: {title_id}, content_id: {content_id}")
    return title_id, content_id

def test_edit_document(client, url_template, content_id, updated_data):
    print_blue("Starting test_edit_document")
    edit_url = reverse(url_template, args=[content_id])
    response = client.post(edit_url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK, f"Expected 200, got {response.status_code}"
    response_data = json.loads(response.content)
    assert 'message' in response_data, "'message' not in response_data"
    print_blue(f"Document with content_id: {content_id} updated successfully")

def test_delete_document(client, url_template, content_id):
    print_blue("Starting test_delete_document")
    delete_url = reverse(url_template, args=[content_id])
    response = client.delete(delete_url)
    assert response.status_code == status.HTTP_200_OK, f"Expected 200, got {response.status_code}"
    response_data = json.loads(response.content)
    assert 'message' in response_data, "'message' not in response_data"
    print_blue(f"Document with content_id: {content_id} deleted successfully")

def test_get_document(client, url_template, content_id):
    print_blue("Starting test_get_document")
    get_url = reverse(url_template, args=[content_id])
    response = client.get(get_url)
    assert response.status_code == status.HTTP_200_OK, f"Expected 200, got {response.status_code}"
    response_data = json.loads(response.content)
    assert 'document' in response_data, "'document' not in response_data"
    assert 'metadata' in response_data, "'metadata' not in response_data"
    print_blue(f"Document with content_id: {content_id} retrieved successfully")

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

    def test_document_lifecycle(self):
        title_id, content_id = test_save_document(self.client, self.save_url, self.sample_data)
        test_get_document(self.client, self.get_url_template, content_id)
        test_edit_document(self.client, self.edit_url_template, content_id, self.updated_data)
        test_delete_document(self.client, self.delete_url_template, content_id)

        test_get_document(self.client, self.get_url_template, title_id)
        test_edit_document(self.client, self.edit_url_template, title_id, self.updated_data)
        test_delete_document(self.client, self.delete_url_template, title_id)
