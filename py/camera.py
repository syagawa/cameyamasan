from time import sleep
import urllib.request
from datetime import datetime
import os


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

def shot(ip, dir, fs):

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

  if framesize == None:
      framesize = framesize_default

  print(f"shot {framesize}, {quality}, {key}")

  params = {
    "fs": framesize,
    "q": quality
  }

  capture_url = f"http://{ip}/cap"
  status_url = f"http://{ip}/status"

  req_status = urllib.request.Request(status_url)
  print(req_status.full_url)

  # check status
  with urllib.request.urlopen(req_status) as res_status:
    status = res_status.read()
    print(status)

  req = urllib.request.Request('{}?{}'.format(capture_url, urllib.parse.urlencode(params)))

  # shot
  with urllib.request.urlopen(req) as res:
    body = res.read()
    t = datetime.now().isoformat()
    filename = "{0}/{1}.jpg".format(dir, t)
    with open(filename, mode='wb') as f:
      f.write(body)


def shots(times, interval, ip, fs):
    t = datetime.now().isoformat()
    dir = "./images/{0}".format(t)
    os.makedirs(dir, exist_ok=True)
    print(f"Image Directory: {dir}")
    for i in range(times):
        shot(ip, dir, fs)
        sleep(interval)
    return True
