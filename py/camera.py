from time import sleep
import urllib.request
from datetime import datetime
import os

def shot(ip, dir, fs):
  print("shot")
  # 1920 x 1080
  # framesize_params = {
  #   "var": "framesize",
  #   "val": "14"
  # }
  # quality_params = {
  #   "var": "quality",
  #   "val": "30"
  # }

  # 1280 x 720
  # framesize_params = {
  #   "var": "framesize",
  #   "val": "11"
  # }

  # 1600 x 1200
  # framesize_params = {
  #   "var": "framesize",
  #   "val": "13"
  # }
  
  fs_640_480 = "8" #low
  fs_800_600 = "9"
  fs_1280_720 = "10" #middle
  fs_1600_1200 = "13"
  fs_1920_1080 = "14" #high

  defualt_fs = fs_1920_1080
  if fs == "low":
    defualt_fs = fs_640_480
  elif fs == "middle":
    defualt_fs = fs_1280_720
  elif fs == "high":
    defualt_fs = fs_1920_1080

  params = {
    "fs": defualt_fs,
    "q": "4"
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


def shots(times, interval, ip):
    t = datetime.now().isoformat()
    dir = "./images/{0}".format(t)
    os.makedirs(dir, exist_ok=True)
    print(f"Image Directory: {dir}")
    for i in range(times):
        shot(ip, dir, "high")
        sleep(interval)
    return True
