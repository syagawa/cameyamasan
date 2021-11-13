
import RPi.GPIO as GPIO

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


def do_action(pressed_pin, state):
    if state == "pressed":
        print("%s %s" % (pressed_pin, state))


def callback(pin, st):
    global state, pressed_pin
    old_state = state
    new_state = st
    old_pressed_pin = pressed_pin
    new_pressed_pin = pin
    if old_state == new_state:
        return
    else:
        state = new_state
        if old_pressed_pin == new_pressed_pin:
            return
        else:
            pressed_pin = new_pressed_pin
            do_action(pressed_pin, state)


while True:
    # with canvas(device) as draw:
    if GPIO.input(KEY_UP_PIN): # button is released
        callback(KEY_UP_PIN, "released")
    else: # button is pressed:
        callback(KEY_UP_PIN, "pressed")

    if GPIO.input(KEY_LEFT_PIN): # button is released
        callback(KEY_LEFT_PIN, "released")
    else: # button is pressed:
        callback(KEY_LEFT_PIN, "pressed")

    if GPIO.input(KEY_RIGHT_PIN): # button is released
        callback(KEY_RIGHT_PIN, "released")
    else: # button is pressed:
        callback(KEY_RIGHT_PIN, "pressed")

    if GPIO.input(KEY_DOWN_PIN): # button is released
        callback(KEY_DOWN_PIN, "released")
    else: # button is pressed:
        callback(KEY_DOWN_PIN, "pressed")

    if GPIO.input(KEY_PRESS_PIN): # button is released
        callback(KEY_PRESS_PIN, "released")
    else: # button is pressed:
        callback(KEY_PRESS_PIN, "pressed")

    if GPIO.input(KEY1_PIN): # button is released
        callback(KEY1_PIN, "released")
    else: # button is pressed:
        callback(KEY1_PIN, "pressed")


    if GPIO.input(KEY2_PIN): # button is released
        callback(KEY2_PIN, "released")
    else: # button is pressed:
        callback(KEY2_PIN, "pressed")

    if GPIO.input(KEY3_PIN): # button is released
        callback(KEY3_PIN, "released")
    else: # button is pressed:
        callback(KEY3_PIN, "pressed")

