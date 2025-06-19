#include <Arduino.h>
#include <Arduino_GFX_Library.h>
#include <lvgl.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
static uint32_t screenWidth;
static uint32_t screenHeight;
static lv_disp_draw_buf_t draw_buf;
static lv_color_t disp_draw_buf[800 * 480 / 10];
static lv_disp_drv_t disp_drv;

// UI
#include <ui.h>
#include "UI/ui_helpers.h"
#include "config.h"

#include <SPI.h>

// Bitcoin API endpoints - using APIs that should work on most networks
const char* bitcoinApiUrl = "https://api.coinlore.net/api/ticker/?id=90"; // CoinLore API (HTTPS)
const char* bitcoinApiUrlBackup = "http://api.coinlore.net/api/ticker/?id=90"; // HTTP fallback

// Bitcoin price variables
float currentBitcoinPrice = 0.0;
float previousBitcoinPrice = 0.0;
bool priceIncreasing = true;
unsigned long lastPriceUpdate = 0;
unsigned long lastStatusUpdate = 0;
const unsigned long PRICE_UPDATE_INTERVAL = 30000; // 30 seconds
const unsigned long STATUS_UPDATE_INTERVAL = 1000; // Update status every 1 second

SPIClass &spi = SPI;
uint16_t touchCalibration_x0 = 300, touchCalibration_x1 = 3600, touchCalibration_y0 = 300, touchCalibration_y1 = 3600;
uint8_t touchCalibration_rotate = 1, touchCalibration_invert_x = 2, touchCalibration_invert_y = 0;

int i = 0;
#define TFT_BL 2

Arduino_ESP32RGBPanel *bus = new Arduino_ESP32RGBPanel(
    GFX_NOT_DEFINED /* CS */, GFX_NOT_DEFINED /* SCK */, GFX_NOT_DEFINED /* SDA */,
    41 /* DE */, 40 /* VSYNC */, 39 /* HSYNC */, 0 /* PCLK */,
    14 /* R0 */, 21 /* R1 */, 47 /* R2 */, 48 /* R3 */, 45 /* R4 */,
    9 /* G0 */, 46 /* G1 */, 3 /* G2 */, 8 /* G3 */, 16 /* G4 */, 1 /* G5 */,
    15 /* B0 */, 7 /* B1 */, 6 /* B2 */, 5 /* B3 */, 4 /* B4 */
);

// option 1:
// 7寸 50PIN 800*480
Arduino_RPi_DPI_RGBPanel *lcd = new Arduino_RPi_DPI_RGBPanel(
    bus,
    800 /* width */, 1 /* hsync_polarity */, 40 /* hsync_front_porch */, 48 /* hsync_pulse_width */, 40 /* hsync_back_porch */,
    480 /* height */, 1 /* vsync_polarity */, 13 /* vsync_front_porch */, 1 /* vsync_pulse_width */, 31 /* vsync_back_porch */,
    1 /* pclk_active_neg */, 16000000 /* prefer_speed */, true /* auto_flush */);

#include "touch.h"
/* Display flushing */
void my_disp_flush(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p)
{
  uint32_t w = (area->x2 - area->x1 + 1);
  uint32_t h = (area->y2 - area->y1 + 1);

  lcd->draw16bitRGBBitmap(area->x1, area->y1, (uint16_t *)&color_p->full, w, h);

  lv_disp_flush_ready(disp);
}

void my_touchpad_read(lv_indev_drv_t *indev_driver, lv_indev_data_t *data)
{
  if (touch_has_signal())
  {
    if (touch_touched())
    {
      data->state = LV_INDEV_STATE_PR;

      /*Set the coordinates*/
      data->point.x = touch_last_x;
      data->point.y = touch_last_y;
    }
    else if (touch_released())
    {
      data->state = LV_INDEV_STATE_REL;
    }
  }
  else
  {
    data->state = LV_INDEV_STATE_REL;
  }
}

void begin_touch_read_write(void)
{
  digitalWrite(38, HIGH); // Just in case it has been left low
  spi.setFrequency(600000);
  digitalWrite(38, LOW);
}

