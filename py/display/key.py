
import RPi.GPIO as GPIO
import time

#GPIO define
RST_PIN        = 25
CS_PIN         = 8
DC_PIN         = 24

KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13

KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

key_names = {
    KEY_UP_PIN: "UP",
    KEY_DOWN_PIN: "DOWN",
    KEY_LEFT_PIN: "LEFT",
    KEY_RIGHT_PIN: "RIGHT",
    KEY_PRESS_PIN: "PRESS",
    KEY1_PIN: "KEY1",
    KEY2_PIN: "KEY2",
    KEY3_PIN: "KEY3"
}

#init GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up


state = None
pressed_pin = None
sleep_time = 0.1


def do_action(pressed_pin, state):
    name = key_names[pressed_pin]
    print("%s %s" % (name, "pressed"))


def press(pin):
    global pressed_pin
    old_pressed_pin = pressed_pin
    new_pressed_pin = pin
    pressed_pin = new_pressed_pin
    if old_pressed_pin == new_pressed_pin:
        return
    else:
        do_action(pressed_pin, state)

def release(pin):
    global pressed_pin
    if pressed_pin == pin:
        pressed_pin = None

def main():
    while True:
        if GPIO.input(KEY_UP_PIN) == GPIO.LOW:
            press(KEY_UP_PIN)
        elif GPIO.input(KEY_UP_PIN) == GPIO.HIGH:
            release(KEY_UP_PIN)

        if GPIO.input(KEY_LEFT_PIN) == GPIO.LOW:
            press(KEY_LEFT_PIN)
        elif GPIO.input(KEY_LEFT_PIN) == GPIO.HIGH:
            release(KEY_LEFT_PIN)

        if GPIO.input(KEY_RIGHT_PIN) == GPIO.LOW:
            press(KEY_RIGHT_PIN)
        elif GPIO.input(KEY_RIGHT_PIN) == GPIO.HIGH:
            release(KEY_RIGHT_PIN)

        if GPIO.input(KEY_DOWN_PIN) == GPIO.LOW:
            press(KEY_DOWN_PIN)
        elif GPIO.input(KEY_DOWN_PIN) == GPIO.HIGH:
            release(KEY_DOWN_PIN)

        if GPIO.input(KEY_PRESS_PIN) == GPIO.LOW:
            press(KEY_PRESS_PIN)
        elif GPIO.input(KEY_PRESS_PIN) == GPIO.HIGH:
            release(KEY_PRESS_PIN)

        if GPIO.input(KEY1_PIN) == GPIO.LOW:
            press(KEY1_PIN)
        elif GPIO.input(KEY1_PIN) == GPIO.HIGH:
            release(KEY1_PIN)


        if GPIO.input(KEY2_PIN) == GPIO.LOW:
            press(KEY2_PIN)
        elif GPIO.input(KEY2_PIN) == GPIO.HIGH:
            release(KEY2_PIN)

        if GPIO.input(KEY3_PIN) == GPIO.LOW:
            press(KEY3_PIN)
        elif GPIO.input(KEY3_PIN) == GPIO.HIGH:
            release(KEY3_PIN)
        
        time.sleep(sleep_time)

main()
