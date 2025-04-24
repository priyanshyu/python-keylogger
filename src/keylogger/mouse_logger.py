import threading
from pynput import mouse
from datetime import datetime
from data_storage import DataStorage

class MouseLogger:
    def __init__(self, output_path="mouse_logs.json"):
        self.output_path = output_path
        self.data_storage = DataStorage(output_path)  # Using DataStorage with a separate file
        self.mouse_data = {
            "clicks": [],
            "scrolls": [],
            "movements": []
        }

    def _save_json(self):
        """Save mouse data to the JSON file using DataStorage."""
        data = self.data_storage.load_data()  # Load existing data
        if "mouse" not in data:
            data["mouse"] = self.mouse_data  # Initialize mouse data if not present
        else:
            # Add new mouse events to the existing data
            for key in self.mouse_data:
                data["mouse"][key].extend(self.mouse_data[key])

        self.data_storage.save_data(data)  # Save the updated data

        # Clear the mouse data after saving
        self.mouse_data = {"clicks": [], "scrolls": [], "movements": []}

    def on_click(self, x, y, button, pressed):
        """Log mouse click events."""
        action = "Pressed" if pressed else "Released"
        self.mouse_data["clicks"].append({
            "button": str(button),
            "action": action,
            "position": [x, y],
            "timestamp": str(datetime.now())
        })

    def on_scroll(self, x, y, dx, dy):
        """Log mouse scroll events."""
        self.mouse_data["scrolls"].append({
            "position": [x, y],
            "delta": [dx, dy],
            "timestamp": str(datetime.now())
        })

    def on_move(self, x, y):
        """Log mouse movement events."""
        self.mouse_data["movements"].append({
            "position": [x, y],
            "timestamp": str(datetime.now())
        })

    def run(self):
        """Start the mouse listener."""
        print("Starting mouse logger... Press Ctrl+C to stop.")
        with mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll,
            on_move=self.on_move
        ) as listener:
            listener.join()

    def start_periodic_save(self, interval=5):
        """Start a periodic save thread."""
        def periodic_save():
            while True:
                threading.Event().wait(interval)
                self._save_json()

        threading.Thread(target=periodic_save, daemon=True).start()

# For testing only
if __name__ == "__main__":
    logger = MouseLogger(output_path="mouse_logs.json")
    logger.start_periodic_save(interval=5)  # Save every 5 seconds

    # Create and run the listener in a separate thread
    listener_thread = threading.Thread(target=logger.run)
    listener_thread.daemon = True
    listener_thread.start()

    try:
        while True:
            pass  # Main thread does nothing, keeps the program alive
    except KeyboardInterrupt:
        print("Mouse logger stopped.")
