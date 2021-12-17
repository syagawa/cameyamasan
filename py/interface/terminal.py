state = 0

states = {
  "in": False,
  "out": False,
}

def callback(key, screen):
  print("in terminal callback")

def start():
  print("in terminal.py")
  return callback


if __name__ == "__main__":
  start()