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


def makeScreen(lines=max_rows):
  if lines > getUsableRows():
    return -1
  global use_rows
  start = use_rows + 1
  end = start + lines - 1
  use_rows = use_rows + lines
  matrix = []
  o = { "start": start, "end": end, "matrix": matrix, "length": lines }
  screens.append(o)
  index = len(screens) - 1
  def add_messsage(mes):
    add(index, mes)
  def clear_message():
    clear(index)

  dic = { "add": add_messsage, "clear": clear_message, "showw": show }
  
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

  uname = platform.uname()
  add(0, "%s: %s" % ("system", uname.system))
  add(1, "%s: %s" % ("node", uname.node))
  add(2, "%s: %s" % ("release", uname.release))
  add(3, "%s: %s" % ("version", uname.version))
  add(4, "%s: %s" % ("machine", uname.machine))
  add(5, "%s: %s" % ("processor", uname.processor))
  show()



show_info2()