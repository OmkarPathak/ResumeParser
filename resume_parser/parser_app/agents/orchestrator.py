from .extraction_agent import ExtractionAgent
from .summary_agent import SummaryAgent

class Orchestrator:
    def __init__(self):
        self.extractor = ExtractionAgent()
        self.summarizer = SummaryAgent()

    def process_resume(self, text):
        """
        Orchestrates the resume parsing process by delegating to specialized agents.
        """
        print("Orchestrator: Starting Agentic Workflow...")
        
        # Step 1: Extract Entities
        print("Orchestrator: Delegating to ExtractionAgent...")
        entity_data = self.extractor.extract_entities(text)
        
        # Step 2: Generate Insights
        print("Orchestrator: Delegating to SummaryAgent...")
        summary_data = self.summarizer.generate_summary(text)
        
        # Step 3: Merge Results
        final_data = {**entity_data, **summary_data}
        
        print(f"Orchestrator: Workflow complete. Extracted {len(final_data)} fields.")
        return final_data
