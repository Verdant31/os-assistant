import os
from langchain_ollama import ChatOllama
from utils import parse_llm_output


class Chat():
    def __init__(self, model_name: str = "gemma3", temperature: float = 0.0):
        llm = ChatOllama(
            model=model_name,
            temperature=temperature,
        )
        self.prompts = self.load_prompts()
        self.llm = llm

    def map_prompt_scripts(self, prompt: str):
        messages = [
            (
                "system",
                self.prompts["map_scripts.md"]
            ),
            ("human", prompt),
        ]
        return parse_llm_output(self.llm.invoke(messages).content)

    def rewrite_prompt(self, prompt: str):
        messages = [
            (
                "system",
                self.prompts["rewrite_prompt.md"]
            ),
            ("human", prompt),
        ]
        return self.llm.invoke(messages).content

    def load_prompts(self):
        dir = "./prompts"
        prompts = {}
        for filename in os.listdir(dir):
            if filename.endswith(".md"):
                with open(os.path.join(dir, filename), 'r', encoding='utf-8') as f:
                    prompts[filename] = f.read()
        return prompts
