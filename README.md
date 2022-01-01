# ESP32 Camera controlled by Python

Wi-Fi ESP32 Camera controlled by python on Linux.

## specs

* Camera
    * ESP32 PSRAM Timer Camera X (M5Stack)

* Controller
    * Linux machine (e.g. Raspberry Pi)
        * python3 / pip3
            * pillow
            * bleak
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
3. $ cp py/variables_sample.py py/variables.py`
4. Write ssid and ps to py/variables.py
5. install library
```bash
$ sudo pip3 install bleak
$ sudo pip3 install aioconsole
```


### Using Linux as a Wi-Fi access point

0. Start Linux
1. Install RTL8188EUS dongle driver 
    * http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/
    * example raspberry pi zero w http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/8188eu-5.4.83-1379.tar.gz
2. `$ iwconfig` to see if wlan1 exists

2. install
```bash
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install hostapd
$ sudo apt install dnsmasq
# $ sudo apt install isc-dhcp-server
```
3. `$ sudo vim /etc/dhcpcd.conf`
```
interface wlan1
 static ip_address=192.168.2.1/24
 static routers=192.168.2.1
 static domain_name_servers=192.168.2.1
 static broadcast 192.168.2.255
```


* reference sites
    * https://ccie-go.com/raspberry-pi-4-chuukeiki/#toc8
    * https://passe-de-mode.uedasoft.com/ja/tips/software/device/raspberrypi/2019.11.buster_r8188eu.html#%E8%83%8C%E6%99%AF



## Usage

1. Start esp32 camera by connect power.
2. `$ python3 py/controller.py` @Controller


### start app in boot

```bash
$ cd <this repository directory>
$ cp ./service/example-camerawithpy.service ./camerawithpy.service
```
Edit <this app directory name> in ./camerawithpy.service

```bash
$ chmod a+x ./py/*
$ chmod a+x ./py/interface/*
$ sudo cp ./camerawithpy.service /etc/systemd/system/
$ systemctl enable camerawithpy.service
$ sudo reboot
```

#### not start in boot
```bash
$ systemctl disable camerawithpy.service
```

