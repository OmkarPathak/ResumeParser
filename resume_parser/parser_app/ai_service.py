from .agents.orchestrator import Orchestrator

# Standard interface kept for views.py compatibility
def get_resume_insights(resume_text):
    """
    Entry point for the Agentic AI Resume Parser.
    Delegates the task to the Orchestrator, which manages the specific agents.
    """
    try:
        # Initialize Orchestrator (Lazy loading handled by BaseAgent)
        orchestrator = Orchestrator()
        
        # Start the Agentic Workflow
        result = orchestrator.process_resume(resume_text)
        return result
        
    except Exception as e:
        print(f"Error in Agentic Workflow: {e}")
        return None
