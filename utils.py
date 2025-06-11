import unicodedata
import re
import json
from langchain.schema import AIMessage


def parse_llm_output(ai_msg):
    """
    Parses the output from the LLM to extract JSON data.
    """
    # Extracting JSON from the message content
    # This regex looks for a JSON object enclosed in triple backticks
    # and captures it for further processing

    match = re.search(r"```json\s*(\{.*?\})\s*```", ai_msg, re.DOTALL)
    if match:
        json_str = match.group(1)
        parsed = json.loads(json_str)
        return parsed
    else:
        print("No valid JSON found.")


def normalize_text(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip().lower()
