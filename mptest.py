import multiprocessing
import time

def test1():
    while True:
        print("test1")
        time.sleep(3)

def test2():
    while True:
        print("test20")
        time.sleep(3)

if __name__ == "__main__":
    m1 = multiprocessing.Process(target=test1)
    m2 = multiprocessing.Process(target=test2)
    m2.start()
    m1.start()