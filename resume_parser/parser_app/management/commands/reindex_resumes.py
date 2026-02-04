from django.core.management.base import BaseCommand
from candidates.models import Candidate
from parser_app.agents.vector_store import VectorStore

class Command(BaseCommand):
    help = 'Re-indexes all candidates into the VectorStore for RAG'

    def handle(self, *args, **options):
        self.stdout.write("Starting indexing process...")
        
        vector_store = VectorStore()
        vector_store.clear_index() # Reset index
        
        # Use Candidate model instead of Resume
        candidates = Candidate.objects.all()
        count = candidates.count()
        
        self.stdout.write(f"Found {count} candidates to index.")
        
        for candidate in candidates:
            # Construct text for embedding
            text = f"{candidate.skills or ''} {candidate.experience_years or ''} years {candidate.ai_summary or ''}"
            
            # Metadata to store
            metadata = {
                'id': candidate.id,
                'name': candidate.name,
                'email': candidate.email,
                'skills': candidate.skills,
                'ai_summary': candidate.ai_summary,
                'file_url': candidate.resume_file.url if candidate.resume_file else '',
                'user_id': candidate.created_by.id if candidate.created_by else None
            }
            
            vector_store.add_document(text, metadata)
            self.stdout.write(f"Indexed: {candidate.name}")
            
        self.stdout.write(self.style.SUCCESS(f"Successfully indexed {count} candidates!"))
