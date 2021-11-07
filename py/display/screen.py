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
screen_index = 0

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
  length = len(screens)
  last_index = length - 1
  # if last_index  < index:
  #   return
  sc = screens[last_index]
  sc["matrix"].append(message)
  max = sc["length"]
  if len(sc["matrix"]) > max:
    sc["matrix"].pop(0)

def clear(index):
  if index < 0:
    return
  sc = screens[index]
  sc["matrix"] = []


def makeScreen(lines=max_rows):
  if lines > getUsableRows():
    return -1
  global use_rows, screen_index
  start = use_rows + 1
  end = start + lines - 1
  use_rows = use_rows + lines
  matrix = []
  o = { "start": start, "end": end, "matrix": matrix, "length": lines }
  screens.append(o)
  screen_index = 0
  def add_messsage(mes):
    global screen_index
    print("screen_index: %s" % screen_index)
    add(screen_index, mes)
    screen_index = screen_index + 1
  def clear_message():
    global screen_index
    print("screen_index: %s" % screen_index)
    clear(screen_index)
    screen_index = screen_index - 1

  dic = { "add": add_messsage, "clear": clear_message, "show": show }
  
  return dic


def show_info():
  arr = []
  uname = platform.uname()
  arr.append("%s: %s" % ("system", uname.system))
  arr.append("%s: %s" % ("node", uname.node))
  arr.append("%s: %s" % ("release", uname.release))
  arr.append("%s: %s" % ("version", uname.version))
  arr.append("%s: %s" % ("machine", uname.machine))
  arr.append("%s: %s" % ("processor", uname.processor))

  for i in range(len(arr)):
    display.showMessage(arr[i], i + 1)
    time.sleep(0.5)


def show_info2():

  s = makeScreen()
  print(s)
  uname = platform.uname()
  s["add"]("%s: %s" % ("system", uname.system))
  s["add"]("%s: %s" % ("node", uname.node))
  s["add"]("%s: %s" % ("release", uname.release))
  s["add"]("%s: %s" % ("version", uname.version))
  s["add"]("%s: %s" % ("machine", uname.machine))
  s["add"]("%s: %s" % ("processor", uname.processor))
  show()


show_info2()