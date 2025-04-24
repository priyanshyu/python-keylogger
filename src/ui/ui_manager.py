import os
import json

class UIManager:
    def __init__(self, config_path="config/settings.json"):
        self.config_path = config_path
        self.settings = self.load_settings()

    def load_settings(self):
        """Load settings from the config file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as config_file:
                return json.load(config_file)
        else:
            print("Settings file not found, using default settings.")
            return self.get_default_settings()

    def get_default_settings(self):
        """Return default settings."""
        return {
            "log_file": "keylogs.json",
            "interval": 5,
            "self_destruction": True,
            "app_monitor": True,
            "remote_communication": False
        }

    def save_settings(self):
        """Save the settings to the config file."""
        with open(self.config_path, "w") as config_file:
            json.dump(self.settings, config_file, indent=4)

    def display_ui(self):
        """A placeholder for UI interactions."""
        print("Welcome to Keylogger UI Manager!")
        print("1. View Settings")
        print("2. Modify Settings")
        print("3. Exit")
        
        user_input = input("Select an option: ")
        
        if user_input == "1":
            self.show_settings()
        elif user_input == "2":
            self.modify_settings()
        elif user_input == "3":
            exit()
        else:
            print("Invalid option, please try again.")
            self.display_ui()

    def show_settings(self):
        """Display current settings."""
        print("Current Settings:")
        for key, value in self.settings.items():
            print(f"{key}: {value}")
        input("Press Enter to go back.")
        self.display_ui()

    def modify_settings(self):
        """Allow the user to modify settings."""
        print("Modify Settings:")
        for key in self.settings:
            new_value = input(f"Enter new value for {key} (current value: {self.settings[key]}): ")
            if new_value:
                self.settings[key] = new_value
        self.save_settings()
        print("Settings updated successfully.")
        input("Press Enter to go back.")
        self.display_ui()
