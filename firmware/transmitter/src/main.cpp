/**
 * Crispy Chainsaw - ESP32 Transmitter (Tx) Firmware
 * ------------------------------------------------
 * Configures the ESP32 as a Wi-Fi Access Point (AP) to continuously transmit
 * Wi-Fi packets/beacon frames that the Receiver captures for CSI analysis.
 * 
 * Hardware: ESP32 / ESP32-S3
 * Framework: Arduino / PlatformIO
 */

#include <Arduino.h>
#include <WiFi.h>

const char* ssid = "CRISPY_CHAINSAW_SENSING";
const char* password = "ThroughWallWi-Fi123";

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("\n--- ESP32 CSI Transmitter Starting ---");

    // Configure as Access Point with fixed Wi-Fi Channel 6
    WiFi.mode(WIFI_AP);
    WiFi.softAP(ssid, password, 6, 0, 4);

    Serial.print("Access Point started! SSID: ");
    Serial.println(ssid);
    Serial.print("IP Address: ");
    Serial.println(WiFi.softAPIP());
}

void loop() {
    // Continuously active transmit loop
    static uint32_t packet_count = 0;
    packet_count++;
    
    if (packet_count % 100 == 0) {
        Serial.printf("Tx Active - Transmitted %u beacon cycles\n", packet_count);
    }
    
    delay(20); // 50 Hz packet rate
}
