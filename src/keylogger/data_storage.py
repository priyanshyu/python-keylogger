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
                # Initialize with an empty keystrokes list
                json.dump({"keystrokes": []}, file, indent=4)

    def load_data(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                # Load the data
                data = json.load(file)

                # Ensure the data has the "keystrokes" key and it's a list
                if not isinstance(data, dict):
                    data = {"keystrokes": []}
                if "keystrokes" not in data:
                    data["keystrokes"] = []

                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # In case of error, return a safe default structure
            return {"keystrokes": [e]}

    def save_data(self, data):
        # Ensure the data has the "keystrokes" key and it's a list
        if "keystrokes" not in data:
            data["keystrokes"] = []
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def append_keystroke(self, key_event):
        data = self.load_data()  # Load the existing data
        data["keystrokes"].append(key_event)  # Append new keystroke to the list
        self.save_data(data)  # Save the updated data
