import platform
import time

if platform.system() == "Windows":
    import win32gui
    import win32process
    import psutil
elif platform.system() == "Linux":
    import subprocess
elif platform.system() == "Darwin":
    from AppKit import NSWorkspace

class AppMonitor:
    def __init__(self):
        self.current_app = None

    def get_active_window(self):
        system = platform.system()

        if system == "Windows":
            try:
                hwnd = win32gui.GetForegroundWindow()
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                return process.name()
            except Exception as e:
                return f"Unknown (Windows Error: {e})"

        elif system == "Linux":
            try:
                output = subprocess.check_output(['xdotool', 'getwindowfocus', 'getwindowname'])
                return output.decode("utf-8").strip()
            except Exception as e:
                return f"Unknown (Linux Error: {e})"

        elif system == "Darwin":
            try:
                return NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
            except Exception as e:
                return f"Unknown (macOS Error: {e})"

        return "Unknown OS"

    def monitor_loop(self, interval=5):
        print("Monitoring active application...")
        while True:
            app = self.get_active_window()
            if app != self.current_app:
                self.current_app = app
                print(f"[Active Window Changed] {app}")
            time.sleep(interval)

# For testing
if __name__ == "__main__":
    monitor = AppMonitor()
    monitor.monitor_loop()
