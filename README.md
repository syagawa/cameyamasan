# ESP32 Camera controlled by Python

Wi-Fi ESP32 Camera controlled by python on Linux.

## specs

* Camera
    * ESP32 PSRAM Timer Camera X (M5Stack)

* Controller
    * Linux machine (e.g. Raspberry Pi)
        * python3
        * Wi-Fi
        * BLE

* PC(Windows or Mac or Linux) for compiling to camera
    * Arduino IDE


## Compile source to Camera @PC

1. git clone this repository to Linux machine.
2. Open this directory by Arduino IDE
3. Connect ESP32 Camera to PC.
4. Compile to ESP32 Camera


## Settings @Controller

1. git clone this repository to Linux machine.
2. Open this directory
3. $ cp py/variables_sample.py py/variables.py
4. Write ssid and ps to py/variables.py


### Using Linux as a Wi-Fi access point

1. Start Linux
2. install
```bash
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install hostapd
$ sudo apt install isc-dhcp-server
```

## Usage

1. Start esp32 camera by connect power.
2. `$ python3 py/controller.py` @Controller
