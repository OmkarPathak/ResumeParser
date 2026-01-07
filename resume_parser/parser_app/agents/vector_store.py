import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings

class VectorStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.index = [] # List of {vector, metadata}
            cls._instance.index_path = os.path.join(settings.BASE_DIR, 'resume_parser', 'vector_index.pkl')
            cls._instance.model_name = 'all-MiniLM-L6-v2'
            cls._instance.load_index()
        return cls._instance

    def load_model(self):
        if self.model is None:
            print(f"Loading Embedding Model: {self.model_name}...")
            self.model = SentenceTransformer(self.model_name)
            print("Embedding Model Loaded.")

    def add_document(self, text, metadata):
        self.load_model()
        vector = self.model.encode(text)
        self.index.append({
            'vector': vector,
            'metadata': metadata
        })
        self.save_index()

    def remove_document(self, doc_id):
        initial_count = len(self.index)
        self.index = [item for item in self.index if item['metadata'].get('id') != doc_id]
        if len(self.index) < initial_count:
            self.save_index()
            print(f"VectorStore: Removed document ID {doc_id}")

    def search(self, query, top_k=3):
        self.load_model()
        if not self.index:
            return []

        query_vector = self.model.encode(query)
        
        # Prepare vectors for matrix operation
        vectors = np.array([item['vector'] for item in self.index])
        
        # Calculate Cosine Similarity
        similarities = cosine_similarity([query_vector], vectors)[0]
        
        # Get Top K indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = similarities[idx]
            if score > 0.2: # Threshold to filter irrelevant results
                result = self.index[idx]['metadata']
                result['score'] = float(score)
                results.append(result)
        
        return results

    def save_index(self):
        with open(self.index_path, 'wb') as f:
            pickle.dump(self.index, f)

    def load_index(self):
        if os.path.exists(self.index_path):
            with open(self.index_path, 'rb') as f:
                self.index = pickle.load(f)
        else:
            self.index = []

    def clear_index(self):
        self.index = []
        self.save_index()
