import os
from huggingface_hub import hf_hub_download

def download_model(model_name="qwen"):
    models = {
        "phi3": {
            "repo_id": "microsoft/Phi-3-mini-4k-instruct-gguf",
            "filename": "Phi-3-mini-4k-instruct-q4.gguf"
        },
        "qwen": {
            "repo_id": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
            "filename": "qwen2.5-1.5b-instruct-q4_k_m.gguf"
        }
    }
    
    selected = models.get(model_name, models["qwen"])
    repo_id = selected["repo_id"]
    filename = selected["filename"]
    
    # Path relative to the script
    model_dir = os.path.join(os.getcwd(), "resume_parser", "models")
    model_path = os.path.join(model_dir, filename)
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    if not os.path.exists(model_path):
        print(f"Downloading {filename} from {repo_id}...")
        try:
            hf_hub_download(
                repo_id=repo_id, 
                filename=filename, 
                local_dir=model_dir, 
                local_dir_use_symlinks=False
            )
            print("Download complete!")
        except Exception as e:
            print(f"Error downloading model: {e}")
    else:
        print(f"Model already exists at {model_path}")

if __name__ == "__main__":
    import sys
    # Default to Qwen for benchmarking speed
    model_choice = sys.argv[1] if len(sys.argv) > 1 else "qwen"
    download_model(model_choice)