void end_touch_read_write(void)
{
  digitalWrite(38, HIGH); // Just in case it has been left low
  spi.setFrequency(600000);
}

uint16_t getTouchRawZ(void)
{

  begin_touch_read_write();

  // Z sample request
  int16_t tz = 0xFFF;
  spi.transfer(0xb0);              // Start new Z1 conversion
  tz += spi.transfer16(0xc0) >> 3; // Read Z1 and start Z2 conversion
  tz -= spi.transfer16(0x00) >> 3; // Read Z2

  end_touch_read_write();

  return (uint16_t)tz;
}

uint8_t getTouchRaw(uint16_t *x, uint16_t *y)
{
  uint16_t tmp;

  begin_touch_read_write();

  // Start YP sample request for x position, read 4 times and keep last sample
  spi.transfer(0xd0); // Start new YP conversion
  spi.transfer(0);    // Read first 8 bits
  spi.transfer(0xd0); // Read last 8 bits and start new YP conversion
  spi.transfer(0);    // Read first 8 bits
  spi.transfer(0xd0); // Read last 8 bits and start new YP conversion
  spi.transfer(0);    // Read first 8 bits
  spi.transfer(0xd0); // Read last 8 bits and start new YP conversion

  tmp = spi.transfer(0); // Read first 8 bits
  tmp = tmp << 5;
  tmp |= 0x1f & (spi.transfer(0x90) >> 3); // Read last 8 bits and start new XP conversion

  *x = tmp;

  // Start XP sample request for y position, read 4 times and keep last sample
  spi.transfer(0);    // Read first 8 bits
  spi.transfer(0x90); // Read last 8 bits and start new XP conversion
  spi.transfer(0);    // Read first 8 bits
  spi.transfer(0x90); // Read last 8 bits and start new XP conversion
  spi.transfer(0);    // Read first 8 bits
  spi.transfer(0x90); // Read last 8 bits and start new XP conversion

  tmp = spi.transfer(0); // Read first 8 bits
  tmp = tmp << 5;
  tmp |= 0x1f & (spi.transfer(0) >> 3); // Read last 8 bits

  *y = tmp;

  end_touch_read_write();

  return true;
}

// WiFi connection function
void connectToWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("WiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("WiFi connection failed!");
  }
}

// Update the Bitcoin display
void updateBitcoinDisplay() {
  Serial.printf("Updating display with price: $%.2f\n", currentBitcoinPrice);
  
  if (currentBitcoinPrice <= 0) {
    Serial.println("Invalid price, not updating display");
    return;
  }
  
  // Create a formatted string for the price with commas
  char priceBuffer[32];
  int price = (int)currentBitcoinPrice;
  
  // Format with commas for thousands
  if (price >= 1000000) {
    sprintf(priceBuffer, "$%d,%03d,%03d", price / 1000000, (price / 1000) % 1000, price % 1000);
  } else if (price >= 1000) {
    sprintf(priceBuffer, "$%d,%03d", price / 1000, price % 1000);
  } else {
    sprintf(priceBuffer, "$%d", price);
  }
  
  // Update main price label (center it properly)
  lv_label_set_text(ui_LabelSpeed, priceBuffer);
  lv_obj_set_style_text_color(ui_LabelSpeed, lv_color_hex(0xFFFFFF), LV_PART_MAIN | LV_STATE_DEFAULT);
  
  // Calculate percentage change
  float percentChange = 0.0;
  if (previousBitcoinPrice > 0) {
    percentChange = ((currentBitcoinPrice - previousBitcoinPrice) / previousBitcoinPrice) * 100.0;
  }
  
  // Update change label with arrow and percentage
  const char* arrow = priceIncreasing ? "↗" : "↘";
  char changeBuffer[32];
  sprintf(changeBuffer, "%s %+.2f%%", arrow, percentChange);
  
  if (ui_LabelChange != NULL) {
    lv_label_set_text(ui_LabelChange, changeBuffer);
    
    // Update change label and container colors based on trend
    lv_color_t trendColor = priceIncreasing ? lv_color_hex(0x00FF88) : lv_color_hex(0xFF4444);
    lv_color_t bgColor = priceIncreasing ? lv_color_hex(0x1A3D2E) : lv_color_hex(0x3D1A1A);
    
    lv_obj_set_style_text_color(ui_LabelChange, trendColor, LV_PART_MAIN | LV_STATE_DEFAULT);
    
    // Update the container background color
    lv_obj_t * changeContainer = lv_obj_get_parent(ui_LabelChange);
    if (changeContainer != NULL) {
      lv_obj_set_style_bg_color(changeContainer, bgColor, LV_PART_MAIN | LV_STATE_DEFAULT);
    }
  }
  
  Serial.printf("Display updated: %s\n", priceBuffer);
}

