import json
from .base_agent import BaseAgent

class SummaryAgent(BaseAgent):
    def generate_summary(self, text):
        """
        Generates a professional summary and identifies key strengths.
        """
        system_prompt = (
            "You are a Senior HR Consultant. "
            "Your job is to read a resume and write a compelling Professional Summary and identify Key Strengths. "
            "Write in a professional, third-person tone."
        )
        
        # Truncate
        truncated_text = text[:3000]
        
        user_prompt = f"""
        Analyze the following resume and generate:
        1. "ai_summary": A 3-4 sentence professional summary highlighting their main expertise.
        2. "ai_strengths": A list of 3-5 key strengths or soft skills.
        
        Output valid JSON only.
        
        Resume Text:
        {truncated_text}
        """
        
        response_content = self.inference(system_prompt, user_prompt, max_tokens=800, response_format={"type": "json_object"})
        
        if response_content:
            try:
                data = json.loads(response_content)
                # Ensure keys exist
                return {
                    "ai_summary": data.get("ai_summary", "Summary not generated."),
                    "ai_strengths": data.get("ai_strengths", "Strengths not generated.")
                }
            except json.JSONDecodeError:
                print("SummaryAgent: Failed to decode JSON")
                return {}
        return {}
