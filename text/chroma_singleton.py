# chroma_singleton.py
import chromadb
from chromadb.config import Settings
from django.conf import settings

class ChromaClientSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = chromadb.PersistentClient(path=settings.CHRMADB_PERSIST_DIR
            )
        return cls._instance
