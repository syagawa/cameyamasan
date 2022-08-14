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

1. このリポジトリを git clone します。
2. Arduino IDE でこのリポジトリのルートを開きます。
3. Arduino IDE のセットアップ
     M5Stack-Timer-Cam を ESP32 Arduino に設定します (M5Stack Arduino ではありません)。
4. Timer Camera X を PC に接続します。
5. Timer Camera X にコンパイルします。