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
            "1. Answer the user's question with a complete sentence.\n"
            "2. When you mention a candidate, you MUST format it as a link: `[Name](Link)`.\n"
            "3. Use the 'Link' provided in the context (it starts with /media).\n"
            "4. Example Output: 'I recommend **[John Doe](/media/resume.pdf)** because he has Python skills.'\n"
            "5. Do NOT output just a name. Explain why."
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
