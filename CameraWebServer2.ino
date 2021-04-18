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
//#define CAMERA_MODEL_M5STACK_V2_PSRAM // M5Camera version B Has PSRAM
//#define CAMERA_MODEL_M5STACK_WIDE // Has PSRAM
//#define CAMERA_MODEL_M5STACK_ESP32CAM // No PSRAM
//#define CAMERA_MODEL_AI_THINKER // Has PSRAM
//#define CAMERA_MODEL_TTGO_T_JOURNAL // No PSRAM

#include "camera_pins.h"
//#include "led.h"
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

// const char* uuidOfService = "00001101-0000-1000-8000-00805f9b34fb";
// const char* uuidOfRxChar = "00001142-0000-1000-8000-00805f9b34fb";
// const char* uuidOfTxChar = "00001143-0000-1000-8000-00805f9b34fb";


// #define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E" // UART service UUID
// #define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
// #define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


#include <Arduino_JSON.h>

JSONVar receivedObj;

bool startedCameraServer = false;
void startCameraServer();

char* var_ssid = "";
char* var_ps = "";


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

};


// BLE
BLEServer *pServer = NULL;
BLECharacteristic * pTxCharacteristic;
bool deviceConnected = false;
bool oldDeviceConnected = false;
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

void parseJsonString(JSONVar obj){
  JSONVar keys = obj.keys();
  // String action = String("\"action\"");
  // String start_server = String("\"start_server\"");
  // String ssid_key = "\"ssid\"";
  // String ps_key = "\"pswd\"";

  String action = String("action");
  String start_server = String("start_server");
  String ssid_key = "ssid";
  String ps_key = "pswd";


  bool start = false;
  bool exists_ssid = false;
  bool exists_pwd = false;
  String ssid_ = "";
  String ps_ = "";
  for(uint8_t i = 0; i < keys.length(); i++){
    JSONVar val = obj[keys[i]];
    String k = String(JSON.stringify(keys[i]));
    String v = String(JSON.stringify(val));
    k.replace("\"", "");
    v.replace("\"", "");
    // {"action":"server", "ssid": "aiueo", "pswd":"secred"}
    

    // String k_s = k.c_str();
    // String v_s = v.c_str();
    // Serial.print(k.c_str());
    Serial.print(k);
    Serial.print(" : ");
    Serial.println(v);

    Serial.println(k.length());
    Serial.println(v.length());
    Serial.println(action.length());
    Serial.println(start_server.length());

    Serial.println(k);
    Serial.println(v);
    Serial.println(action);
    Serial.println(start_server);



    if(k.equals(action) && v.equals(start_server)){
      Serial.println("start server!0");
      start = true;
    }
    if(k.equals(ssid_key)){
      Serial.println("ssid");
      ssid_ = v;
      exists_ssid = true;
    }
    if(k.equals(ps_key)){
      ps_ = v;
      exists_pwd = true;
    }

    

    if(start && exists_ssid && exists_pwd){
      Serial.print("aru");
      // const char* s = ssid_.c_str();
      // const char* p = ps_.c_str();

      int len_s = ssid_.length() + 1; 
      char char_array_s[len_s];
      ssid_.toCharArray(char_array_s, len_s);

      int len_p = ps_.length() + 1; 
      char char_array_p[len_p];
      ps_.toCharArray(char_array_p, len_p);


      startCameraServerWithWifi(char_array_s, char_array_p);

    }


  }
      // startCameraServerWithWifi(NULL, NULL);
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();


  // BLE
  bleDataIsReceived = false;
  // Create the BLE Device
  BLEDevice::init("timerx");
  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);
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
  pServer->getAdvertising()->start();
  Serial.println("Waiting a client connection to notify...");




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
  // drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_QVGA);

#if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif


  startCameraServerWithWifi(NULL, NULL);


  pinMode(LED_BUILTIN, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

  if(deviceConnected){
    portENTER_CRITICAL_ISR(&storeDataMux);
    if (bleDataIsReceived) {
      bleDataIsReceived = false;
      Serial.print("data from py: ");
      
      Serial.println(storedValue.c_str());

      parseJsonString(receivedObj);

      pTxCharacteristic->setValue(storedValue);
      pTxCharacteristic->notify();
    }
    portEXIT_CRITICAL_ISR(&storeDataMux);
  }

  digitalWrite(LED_BUILTIN, LOW);
  delay(10000);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(10000);
}
