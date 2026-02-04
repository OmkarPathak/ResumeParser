import json
from .base_agent import BaseAgent
from .vector_store import VectorStore

class RAGAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.vector_store = VectorStore()

    def chat(self, user_query, history=None, user_id=None, return_context=False):
        if history is None:
            history = []

        # 1. Retrieve Context
        results = self.vector_store.search(user_query, top_k=3, user_id=user_id)
        
        context_str = ""
        context_list = [] # For evaluation
        if results:
            context_str += "Here are the most relevant candidates from the database:\n\n"
            for i, res in enumerate(results, 1):
                # Construct clean context string for LLM
                c_text = f"Name: {res.get('name', 'Unknown')}\n"
                c_text += f"Link: {res.get('file_url', '#')}\n"
                c_text += f"Skills: {res.get('skills', 'N/A')}\n"
                c_text += f"Summary: {res.get('ai_summary', 'N/A')}\n"
                context_str += c_text + "---\n"
                
                # Keep raw context for eval
                context_list.append(c_text)
        else:
            context_str = "No relevant resumes found."

        # Format history
        history_str = ""
        if history:
            history_str = "Chat History:\n"
            for turn in history:
                role = turn.get('role', 'User')
                content = turn.get('content', '')
                history_str += f"{role}: {content}\n"
            history_str += "\n"

        # 2. Construct Prompt
        system_prompt = (
            "You are a helpful Recruitment Assistant. "
            "1. Answer the user's question based ONLY on the provided 'List of Candidates'.\n"
            "2. If the candidate is not in the list, do NOT invent one.\n"
            "3. When you mention a candidate, you MUST format it as a link: `[Name](Link)`.\n"
            "4. Use the 'Link' provided in the context.\n"
            "5. Example Output: 'I recommend **[Name](Link)** because...' \n"
            "6. Explain your reasoning briefly."
        )

        user_prompt = f"""
        {history_str}
        
        List of Candidates:
        {context_str}

        Question: {user_query}
        
        Answer:
        """

        # 3. Generate Answer
        print("RAGAgent: Generating response...")
        answer = self.inference(system_prompt, user_prompt, max_tokens=600)
        
        if return_context:
            return answer, context_list
            
        return answer
