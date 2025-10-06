import time

from progress.bar import Bar
from tqdm import tqdm


def long_process_bar():
    print("Progress bar with progress")
    bar = Bar("Processing", max=50)
    for _ in range(50):
        time.sleep(0.1)  # Simulate work being done
        bar.next()
    bar.finish()


def long_process_tqdm():
    print("Progress bar with tqdm")
    for _ in tqdm(range(50), desc="Processing"):
        time.sleep(0.1)  # Simulate work being done


if __name__ == "__main__":
    long_process_tqdm()
    long_process_bar()
