import time
import threading


def f1():
  for n in range(10):
    print("func1 {0}".format(n))
    time.sleep(1)

def f2():
  for n in range(20):
    print("func2 {0}".format(n))
    time.sleep(0.5)

if __name__ == "__main__":
  thread1 = threading.Thread(target=f1)
  thread2 = threading.Thread(target=f2)
  thread1.start()
  thread2.start()