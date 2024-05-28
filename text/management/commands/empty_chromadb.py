# myapp/management/commands/empty_chromadb.py

from django.core.management.base import BaseCommand, CommandError
from chromadb.config import Settings
import chromadb
from WriteStackAI import settings

class Command(BaseCommand):
    help = 'Empties the specified ChromaDB collections'

    def handle(self, *args, **options):
        try:
            client = chromadb.PersistentClient(path=settings.CHRMADB_PERSIST_DIR)
            collections = ["title_embeddings", "content_embeddings"]

            for collection_name in collections:
                client.delete_collection(name=collection_name)

        except Exception as e:
            raise CommandError(f'Error emptying ChromaDB collections: {e}')

        self.stdout.write(self.style.SUCCESS('Successfully emptied all specified ChromaDB collections'))
