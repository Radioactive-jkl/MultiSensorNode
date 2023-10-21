/******************************
 * Code for Node X            *
 * Author: Radioactive-jkl    *
 * Date: 2023/10/5            *
 ******************************/

 
/*
 * Includes
 */
#include <math.h>
#include <U8g2lib.h>
#include <DHT.h>
#include <BH1750.h>
#include <Wire.h>
#include <WiFi.h>
#include <AliyunIoTSDK.h>


/*
 * User Definition
 */
// WIFI
#define WIFI_SSID     "Your_WiFi_ID"
#define WIFI_PASSWD   "Your_WiFi_Password"
static WiFiClient espClient;

// Aliyun-IoT
#define PRODUCT_KEY   "xxxxx"
#define DEVICE_NAME   "NodeX"
#define DEVICE_SECRET "xxxxx"
#define REGION_ID     "cn-shanghai"


/*
 * Hardware Definition
 */
// OLED
#define sda_oled 5
#define scl_oled 23
U8G2_SSD1306_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, scl_oled, sda_oled, U8X8_PIN_NONE);

// DHT
#define DHTPIN 18
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// MQ2
#define D0 33
#define A0 32
static float R0;

// GY-30
#define sda_gy30  21
#define scl_gy30  22
BH1750 lightMeter;

// BAT
#define ANALOG_PIN 34
int percentage = 100;
double capacity[101]={
          4.179,4.169,4.157,4.146,4.134,4.123,4.111,4.099,4.088,4.076,
          4.063,4.051,4.040,4.028,4.017,4.005,3.994,3.982,3.971,3.960,
          3.949,3.938,3.927,3.916,3.906,3.895,3.885,3.875,3.865,3.855,
          3.845,3.836,3.827,3.818,3.809,3.800,3.792,3.784,3.775,3.768,
          3.760,3.753,3.745,3.738,3.732,3.725,3.719,3.713,3.707,3.701,
          3.695,3.690,3.685,3.679,3.675,3.670,3.665,3.661,3.657,3.652,
          3.648,3.645,3.641,3.637,3.633,3.630,3.626,3.623,3.619,3.616,
          3.613,3.609,3.606,3.602,3.599,3.595,3.592,3.588,3.584,3.580,
          3.576,3.571,3.567,3.562,3.557,3.552,3.546,3.540,3.534,3.528,
          3.521,3.513,3.506,3.498,3.489,3.480,3.370,3.260,3.149,3.138,
          3.126};/*Points on curve of V-SOC | 1S(3.7v)lithium battery 20℃*/


/*
 * Tool Functions
 */
// Tools for Calculation
float mean(float data[], int& length)
{
    float mean = 0.0;
    for (int i = 0; i < length; i++)
    {
        mean += data[i];
    }
    mean /= length;
    return mean;
}

float stdDeviation(float data[], int& length)
{
    float avg = mean(data, length);
    float result = 0.0;

    for (int i = 0; i < length; ++i)
    {
        result += pow(data[i] - avg, 2);
    }
    result = sqrt(result / (length - 1));

    return result;
}

bool removeOutliers(float data[], int& length)
{
    bool isAllLegal = true;
    float avg = mean(data, length);
    float threshold = stdDeviation(data, length) * 3;

    for (int i = 0; i < length; )
    {
        if (fabs(data[i] - avg) > threshold)
        {
            isAllLegal = false;
            // kick off
            for (int j = i; j < length - 1; j++)   
            {
                data[j] = data[j + 1];
            }
            length--;
        }
        else
        {
            i++;
        }
    }
    return isAllLegal;
}

float processData(float data[], int& length)
{
    while (removeOutliers(data, length) == false)
    {
        ;
    }
    return mean(data, length);
}

float stdDeviationOfArithmeticMean(float data[], int& length)
{
    float avg = mean(data, length);
    float result = 0.0;

    for (int i = 0; i < length; ++i)
    {
        result += pow(data[i] - avg, 2);
    }
    result = sqrt(result / (length - 1) / length);

    return result;
}

