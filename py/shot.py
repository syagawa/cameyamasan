from time import sleep


def shot():
  print("shot")

def shots(count, interval):
    for i in range(count):
        shot()
        sleep(interval)
