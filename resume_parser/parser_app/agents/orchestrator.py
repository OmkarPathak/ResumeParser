from .extraction_agent import ExtractionAgent

class Orchestrator:
    def __init__(self):
        self.extractor = ExtractionAgent()

    def process_resume(self, text):
        """
        Orchestrates the resume parsing process by delegating to specialized agents.
        Consolidated into a single agent call for performance (approx. 50% speed increase).
        """
        print("Orchestrator: Starting Consolidated Agentic Workflow...")
        
        # Consolidation: Combined Entity Extraction + Summary + Strengths
        print("Orchestrator: Delegating to ExtractionAgent ...")
        final_data = self.extractor.extract_entities(text)
        
        print(f"Orchestrator: Workflow complete. Extracted {len(final_data)} fields.")
        return final_data
