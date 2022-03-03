#!/usr/bin/python3

import asyncio
from interface.key import start_standby, key_names
from interface.terminal import start_terminal
from interface.screen import make_screen
from controller import connect

import socket
import psutil

import subprocess

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
  { "key": "start", "state": False},
  { "key": "stop", "state": False},
  { "key": "reboot", "state": False},
  { "key": "exit", "state": False},
]
confirm = None

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
  print("in get_select %s" % index)
  for i, item in enumerate(selects):
    print("in get_select for")
    if i == index:
      print("in get_select for if")
      return selects[i]

def reboot():
  subprocess.run(["sudo", "reboot"])

def shutdown():
  subprocess.run(["sudo", "shutdown", "-h", "now"])


def push_up_or_down(mode):
  if mode == None:
    return

  global confirm
  if confirm == None:
    confirm = 0

  if mode == "up":
    confirm = confirm - 1
  elif mode == "down":
    confirm = confirm + 1
  else:
    return

  min = 0
  max = len(selects) - 1

  if confirm >= max:
    confirm = min
  if confirm < min:
    confirm = max

  s = get_select(confirm)

  if s is None:
    return

  key = s["key"]

  screen.update("%s ?" % (key))


def push_up():
  push_up_or_down("up")

def push_down():
  push_up_or_down("down")

# def push_up():
#   global selected
#   if selected == None:
#     selected = 0

#   selected = selected - 1

#   min = 0
#   max = len(selects) - 1

#   if selected >= max:
#     selected = min
#   if selected < min:
#     selected = max

#   s = get_select(selected)

#   if s is None:
#     return

#   key = s["key"]

#   screen.update("%s ?" % (key))

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

def push_2():
  screen.add("shutdown...")
  shutdown()

def push_3():
  screen.add("reboot...")
  reboot()


def key_callback(pin, state):
  print("in key_callback")
  name = key_names[pin]
  screen.update("%s, %s, %s" % (name, pin, state))
  if name == "UP":
    push_up()
  if name == "KEY2":
    push_2()
  if name == "KEY3":
    push_3()
  

def show_selects():
  for index, item in enumerate(selects):
    screen.add("%s: %s" % (index + 1, item.key))

def main():
  global screen
  screen = make_screen()
  screen.add("start app!")
  screen.add(get_ip_string("wlan0"))
  screen.add(get_ip_string("wlan1"))
  screen.add("please input! ^ < > v")

  loop = asyncio.get_event_loop()
  loop.run_until_complete(start_standby(None, key_callback))
  loop.run_until_complete(connect())

if __name__ == "__main__":
  main()