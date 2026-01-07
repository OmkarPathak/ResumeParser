from django.core.management.base import BaseCommand
from parser_app.models import Resume
from parser_app.agents.vector_store import VectorStore

class Command(BaseCommand):
    help = 'Re-indexes all resumes into the VectorStore for RAG'

    def handle(self, *args, **options):
        self.stdout.write("Starting indexing process...")
        
        vector_store = VectorStore()
        vector_store.clear_index() # Reset index
        
        resumes = Resume.objects.all()
        count = resumes.count()
        
        self.stdout.write(f"Found {count} resumes to index.")
        
        for resume in resumes:
            # Construct text for embedding
            # We combine key fields to create a semantic representation
            text = f"{resume.skills or ''} {resume.experience or ''} {resume.ai_summary or ''}"
            
            # Metadata to store
            metadata = {
                'id': resume.id,
                'name': resume.name,
                'email': resume.email,
                'skills': resume.skills,
                'ai_summary': resume.ai_summary,
                'file_url': resume.resume.url if resume.resume else ''
            }
            
            vector_store.add_document(text, metadata)
            self.stdout.write(f"Indexed: {resume.name}")
            
        self.stdout.write(self.style.SUCCESS(f"Successfully indexed {count} resumes!"))
