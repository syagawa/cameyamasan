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
selected = None


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
  for i, item in enumerate(selects):
    if i == index:
      return selects[i]

def reboot():
  subprocess.run(["sudo", "reboot"])

def push_up():
  global selected
  if selected == None:
    selected = 0

  selected = selected - 1

  if selected + 1 > len(selects):
    selected = 0
  if selected < -1:
    selected = 0

  s = get_select(selected)

  key = s.key

  screen.add("%s ?" % (key))

def push_3():
  reboot()




def key_callback(pin, state):
  name = key_names[pin]
  screen.add("%s, %s, %s" % (name, pin, state))
  # show_selects()
  if name == "UP":
    push_up()
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
  loop = asyncio.get_event_loop()
  loop.run_until_complete(start_standby(None, key_callback))
  loop.run_until_complete(connect())

if __name__ == "__main__":
  main()