# Timelapse Camera controlled by Raspberry Pi

Time-lapse camera using M5Stack Timer Camera X and Raspberry Pi.

Set Timer Camera X and Raspberry Pi on the same Wi-Fi network, start a web server on Timer Camera X, and get images with HTTP requests from Raspberry Pi.

## Specs

Use M5Stack Timer Camera X and Raspberry Pi Wi-Fi model. The recommended model is Raspberry Pi Zero WH. I recommend the one with the pin header because the HAT is also used.

* Camera - ESP32 PSRAM Timer Camera X (M5Stack)
    * https://shop.m5stack.com/products/esp32-psram-timer-camera-x-ov3660
    * Arduino
    * Power
        Mobile battery ( e.g. Anker PowerCore Fusion 5000 https://www.ankerjapan.com/products/a1621 )
        or USB power

* Controller - Raspberry Pi (with Wi-Fi / Pin Header e.g. Raspberry Pi Zero WH)
    * python3 / pip3
    * Wi-Fi
    * BLE
    * OLED Screen and buttons(HAT)
        128x64, 1.3inch OLED display HAT for Raspberry Pi https://www.waveshare.com/1.3inch-oled-hat.htm
    * Power
        Mobile battery ( e.g. cheero Canvas 3200mAh IoT 機器対応 https://cheero.shop/products/che-061 )
        or USB power
    * micro SD card

* PC for compiling to Timer Camera X (Windows, Mac or Linux)
    * Arduino IDE or VSCode + platformIO

## 1. Compile Timer Camera X

Compile software for camera on PC and write it to Timer Camera X.

### Compile source to Camera by Arduino in PC

1. Install Arduino IDE to PC.
2. git clone this repository.
3. Open this repository's root by Arduino IDE.
4. Setup Arduino IDE
    set M5Stack-Timer-Cam in ESP32 Arduino( not M5Stack Arduino)
5. Connect Timer Camera X to PC by USB.
6. Compile to Timer Camera X.

### Compile source to Camera by PlatformIO in PC

1. Install VSCode & PlatformIO to PC.
2. git clone this repository.
3. Install VSCode on pc, start VSCode, then install PlatformIO extension.
    * Set M5Stack-Timer-Cam
4. Open this repository in VSCode.
5. Open ar diretory by PlatformIO extension.
6. Connect Timer Camera X to PC by USB.
7. Compile to Timer Camera X.

*** Compiling on PlatformIO is not well tested, so I recommend compiling on Arduino. ***

## 2. Raspberry Pi settings

1. Install Raspberry Pi OS to Raspberry Pi. Refer to the following link for the installation. https://www.raspberrypi.com/documentation/computers/getting-started.html
2. Install git.
    ```bash
    $ sudo apt update
    $ sudo apt upgrade
    $ sudo apt install git
    ```
3. Start Raspberry Pi and git clone this repository in Raspberry Pi's `home`.
4. `$ cd ~/<this repository name>`
5. `$ cp py/variables_sample.py py/variables.py`
6. Install python3, pip and ffmpeg.
    ```bash
    $ sudo apt install -y python3 python3-pip ffmpeg
    $ sudo pip3 install bleak
    $ sudo pip3 install aioconsole
    $ sudo pip3 install psutil
    ```

## 3. Wi-Fi settings

Set up Wi-Fi by A or B below.
A is only Raspberry Pi and Timer Camera X. 
B requires a Raspberry Pi, a Timer Camera X and a Wi-Fi router.
B is easier, but A is recommended for outdoor use.

### A. How to use Raspberry Pi as a Wi-Fi access point (Case of RTL8188EUS USB dongle)

1. Start Raspberry Pi
2. Install RTL8188EUS dongle driver 
    * http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/
    * Example of raspberry pi zero w http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/8188eu-5.4.83-1379.tar.gz

3. `$ iwconfig` to see if wlan1 exists

4. Install
```bash
$ sudo apt update
$ sudo apt upgrade -y
$ sudo apt install hostapd
$ sudo apt install dnsmasq
```

5. Edit /etc/dhcpcd.conf

`$ sudo vim /etc/dhcpcd.conf`

```
interface wlan1
 static ip_address=192.168.2.1/24
 static routers=192.168.2.1
 static domain_name_servers=192.168.2.1
 static broadcast 192.168.2.255
```

6. Edit ./py/variables.py

`$ vim ./py/variables.py.`

Write ssid and wpa_passphrase(ps) in py/variables.py.

7. Edit /etc/hostapd/hostapd.conf

`$ sudo vim /etc/hostapd/hostapd.conf`

Write ssid and wpa_passphrase(ps) from py/variables.py.

```
interface=<wlan1>
driver=nl80211
ssid=MY-RP-SERVER
hw_mode=g
#channel=11
channel=3
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ieee80211n=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
wpa_passphrase=Password
```

8. Edit dnsmsq

`$ sudo vim /etc/dnsmasq.conf`

```
interface=wlan1
dhcp-range=192.168.2.2,192.168.2.100,255.255.255.0,24h
```

9. Edit syctl.conf

`$ sudo vim /etc/sysctl.conf`

Uncomment the next line to enable packet forwarding for IPv4.

```
net.ipv4.ip_forward=1
```
`$ sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE`
`$ sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"`

<!-- # select legacy
$ sudo update-alternatives --config iptables

sudo iptables --table nat --append POSTROUTING --out-interface wlan0 -j MASQUERADE
sudo iptables --append FORWARD --in-interface wlan1 -j ACCEPT -->


10. unmask settings
```
$ sudo systemctl stop hostapd
$ sudo systemctl unmask hostapd
($ sudo hostapd /etc/hostapd/hostapd.conf)
$ sudo systemctl enable hostapd
$ sudo systemctl start hostapd
$ sudo systemctl start dnsmasq
```

11. Check Wi-Fi Access Point
```
$ python -m http.server 3000
```
Connect MY-RP-SERVER from PC or Smartphone.
Open 192.168.2.1:3000.

12. add below to /etc/rc.local at before exit 0
`$ sudo vim /etc/rc.local`

```
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sh -c "iptables-save > /etc/iptables.ipv4.nat"

service dnsmasq stop
sleep 8
service dnsmasq start
iptables-restore < /etc/iptables.ipv4.nat
sleep 3
service hostapd restart
```




13. check connecting internet

```
$ ping google.com

# if nothing receives
$ sudo dhclient wlan0
```

* reference pages
    * https://ccie-go.com/raspberry-pi-4-chuukeiki/#toc8
    * https://passe-de-mode.uedasoft.com/ja/tips/software/device/raspberrypi/2019.11.buster_r8188eu.html#%E8%83%8C%E6%99%AF
    * https://zenn.dev/yutafujii/books/fcb457e798a3d5/viewer/fe7472


### B. Use Wi-Fi router

Check Wi-Fi router's ssid and password.

1. Write ssid and ps(password) in py/variables.py.

`$ vim ./py/variables.py.`





## Usage
1. Set HAT(OLED Screen and buttons HAT) to Raspberry Pi.
2. Start Raspberry Pi by connect USB Power.
3. `$ python3 py/app.py` in Raspberry Pi's this repository home.
4. Start Timer Camera X by connect USB Power.


### Start app at Raspberry Pi boots

```bash
$ cd <home directory of this repository>
$ cp ./service/example-camerawithpy.service ./camerawithpy.service
```
Edit <this app directory name> in ./camerawithpy.service and Uncomment
Edit <this py directory name> in ./start.sh.

```bash
$ chmod a+x ./py/*
$ chmod a+x ./py/interface/*
$ chmod a+x ./start.sh
$ sudo cp ./camerawithpy.service /etc/systemd/system/
$ systemctl enable camerawithpy.service
$ sudo reboot
```

* reference sites
    * https://superuser.com/questions/544399/how-do-you-make-a-systemd-service-as-the-last-service-on-boot

#### Not start in boot
```bash
$ systemctl disable camerawithpy.service
```

### Start shooting

1. Turn on the power of Timer Camera X and Raspberry Pi.
2. If app is starts, "app start!" on the OLED screen on RPI.
3. Raspberry Pi connects Timer Camera X and Timer Camera X starts wi-fi server automatically.
4. Start shooting.
5. Press the button up or down to display `stopshoot ?` on the OLED screen and press `key1` to finish shooting.

### make timelapse video

Create a video after shooting.

```
# in Raspberry Pi
$ cd <this repository root>
$ ./make_static_video_current_dir.sh
```

Rreferred to the following page
https://gist.github.com/CMCDragonkai/e00d114b43e38cb2c1b04594229e1df6


### Change settings of shooting conditions

`$ cp py/variables_sample.py py/variables.py`
Change `py/variables.py`.




```
max_camera_shooting_counts: max shooting counts
camera_shooting_interval: shooting interval in seconds
```