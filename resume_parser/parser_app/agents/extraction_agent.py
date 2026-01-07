import json
from .base_agent import BaseAgent

class ExtractionAgent(BaseAgent):
    def extract_entities(self, text):
        """
        Extracts structured entities (Name, Email, Skills, etc.) from the text.
        """
        system_prompt = (
            "You are an expert Data Extractor. "
            "Your job is to extract factual details from resumes into strict JSON format. "
            "Do not invent information. If a field is missing, leave it as null or empty string."
        )
        
        # Truncate to ensure safety
        truncated_text = text[:3000] 
        
        user_prompt = f"""
        Extract the following fields from the resume text below:
        
        - name (string)
        - email (string)
        - mobile_number (string)
        - skills (comma-separated string)
        - education (string: Degree, College, Year)
        - college_name (string: Just the university/college name)
        - designation (string: Current or last job title)
        - experience (string summary of work history)
        - total_experience (string, e.g. "5 years")
        - company_names (comma-separated string of companies worked at)
        
        Output valid JSON only.
        
        Resume Text:
        {truncated_text}
        """
        
        response_content = self.inference(system_prompt, user_prompt, max_tokens=1000, response_format={"type": "json_object"})
        
        if response_content:
            try:
                return json.loads(response_content)
            except json.JSONDecodeError:
                print("ExtractionAgent: Failed to decode JSON")
                return {}
        return {}
