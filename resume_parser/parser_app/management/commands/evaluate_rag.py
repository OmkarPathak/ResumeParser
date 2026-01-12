import os
import json
import re
import time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from parser_app.agents.rag_agent import RAGAgent
from parser_app.evaluation.simple_metrics import RAGEvaluator

class Command(BaseCommand):
    help = 'Evaluate RAG Agent using Gemini and Custom Metrics'

    def clean_json(self, text):
        # Extract JSON block if wrapped in markdown
        match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            return match.group(1)
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            return match.group(1)
        return text

    def handle(self, *args, **kwargs):
        # Setup API Key
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            try:
                import dotenv
                dotenv.load_dotenv()
                api_key = os.environ.get("GOOGLE_API_KEY")
            except ImportError:
                pass
        
        if not api_key:
            self.stdout.write(self.style.ERROR("Error: GOOGLE_API_KEY not found. Please set it in .env"))
            return

        # Get User
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("Error: No users found in database."))
            return
            
        self.stdout.write(self.style.SUCCESS(f"Initializing Evaluation with User: {user.username}..."))
        
        # Initialize
        evaluator = RAGEvaluator(api_key)
        agent = RAGAgent()
        
        queries = [
            "Who has experience with Python?",
            "Show me candidates with Machine Learning skills.",
            # "Tell me about the candidates.",
        ]
        
        self.stdout.write("Running Evaluation...\n")
        
        for query in queries:
            print(f"Query: {query}")
            try:
                # Add delay to avoid Rate Limits (Gemini Free Tier)
                if queries.index(query) > 0:
                    print("Waiting 10s to respect Rate Limits...")
                    time.sleep(10)

                actual_output, retrieval_context = agent.chat(query, return_context=True, user_id=user.id)
                context_text = "\n".join(retrieval_context)
                
                print(f"  > Answer: {actual_output[:100]}...")
                
                # 1. Faithfulness
                f_res = evaluator.evaluate_faithfulness(actual_output, context_text)
                f_json = json.loads(self.clean_json(f_res))
                print(f"  [Faithfulness]: Score {f_json.get('score')} - {f_json.get('reason')}")
                time.sleep(2) # Short pause between metrics
                
                # 2. Relevance
                r_res = evaluator.evaluate_relevance(query, actual_output)
                r_json = json.loads(self.clean_json(r_res))
                print(f"  [Relevance]   : Score {r_json.get('score')} - {r_json.get('reason')}")
                time.sleep(2)
                
                # 3. Bias
                b_res = evaluator.evaluate_bias(actual_output)
                b_json = json.loads(self.clean_json(b_res))
                print(f"  [Bias]        : Score {b_json.get('score')} - {b_json.get('reason')}")
                
                print("-" * 50)
                
            except Exception as e:
                print(f"Error processing query '{query}': {e}")
        
        self.stdout.write(self.style.SUCCESS("\nEvaluation Complete."))
