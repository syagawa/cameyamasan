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

### platformioでのコンパイル

1. PC に VS Code をインストールし、VS Code を起動して、platformio 拡張機能をインストールします。
    M5Stack-Timer-Camを設定
2. このリポジトリを git clone します。
3. VS Code でこのリポジトリを開きます。
4. platformio 拡張機能で ar ディレクトリを開きます。
5. タイマーカメラ X を PC に接続します。
6. Timer Camera X にコンパイルします。