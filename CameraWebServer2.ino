//#include <M5Stack.h>

#include "esp_camera.h"
#include <WiFi.h>

//
// WARNING!!! PSRAM IC required for UXGA resolution and high JPEG quality
//            Ensure ESP32 Wrover Module or other board with PSRAM is selected
//            Partial images will be transmitted if image exceeds buffer size
//

// Select camera model
//#define CAMERA_MODEL_WROVER_KIT // Has PSRAM
//#define CAMERA_MODEL_ESP_EYE // Has PSRAM
#define CAMERA_MODEL_M5STACK_PSRAM // Has PSRAM
// #define CAMERA_MODEL_M5STACK_V2_PSRAM // M5Camera version B Has PSRAM
//#define CAMERA_MODEL_M5STACK_WIDE // Has PSRAM
//#define CAMERA_MODEL_M5STACK_ESP32CAM // No PSRAM
//#define CAMERA_MODEL_AI_THINKER // Has PSRAM
//#define CAMERA_MODEL_TTGO_T_JOURNAL // No PSRAM

#include "camera_pins.h"
// #include "led.h"
//#include "bmm8563.h"
#include "constants.h"


#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

// #include <WiFiMulti.h>

#define SERVICE_UUID           "00001141-0000-1000-8000-00805f9b34fb" // UART service UUID
#define CHARACTERISTIC_UUID_RX "00001142-0000-1000-8000-00805f9b34fb"
#define CHARACTERISTIC_UUID_TX "00001143-0000-1000-8000-00805f9b34fb"


#include <Arduino_JSON.h>
#include "EEPROM.h"

JSONVar receivedObj;

bool startedCameraServer = false;
bool lighted = false;
void startCameraServer();

char* var_ssid = "";
char* var_ps = "";

// BLE
BLEServer *pServer = NULL;
BLEService *pService = NULL;
BLEAdvertising *pAdvertising = NULL;

BLECharacteristic * pTxCharacteristic;
bool deviceConnected = false;
bool oldDeviceConnected = false;
bool deviceConnectedOneLoopBefore = false;
boolean bleDataIsReceived;
std::string storedValue;
portMUX_TYPE storeDataMux = portMUX_INITIALIZER_UNLOCKED;
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};
class MyCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      std::string rxValue = pCharacteristic->getValue();
      Serial.println("write in esp32");

      if (rxValue.length() > 0) {
        portENTER_CRITICAL_ISR(&storeDataMux);
        storedValue = rxValue;
        receivedObj = JSON.parse(storedValue.c_str());
        bleDataIsReceived = true;
        portEXIT_CRITICAL_ISR(&storeDataMux);
      }
    }

    void onRead(BLECharacteristic *pCharacteristic) {
      Serial.println("read in esp32");
      pCharacteristic->setValue("Hello from esp32! onRead");
    }
};



int address_ssid = 0;
int address_ps = 128;
int length_for_rom = 100;
int rom_size = 500;
void writeWifiData(String ssid, String ps){
  EEPROM.writeString(address_ssid, ssid);
  EEPROM.writeString(address_ps, ps);
}

void readWifiData(){
  String ssid = EEPROM.readString(address_ssid);
  String ps = EEPROM.readString(address_ps);
  Serial.println(ssid);
  Serial.println(ps);
  Serial.println("readed?");
}

void writeDataToRom(String String_data, int start, int len) {
  byte Byte_data[len];
  String_data.getBytes(Byte_data, len);
  int k;
  for (k = start; k < len && Byte_data[k] != '\0'; k++) {
    EEPROM.write(k, Byte_data[k]);
  }
  EEPROM.write(k, '\0');
}

String readDataFromRom(int start, int len) {
  String data_from_rom;
  for (int i = start; i < len && EEPROM.read(i) != '\0' ; i++) {
    char c = EEPROM.read(i);
    data_from_rom = data_from_rom + String(c);
  }
  return data_from_rom;
}
void clearRom() {
  if (!EEPROM.begin(rom_size)){
    Serial.println("Failed to initialise EEPROM");
    Serial.println("Restarting...");
    delay(1000);
    ESP.restart();
  }

  Serial.println("in clearRom0");
  for(int i = 0; i < rom_size; i++){
    EEPROM.write(i, 0);
  }
  Serial.println("in clearRom1");
  EEPROM.end();
  // EEPROM.commit();
  Serial.println("in clearRom2");

}



void startCameraServerWithWifi(char* ssid, char* ps) {
  Serial.println("in startCameraSeverWithWifi0");
  if(ssid == NULL){
    var_ssid = (char*)SSID;
  }else{
    var_ssid = ssid;
  }
  Serial.println("in startCameraSeverWithWifi1");

  if(ps == NULL){
    var_ps = (char*)PASSWORD;
  }else{
    var_ps = ps;
  }
  Serial.println("in startCameraSeverWithWifi2");
  Serial.println(var_ssid);
  Serial.println(var_ps);

  if(ssid != NULL){
    WiFi.disconnect();
  }
  WiFi.begin(var_ssid, var_ps);
  Serial.println("in startCameraSeverWithWifi3");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Waiting for Wi-Fi connection...");
  }
  Serial.println("");
  Serial.print("WiFi connected : ");
  Serial.println(var_ssid);

  if(!startedCameraServer){
    startCameraServer();
    startedCameraServer = true;
  }

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");

  String ip_ss = WiFi.localIP().toString();
  String j = "{\"ip\":\"" + ip_ss + "\"}";
  std::string j_str = j.c_str();
  pTxCharacteristic->setValue(j_str);
  pTxCharacteristic->notify();

}

