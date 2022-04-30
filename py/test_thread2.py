import time
from threading import Thread
import asyncio

loop_a = asyncio.new_event_loop()
loop_b = asyncio.new_event_loop()

def f1():
  for n in range(10):
    print("func1 {0}".format(n))
    time.sleep(1)

def f2():
  for n in range(20):
    print("func2 {0}".format(n))
    time.sleep(0.5)

def cb_a():
  asyncio.set_event_loop(loop_a)
  asyncio.get_event_loop().call_soon(lambda: f1())
  loop_a.run_forever()

def cb_b():
  asyncio.set_event_loop(loop_b)
  asyncio.get_event_loop().call_soon(lambda: f2())
  loop_b.run_forever()



if __name__ == "__main__":
  thread1 = Thread(target=cb_a)
  thread2 = Thread(target=cb_b)
  thread1.start()
  thread2.start()



