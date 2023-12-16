import multiprocessing
import time

def countdown(n):
    while n > 0:
        print(f"{n} seconds remaining...")
        time.sleep(1)
        n -= 1

if __name__ == "__main__":
    # Create and start two processes running the countdown function
    process1 = multiprocessing.Process(target=countdown, args=(5,))
    process2 = multiprocessing.Process(target=countdown, args=(5,))
    process1.start()
    process2.start()

    # Wait for both processes to finish
    process2.join()
    print("Done!")
    process1.terminate()
    time.sleep(1)
    process1 = multiprocessing.Process(target=countdown, args=(5,))
    process1.start()