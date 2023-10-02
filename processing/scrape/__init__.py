import time


def waiting():
    max_timeout = 10
    remaining_time = max_timeout

    while remaining_time > 0:
        print(f"Waiting... {remaining_time} seconds remaining")
        time.sleep(1)
        remaining_time -= 1

    print("Start Pulling Data...")
    print("\nData is here!\n")
