# Timer Camera X タイムラプスカメラ

M5Stack Timer Camera X とRaspberry Piを使用したタイムラプスカメラ。

Timer Camera XでWebサーバーを起動し、Raspberry Piで画像を取得する。

## スペック & マシン

* カメラ - ESP32 PSRAM Timer Camera X (M5Stack)
    * Arduino

* コントローラ - Raspberry Pi (Wi-Fiモデル)
    * python3 / pip3
    * Wi-Fi
    * BLE
    * OLED Screen and buttons(HAT)

* PC(Timer Camera Xへのコンパイル)
    * Arduino IDE or platform.io

## 1. コンパイル

### Arduinoでのコンパイル

1. このリポジトリを`git clone`する
2. Arduino IDE でこのリポジトリのルートを開く
3. Arduino IDE のセットアップ
     M5Stack-Timer-Cam を ESP32 Arduino に設定します (M5Stack Arduinoではない)
4. Timer Camera X を PC に接続
5. Timer Camera X にコンパイル

### PlatformIOでのコンパイル

1. このリポジトリを`git clone`する
2. VS Code をインストールし、VS Code P起動して、platformIO 拡張機能をインストールする
    M5Stack-Timer-Camを設定
3. VS Code でこのリポジトリを開く
4. PlatformIO 拡張機能で ar ディレクトリを開く
5. タイマーカメラ X を PC に接続
6. Timer Camera X にコンパイル


## 2. Raspberry Piの設定

1. Raspberry Pi の`home`にこのリポジトリを`git clone`
2. `cd ~/<this repository name>`
3. `$ cp py/variables_sample.py py/variables.py`
4. Pythonとライブラリをインストール
    ```bash
    $ sudo apt install -y python3 python3-pip ffmpeg
    $ sudo pip3 install bleak
    $ sudo pip3 install aioconsole
    $ sudo pip3 install psutil
    ```

## 3. Wi-Fiの設定

AまたはBの方法でWi-Fiを設定します。
AはRaspberry PiとTimer Camera Xのみ。
B には Raspberry Pi、Timer Camera X、Wi-Fi ルーターが必要です。
Bの方が簡単ですが、屋外での使用にはAがおすすめです。


### A. Raspberry Pi を Wi-Fi アクセスポイントとして使用する方法（RTL8188EUS USB ドングルの場合）

0. ラズベリーパイを起動
1. RTL8188EUS ドングル ドライバーをインストールします。
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

py/variables.py の ssid と wpa_passphrase(ps)を変更します。

6. `$ sudo vim /etc/hostapd/hostapd.conf`

py/variables.pyに書いたssid と wpa_passphrase(ps) を /etc/hostapd/hostapd.conf に書きます。

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