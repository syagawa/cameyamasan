# Timelapse Camera controlled by Raspberry Pi

Time-lapse camera using M5Stack Timer Camera X and Raspberry Pi.

Set Timer Camera X and Raspberry Pi on the same Wi-Fi network, start a web server on Timer Camera X, and get images with HTTP requests from Raspberry Pi.


## Specs

* Camera - ESP32 PSRAM Timer Camera X (M5Stack)
    * https://shop.m5stack.com/products/esp32-psram-timer-camera-x-ov3660
    * Arduino

* Controller - Raspberry Pi (with Wi-Fi)
    * python3 / pip3
    * Wi-Fi
    * BLE
    * OLED Screen and buttons(HAT)
        128x64, 1.3inch OLED display HAT for Raspberry Pi https://www.waveshare.com/1.3inch-oled-hat.htm

* PC for compiling to Timer Camera X
    * Arduino IDE or platformIO

## 1. Compile Timer Camera X

### Compile source to Camera by Arduino in PC

0. Install Arduino IDE
1. git clone this repository.
2. Open this repository's root by Arduino IDE.
3. setup Arduino IDE
    set M5Stack-Timer-Cam in ESP32 Arduino( not M5Stack Arduino)
4. Connect Timer Camera X to PC.
5. Compile to Timer Camera X.

### Compile source to Camera by PlatformIO in PC

0. Install VSCode & PlatformIO
1. git clone this repository.
2. Install VSCode on pc, start VSCode, then install PlatformIO extension.
    set M5Stack-Timer-Cam
3. Open this repository in VSCode.
4. Open ar diretory by PlatformIO extension.
5. Connect Timer Camera X to PC.
6. Compile to Timer Camera X.


## 2. Raspberry Pi settings

1. git clone this repository in Raspberry Pi's `home`.
2. `$ cd ~/<this repository name>`
3. `$ cp py/variables_sample.py py/variables.py`
4. install python3, pip and python libraries
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

0. Start Raspberry Pi
1. Install RTL8188EUS dongle driver 
    * http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/
    * example raspberry pi zero w http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/8188eu-5.4.83-1379.tar.gz

2. `$ iwconfig` to see if wlan1 exists

3. install
```bash
$ sudo apt update
$ sudo apt upgrade -y
$ sudo apt install hostapd
$ sudo apt install dnsmasq
```

4. /etc/dhcpcd.conf

`$ sudo vim /etc/dhcpcd.conf`

```
interface wlan1
 static ip_address=192.168.2.1/24
 static routers=192.168.2.1
 static domain_name_servers=192.168.2.1
 static broadcast 192.168.2.255
```

5. ./py/variables.py.

`$ vim ./py/variables.py.`

Write ssid and wpa_passphrase(ps) in py/variables.py.

6. /etc/hostapd/hostapd.conf

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

7. edit dnsmsq

`$ sudo vim /etc/dnsmasq.conf`

```
interface=wlan1
dhcp-range=192.168.2.2,192.168.2.100,255.255.255.0,24h
```

8. edit syctl.conf

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


9. unmask settings
```
$ sudo systemctl stop hostapd
$ sudo systemctl unmask hostapd
($ sudo hostapd /etc/hostapd/hostapd.conf)
$ sudo systemctl enable hostapd
$ sudo systemctl start hostapd
$ sudo systemctl start dnsmasq
```

10. check Wi-Fi Access Point
```
$ python -m http.server 3000
```
Connect MY-RP-SERVER from PC or Smartphone.
Open 192.168.2.1:3000 by Browser in PC or Smartphone.

11. add below to /etc/rc.local at before exit 0

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

12. check connecting internet

```
$ ping google.com

# if not receive
$ sudo dhclient wlan0

```

* reference sites
    * https://ccie-go.com/raspberry-pi-4-chuukeiki/#toc8
    * https://passe-de-mode.uedasoft.com/ja/tips/software/device/raspberrypi/2019.11.buster_r8188eu.html#%E8%83%8C%E6%99%AF
    * https://zenn.dev/yutafujii/books/fcb457e798a3d5/viewer/fe7472


### B. Use Wi-Fi router

Check Wi-Fi router's ssid and password.

1. `$ vim ./py/variables.py.`

Write ssid and ps(password) in py/variables.py.


## Usage

1. Start esp32 camera by connect USB Power.
2. `$ python3 py/app.py` in Raspberry Pi's this repository home.


### start app in boot

```bash
$ cd <this repository directory>
$ cp ./service/example-camerawithpy.service ./camerawithpy.service
```
Edit <this app directory name> in ./camerawithpy.service
Edit <absolute path of this app directory> in ./camerawithpy.service and Uncomment
Edit <this py directory name> in ./start.sh

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

#### not start in boot
```bash
$ systemctl disable camerawithpy.service
```

### start shooting

1. Turn on the power of Timer Camera X and Raspberry Pi.
2. If app is starts, "app start!" on the OLED screen on RPI.
3. Connect timerx and start wi-fi server in Timer Camera X automatically.
4. start shooting!!!

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