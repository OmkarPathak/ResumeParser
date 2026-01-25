import json
from .base_agent import BaseAgent

class OptimizationAgent(BaseAgent):
    def optimize_resume(self, resume_text, job_description):
        """
        Analyzes a resume against a job description and provides optimization suggestions.
        """
        system_prompt = (
            "You are a Senior Career Coach and Expert Technical Recruiter. "
            "Your job is to help candidates optimize their resumes to better match a specific Job Description (JD). "
            "You provide actionable, specific advice on what to add, modify, or highlight."
        )
        
        # Reduced truncation for faster processing while maintaining context
        truncated_resume = resume_text[:2500]
        truncated_jd = job_description[:1500]
        
        user_prompt = f"""
        Critical Task: Perform a rigorous, objective comparison between the candidate's Resume and the Job Description (JD).
        
        Scoring Rubric (Strict):
        1. Required Technical Skills (60%): Compare every keyword in JD to Resume.
        2. Years & Depth of Experience (30%): seniority level match.
        3. Education & Certs (10%): Degree alignment.
        
        Output valid JSON with the following structure:
        {{
            "match_score": (integer 0-100),
            "score_reasoning": "A one-sentence justification.",
            "strengths": ["exactly matching credentials"],
            "gaps": ["required skills NOT found"],
            "suggestions": ["prioritized modifications"],
            "action_items": ["3-5 immediate steps"]
        }}
        
        Resume Text:
        {truncated_resume}
        
        Job Description:
        {truncated_jd}
        """
        
        # Reduced max_tokens to 800 for faster generation
        response_content = self.inference(system_prompt, user_prompt, max_tokens=800, response_format={"type": "json_object"}, temperature=0.2)
        
        if response_content:
            try:
                return json.loads(response_content)
            except json.JSONDecodeError:
                print("OptimizationAgent: Failed to decode JSON")
                return {
                    "match_score": "N/A",
                    "strengths": [],
                    "gaps": ["Error processing AI response."],
                    "suggestions": [],
                    "action_items": []
                }
        return {
            "match_score": "N/A",
            "strengths": [],
            "gaps": ["AI agent did not return a response."],
            "suggestions": [],
            "action_items": []
        }
