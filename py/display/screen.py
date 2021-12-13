import time
import subprocess

import display

import platform

info = display.getDisplayInfo()
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
  display.drawBlackRect()

  for sc in screens:
    display.showMessages(sc["matrix"], sc["start"])

def add(index, message):
  if index < 0:
    return
  print("index: %s" % (index))
  print("index: %s" % (index))
  print("len: %s" % (len(screens)))
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
    show()
  def add(mes):
    print("screen_index: %s" % screen_index)
    add(screen_index, mes)
  def clear():
    print("screen_index: %s" % screen_index)
    clear(screen_index)
  def show():
    show()


def make_screen_(lines=max_rows):
  if lines > getUsableRows():
    return -1
  global use_rows, screen_index
  start = use_rows + 1
  end = start + lines - 1
  use_rows = use_rows + lines
  matrix = []
  o = { "start": start, "end": end, "matrix": matrix, "length": lines }
  screens.append(o)
  def add_messsage(mes):
    print("screen_index: %s" % screen_index)
    add(screen_index, mes)
  def clear_message():
    print("screen_index: %s" % screen_index)
    clear(screen_index)

  dic = { "add": add_messsage, "clear": clear_message, "show": show }
  if screen_index == None:
    screen_index =  0
  else:
    screen_index = screen_index + 1
  return dic

def make_screen(lines=max_rows):
  if lines > getUsableRows():
    return -1
  screen = Screen(lines)
  
  return screen


def show_info():

  s = make_screen()
  print(s)
  uname = platform.uname()
  s.show("1")
  s.show("2")
  s.show("3")
  s.show("4")
  s.show("5")
  s.show("%s: %s" % ("system", uname.system))
  s.show("%s: %s" % ("node", uname.node))
  s.show("%s: %s" % ("release", uname.release))
  s.show("%s: %s" % ("version", uname.version))
  s.show("%s: %s" % ("machine", uname.machine))
  s.show("%s: %s" % ("processor", uname.processor))
  s.show()

if __name__ == "__main__":
  show_info()