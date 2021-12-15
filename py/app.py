from interface.key import start_standby

from interface.screen import make_screen

screen = None

def key_callback(pin, state):
  screen.add("%s, %s" % (pin, state))

def main():
  screen = make_screen()
  screen.add("start app!")
  start_standby(None, key_callback)

if __name__ == "__main__":
  main()