import json
from .base_agent import BaseAgent
from .vector_store import VectorStore

class RAGAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.vector_store = VectorStore()

    def chat(self, user_query):
        # 1. Retrieve Context
        results = self.vector_store.search(user_query, top_k=3)
        
        context_str = ""
        if results:
            context_str += "Here are the most relevant candidates from the database:\n\n"
            for i, res in enumerate(results, 1):
                context_str += f"Name: {res.get('name', 'Unknown')}\n"
                context_str += f"Link: {res.get('file_url', '#')}\n"
                context_str += f"Skills: {res.get('skills', 'N/A')}\n"
                context_str += f"Summary: {res.get('ai_summary', 'N/A')}\n"
                context_str += "---\n"
        else:
            context_str = "No relevant resumes found."

        # 2. Construct Prompt
        system_prompt = (
            "You are a helpful Recruitment Assistant. "
            "Answer the user's question based on the list of candidates provided below. "
            "When you mention a candidate's name, you must format it as a link using their Link URL. "
            "Format: [Name](Link). "
            "Keep your answer concise and helpful."
        )

        user_prompt = f"""
        List of Candidates:
        {context_str}

        Question: {user_query}
        
        Answer:
        """

        # 3. Generate Answer
        print("RAGAgent: Generating response...")
        return self.inference(system_prompt, user_prompt, max_tokens=600)
