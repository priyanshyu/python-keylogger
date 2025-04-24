# src/system/ai_service.py
import os
import json
from groq import Groq
from dotenv import load_dotenv
from prompts.system_prompt import SYSTEM_PROMPT_SUMMARY
# Load API key from .env file
load_dotenv()

class AIAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-70b-8192"
        self.temperature = 0.7
        self.max_tokens = 2048
        self.system_prompt = (SYSTEM_PROMPT_SUMMARY)

    def _load_json_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to load {filepath}: {e}"}

    def analyze(self, keylog_path="keylogs.json", mouse_log_path="mouse_logs.json"):
        keylog_data = self._load_json_file(keylog_path)
        mouse_data = self._load_json_file(mouse_log_path)

        combined_data = {
            "keylogs": keylog_data,
            "mouse_logs": mouse_data
        }

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": json.dumps(combined_data)}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content.strip()

# Example usage
if __name__ == "__main__":
    analyzer = AIAnalyzer()
    result = analyzer.analyze()
    print(result)
