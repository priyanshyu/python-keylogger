import json
import os

class DataStorage:
    def __init__(self, filepath="keylogs.json"):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True) if os.path.dirname(self.filepath) else None
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump({"keystrokes": []}, file, indent=4)

    def load_data(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"keystrokes": []}

    def save_data(self, data):
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def append_keystroke(self, key_event):
        data = self.load_data()
        data["keystrokes"].append(key_event)
        self.save_data(data)
