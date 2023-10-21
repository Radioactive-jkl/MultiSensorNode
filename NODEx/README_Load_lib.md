# NODE X

Radioactive-jkl<br>
2023/10/5<br>

[![Github](https://img.shields.io/badge/-Github%20-000000?style=flat&logo=Github&logoColor=white)](https://github.com/Radioactive-jkl/MultiSensorNode)
[![Git](https://img.shields.io/badge/-Git%20-2088FF?style=flat&logo=Git&logoColor=white)](https://git-scm.com/)
[![Arduino](https://img.shields.io/badge/Arduino-00878F?logo=arduino&logoColor=white)](https://www.arduino.cc/)


#### Contents

- [NODE X](#node-x)
      - [Contents](#contents)
  - [Introduction](#introduction)
  - [Development](#development)


## Introduction

> This is the **`Arduino`** code for the nodes in my Embedded Systems Design course's curriculum design. Nodes detect environmental data and their own power levels, and then upload them to AliyunIoT server. The node is controlled by an ESP32 and utilizes the DHT22 temperature and humidity sensor, MQ-135 air quality sensor, and GY-30 light intensity sensor. It also simply uses an OLED display to show the data.


## Development

1. Download the following libraries in Arduino **library manager**.
    > **U8g2**<br>
    > **DHT sensor library**<br>
    > **BH1750**<br>
    > **WiFi**<br>
    > **AliyunIoTSDK**<br>
    > **Crypto**<br>
    > **...***(fill other libs if necessary)*

2. Add some information to the code to use it.