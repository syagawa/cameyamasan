import time
from threading import Thread
import asyncio
from datetime import datetime

loop_a = asyncio.new_event_loop()
loop_b = asyncio.new_event_loop()

global_counter = 0

def start_loop(loop: asyncio.AbstractEventLoop):
  asyncio.set_event_loop(loop)
  loop.run_forever()

async def f1(params):
  global global_counter
  print("func1 pram {0}".format(params))
  for n in range(6):
    global_counter = global_counter + 1
    print("func1 {0} gcounter:{1}".format(n, global_counter))
    await asyncio.sleep(1)
  return "OK1"

async def f2(params):
  global global_counter
  print("func2 pram {0}".format(params))
  for n in range(9):
    global_counter = global_counter + 1
    print("func2 {0} gcounter:{1}".format(n, global_counter))
    await asyncio.sleep(0.5)
  return "OK2"

async def f3(params):
  global global_counter
  print("func3 pram {0}".format(params))
  n = -1
  while True:
    n = n + 1
    global_counter = global_counter + 1
    print("func3 {0} gcounter:{1}".format(n, global_counter))
    await asyncio.sleep(1.5)


async def do_make_task_and_go(loop, funcs):
  tasks = [loop.create_task(f["func"](*f["params"])) for f in funcs]
  results = await asyncio.gather(*tasks)
  return results

def make_task_and_go(loop, funcs):
  return asyncio.run_coroutine_threadsafe(do_make_task_and_go(loop, funcs), loop)

def main():
  loop = asyncio.new_event_loop()
  t = Thread(target=start_loop, args=(loop,), daemon=True)
  t.start()

  start_time = datetime.now()

  task = make_task_and_go(loop, [{"func": f1,"params": [1]}, {"func": f2,"params": [2]}, {"func": f3,"params": [3]}])
  for mes in task.result():
    print(mes)

  exec_time = (datetime.now() - start_time).total_seconds()

  print(f"It took {exec_time:,.2f} seconds to run")
  loop.stop()

if __name__ == "__main__":
  main()


