from time import sleep
from urllib.error import ContentTooShortError, HTTPError, URLError
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
shooting_counts = 0
log_counts = [0, 10, 50, 100, 500, 1000, 2000]
could_not_shoot = False

pwd = os.getcwd()

def shoot_image(ip, dir, fs):
  log("in shoot1")
  global shooting_counts, could_not_shoot

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
  log("in shoot2")

  if framesize == None:
    framesize = framesize_default

  log(f"shoot {framesize}, {quality}, {key}")

  params = {
    "fs": framesize,
    "q": quality
  }

  capture_url = f"http://{ip}/cap"

  # check status
  if shooting_counts == 0:
    status_url = f"http://{ip}/status"
    req_status = urllib.request.Request(status_url)
    log(req_status.full_url)
    with urllib.request.urlopen(req_status) as res_status:
      status = res_status.read()
      log(status)

  req = urllib.request.Request('{}?{}'.format(capture_url, urllib.parse.urlencode(params)))

  # shoot
  try:
    with urllib.request.urlopen(req) as res:
      body = res.read()
      t = datetime.now().isoformat()
      filename = "{0}/{1}.jpg".format(dir, t)
      with open(filename, mode='wb') as f:
        f.write(body)
    shooting_counts = shooting_counts + 1
    if could_not_shoot == True:
      could_not_shoot = False
      log_screen("succeeded shooting")
  except (URLError, HTTPError, ContentTooShortError) as e:
    log_screen("could not shoot")
    could_not_shoot = True



def shoot_images_for_main(times, interval, ip, fs):
    t = datetime.now().isoformat()
    dir = "{0}/images/{1}".format(pwd, t)
    os.makedirs(dir, exist_ok=True)
    log(f"Image Directory: {dir}")
    for i in range(times):
      if shooting_counts == 0:
        log_screen("before first shooting!")
      shoot_image(ip, dir, fs)
      if shooting_counts == 1:
        log_screen("after first shooting!")
      sleep(interval)
    return True


def get_hour_minute_second(td):
  m, s = divmod(td.seconds, 60)
  h, m = divmod(m, 60)
  return h, m, s

async def shoot_images(times, interval, ip, fs):
    global shooting_counts
    now = datetime.now()
    t = now.isoformat()
    dir = "{0}/images/{1}".format(pwd, t)
    os.makedirs(dir, exist_ok=True)
    log(f"Image Directory: {dir}")
    start_time = now
    for i in range(times):
      log("stop_shoot %s" % str(g.stop_shoot))
      if g.stop_shoot == True:
        log_screen("stop_shoot!! ")
        break
      c = shooting_counts
      if c in log_counts:
        log_screen("before %s shot" % str(c))
      shoot_image(ip, dir, fs)
      if c in log_counts:
        log_screen("after %s shot" % str(c))
      await asyncio.sleep(interval)
    end_time = datetime.now()
    dt = end_time - start_time
    gap = get_hour_minute_second(dt)
    log_screen("count: %s, inter: %ss" % (str(shooting_counts), str(interval)))
    log_screen("%sh %sm %ss" % (gap[0], gap[1], gap[2]))
    return True