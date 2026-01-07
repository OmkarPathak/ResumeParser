from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Resume
from .agents.vector_store import VectorStore

@receiver(post_delete, sender=Resume)
def remove_from_vector_store(sender, instance, **kwargs):
    """
    Automatically removes the resume from the Vector Search Index when deleted from DB.
    """
    try:
        VectorStore().remove_document(instance.id)
        print(f"Signal: Removed Resume ID {instance.id} from Vector Index.")
    except Exception as e:
        print(f"Signal Error: Could not remove from index: {e}")
