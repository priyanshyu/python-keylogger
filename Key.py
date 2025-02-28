from Utils.utils import I_see_u
from time import sleep, time


def run():
    start_time = time()
    while time() - start_time < 300:  # Stop after timeout
        try:
            logger = I_see_u(1)
            logger.Run()
        except Exception as e:
            print(f"Error: {e}")
            sleep(120)
run()
