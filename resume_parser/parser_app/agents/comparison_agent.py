import json
from .base_agent import BaseAgent

class ComparisonAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def compare_candidates(self, candidates_data):
        """
        Analyzes a list of candidates and generates a comparative analysis.
        
        Args:
            candidates_data (list): List of dicts, each containing 'name', 'skills', 'experience', 'summary'.
            
        Returns:
            dict: JSON object with comparison matrix and verdict.
        """
        if not candidates_data:
            return {"error": "No candidates provided"}

        # Prepare the input for the LLM
        candidates_text = ""
        for i, cand in enumerate(candidates_data):
            candidates_text += f"""
            Candidate {i+1}: {cand.get('name')}
            Skills: {cand.get('skills')}
            Experience: {cand.get('experience')}
            Education: {cand.get('education')}
            Summary: {cand.get('ai_summary')}
            -----------------------------------
            """

        system_prompt = """
        You are an Expert HR Recruiter and Talent Analyst. 
        Your task is to compare the provided candidates side-by-side and provide a structured decision matrix.
        
        Analyze them based on:
        1. Key Strengths (Technical & Soft skills)
        2. Experience Depth
        3. Potential Red Flags or Weaknesses
        4. Best Fit Role Recommendation
        
        Output MUST be in strict JSON format with the following structure:
        {
            "candidates": [
                {
                    "name": "Candidate Name",
                    "strengths": ["Strength 1", "Strength 2"],
                    "weaknesses": ["Weakness 1", "Weakness 2"],
                    "rating": 8.7, // Precise score out of 10. Avoid ties.
                    "verdict": "Brief 1-sentence assessment"
                }
            ],
            "winner": "Name of the best candidate",
            "reasoning": "Why this candidate is the best choice."
        }

        IMPORTANT SCORING RULES:
        1. DO NOT give identical scores (e.g. both 8.5/10). DIFFERENTIATE based on nuance.
        2. Use decimals (e.g. 8.2, 8.7) to create separation.
        3. Be critical. An average candidate is 6.0, good is 7.5, excellent is 9.0.
        4. If candidates are very similar, force a 0.1 difference based on specific skills or experience depth.
        """

        user_prompt = f"""
        Here are the candidates to compare:
        {candidates_text}
        
        Provide the comparative analysis in JSON format.
        """

        try:
            response = self.inference(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format={"type": "json_object"},
                temperature=0.4 # Lower temperature for more analytical consistency
            )
            
            if response:
                result = json.loads(response)
                
                # Post-processing: Enforce tie-breaking
                try:
                    candidates = result.get('candidates', [])
                    winner_name = result.get('winner', '')
                    
                    if len(candidates) >= 2:
                        # Find the winner object
                        winner_obj = next((c for c in candidates if c['name'] == winner_name), None)
                        
                        # Find the highest rating among non-winners
                        others = [c for c in candidates if c['name'] != winner_name]
                        if winner_obj and others:
                            max_other_rating = max(c.get('rating', 0) for c in others)
                            
                            # If winner is tied or lower (unlikely but possible), boost winner
                            if winner_obj.get('rating', 0) <= max_other_rating:
                                winner_obj['rating'] = round(max_other_rating + 0.1, 1)
                                # Cap at 9.9
                                if winner_obj['rating'] > 9.9:
                                    winner_obj['rating'] = 9.9
                                    # Drop others if needed
                                    for o in others:
                                        if o['rating'] >= 9.9:
                                            o['rating'] = 9.8
                except Exception as e:
                    print(f"Tie-breaking error: {e}")

                return result
            return {"error": "Failed to generate comparison"}
            
        except Exception as e:
            print(f"Comparison Agent Error: {e}")
            return {"error": str(e)}
