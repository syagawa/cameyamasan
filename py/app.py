#!/usr/bin/python3

import asyncio
from interface.key import start_standby, key_names
from interface.terminal import start_terminal
from interface.screen import make_screen
from controller import connect, connect2

import socket
import psutil

import subprocess

from logger import log

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
  log("start app!")
  screen.add("start app!")
  screen.add("please input! ^ < > v")

  loop = asyncio.get_event_loop()
  asyncio.ensure_future(start_standby(None, key_callback))
  log("started app1")
  asyncio.ensure_future(connect2(key_callback))

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
  log("started2 app1")
  async def cor2():
    await connect2(key_callback)
  f2 = asyncio.ensure_future(cor2)
  f2.add_done_callback(callback)
  futures.append(f2)

  log("started2 app2")
  log(f1 == f2)
  # loop.run_forever()
  await asyncio.wait(futures)
  log("started2 app3")


if __name__ == "__main__2":
  main()

if __name__ == "__main__":
  log("in main0")
  results = []
  def store_result(f):
    results.append(f.result())
  loop = asyncio.get_event_loop()
  log("in main1")
  loop.run_until_complete(main2(store_result))
  log("in main2")
  for res in results:
    log("{0}".format(res))
