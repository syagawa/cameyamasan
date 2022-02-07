from os import sched_rr_get_interval
import time
import subprocess

from . import display_module

import platform

info = display_module.getDisplayInfo()
rows = info["rows"]
columns = info["columns"]
max_rows = rows
use_rows = 0
screens = []
screen_index = None

def getUsableRows():
  n = max_rows - use_rows
  if n < 0:
    return 0
  else:
    return n

def show():
  display_module.drawBlackRect()
  for sc in screens:
    display_module.showMessages(sc["matrix"], sc["start"])

def add(index, message):
  if index < 0:
    return
  print("add@screen.py index: %s" % (index))
  print("add@screen.py len: %s" % (len(screens)))
  sc = screens[index]
  sc["matrix"].append(message)
  max = sc["length"]
  if len(sc["matrix"]) > max:
    sc["matrix"].pop(0)

def clear(index):
  if index < 0:
    return
  sc = screens[index]
  sc["matrix"] = []

def update(index, message):
  sc = screens[index]
  if len(sc["matrix"]) > 0:
    sc["matrix"].pop(0)
  add(index, message)

def delete(index):
  sc = screens[index]
  if len(sc["matrix"]) > 0:
    sc["matrix"].pop(0)


def get_messages(index):
  sc = screens[index]
  return sc["matrix"]

class Screen:
  def __init__(self, lines):
    global use_rows, screen_index
    start = use_rows + 1
    end = start + lines - 1
    use_rows = use_rows + lines
    matrix = []
    screens.append({ "start": start, "end": end, "matrix": matrix, "length": lines })
    if screen_index == None:
      screen_index =  0
    else:
      screen_index = screen_index + 1
    self.self_index = screen_index
    show()
  def add(self, mes=None):
    if mes == None:
      return
    print("screen_index: %s" % self.self_index)
    add(self.self_index, mes)
    show()
  def clear(self):
    print("screen_index: %s" % self.self_index)
    clear(self.self_index)
    show()
  def update(self, mes=None):
    print("screen_index: %s" % self.self_index)
    update(self.self_index, mes)
    show()
  def show(self):
    show()
  def get_messages(self):
    get_messages(self.self_index)
  def delete(self):
    delete(self.self_index)

  

def make_screen(lines=max_rows):
  if lines > getUsableRows():
    return -1
  screen = Screen(lines)
  
  return screen

def show_info():
  s = make_screen()
  print(s)
  uname = platform.uname()
  print("aaa")
  print(s.add)
  s.add()
  s.add("1")
  s.add("2")
  s.add("3")
  s.add("4")
  s.add("5")
  s.add("%s: %s" % ("system", uname.system))
  s.add("%s: %s" % ("node", uname.node))
  s.add("%s: %s" % ("release", uname.release))
  s.add("%s: %s" % ("version", uname.version))
  s.add("%s: %s" % ("machine", uname.machine))
  s.add("%s: %s" % ("processor", uname.processor))
  s.show()

if __name__ == "__main__":
  show_info()