// Update the status timestamp
void updateStatusTimestamp() {
  if (ui_LabelStatus == NULL) {
    return;
  }
  
  // If no price update yet, show loading status
  if (lastPriceUpdate == 0) {
    lv_label_set_text(ui_LabelStatus, "Live Price - Connecting...");
    return;
  }
  
  unsigned long currentMillis = millis();
  unsigned long timeSinceUpdate = (currentMillis - lastPriceUpdate) / 1000; // Convert to seconds
  
  char statusBuffer[64];
  
  if (timeSinceUpdate < 60) {
    // Show seconds
    if (timeSinceUpdate == 0) {
      sprintf(statusBuffer, "Live Price • Updated now");
    } else if (timeSinceUpdate == 1) {
      sprintf(statusBuffer, "Live Price • Updated 1s ago");
    } else {
      sprintf(statusBuffer, "Live Price • Updated %lus ago", timeSinceUpdate);
    }
  } else {
    // Show minutes
    unsigned long minutes = timeSinceUpdate / 60;
    if (minutes == 1) {
      sprintf(statusBuffer, "Live Price • Updated 1m ago");
    } else {
      sprintf(statusBuffer, "Live Price • Updated %lum ago", minutes);
    }
  }
  
  lv_label_set_text(ui_LabelStatus, statusBuffer);
}

// Fetch Bitcoin price from API
void fetchBitcoinPrice() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected, cannot fetch price");
    return;
  }
  
  Serial.println("Attempting to fetch Bitcoin price...");
  
  HTTPClient http;
  
  // Try CoinLore API first (usually works on most networks)
  Serial.println("Trying CoinLore API (HTTPS)...");
  http.begin(bitcoinApiUrl);
  http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
  
  http.setTimeout(15000); // 15 second timeout
  
  int httpResponseCode = http.GET();
  
  if (httpResponseCode == 200) {
    String payload = http.getString();
    Serial.println("Received response:");
    Serial.println(payload.substring(0, 200)); // Print first 200 chars
    
    // Parse JSON response
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, payload);
    
    if (error) {
      Serial.print("JSON parsing failed: ");
      Serial.println(error.c_str());
      return;
    }
    
    // Extract Bitcoin price in USD
    previousBitcoinPrice = currentBitcoinPrice;
    
    // Try CoinLore format (array with price_usd)
    if (doc[0]["price_usd"]) {
      String priceStr = doc[0]["price_usd"];
      currentBitcoinPrice = priceStr.toFloat();
      Serial.println("Using CoinLore data");
    } else {
      Serial.println("Could not parse price from JSON");
      Serial.println("JSON structure not recognized");
      return;
    }
    
    // Determine price trend
    if (currentBitcoinPrice > previousBitcoinPrice) {
      priceIncreasing = true;
    } else if (currentBitcoinPrice < previousBitcoinPrice) {
      priceIncreasing = false;
    }
    
    Serial.printf("Bitcoin Price: $%.2f\n", currentBitcoinPrice);
    updateBitcoinDisplay();
    lastPriceUpdate = millis(); // Update timestamp after successful fetch
    
  } else {
    Serial.printf("HTTP Error: %d\n", httpResponseCode);
    
    // If HTTPS failed with redirect, try HTTP fallback
    if (httpResponseCode == 301 || httpResponseCode == 302) {
      Serial.println("Redirect detected, trying HTTP fallback...");
      http.end();
      
      http.begin(bitcoinApiUrlBackup); // HTTP version
      int httpResponseCode2 = http.GET();
      
      if (httpResponseCode2 == 200) {
        String payload = http.getString();
        Serial.println("Received response from HTTP fallback:");
        Serial.println(payload.substring(0, 200));
        
        JsonDocument doc;
        DeserializationError error = deserializeJson(doc, payload);
        
        if (!error && doc[0]["price_usd"]) {
          previousBitcoinPrice = currentBitcoinPrice;
          String priceStr = doc[0]["price_usd"];
          currentBitcoinPrice = priceStr.toFloat();
          
          if (currentBitcoinPrice > previousBitcoinPrice) {
            priceIncreasing = true;
          } else if (currentBitcoinPrice < previousBitcoinPrice) {
            priceIncreasing = false;
          }
          
          Serial.printf("Bitcoin Price: $%.2f\n", currentBitcoinPrice);
          updateBitcoinDisplay();
          lastPriceUpdate = millis(); // Update timestamp after successful fetch
        } else {
          Serial.println("Failed to parse HTTP fallback response");
        }
      } else {
        Serial.printf("HTTP Fallback also failed: %d\n", httpResponseCode2);
      }
    } else {
      Serial.println("Check your internet connection and DNS settings");
    }
  }
  
  http.end();
}

