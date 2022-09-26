# Timer Camera XをRaspberry Piで制御するタイムラプスカメラ

M5Stack Timer Camera X とRaspberry Piを使用したタイムラプスカメラ。

Timer Camera XとRaspberry Piを同じWi-Fiネットワーク上に置き、Timer Camera XでWebサーバーを起動し、Raspberry PiからのHTTPリクエストで画像を取得する。

## スペック

* カメラ - ESP32 PSRAM Timer Camera X (M5Stack)
    * M5StackのTimer Camera Xを使用 https://shop.m5stack.com/products/esp32-psram-timer-camera-x-ov3660
    * Arduino

* コントローラ - Raspberry Pi (Wi-Fiモデル)
    * python3 / pip3
    * Wi-Fi
    * BLE
    * OLED スクリーンとボタンの付いたHAT
        128x64, 1.3inch OLED display HAT for Raspberry Pi https://www.waveshare.com/1.3inch-oled-hat.htm

* PC(Timer Camera Xへのコンパイル)
    * Arduino IDE もしくは platformIO

## 1. Timer Camera X へのコンパイル

### Arduinoでのコンパイル

0. Arduino IDEのインストール
1. このリポジトリを`git clone`する
2. Arduino IDE でこのリポジトリのルートを開く
3. Arduino IDE のセットアップ
     M5Stack-Timer-Cam を ESP32 Arduino に設定します (M5Stack Arduinoではない)
4. Timer Camera X を PC に接続
5. Timer Camera X にコンパイル

### PlatformIOでのコンパイル

0. VS CodeとPlatformIOのインストール
1. このリポジトリを`git clone`する
2. VS Code をインストールし、VS Code P起動して、platformIO 拡張機能をインストールする
    M5Stack-Timer-Camを設定
3. VS Code でこのリポジトリを開く
4. PlatformIO 拡張機能で ar ディレクトリを開く
5. タイマーカメラ X を PC に接続
6. Timer Camera X にコンパイル


## 2. Raspberry Piの設定

1. Raspberry Pi の`home`にこのリポジトリを`$ git clone`
2. `$ cd ~/<this repository name>`
3. `$ cp py/variables_sample.py py/variables.py`
4. Python3とpipとライブラリをインストール
    ```bash
    $ sudo apt install -y python3 python3-pip ffmpeg
    $ sudo pip3 install bleak
    $ sudo pip3 install aioconsole
    $ sudo pip3 install psutil
    ```

## 3. Wi-Fiの設定

AまたはBの方法でWi-Fiを設定します。
AはRaspberry PiとTimer Camera Xのみ。
Bには Raspberry Pi、Timer Camera X、Wi-Fi ルーターが必要です。
Bの方が簡単ですが、屋外での使用にはAがおすすめです。


### A. Raspberry Pi を Wi-Fi アクセスポイントとして使用する方法（RTL8188EUS USB ドングルを使用）

0. ラズベリーパイを起動
1. RTL8188EUS ドングル ドライバーをインストールする
     * http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/
     * ラズパイゼロの例 http://downloads.fars-robotics.net/wifi-drivers/8188eu-drivers/8188eu-5.4.83-1379.tar.gz

2. `$ iwconfig` で wlan1 が存在するかどうかを確認する

3. インストール
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

5. `$ vim ./py/variables.py.`

py/variables.py の ssid と wpa_passphrase(ps)を変更

6. `$ sudo vim /etc/hostapd/hostapd.conf`

py/variables.pyに書いたssid と wpa_passphrase(ps) と同じ値を /etc/hostapd/hostapd.conf の下記部分に設定

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

7. dnsmsqを編集

`$ sudo vim /etc/dnsmasq.conf`
```
interface=wlan1
dhcp-range=192.168.2.2,192.168.2.100,255.255.255.0,24h
```

8. sysctl.confを編集

 `$ sudo vim /etc/sysctl.conf`

net.ipv4.ipforward=0の部分のコメントアウトをキャンセルして、値を1にします。

```
net.ipv4.ip_forward=1

```
`$ sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE`
`$ sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"`

9. unmaskの設定
```
$ sudo systemctl stop hostapd
$ sudo systemctl unmask hostapd
($ sudo hostapd /etc/hostapd/hostapd.conf)
$ sudo systemctl enable hostapd
$ sudo systemctl start hostapd
$ sudo systemctl start dnsmasq
```

10. Wi-Fi アクセスポイントの確認
```
$ python -m http.server 3000
```

PCかスマホでMY-RP=SERVERに接続し、ブラウザで192.168.2.1:3000を開きます。

11. `$ sudo vim /etc/rc.local`で `exit 0`の直前の行に下記の記述を追加する

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

12. インターネットへの接続を確認

```
$ ping google.com

# 何も返ってこないようなら
$ sudo dhclient wlan0
```

* 参考サイト
    * https://ccie-go.com/raspberry-pi-4-chuukeiki/#toc8
    * https://passe-de-mode.uedasoft.com/ja/tips/software/device/raspberrypi/2019.11.buster_r8188eu.html#%E8%83%8C%E6%99%AF
    * https://zenn.dev/yutafujii/books/fcb457e798a3d5/viewer/fe7472

### B. Wi-Fi ルータを使用

Wi-Fi ルーターのssid と passwordを確認

1. py/variables.pyにssidとpasswordを記入

`$ vim ./py/variables.py.`


## 使用方法

1. Timer Camera XにUSB電源を接続して起動
2. Raspberry Piでこのレポジトリのホームへ行き `$ python3 py/app.py`を実行


### 起動時にスタートさせる方法

```bash
$ cd <このレポジトリ>
$ cp ./service/example-camerawithpy.service ./camerawithpy.service
```
`./camerawithpy.service` の <this app directory name> を編集
`./start.sh` の <this py directory name> を編集

```bash
$ chmod a+x ./py/*
$ chmod a+x ./py/interface/*
$ chmod a+x ./start.sh
$ sudo cp ./camerawithpy.service /etc/systemd/system/
$ systemctl enable camerawithpy.service
$ sudo reboot
```

* 参照サイト
    * https://superuser.com/questions/544399/how-do-you-make-a-systemd-service-as-the-last-service-on-boot

#### 起動時にスタートさせない場合
```bash
$ systemctl disable camerawithpy.service
```

### 撮影開始

1. Timer Camera XとRassberry Piを起動
2. Rassberry Piの OLEDスクリーンに "app start!"と表示されます
3. Rassberry PiがTimer Camera Xに接続し、CameraのWi-Fiサーバーがスタートします
4. 撮影が開始されます

### 動画の作成

撮影後の動画の作成

```
$ cd <撮影した画像のあるディレクトリ>
$ ls ./*.jpg | awk '{ printf "mv %s ./source%04d.jpg\n", $0, NR }' | sh

$ ffmpeg -f image2 -r 3 -i ./source%04d.jpg -r 3 -an -vcodec libx264 -pix_fmt yuv420p ./video.mp4

# または

$ ffmpeg \
  -pattern_type glob \
  -i '*.jpg' \
  -vf 'zoompan=d=(0.2+0.1)/0.1:s=800x600:fps=1/0.1,framerate=25:interp_start=0:interp_end=255:scene=100' \
  -c:v mpeg4 \
  -q:v 1 \
  video.mp4
```

参照ページ
https://gist.github.com/CMCDragonkai/e00d114b43e38cb2c1b04594229e1df6