void startServerIfExistsData(){


  if (!EEPROM.begin(rom_size)){
    Serial.println("Failed to initialise EEPROM");
    Serial.println("Restarting...");
    delay(1000);
    ESP.restart();
  }

  String ssid = readDataFromRom(address_ssid, length_for_rom);
  String ps = readDataFromRom(address_ps, length_for_rom);

  Serial.println(ssid);
  Serial.println(ps);
  Serial.println("readed?");

  if(ssid.length() > 0 && ps.length() > 0){
    int len_s = ssid.length() + 1; 
    char char_array_s[len_s];
    ssid.toCharArray(char_array_s, len_s);

    int len_p = ps.length() + 1; 
    char char_array_p[len_p];
    ps.toCharArray(char_array_p, len_p);

    startCameraServerWithWifi(char_array_s, char_array_p);
  }else{
    clearRom();
  }

}



void sendStatusToBle(){
  std::string s_value;

  if(startedCameraServer){
    s_value = "server started!";
  }else{
    s_value = "server not started...";
  }
  pTxCharacteristic->setValue(s_value);
  pTxCharacteristic->notify();
}

void parseMessageFromBle(JSONVar obj){
  String action_key = String("action");
  String start_server_val = String("start_server");
  String ssid_key = "ssid";
  String ps_key = "pswd";
  String server_status_val = "server_status";

  JSONVar keys = obj.keys();

  bool start = false;
  bool status = false;
  bool exists_ssid = false;
  bool exists_pwd = false;
  String ssid_val = "";
  String ps_val = "";

  for(uint8_t i = 0; i < keys.length(); i++){
    JSONVar val = obj[keys[i]];
    String k = String(JSON.stringify(keys[i]));
    String v = String(JSON.stringify(val));
    k.replace("\"", "");
    v.replace("\"", "");
    Serial.print(k);
    Serial.print(" : ");
    Serial.println(v);

    Serial.println(k.length());
    Serial.println(v.length());

    Serial.println(action_key.length());
    Serial.println(start_server_val.length());


    if(k.equals(action_key)){
      if(v.equals(start_server_val)){
        Serial.println("start server!0");
        start = true;
      }else if(v.equals(server_status_val)){
        Serial.println("server status");
        status = true;
      }
    }


    if(k.equals(ssid_key)){
      Serial.print("ssid is ");
      ssid_val = v;
      exists_ssid = true;
      Serial.println(ssid_val);
    }
    if(k.equals(ps_key)){
      Serial.print("ps is ");
      ps_val = v;
      exists_pwd = true;
      Serial.println(ps_val);
    }
  }

  if(start && exists_ssid && exists_pwd){

    int len_s = ssid_val.length() + 1;
    char char_array_s[len_s];
    ssid_val.toCharArray(char_array_s, len_s);

    int len_p = ps_val.length() + 1; 
    char char_array_p[len_p];
    ps_val.toCharArray(char_array_p, len_p);

    startCameraServerWithWifi(char_array_s, char_array_p);
  }else if(status){
    sendStatusToBle();
  }
}

void setupBLE() {
  // BLE
  bleDataIsReceived = false;
  // Create the BLE Device
  BLEDevice::init("timerx");
  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  // Create the BLE Service
  pService = pServer->createService(SERVICE_UUID);
  // BLEService *pService = pServer->createService(SERVICE_UUID);
  // Create a BLE Characteristic
  pTxCharacteristic = pService->createCharacteristic(
                    CHARACTERISTIC_UUID_TX,
                    BLECharacteristic::PROPERTY_NOTIFY
                  );
  pTxCharacteristic->addDescriptor(new BLE2902());
  BLECharacteristic * pRxCharacteristic = pService->createCharacteristic(
                       CHARACTERISTIC_UUID_RX,
                      BLECharacteristic::PROPERTY_WRITE
                    );
  pRxCharacteristic->setCallbacks(new MyCallbacks());
  // Start the service
  pService->start();
  // Start advertising
  pAdvertising = pServer->getAdvertising();

  pAdvertising->start();
  // pServer->getAdvertising()->start();
  Serial.println("Waiting a client connection to notify...");

}

void flick_led(int num) {
  digitalWrite(LED_BUILTIN, LOW);
  delay(num);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(num);
  digitalWrite(LED_BUILTIN, LOW);
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // BLE
  setupBLE();


  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

#if defined(CAMERA_MODEL_ESP_EYE)
  pinMode(13, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
#endif

    
  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  s->set_framesize(s, FRAMESIZE_QVGA);

#if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif


  pinMode(LED_BUILTIN, OUTPUT);

}

void loop() {

  flick_led(100);

  noInterrupts();
  if(deviceConnected){
    portENTER_CRITICAL_ISR(&storeDataMux);
    if (bleDataIsReceived) {
      bleDataIsReceived = false;
      Serial.print("data from py: ");
      
      Serial.println(storedValue.c_str());

      pTxCharacteristic->setValue(storedValue);
      pTxCharacteristic->notify();
      deviceConnectedOneLoopBefore = true;
    }
    portEXIT_CRITICAL_ISR(&storeDataMux);
  }
  if(deviceConnectedOneLoopBefore){
    deviceConnectedOneLoopBefore = false;
    parseMessageFromBle(receivedObj);
    delay(1000);
  }

  interrupts();
  if(startedCameraServer && !lighted){
    flick_led(500);
    lighted = true;
  }
}
