from time import sleep
import urllib.request
from datetime import datetime
import os
import asyncio

from logger import log, log_screen

import global_value as g

framesizes = [
  { "key": "fs_96_96", "value": "0", "default": False},
  { "key": "fs_160_120", "value": "1", "default": False},
  { "key": "fs_176_144", "value": "2", "default": False},
  { "key": "fs_240_176", "value": "3", "default": False},
  { "key": "fs_240_240", "value": "4", "default": False},
  { "key": "fs_320_240", "value": "5", "default": False},
  { "key": "fs_400_296", "value": "6", "default": False},
  { "key": "fs_480_320", "value": "7", "default": False},
  { "key": "fs_640_480", "value": "8", "default": False},
  { "key": "fs_800_600", "value": "9", "default": False},
  { "key": "fs_1024_768", "value": "10", "default": False},
  { "key": "fs_1280_720", "value": "11", "default": True},
  { "key": "fs_1280_1024", "value": "12", "default": False},
  { "key": "fs_1600_1200", "value": "13", "default": False},
  { "key": "fs_1920_1080", "value": "14", "default": False}
]

quality = "4"
shot_count = 0
log_counts = [0, 10, 50, 100, 500, 1000, 2000]

def shot(ip, dir, fs):
  log("in shot1")
  global shot_count

  log("fs: %s" % fs)
  framesize = None
  framesize_default = None
  key = ""
  for elm in framesizes:
    val = elm["value"]
    if val == fs:
      framesize = fs
      key = elm["key"]
      break

    if elm["default"]:
      framesize_default = val
  log("in shot2")

  if framesize == None:
      framesize = framesize_default

  log(f"shot {framesize}, {quality}, {key}")

  params = {
    "fs": framesize,
    "q": quality
  }

  capture_url = f"http://{ip}/cap"

  # capture_url_sample = "http://192.168.x.x/cap?fs=9&q=4"

  # check status
  if shot_count == 0:
    status_url = f"http://{ip}/status"
    req_status = urllib.request.Request(status_url)
    log(req_status.full_url)
    with urllib.request.urlopen(req_status) as res_status:
      status = res_status.read()
      log(status)

  req = urllib.request.Request('{}?{}'.format(capture_url, urllib.parse.urlencode(params)))

  # shot
  try:
    with urllib.request.urlopen(req) as res:
      body = res.read()
      t = datetime.now().isoformat()
      filename = "{0}/{1}.jpg".format(dir, t)
      with open(filename, mode='wb') as f:
        f.write(body)
    shot_count = shot_count + 1
  except:
    log_screen("cant shot")



def shots(times, interval, ip, fs):
    t = datetime.now().isoformat()
    dir = "./images/{0}".format(t)
    os.makedirs(dir, exist_ok=True)
    log(f"Image Directory: {dir}")
    for i in range(times):
        if shot_count == 0:
          log_screen("before first shot!")
        shot(ip, dir, fs)
        if shot_count == 1:
          log_screen("after first shot!")
        sleep(interval)
    return True

async def shots2(times, interval, ip, fs):
    global shot_count
    t = datetime.now().isoformat()
    dir = "./images/{0}".format(t)
    os.makedirs(dir, exist_ok=True)
    log(f"Image Directory: {dir}")
    for i in range(times):
        log("stop_shot %s" % str(g.stop_shot))
        if g.stop_shot == True:
          log_screen("stop_shot!! ")
          break
        c = shot_count
        if c in log_counts:
          log_screen("before %s shot" % str(c))
        shot(ip, dir, fs)
        if c in log_counts:
          log_screen("after %s shot" % str(c))
        await asyncio.sleep(interval)
    log_screen("count: %s, inter: %ss" % (str(shot_count), str(interval)))
    return True