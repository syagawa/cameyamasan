from display.key import start_standby

import controller
from display.screen import make_screen


def main():
  s = make_screen
  s["add"]("Start!")

if __name__ == "__main__":
  main()