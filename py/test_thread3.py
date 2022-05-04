import time
from threading import Thread
import asyncio
from datetime import datetime

loop_a = asyncio.new_event_loop()
loop_b = asyncio.new_event_loop()


def start_loop(loop: asyncio.AbstractEventLoop):
  asyncio.set_event_loop(loop)
  loop.run_forever()

async def f1():
  for n in range(6):
    print("func1 {0}".format(n))
    await asyncio.sleep(1)
  return "OK1"

async def f2():
  for n in range(9):
    print("func2 {0}".format(n))
    await asyncio.sleep(0.5)
  return "OK2"

async def f3():
  n = -1
  while True:
    n = n + 1
    print("func3 {0}".format(n))
    await asyncio.sleep(1.5)


async def do_make_task_and_go(loop, funcs):
  # tasks = [loop.create_task(f1()), loop.create_task(f2()), loop.create_task(f3())]
  tasks = [loop.create_task(f()) for f in funcs]
  results = await asyncio.gather(*tasks)
  return results

def make_task_and_go(loop, funcs):
  return asyncio.run_coroutine_threadsafe(do_make_task_and_go(loop, funcs), loop)

def main():
  loop = asyncio.new_event_loop()
  t = Thread(target=start_loop, args=(loop,), daemon=True)
  t.start()

  start_time = datetime.now()

  task = make_task_and_go(loop, [f1, f2, f3])
  for mes in task.result():
    print(mes)

  exec_time = (datetime.now() - start_time).total_seconds()

  print(f"It took {exec_time:,.2f} seconds to run")
  loop.stop()

if __name__ == "__main__":
  main()