bool linearAccumulativeSystemError(float data[], int& length)
{
  float threshold = 0.1,
        M = 0.0;
        
  for (int i = 0; i < (length + 1)/2; ++i)
  {
    M = M + data[i] - data[length - 1 - i];
  }

  if (fabs(M) > threshold) return true;
  else return false;
}

bool periodicSystemError(float data[], int& length)
{
  float avg = mean(data, length);
  float threshold = 0.0;
  
  for (int i = 0; i < length; ++i)
  {
      threshold += pow(data[i] - avg, 2);
  }
  threshold = threshold / sqrt(length - 1);

  float B = 0.0;
  
  for (int i = 0; i < length - 1; ++i)
  {
      B = B + data[i] * data[i + 1];
  }

  if (fabs(B) > threshold) return true;
  else return false;
}

// Tools for WiFi
void setupWifi()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWD);
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_ncenB08_tr);
  u8g2.setCursor(0,30);
  u8g2.print("Connecting");
  u8g2.sendBuffer();
  while (!WiFi.isConnected())
  {
    u8g2.print(".");
    u8g2.sendBuffer();
    delay(500);
  }
  u8g2.clearBuffer();
  u8g2.setCursor(0,20);
  u8g2.print("Wifi connected!");
  u8g2.setCursor(0,40);
  u8g2.print("IP address: ");
  u8g2.setCursor(0,60);
  u8g2.print(WiFi.localIP());
  u8g2.sendBuffer();
  delay(2000);
}

/*
 * Data Structure
 */
struct DHT_values
{
  bool  getdht;
  float temperature;
  float humidity;
};

struct MQ2_values
{
  float smokescope;
  bool linearError;
  bool periodicError;
};

struct GY3_values
{
  int illumination;
  float std_illumination;
  bool linearError;
  bool periodicError;
};

struct BAT_values
{
  int battery;
};

struct Values
{
  struct DHT_values dhtValues;
  struct MQ2_values mq2Values;
  struct GY3_values gy3Values;
  struct BAT_values batValues;
};


/*
 * Functions for Structure
 */
// OLED
void OLED_write(struct Values temp)
{
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_ncenB08_tr);

  u8g2.setCursor(0,10);
  u8g2.print("Node X:");
  
  u8g2.setCursor(0,20);
  u8g2.print("Tempera: ");
  u8g2.setCursor(64,20);
  u8g2.print(String(temp.dhtValues.temperature)+" *C");
  
  u8g2.setCursor(0,30);
  u8g2.print("Humidit: ");
  u8g2.setCursor(64,30);
  u8g2.print(String(temp.dhtValues.humidity)+" %RH");
  
  u8g2.setCursor(0,40);
  u8g2.print("Smokesc: ");
  u8g2.setCursor(64,40);
  u8g2.print(String(temp.mq2Values.smokescope)+" ppm");

  u8g2.setCursor(0,50);
  u8g2.print("Illumin: ");
  u8g2.setCursor(64,50);
  u8g2.print(String(temp.gy3Values.illumination)+" lux");

  u8g2.setCursor(0,60);
  u8g2.print("Battery: ");
  u8g2.setCursor(64,60);
  u8g2.print(String(temp.batValues.battery)+" %");
  
  u8g2.sendBuffer();
}

// Aliyun-MQTT
void MQTT_write(struct Values temp)
{
  AliyunIoTSDK::send((char*)"temperatureX",    temp.dhtValues.temperature);
  AliyunIoTSDK::send((char*)"humidityX",       temp.dhtValues.humidity);
  AliyunIoTSDK::send((char*)"smokescopeX",     temp.mq2Values.smokescope);
  AliyunIoTSDK::send((char*)"smokescopeleX",   temp.mq2Values.linearError);
  AliyunIoTSDK::send((char*)"smokescopepeX",   temp.mq2Values.periodicError);
  AliyunIoTSDK::send((char*)"illuminationX",   temp.gy3Values.illumination);
  AliyunIoTSDK::send((char*)"illuminationstdX",temp.gy3Values.std_illumination);
  AliyunIoTSDK::send((char*)"illuminationleX", temp.gy3Values.linearError);
  AliyunIoTSDK::send((char*)"illuminationpeX", temp.gy3Values.periodicError);
  AliyunIoTSDK::send((char*)"batteryX",        temp.batValues.battery);
}

