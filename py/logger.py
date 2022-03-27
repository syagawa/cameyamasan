import datetime

def log(mes):
  d = datetime.datetime.today()
  s = d.strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
  print("[%s] %s" % (s, mes))