#!/usr/bin/python3

import asyncio
from asyncio.log import logger
from interface.key import start_standby, key_names
from interface.terminal import start_terminal
from interface.screen import make_screen
from controller import connect, connect2

import socket
import psutil

import subprocess
import threading

from logger import log, set_screen_to_log, log_screen

import global_value as g

g.stop_shot = False

def get_ip_addresses(family):
  for interface, snics in psutil.net_if_addrs().items():
    for snic in snics:
      if snic.family == family:
        yield(interface, snic.address)

def get_ip_string(name):
  iplist = list(get_ip_addresses(socket.AF_INET))
  str = ""
  for elm in iplist:
    if elm[0] == name:
      str = "%s:%s" % (elm[0], elm[1])
  return str


screen = None

states = {
  "in": False,
  "out": False,
  "waiting": False,
}

selects = [
  { "key": "reboot", "state": False},
  { "key": "shutdown", "state": False},
  { "key": "connectnet", "state": False},
  { "key": "showinfo", "state": False},
  { "key": "restartself", "state": False},
  { "key": "stopshot", "state": False},
]
select = None

confirms = [
  { "key": "ok", "confirm": True},
  { "key": "ng", "confirm": False},
]

confirm = None


def get_state():
  key = None
  for k, v in states:
    if v == True:
      key = k
      break
  return key

def set_state(key, b):
  _bool = bool(b)
  if key in states:
    states[key] = _bool

def get_select(index):
  log("in get_select %s" % index)
  for i, item in enumerate(selects):
    log("in get_select for")
    if i == index:
      log("in get_select for if")
      return selects[i]

def reboot():
  subprocess.run(["sudo", "reboot"])

def shutdown():
  subprocess.run(["sudo", "shutdown", "-h", "now"])

def showinfo():
  screen.add(get_ip_string("wlan0"))
  screen.add(get_ip_string("wlan1"))

def connectnet():
  screen.add("connect wlan0 to net")
  subprocess.run(["sudo", "dhclient", "wlan0"])

def restartself():
  screen.add("restart app")
  subprocess.run(["sudo", "systemctl", "restart", "camerawithpy.service"])

def init_stopshot():
  exec("g.stop_shot=False")

def stopshot():
  exec("g.stop_shot=True")

def push_up_or_down(mode):
  if mode == None:
    return

  global select
  if select == None:
    select = 0

  if mode == "up":
    select = select - 1
  elif mode == "down":
    select = select + 1
  else:
    return

  min = 0
  max = len(selects) - 1

  if select > max:
    select = min
  if select < min:
    select = max

  s = get_select(select)

  if s is None:
    return

  key = s["key"]

  screen.update("%s ?" % (key))


def push_up():
  push_up_or_down("up")

def push_down():
  push_up_or_down("down")


def push_left():
  push_left_or_right("left")

def push_right():
  push_left_or_right("right")

def push_left_or_right(mode):
  if mode == None:
    return

  global confirm
  if confirm == None:
    confirm = 0

  if mode == "left":
    confirm = confirm - 1
  elif mode == "right":
    confirm = confirm + 1
  else:
    return

  min = 0
  max = len(confirms) - 1

  if confirm >= max:
    confirm = min
  if confirm < min:
    confirm = max

  c = confirms[confirm]

  if c is None:
    return

  key = c["key"]

  screen.update("%s ?" % (key))


def push_1():
  screen.add("execute...")
  s = get_select(select)
  if s is None:
    return
  key = s["key"]
  if key == "shutdown":
    shutdown()
    screen.add("shutdown...")
  if key == "reboot":
    reboot()
    screen.add("reboot...")
  if key == "showinfo":
    showinfo()
  if key == "connectnet":
    connectnet()
  if key == "restartself":
    restartself()
  if key == "stopshot":
    stopshot()


  screen.add("please input! ^ < > v")
  

def push_2():
  screen.add("shutdown...")
  shutdown()

def push_3():
  screen.add("reboot...")
  reboot()


def key_callback(pin, state):
  log("in key_callback")
  name = key_names[pin]
  # screen.update("%s, %s, %s" % (name, pin, state))
  if name == "UP":
    push_up()
  if name == "DOWN":
    push_down()
  if name == "LEFT":
    push_left()
  if name == "RIGHT":
    push_right()
  if name == "KEY1":
    push_1()
  if name == "KEY2":
    push_2()
  if name == "KEY3":
    push_3()

def controller_callback(message):
  log(message)
  screen.add("%s in cc" % message)


def show_selects():
  for index, item in enumerate(selects):
    screen.add("%s: %s" % (index + 1, item.key))

def main():
  global screen
  screen = make_screen()
  set_screen_to_log(screen)
  log("start app!")
  screen.add("please input! ^ < > v")

  loop = asyncio.get_event_loop()
  asyncio.ensure_future(start_standby(None, key_callback))
  log("started app1")
  res_connect2 = asyncio.ensure_future(connect2(key_callback))

  log("started app2")
  loop.run_forever()
  log("started app3")


async def main2(callback):
  global screen
  screen = make_screen()
  log("start2 app!")
  screen.add("start2 app!")
  screen.add("please2 input! ^ < > v")
  log("s22")

  futures = []
  cor1 = start_standby(None, key_callback)
  log("s23")
  f1 = asyncio.ensure_future(cor1)
  log("s24")
  f1.add_done_callback(callback)
  log("s25")
  futures.append(f1)
  log("s26")
  cor2 = connect2(key_callback)
  f2 = asyncio.ensure_future(cor2)
  f2.add_done_callback(callback)
  futures.append(f2)

  log("s27")
  # loop.run_forever()
  await asyncio.wait(futures)
  log("s28")

def main3():
  global screen
  screen = make_screen()
  log("start3 app!")
  screen.add("start3 app!")
  screen.add("please3 input! ^ < > v")

  thread1 = threading.Thread(target=start_standby, args=(None, key_callback))
  thread2 = threading.Thread(target=connect, args=(key_callback,))
  thread1.start()
  thread2.start()
  log("start3 ---")

def start_loop(loop: asyncio.AbstractEventLoop):
  asyncio.set_event_loop(loop)
  loop.run_forever()

async def do_make_task_and_go(loop, funcs):
  tasks = [loop.create_task(f["func"](*f["params"])) for f in funcs]
  results = await asyncio.gather(*tasks)
  return results

def make_task_and_go(loop, funcs):
  return asyncio.run_coroutine_threadsafe(do_make_task_and_go(loop, funcs), loop)

def main4():
  global screen
  screen = make_screen()
  set_screen_to_log(screen)
  log_screen("start4 app!")
  screen.add("please3 input! ^ < > v")

  init_stopshot()

  loop = asyncio.new_event_loop()
  t = threading.Thread(target=start_loop, args=(loop,), daemon=True)
  t.start()

  task = make_task_and_go(loop, [
    {"func": start_standby, "params": [None, key_callback]},
    {"func": connect2, "params": [controller_callback]}
  ])

  for mes in task.result():
    print(mes)

  log("start4 ---")



if __name__ == "__main__1":
  main()

if __name__ == "__main__2":
  log("---------------------")
  results = []
  def store_result(f):
    results.append(f.result())
  loop = asyncio.get_event_loop()
  log("in main1")
  loop.run_until_complete(main2(store_result))
  log("in main2")
  for res in results:
    log("{0}".format(res))

if __name__ == "__main__3":
  log("---------------------")
  main3()
  log("after main3")

if __name__ == "__main__":
  log("---------------------")
  main4()
  log("after main4")