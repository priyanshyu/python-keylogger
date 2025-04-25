import threading
from pynput import mouse
from datetime import datetime
from keylogger.data_storage import DataStorage

class MouseLogger:
    def __init__(self, output_path="mouse_logs.json"):
        self.output_path = output_path
        self.data_storage = DataStorage(output_path)
        self.mouse_data = {
            "clicks": [],
            "scrolls": [],
            "movements": []
        }
        self.listener = None
        self._stop_saving = threading.Event()

    def _save_json(self):
        data = self.data_storage.load_data()
        if "mouse" not in data:
            data["mouse"] = self.mouse_data
        else:
            for key in self.mouse_data:
                data["mouse"][key].extend(self.mouse_data[key])

        self.data_storage.save_data(data)
        self.mouse_data = {"clicks": [], "scrolls": [], "movements": []}

    def on_click(self, x, y, button, pressed):
        action = "Pressed" if pressed else "Released"
        self.mouse_data["clicks"].append({
            "button": str(button),
            "action": action,
            "position": [x, y],
            "timestamp": str(datetime.now())
        })

    def on_scroll(self, x, y, dx, dy):
        self.mouse_data["scrolls"].append({
            "position": [x, y],
            "delta": [dx, dy],
            "timestamp": str(datetime.now())
        })

    def on_move(self, x, y):
        self.mouse_data["movements"].append({
            "position": [x, y],
            "timestamp": str(datetime.now())
        })

    def start_listener(self):
        self.listener = mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll,
            on_move=self.on_move
        )
        self.listener.start()

    def stop_listener(self):
        if self.listener:
            self.listener.stop()
        self._stop_saving.set()

    def start_periodic_save(self, interval=5):
        def periodic_save():
            while not self._stop_saving.is_set():
                threading.Event().wait(interval)
                self._save_json()
        threading.Thread(target=periodic_save, daemon=True).start()