void lvgl_loop(void *parameter)
{
  while (true)
  {
    lv_timer_handler();
  }
  vTaskDelete(NULL);
}

void guiHandler()
{
  xTaskCreatePinnedToCore(
      lvgl_loop,   // Function that should be called
      "LVGL Loop", // Name of the task (for debugging)
      20480,       // Stack size (bytes)
      NULL,        // Parameter to pass
      1,           // Task priority
      NULL,        // Task handle
      1);
}

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200); // Init Display
  
  // Connect to WiFi
  connectToWiFi();

  lcd->begin();
  lcd->fillScreen(BLACK);
  lcd->setTextSize(2);
  delay(200);

  lv_init();
  touch_init();
  screenWidth = lcd->width();
  screenHeight = lcd->height();

  lv_disp_draw_buf_init(&draw_buf, disp_draw_buf, NULL, screenWidth * screenHeight / 10);

  /* Initialize the display */
  lv_disp_drv_init(&disp_drv);
  /* Change the following line to your display resolution */
  disp_drv.hor_res = screenWidth;
  disp_drv.ver_res = screenHeight;
  disp_drv.flush_cb = my_disp_flush;
  disp_drv.draw_buf = &draw_buf;
  lv_disp_drv_register(&disp_drv);

  /* Initialize the (dummy) input device driver */
  static lv_indev_drv_t indev_drv;
  lv_indev_drv_init(&indev_drv);
  indev_drv.type = LV_INDEV_TYPE_POINTER;
  indev_drv.read_cb = my_touchpad_read;
  lv_indev_drv_register(&indev_drv);

  // Back light
  pinMode(TFT_BL, OUTPUT);
  digitalWrite(TFT_BL, HIGH);

  lcd->fillScreen(BLACK);

  ui_init();
  guiHandler();
  
  // Initialize timestamp tracking
  lastStatusUpdate = millis();
  
  // Fetch initial Bitcoin price
  if (WiFi.status() == WL_CONNECTED) {
    fetchBitcoinPrice();
  }
}

unsigned long previousMillis = 0;

void loop()
{
  unsigned long currentMillis = millis();
  
  // Update Bitcoin price every 30 seconds
  if (currentMillis - lastPriceUpdate >= PRICE_UPDATE_INTERVAL) {
    if (WiFi.status() == WL_CONNECTED) {
      fetchBitcoinPrice();
    } else {
      // Try to reconnect WiFi if disconnected
      connectToWiFi();
    }
  }
  
  // Update status timestamp every second
  if (currentMillis - lastStatusUpdate >= STATUS_UPDATE_INTERVAL) {
    updateStatusTimestamp();
    lastStatusUpdate = currentMillis;
  }
  
  delay(100); // Small delay to prevent excessive CPU usage
}
