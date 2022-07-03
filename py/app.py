#!/usr/bin/python3

import asyncio
from asyncio.log import logger
from interface.key import start_standby, key_names
from interface.terminal import start_terminal
from interface.screen import make_screen
from controller import connect

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

def start_loop(loop: asyncio.AbstractEventLoop):
  asyncio.set_event_loop(loop)
  loop.run_forever()

async def do_make_task_and_go(loop, funcs):
  tasks = [loop.create_task(f["func"](*f["params"])) for f in funcs]
  results = await asyncio.gather(*tasks)
  return results

def make_task_and_go(loop, funcs):
  return asyncio.run_coroutine_threadsafe(do_make_task_and_go(loop, funcs), loop)

def main():
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
    {"func": connect, "params": [controller_callback]}
  ])

  for mes in task.result():
    print(mes)

  log("start4 ---")



if __name__ == "__main__":
  log("---------------------")
  main()
  log("after main")