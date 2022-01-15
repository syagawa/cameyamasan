#!/usr/bin/python3

import asyncio
from interface.key import start_standby, key_names
from interface.terminal import start_terminal
from interface.screen import make_screen
from controller import connect

import socket
import psutil

def get_ip_addresses(family):
  for interface, snics in psutil.net_if_addrs().items():
    for snic in snics:
      if snic.family == family:
        yield(interface, snic.address)

def get_ip_string():
  iplist = list(get_ip_addresses(socket.AF_INET))
  arr = []
  for elm in iplist:
    if elm[0] == "wlan0":
      arr.append("%s:%s" % (elm[0], elm[1]))
    if elm[0] == "wlan1":
      arr.append("%s:%s" % (elm[0], elm[1]))
  str = "".join(arr)
  return str




screen = None

states = {
  "in": False,
  "out": False,
  "waiting": False,
}

selects = {
  "start": False,
  "stop": False,
  "reboot": False,
  "exit": False,
}

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


def key_callback(pin, state):
  name = key_names[pin]
  screen.add("%s, %s, %s" % (name, pin, state))
  show_selects()

def show_selects():
  counter = 0
  for key in selects:
    counter = counter + 1
    screen.add("%s: %s" % (counter, key))

def main():
  global screen
  screen = make_screen()
  screen.add("start app!")
  screen.add(get_ip_string())
  loop = asyncio.get_event_loop()
  loop.run_until_complete(start_standby(None, key_callback))
  loop.run_until_complete(connect())

if __name__ == "__main__":
  main()