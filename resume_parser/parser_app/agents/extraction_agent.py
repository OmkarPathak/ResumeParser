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
        
        # Balanced truncation for 4k context (4000 chars covers most resumes)
        truncated_text = text[:4000] 
        
        user_prompt = f"""
        Analyze the resume text and extract structured information into JSON.
        
        Fields:
        - name, email, mobile_number: strings
        - skills, company_names: comma-separated strings
        - education, designation, total_experience: strings
        - ai_summary: 3 sentence professional summary
        - ai_strengths: list of 3-5 strings
        - experiences (list of objects):
            - designation, company, start_date, end_date: strings
            - job_description: bullet points of achievements

        RULES for 'experiences':
        1. Only include professional roles (Jobs, Internships). 
        2. DO NOT include standalone Projects, Skill headers, or Certifications as a 'job'.
        3. If a section looks like a "Project" section, ignore it for the 'experiences' list.
        4. Capture the full Job Description. Do not summarize it into a single line; include key achievements.
        5. Sort by date, most recent first.
        
        Output valid JSON only.
        
        Resume Text:
        {truncated_text}
        """
        
        response_content = self.inference(system_prompt, user_prompt, max_tokens=1500, response_format={"type": "json_object"}, temperature=0.0)
        
        if response_content:
            try:
                return json.loads(response_content)
            except json.JSONDecodeError as e:
                print(f"ExtractionAgent: Failed to decode JSON. Error: {e}")
                print(f"RAW CONTENT: {repr(response_content)}")
                return {}
        return {}
