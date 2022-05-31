import datetime

screen = None

def set_screen_to_log(s):
  global screen
  if s != None:
    screen = s

def log(mes):
  d = datetime.datetime.today()
  s = d.strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
  print("[%s] %s" % (s, mes))


def log_screen(mes):
  d = datetime.datetime.today()
  s = d.strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
  print("[%s] %s" % (s, mes))
  global screen
  if screen != None:
    screen.add_from_log(mes)
