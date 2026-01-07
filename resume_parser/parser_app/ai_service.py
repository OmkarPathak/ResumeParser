import os
import json
from django.conf import settings

# Global variable to hold the model instance (Lazy Loading)
LLM_MODEL = None

def get_llm_model():
    global LLM_MODEL
    if LLM_MODEL is None:
        try:
            from llama_cpp import Llama
            # Switching to Qwen2.5-1.5B (Faster & Lighter)
            model_path = os.path.join(settings.BASE_DIR, 'models', 'qwen2.5-1.5b-instruct-q4_k_m.gguf')
            
            if not os.path.exists(model_path):
                print(f"AI Model not found at {model_path}")
                return None
                
            print(f"Loading AI Model: {os.path.basename(model_path)}...")
            
            # Qwen 1.5B is light, but your Mac has strict GPU timeouts.
            # Running on CPU (n_gpu_layers=0) for 100% stability.
            # Since it's a small model (1.5B), it will still be reasonably fast on CPU.
            LLM_MODEL = Llama(
                model_path=model_path,
                n_ctx=2048, 
                n_gpu_layers=0, # Force CPU for stability
                verbose=True 
            )
            print("AI Model Loaded Successfully")
        except Exception as e:
            print(f"Error loading AI Model: {e}")
            return None
    return LLM_MODEL

def get_resume_insights(resume_text):
    """
    Generates a summary and strengths for the given resume text.
    """
    llm = get_llm_model()
    if not llm:
        return None

    # Truncate text to ensure it fits in context (2048 tokens matches approx 6000-8000 chars, but we keep it safe)
    # Reducing to 1500 chars to be safe (approx 400-500 tokens) + system prompt + output
    truncated_text = resume_text[:1500]

    system_prompt = "You are an expert HR Recruiter and Resume Parser. Extract all details from the resume into a valid JSON format."
    user_prompt = f"""
    Analyze the following resume text and extract these details in JSON format:
    - name (string)
    - email (string)
    - mobile_number (string)
    - skills (comma-separated string)
    - education (string)
    - college_name (string)
    - designation (string)
    - experience (string summary)
    - total_experience (string, e.g. "5 years")
    - company_names (string, comma-separated)
    - ai_summary (short professional summary)
    - ai_strengths (key strengths)
    
    Resume Text:
    {truncated_text}
    """

    try:
        response = LLM_MODEL.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1000  # Optimized for performance
        )
        
        content = response['choices'][0]['message']['content']
        return json.loads(content)
    except Exception as e:
        print(f"Error generating insights: {e}")
        return None
