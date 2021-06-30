from time import sleep
import urllib.request
from datetime import datetime


def shot(ip):
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
  # quality_params = {
  #   "var": "quality",
  #   "val": "4"
  # }

  # 1600 x 1200
  # framesize_params = {
  #   "var": "framesize",
  #   "val": "10"
  # }

  params = {
    "fs": "1",
    "q": "4"
  }


  capture_url = f"http://{ip}/cap"
  status_url = f"http://{ip}/status"

  req_status = urllib.request.Request(status_url)
  print(req_status.full_url)
  with urllib.request.urlopen(req_status) as res_status:
    status = res_status.read()
    print(status)


  req = urllib.request.Request('{}?{}'.format(capture_url, urllib.parse.urlencode(params)))


  with urllib.request.urlopen(req) as res:
    body = res.read()
    t = datetime.now().isoformat()
    filename = "./images/%s.jpg" % t

    with open(filename, mode='wb') as f:
      f.write(body)


def shots(count, interval):
    for i in range(count):
        shot()
        sleep(interval)
