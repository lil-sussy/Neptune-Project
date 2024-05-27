# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DocumentSerializer
from datetime import datetime
import requests
import logging
import colorlog
from django.conf import settings
from .chroma_singleton import ChromaClientSingleton  # Singleton Chroma client
from dotenv import load_dotenv
import os
import json

# ANSI escape sequences
WHITE = "\033[97m"
BLUE = "\033[94m"
ITALIC = "\033[3m"
RESET = "\033[0m"

# Configure logging with colorlog
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'bold_blue',
        'INFO': 'bold_green',
        'WARNING': 'bold_yellow',
        'ERROR': 'bold_red',
        'CRITICAL': 'bold_red,bg_white',
    }
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.propagate = False

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def get_embeddings_openai(texts):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    url = "https://api.openai.com/v1/embeddings"
    payload = {
        "input": texts,
        "model": "text-embedding-3-small"
    }
    try:
        logger.info(f"{WHITE}Requesting embeddings for texts: {BLUE}{ITALIC}{texts}{RESET}")
        return requests.post(url, headers=headers, json=payload).json()['data'][0]['embedding']
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching embeddings from OpenAI: {e}")
        return None

class SaveDocumentView(APIView):
    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            title = data['title']
            content = data['content']
            tags = data['tags']
            timestamp = datetime.now().isoformat()

            client = ChromaClientSingleton.get_instance()

            # Collection 1: Embedding from Title
            collection1 = client.get_or_create_collection(name="title_embeddings")
            collection1.add(
                embeddings=[get_embeddings_openai(title)],
                documents=[title],
                metadatas=[{
                    "title": title,
                    "add_date": timestamp,
                    "last_edit": timestamp,
                    "previous_version_text": content,
                    "previous_version_title": title,
                    "tags": json.dumps(tags)
                }],
                ids=[f"title_{title}_{timestamp}"]
            )

            # Collection 2: Embedding from Content
            collection2 = client.get_or_create_collection(name="content_embeddings")
            collection2.add(
                embeddings=[get_embeddings_openai(content)],
                documents=[content],
                metadatas=[{
                    "title": title,
                    "add_date": timestamp,
                    "last_edit": timestamp,
                    "previous_version_text": content,
                    "previous_version_title": title,
                    "tags": json.dumps(tags)
                }],
                ids=[f"content_{title}_{timestamp}"]
            )

            return Response({"message": "Document saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditDocumentView(APIView):
    def post(self, request, id):
        data = request.data
        title = data.get('title')
        content = data.get('content')
        tags = data.get('tags')
        timestamp = datetime.now().isoformat()
        
        client = ChromaClientSingleton.get_instance()
        collections = ["title_embeddings", "content_embeddings"]
        
        for collection_name in collections:
            collection = client.get_or_create_collection(name=collection_name)
            collection.update(
                ids=[id],
                documents=[content if collection_name == "content_embeddings" else title],
                metadatas=[{
                    "title": title,
                    "add_date": timestamp,
                    "last_edit": timestamp,
                    "previous_version_text": content,
                    "previous_version_title": title,
                    "tags": json.dumps(tags)
                }]
            )
        
        return Response({"message": "Document updated successfully"}, status=status.HTTP_200_OK)

class DeleteDocumentView(APIView):
    def delete(self, request, id):
        client = ChromaClientSingleton.get_instance()
        collections = ["title_embeddings", "content_embeddings"]
        
        for collection_name in collections:
            collection = client.get_or_create_collection(name=collection_name)
            collection.delete(ids=[id])
        
        return Response({"message": "Document deleted successfully"}, status=status.HTTP_200_OK)

class GetDocumentView(APIView):
    def get(self, request, id):
        client = ChromaClientSingleton.get_instance()
        collection = client.get_or_create_collection(name="content_embeddings")  # Or the appropriate collection
        result = collection.get(ids=[id])
        
        if not result['documents']:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        
        document_data = result['documents'][0]
        metadata = result['metadatas'][0]
        
        response_data = {
            "document": document_data,
            "metadata": json.loads(metadata)
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
