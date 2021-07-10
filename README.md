# ESP32 Camera with Python

## specs

* Camera Device
    * ESP32 PSRAM Timer Camera X (M5Stack)

* Controller Device
    * Linux machine with Wi-Fi and Bluetooth(e.g. Raspberry Pi)
    * python3
    * Wi-Fi
    * BLE


## install to Camera Device

1. Open this directory by Arduino IDE
2. Compile to ESP32


## install to Controller Device

1. Start Linux
2. Open Wi-Fi settings


## usage

1. Copy py/variables_sample.py to py/variables.py. And change ssid, ps to your Wi-Fi.
2. Start esp32 by connect power.
3. `$ python3 py/app.py`