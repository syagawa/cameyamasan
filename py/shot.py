from time import sleep
import urllib.request


def shot(url):
  print("shot")
  params = {
    "aaa": "bbb"
  }
  req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
  with urllib.request.urlopen(req) as res:
    body = res.read()
    print(body)
    with open("./aaa", mode='wb') as f:
      f.write(body)
 

def shots(count, interval):
    for i in range(count):
        shot()
        sleep(interval)
