# views.py
import uuid
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
# Define the expected dimension of the embeddings
EXPECTED_DIMENSION = 1536  # Set this to the correct dimension based on your model


def get_embeddings_openai(texts):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    url = "https://api.openai.com/v1/embeddings"
    payload = {
        "input": texts,
        "model": "text-embedding-3-small"  # Ensure this model gives embeddings of expected dimension
    }
    try:
        logger.info(f"{WHITE}Requesting embeddings for texts: {BLUE}{ITALIC}{texts}{RESET}")
        response = requests.post(url, headers=headers, json=payload).json()
        embedding = response['data'][0]['embedding']

        # Validate embedding dimension
        if len(embedding) != EXPECTED_DIMENSION:
            raise ValueError(f"Embedding dimension {len(embedding)} does not match expected dimension {EXPECTED_DIMENSION}")

        return embedding
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching embeddings from OpenAI: {e}")
        return None
    except KeyError:
        logger.error("Error in response format: 'data' key not found")
        return None
    except ValueError as e:
        logger.error(f"Invalid embedding dimension: {e}")
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

            title_embedding = get_embeddings_openai(title)
            content_embedding = get_embeddings_openai(content)

            if title_embedding is None or content_embedding is None:
                return Response({"error": "Failed to generate embeddings"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            title_id = f"title_{uuid.uuid4()}"
            content_id = f"content_{uuid.uuid4()}"
            
            # Collection 1: Embedding from Title
            collection1 = client.get_or_create_collection(name="title_embeddings")
            collection1.add(
                embeddings=[title_embedding],
                documents=[title],
                metadatas=[{
                    "title": title,
                    "add_date": timestamp,
                    "last_edit": timestamp,
                    "previous_version_text": content,
                    "previous_version_title": title,
                    "tags": json.dumps(tags)
                }],
                ids=[title_id]
            )

            # Collection 2: Embedding from Content
            collection2 = client.get_or_create_collection(name="content_embeddings")
            collection2.add(
                embeddings=[content_embedding],
                documents=[content],
                metadatas=[{
                    "title": title,
                    "add_date": timestamp,
                    "last_edit": timestamp,
                    "previous_version_text": content,
                    "previous_version_title": title,
                    "tags": json.dumps(tags)
                }],
                ids=[content_id]
            )

            return Response({"message": "Document saved successfully", "title_id": title_id, "content_id": content_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

class EditDocumentView(APIView):
    def post(self, request, id):
        data = request.data
        title = data.get('title')
        content = data.get('content')
        tags = data.get('tags')
        timestamp = datetime.now().isoformat()

        client = ChromaClientSingleton.get_instance()

        title_embedding = get_embeddings_openai(title)
        content_embedding = get_embeddings_openai(content)

        if title_embedding is None or content_embedding is None:
            return Response({"error": "Failed to generate embeddings"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if id.startswith("title_"):
            collection_name = "title_embeddings"
            embedding = title_embedding
            document = title
        elif id.startswith("content_"):
            collection_name = "content_embeddings"
            embedding = content_embedding
            document = content
        else:
            return Response({"error": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)

        collection = client.get_or_create_collection(name=collection_name)
        collection.update(
            ids=[id],
            embeddings=[embedding],
            documents=[document],
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

        if id.startswith("title_"):
            collection_name = "title_embeddings"
        elif id.startswith("content_"):
            collection_name = "content_embeddings"
        else:
            return Response({"error": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)

        collection = client.get_or_create_collection(name=collection_name)
        collection.delete(ids=[id])

        return Response({"message": "Document deleted successfully"}, status=status.HTTP_200_OK)

class GetDocumentView(APIView):
    def get(self, request, id):
        client = ChromaClientSingleton.get_instance()

        if id.startswith("title_"):
            collection_name = "title_embeddings"
        elif id.startswith("content_"):
            collection_name = "content_embeddings"
        else:
            return Response({"error": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)

        collection = client.get_or_create_collection(name=collection_name)
        result = collection.get(ids=[id])

        if not result['documents']:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

        document_data = result['documents'][0]
        metadata = result['metadatas'][0]
        metadata['tags'] = json.loads(metadata['tags'])

        response_data = {
            "document": document_data,
            "metadata": metadata
        }

        return Response(response_data, status=status.HTTP_200_OK)