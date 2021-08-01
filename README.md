# ESP32 Camera with Python

Wi-Fi Camera controlled by python on Linux.

## specs

* Camera
    * ESP32 PSRAM Timer Camera X (M5Stack)

* Controller
    * Linux machine (e.g. Raspberry Pi)
        * python3
        * Wi-Fi
        * BLE


## install to Camera

1. Open this directory by Arduino IDE
2. Compile to ESP32


## install to Controller

1. git clone this repository to Linux machine.
2. $ cp py/variables_sample.py py/variables.py
3. write wi-fi info to py/variables.py


### Using Linux as a Wi-Fi access point

1. Start Linux
2. install
```bash
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install hostapd
$ sudo apt install isc-dhcp-server
```





## usage

1. Copy py/variables_sample.py to py/variables.py. And change ssid, ps to your Wi-Fi.
2. Start esp32 by connect power.
3. `$ python3 py/app.py`