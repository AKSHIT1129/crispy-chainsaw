/**
 * Crispy Chainsaw - ESP32 Receiver (Rx) CSI Extractor Firmware
 * -----------------------------------------------------------
 * Connects to the Transmitter AP and registers the Espressif WiFi CSI callback.
 * Dumps raw CSI subcarrier amplitudes over Serial (UART) for Python parsing.
 * 
 * Hardware: ESP32 / ESP32-S3
 * Framework: Arduino / PlatformIO / ESP-IDF
 */

#include <Arduino.h>
#include <WiFi.h>
#include "esp_wifi.h"

const char* ssid = "CRISPY_CHAINSAW_SENSING";
const char* password = "ThroughWallWi-Fi123";

// ESP-IDF CSI Callback Function
void _wifi_csi_cb(void *ctx, wifi_csi_info_t *info) {
    if (!info || !info->buf) return;

    wifi_pkt_rx_ctrl_t rx_ctrl = info->rx_ctrl;

    // Print header line format expected by Python parser
    Serial.printf("CSI_DATA,1,%02x:%02x:%02x:%02x:%02x:%02x,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%u,%d,%d,%d,%d,[",
        info->mac[0], info->mac[1], info->mac[2], info->mac[3], info->mac[4], info->mac[5],
        rx_ctrl.rssi, rx_ctrl.rate, rx_ctrl.sig_mode, rx_ctrl.mcs, rx_ctrl.cwm,
        rx_ctrl.smoothing, rx_ctrl.not_sounding, rx_ctrl.aggregation, rx_ctrl.stbc,
        rx_ctrl.fec_coding, rx_ctrl.sgi, rx_ctrl.noise_floor, rx_ctrl.ampdu_cnt,
        rx_ctrl.channel, rx_ctrl.secondary_channel, rx_ctrl.timestamp, rx_ctrl.ant,
        rx_ctrl.sig_len, rx_ctrl.rx_state, info->len
    );

    // Print raw signed subcarrier array values
    int8_t *csi_buf = (int8_t *)info->buf;
    for (int i = 0; i < info->len; i++) {
        Serial.printf("%d ", csi_buf[i]);
    }
    Serial.println("]");
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("\n--- ESP32 CSI Receiver Starting ---");

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    Serial.print("Connecting to AP: ");
    Serial.println(ssid);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to AP!");

    // Initialize CSI configuration
    wifi_csi_config_t csi_config = {
        .lltf_en           = true,
        .htltf_en          = true,
        .stbc_htltf2_en    = true,
        .ltf_merge_en      = true,
        .channel_filter_en = false,
        .manu_scale        = false,
        .shift             = false,
    };

    ESP_ERROR_CHECK(esp_wifi_set_csi_config(&csi_config));
    ESP_ERROR_CHECK(esp_wifi_set_csi_rx_cb(_wifi_csi_cb, NULL));
    ESP_ERROR_CHECK(esp_wifi_set_csi(true));

    Serial.println("CSI Callback Registered Successfully. Dumping CSI stream...");
}

void loop() {
    delay(1000);
}
