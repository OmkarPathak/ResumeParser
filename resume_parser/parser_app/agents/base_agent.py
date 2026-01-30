import os
from django.conf import settings

# Global variable for Singleton Pattern
LLM_MODEL = None

class BaseAgent:
    def __init__(self):
        """
        Base Agent that manages the connection to the Local LLM.
        Uses Singleton pattern to avoid re-loading the model for every agent.
        """
        self.model = self._get_llm_model()

    def _get_llm_model(self):
        global LLM_MODEL
        if LLM_MODEL is None:
            try:
                from llama_cpp import Llama
                # Define model path
                model_dir = os.path.join(settings.BASE_DIR, 'models')
                model_path = os.path.join(model_dir, 'qwen2.5-1.5b-instruct-q4_k_m.gguf')
                
                # Check for existence
                if not os.path.exists(model_path):
                    print(f"Agent Warning: Primary model not found at {model_path}")
                    # Fallback check for Phi-3 just in case
                    fallback = os.path.join(model_dir, 'Phi-3-mini-4k-instruct-q4.gguf')
                    if os.path.exists(fallback):
                        print("Using fallback Phi-3 model.")
                        model_path = fallback
                    else:
                        print("No models found!")
                        return None

                print(f"Loading Base AI Model: {os.path.basename(model_path)}...")
                
                # Load Model
                # Qwen 1.5B is light enough for CPU or GPU
                # Using n_gpu_layers=0 for Max Stability on user's Mac as requested
                LLM_MODEL = Llama(
                    model_path=model_path,
                    n_ctx=4096, # Increased context for multi-agent flow
                    n_gpu_layers=0, 
                    verbose=False 
                )
                print("Base AI Model Loaded Successfully")
            except Exception as e:
                print(f"Error loading Base AI Model: {e}")
                return None
        return LLM_MODEL

    def inference(self, system_prompt, user_prompt, max_tokens=1000, response_format=None, temperature=0.7):
        """
        Common method to generate a response from the LLM.
        """
        if not self.model:
            return None

        try:
            kwargs = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if response_format:
                kwargs["response_format"] = response_format

            response = self.model.create_chat_completion(**kwargs)
            content = response['choices'][0]['message']['content']
            
            if response_format and response_format.get("type") == "json_object":
                return self._clean_json_response(content)
                
            return content
        except Exception as e:
            print(f"Agent Inference Error: {e}")
            return None

    def _clean_json_response(self, content):
        """
        Helper to strip markdown code blocks (```json ... ```) from the response.
        """
        clean_content = content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content[7:]
        if clean_content.startswith("```"):
            clean_content = clean_content[3:]
        if clean_content.endswith("```"):
            clean_content = clean_content[:-3]
        return clean_content.strip()
