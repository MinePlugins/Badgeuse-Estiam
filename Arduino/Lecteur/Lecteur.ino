#include <SPI.h>
#include <RFID.h>
#include <ArduinoJson.h>
/*
RC522   | Arduino Pin
  VCC   |  +5V
  RST   |   9
  GND   |   GND
  MISO  |   12
  MOSI  |   11
  SCK   |   13
  NSS   |   10
  IRC   |   /
*/
RFID rfid(10,9); // Pin du lecteur de carte

int UID[5]; // Taille de l'uid

void setup()
{
  Serial.begin(9600); // Vitesse de la liaison série
  SPI.begin(); // Initialisation de la communication SPI
  rfid.init();  // Initialisation du module RFID

}

void loop()
{
    StaticJsonDocument<256> data; // JSON data
    if (rfid.isCard()) {  // Si il y a une carte
          if (rfid.readCardSerial()) {        // Lire la carte
            data["uuid"] = "ESTIAM"+String(rfid.serNum[0])
                                   +String(rfid.serNum[1])
                                   +String(rfid.serNum[2])
                                   +String(rfid.serNum[3])
                                   +String(rfid.serNum[4]); // Formatter au format ESTIAM
            serializeJson(data, Serial); // Envoyé la donné en JSON
            Serial.println(); // Carriage return
          }          
          rfid.halt(); // Reset du lecteur de carte
    }
    
}
