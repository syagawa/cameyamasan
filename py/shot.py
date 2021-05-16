from time import sleep
import urllib.request


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
  framesize_params = {
    "var": "framesize",
    "val": "10"
  }
  quality_params = {
    "var": "quality",
    "val": "4"
  }


  set_url = f"http://{ip}/control"
  capture_url = f"http://{ip}/capture"

  req1 = urllib.request.Request('{}?{}'.format(set_url, urllib.parse.urlencode(framesize_params)))
  print(req1.full_url)
  req2 = urllib.request.Request('{}?{}'.format(set_url, urllib.parse.urlencode(quality_params)))
  print(req2.full_url)
  req3 = urllib.request.Request(capture_url)
  print(req3.full_url)

  with urllib.request.urlopen(req1) as res1:
    print(res1)
  with urllib.request.urlopen(req2) as res2:
    print(res2)

  with urllib.request.urlopen(req3) as res3:
    body = res3.read()
    with open("./aaa,jpg", mode='wb') as f:
      f.write(body)


def shots(count, interval):
    for i in range(count):
        shot()
        sleep(interval)
