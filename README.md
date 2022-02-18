# ESP32 Camera controlled by Raspberry Pi

Timer Camera X (M5Stack) controlled by python on Raspberry Pi.

## specs

* Camera Module
    * ESP32 PSRAM Timer Camera X (M5Stack)
        * Arduino

* Controller Module
    * Raspberry Pi (with Wi-Fi)
        * python3 / pip3
            * pillow
            * bleak
        * Wi-Fi
        * BLE

* PC(Win or Mac or Linux) for compiling to camera
    * Arduino IDE


## Compile source to Camera @PC

1. git clone this repository to PC.
2. Open this directory by Arduino IDE.
3. Connect Timer Camera X to PC.
4. Compile to Timer Camera X.


## Settings @Controller

1. git clone this repository to Raspberry Pi's `home`.
2. `cd ~/<this repository name>`
3. `$ cp py/variables_sample.py py/variables.py`
4. Write ssid and ps to py/variables.py
5. install python and libraries
```bash
$ sudo apt install -y python3 python3-pip
$ sudo pip3 install bleak
$ sudo pip3 install aioconsole
$ sudo pip3 install psutil
```


### How to use Raspberry Pi as a Wi-Fi access point (Case of RTL8188EUS USB dongle)

0. Start Raspberry Pi
1. Install RTL8188EUS dongle driver 
    * http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/
    * example raspberry pi zero w http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/8188eu-5.4.83-1379.tar.gz

2. `$ iwconfig` to see if wlan1 exists

3. install
```bash
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install hostapd
$ sudo apt install dnsmasq
```

4. `$ sudo vim /etc/dhcpcd.conf`
```
interface wlan1
 static ip_address=192.168.2.1/24
 static routers=192.168.2.1
 static domain_name_servers=192.168.2.1
 static broadcast 192.168.2.255
```

5. `$ sudo vim /etc/hostapd/hostapd.conf`

```
interface=<wlan1>
driver=nl80211
ssid=MY-RP-SERVER
hw_mode=g
#channel=3
channel=11
#wmm_enabled=0
wme_enabled=1
macaddr_acl=0
ignore_broadcast_ssid=0
auth_algs=1
ieee80211n=1
wpa=2
wpa_key_mgmt=WPA-PSK
#rsn_pairwise=CCMP
wpa_pairwise=CCMP
wpa_passphrase=Password
```

6. `$ sudo vim /etc/dnsmasq.conf`
```
interface=wlan1
dhcp-range=192.168.2.2,192.168.2.100,255.255.255.0,24h
```

7. `$ sudo vim /etc/sysctl.conf`
```
# Uncomment the next line to enable packet forwarding for IPv4
net.ipv4.ip_forward=1
```
`$ sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"`
`$ sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`

8. unmask
```
$ sudo systemctl stop hostapd
$ sudo systemctl unmask hostapd
($ sudo hostapd /etc/hostapd/hostapd.conf)
$ sudo systemctl enable hostapd
$ sudo systemctl start hostapd
$ sudo systemctl start dnsmasq
```

9. check Wi-Fi Access Point
```
$ python -m http.server 3000
```
Connect MY-RP=SERVER from PC or Smartphone.
Open 192.168.2.1:3000 by Browser in PC or Smartphone.


* reference sites
    * https://ccie-go.com/raspberry-pi-4-chuukeiki/#toc8
    * https://passe-de-mode.uedasoft.com/ja/tips/software/device/raspberrypi/2019.11.buster_r8188eu.html#%E8%83%8C%E6%99%AF
    * https://zenn.dev/yutafujii/books/fcb457e798a3d5/viewer/fe7472



## Usage

1. Start esp32 camera by connect power.
2. `$ python3 py/app.py` @Controller


### start app in boot

```bash
$ cd <this repository directory>
$ cp ./service/example-camerawithpy.service ./camerawithpy.service
```
Edit <this app directory name> in ./camerawithpy.service
Edit <this py directory name> in ./start.sh

```bash
$ chmod a+x ./py/*
$ chmod a+x ./py/interface/*
$ chmod a+x ./start.sh
$ sudo cp ./camerawithpy.service /etc/systemd/system/
$ systemctl enable camerawithpy.service
$ sudo reboot
```

#### not start in boot
```bash
$ systemctl disable camerawithpy.service
```