// DHT
struct DHT_values DHT_read()
{
  struct DHT_values temp = {true, 0, 0};
  temp.temperature = dht.readTemperature();
  temp.humidity = dht.readHumidity();
  temp.getdht = dht.readTemperature(true);
  if (isnan(temp.temperature) || isnan(temp.humidity) || isnan(temp.getdht))
  {
    temp.getdht = false;
    temp.temperature = 0.0;
    temp.humidity = 0.0;
  }
  return temp;
}

// MQ2
struct MQ2_values MQ2_read()
{
  struct MQ2_values temp = {0.0, false, false};
  // calibrate
  if(millis() < 60000)
  {
    float Vrl = 3.3f * analogRead(A0) / 4096.f;
    float RS = (3.3f - Vrl) / Vrl * 5.00;
    R0 = RS / pow(20 / 613.9f, 1 / -2.074f); 
  }
  // read adc
  float adc[10] = {};
  for (int i = 0; i < 10; i++)
  {
    adc[i] = analogRead(A0);
    delay(5);
  }
  // calculate
  int leng = 10;
  int& lengt = leng; 
  Vrl = 3.3f * processData(adc, lengt) / 4096.f;
  RS = (3.3 - Vrl) / Vrl * 5.00;
  float ppm = 613.9 * pow(RS/R0, -2.074);
  temp.smokescope = ppm;
  temp.linearError = linearAccumulativeSystemError(adc, lengt);
  temp.periodicError = periodicSystemError(adc, lengt);
  return temp;
}

// GY-30
struct GY3_values GY3_read()
{
  struct GY3_values temp = {0, 0.0, false, false};
  float light[10] = {0};
  for (int i = 0; i < 10; i++)
  {
    while (!lightMeter.measurementReady(true)) 
    {
      yield();
    }
    lightMeter.configure(BH1750::ONE_TIME_HIGH_RES_MODE);
    light[i] = lightMeter.readLightLevel();
  }
  int leng = 10;
  int& lengt = leng; 
  temp.illumination = (int)processData(light, lengt);
  temp.std_illumination = 3 * stdDeviationOfArithmeticMean(light, lengt);
  temp.linearError = linearAccumulativeSystemError(light, lengt);
  temp.periodicError = periodicSystemError(light, lengt);
  return temp;
}

// BAT
struct BAT_values BAT_read()
{
  struct BAT_values temp = {0};
  float val=0;
  for (int i = 0; i < 10; i++)
  {
    val+=analogRead(ANALOG_PIN);
    delay(5);
  }
  val /= 10;
  float voltage = (((float)val)/4095)*3.3*3.0;
  for (int i = 0; i < 100; i++)
  {
    if ((voltage>=capacity[i+1]) || (voltage<=capacity[i]))
    {
      percentage = 100 - i;
      break;
    }
  }
  temp.battery = percentage;
  return temp;
}


/*
 * Main Function
 */
void setup()
{
  // OLED
  u8g2.begin();
  
  // DHT22
  dht.begin();
  
  // GY-30
  Wire.begin(sda_gy30,scl_gy30);
  lightMeter.begin(BH1750::ONE_TIME_HIGH_RES_MODE);
  
  // WiFi
  setupWifi();
  
  // AliyunIoT
  AliyunIoTSDK::begin(espClient, PRODUCT_KEY, DEVICE_NAME, DEVICE_SECRET, REGION_ID);
}

void loop()
{
  // Check WiFi
  while (!WiFi.isConnected())
  {
    setupWifi();
  }
  
  struct Values sensorValues = {{true, 0.0, 0.0}, {0.0, false, false}, {0, 0.0, false, false}, {0}};
  
  sensorValues.dhtValues = DHT_read();
  sensorValues.mq2Values = MQ2_read();
  sensorValues.gy3Values = GY3_read();
  sensorValues.batValues = BAT_read();
  
  OLED_write(sensorValues);
  MQTT_write(sensorValues);
  
  AliyunIoTSDK::loop();
}
