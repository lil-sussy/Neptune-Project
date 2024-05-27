from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
import chromadb
from chromadb.config import Settings
import json
from WriteStackAI import settings

# Helper function to get ChromaDB client
def get_chromadb_client():
    return chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=settings.CHRMADB_PERSIST_DIR))

class DocumentTests(APITestCase):

    def setUp(self):
        # Set up initial data
        self.client = get_chromadb_client()
        self.collections = ["title_embeddings", "content_embeddings"]
        for collection_name in self.collections:
            self.client.get_or_create_collection(name=collection_name)

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
        url = reverse('save_document')
        response = self.client.post(url, self.sample_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for collection_name in self.collections:
            collection = self.client.get_or_create_collection(name=collection_name)
            results = collection.query(query_texts=["Sample"], n_results=1)
            self.assertGreater(len(results['documents']), 0)

    def test_edit_document(self):
        # First, save a document
        save_url = reverse('save_document')
        self.client.post(save_url, self.sample_data, format='json')

        # Then, edit the document
        edit_url = reverse('edit_document', args=['content_Sample Title_' + timezone.now().isoformat()])
        response = self.client.post(edit_url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for collection_name in self.collections:
            collection = self.client.get_or_create_collection(name=collection_name)
            results = collection.query(query_texts=["Updated"], n_results=1)
            self.assertGreater(len(results['documents']), 0)

    def test_delete_document(self):
        # First, save a document
        save_url = reverse('save_document')
        self.client.post(save_url, self.sample_data, format='json')

        # Then, delete the document
        delete_url = reverse('delete_document', args=['content_Sample Title_' + timezone.now().isoformat()])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for collection_name in self.collections:
            collection = self.client.get_or_create_collection(name=collection_name)
            results = collection.query(query_texts=["Sample"], n_results=1)
            self.assertEqual(len(results['documents']), 0)

    def test_get_document(self):
        # First, save a document
        save_url = reverse('save_document')
        self.client.post(save_url, self.sample_data, format='json')

        # Then, retrieve the document
        get_url = reverse('get_document', args=['content_Sample Title_' + timezone.now().isoformat()])
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('document', response.data)
        self.assertIn('metadata', response.data)
