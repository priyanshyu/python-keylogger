import ctypes
import threading
from time import sleep
from datetime import datetime
import json
import os

class VirtualKeyboardLogger:
    def __init__(self, output_path="keylogs_virtual.json", interval=2):
        self.interval = interval
        self.output_path = output_path
        self.data = []

    def get_clipboard_text(self):
        CF_TEXT = 1
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32

        user32.OpenClipboard(0)
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            h_clip_mem = user32.GetClipboardData(CF_TEXT)
            text = ctypes.c_char_p(h_clip_mem).value.decode('utf-8')
            user32.CloseClipboard()
            return text
        user32.CloseClipboard()
        return ""

    def capture_clipboard(self):
        prev_text = ""
        while True:
            try:
                text = self.get_clipboard_text()
                if text and text != prev_text:
                    print(f"[Clipboard Detected] {text}")
                    self.data.append({
                        "text": text,
                        "timestamp": str(datetime.now())
                    })
                    self.save_data()
                    prev_text = text
            except Exception as e:
                print(f"Clipboard Error: {e}")
            sleep(self.interval)

    def save_data(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True) if os.path.dirname(self.output_path) else None
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def run(self):
        t = threading.Thread(target=self.capture_clipboard)
        t.daemon = True
        t.start()

# For testing
if __name__ == "__main__":
    logger = VirtualKeyboardLogger()
    logger.run()
    while True:
        sleep(10)
