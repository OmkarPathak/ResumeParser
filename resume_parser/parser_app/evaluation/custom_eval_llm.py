from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_google_genai import ChatGoogleGenerativeAI

class CustomGeminiLLM(DeepEvalBaseLLM):
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", # Or gemini-pro, gemini-1.5-flash
            temperature=0,
        )

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        res = self.model.invoke(prompt)
        return res.content

    async def a_generate(self, prompt: str) -> str:
        res = await self.model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return "Gemini 1.5 Pro"
