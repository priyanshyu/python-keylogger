import os
import json
from groq import Groq
from dotenv import load_dotenv
from prompts.system_prompt import SYSTEM_PROMPT_SUMMARY
from itertools import islice

# Load API key from .env file
load_dotenv()

class AIAnalyzer:
    def __init__(self, keylog_path="keylogs.json", mouse_log_path="mouse_logs.json"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-70b-8192"
        self.temperature = 0.45
        self.max_tokens = 5000
        self.system_prompt = SYSTEM_PROMPT_SUMMARY

        # Set the file paths as instance variables
        self.keylog_path = keylog_path
        self.mouse_log_path = mouse_log_path

    def _load_json_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to load {filepath}: {e}"}

    def _batch_data(self, data, batch_size=500):
        """Splits data into batches of batch_size."""
        it = iter(data)
        for batch in iter(lambda: list(islice(it, batch_size)), []):
            yield batch

    def _process_batch(self, keylog_batch, mouse_batch):
        """Create the prompt and make an API request for a single batch."""
        combined_data = {
            "keylogs": keylog_batch,
            "mouse_logs": mouse_batch
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

    def analyze(self):
        keylog_data = self._load_json_file(self.keylog_path)
        mouse_data = self._load_json_file(self.mouse_log_path)

        # Batch the data
        keylog_batches = self._batch_data(keylog_data)
        mouse_batches = self._batch_data(mouse_data)

        # Process each batch and accumulate results
        results = []
        for keylog_batch, mouse_batch in zip(keylog_batches, mouse_batches):
            result = self._process_batch(keylog_batch, mouse_batch)
            results.append(result)

        # Combine the results from all batches
        final_result = "\n".join(results)
        return final_result

# Example usage
if __name__ == "__main__":
    analyzer = AIAnalyzer(keylog_path="keylogs.json", mouse_log_path="mouse_logs.json")
    result = analyzer.analyze()
    print(result)
