import asyncio
from interface.key import start_standby

from interface.screen import make_screen

screen = None

def key_callback(pin, state):
  screen.add("%s, %s" % (pin, state))

def main():
  global screen
  screen = make_screen()
  screen.add("start app!")
  loop = asyncio.get_event_loop()
  loop.run_until_complete(start_standby(None, key_callback))

if __name__ == "__main__":
  main()