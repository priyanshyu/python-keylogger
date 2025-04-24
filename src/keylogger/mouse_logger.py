from pynput import mouse
from datetime import datetime
import json
import os

class MouseLogger:
    def __init__(self, output_path="keylogs.json"):
        self.output_path = output_path
        self.mouse_data = {
            "clicks": [],
            "scrolls": [],
            "movements": []
        }

    def _save_json(self):
        if not os.path.exists(self.output_path):
            print("Keylog file not found. Make sure keylogger is initialized first.")
            return

        with open(self.output_path, "r+", encoding="utf-8") as file:
            data = json.load(file)
            if "mouse" not in data:
                data["mouse"] = self.mouse_data
            else:
                for key in self.mouse_data:
                    data["mouse"][key].extend(self.mouse_data[key])
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def on_click(self, x, y, button, pressed):
        action = "Pressed" if pressed else "Released"
        self.mouse_data["clicks"].append({
            "button": str(button),
            "action": action,
            "position": [x, y],
            "timestamp": str(datetime.now())
        })
        self._save_json()

    def on_scroll(self, x, y, dx, dy):
        self.mouse_data["scrolls"].append({
            "position": [x, y],
            "delta": [dx, dy],
            "timestamp": str(datetime.now())
        })
        self._save_json()

    def on_move(self, x, y):
        self.mouse_data["movements"].append({
            "position": [x, y],
            "timestamp": str(datetime.now())
        })
        self._save_json()

    def run(self):
        print("Starting mouse logger... Press Ctrl+C to stop.")
        with mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll,
            on_move=self.on_move
        ) as listener:
            listener.join()

# For testing only
if __name__ == "__main__":
    logger = MouseLogger()
    logger.run()
