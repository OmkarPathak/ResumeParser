from sentence_transformers import SentenceTransformer

def download_models():
    print("Downloading Sentence Transformer model...")
    # This will cache the model in ~/.cache/torch/sentence_transformers
    SentenceTransformer('all-MiniLM-L6-v2')
    print("Models downloaded successfully.")

if __name__ == "__main__":
    download_models()
