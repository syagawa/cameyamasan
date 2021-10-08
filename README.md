# ESP32 Camera with Python

Wi-Fi ESP32 Camera controlled by python on Linux.

## specs

* Camera
    * ESP32 PSRAM Timer Camera X (M5Stack)

* Controller
    * Linux machine (e.g. Raspberry Pi)
        * python3
        * Wi-Fi
        * BLE

* PC(Windows or Mac or Linux)
    * Arduino IDE


## install

git clone this repository to Linux machine.

## settings

### Camera

1. Open this directory by Arduino IDE
2. Connect ESP32 Camera to PC.
3. Compile to ESP32 Camera


### Controller

1. Open this directory
2. $ cp py/variables_sample.py py/variables.py
3. Write ssid and ps to py/variables.py


## Using Linux as a Wi-Fi access point

1. Start Linux
2. install
```bash
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install hostapd
$ sudo apt install isc-dhcp-server
```

## usage

1. Start esp32 by connect power.
2. `$ python3 py/controller.py` @Controller
