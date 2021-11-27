# sudo apt install python3-pip
# sudo pip3 install Adafruit-Blinka
# sudo pip3 install adafruit-circuitpython-ssd1306
# sudo apt install python3-pil
# for 128 * 64 display

import time
import subprocess

import random

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
# import adafruit_ssd1306
import SH1106


display_reset = digitalio.DigitalInOut(board.D4)

w = 128
h = 64
rows = 8
columns = 21

white = 0
black = 255


pad = -2
top = pad
bottom = h - pad
line_height = 8
x = 0


I2C = board.I2C()

d = SH1106.SH1106()
d.Init()
d.clear()

image = Image.new("1", (d.width, d.height), "grey")
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()


def drawBlackRect():
  one_line = h / rows
  draw.rectangle((0, 0, w, h), outline=black, fill=black)

def drawBlackLines(start, lines):
  one_line = h / rows
  start_y = (start - 1 ) * one_line
  print(start_y)
  print(one_line * lines)
  draw.rectangle((0, start_y, w, one_line * lines), outline=0, fill=black)

def drawWhiteRect(lines=line_height):
  draw.rectangle((0, 0, w, h), outline=black, fill=white)

def showMessage(mes, line):
  l = line - 1
  draw.text( (x, top + (line_height * l) ), mes, font=font, fill=white)
  d.ShowImage(d.getbuffer(image))
  # d.show()

def showMessages(messages, start):
  length = len(messages)
  for i in range(length):
    l = start + i - 1
    mes = messages[i]
    draw.text( (x, top + (line_height * l) ), mes, font=font, fill=white)
  d.ShowImage(d.getbuffer(image))
  # d.show()



def getDisplayInfo():
  return { "columns": columns, "rows": rows }


drawBlackRect()


def test_display():
  count = 0
  messages = ["AAA", "BBB", "CCC"]
  m_len = len(messages)

  while True:
    count = count + 1
    drawBlackRect()
    i = random.randint(0, m_len - 1)
    message = "%s %s" % (messages[i], count)

    l = random.randint(1, 8)
    showMessage(message, l)
    time.sleep(0.5)
    print("loop")

if __name__ == "__main__":
  test_display()
