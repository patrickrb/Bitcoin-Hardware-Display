# Bitcoin Hardware Display

A real-time Bitcoin price display built for ESP32-S3 development boards with 7-inch RGB displays. This project fetches live Bitcoin price data and displays it with a modern UI featuring trend indicators, price change percentages, and visual feedback.

## Hardware Requirements

### Primary Components
- **ESP32-S3 DevKit-C-1** development board
- **7-inch RGB LCD Display** (800x480 resolution)
- **GT911 Touch Controller** (connected via SPI)

### Display Specifications
- **Resolution**: 800 × 480 pixels
- **Interface**: RGB parallel interface (50-pin connector)
- **Touch**: Capacitive touch with GT911 controller
- **Backlight**: GPIO-controlled LED backlight

### Pin Configuration
The project uses the following ESP32-S3 GPIO pins for the RGB display:

**RGB Data Lines:**
- R0-R4: GPIO 14, 21, 47, 48, 45
- G0-G5: GPIO 9, 46, 3, 8, 16, 1  
- B0-B4: GPIO 15, 7, 6, 5, 4

**Control Signals:**
- DE (Data Enable): GPIO 41
- VSYNC: GPIO 40
- HSYNC: GPIO 39
- PCLK (Pixel Clock): GPIO 0

**Touch Interface:**
- SPI communication for GT911 touch controller
- CS: GPIO 38
- Backlight: GPIO 2

## Features

- **Live Bitcoin Price**: Real-time price fetching from CoinLore API
- **Trend Indicators**: Visual indicators showing price increases (green ↗) or decreases (red ↘)
- **Price Change Percentage**: Shows percentage change with color-coded background
- **Auto-refresh**: Updates price data every 30 seconds
- **WiFi Auto-reconnect**: Automatically reconnects if WiFi connection is lost
- **Modern UI**: Dark theme with Bitcoin orange accents and progress arcs
- **Status Display**: Shows time since last update (e.g., "Updated 15s ago")

## Software Requirements

### Development Environment
- **PlatformIO** (recommended) or Arduino IDE
- **ESP32 Arduino Core** v2.0.3
- **USB cable** for programming and power

### Dependencies (automatically installed)
- `lvgl/lvgl@8.3.6` - GUI library
- `tamctec/TAMC_GT911@^1.0.2` - Touch controller driver
- `moononournation/GFX Library for Arduino@1.2.8` - Graphics library
- `bblanchon/ArduinoJson@^7.0.4` - JSON parsing

## Setup Instructions

### 1. WiFi Configuration

**Option A: Using config.h (Recommended)**
1. Copy the sample configuration file:
   ```bash
   cp src/config.h.sample src/config.h
   ```
2. Edit `src/config.h` with your WiFi credentials:
   ```cpp
   const char* ssid = "Your_WiFi_Network";
   const char* password = "Your_WiFi_Password";
   ```

**Option B: Direct editing**
1. Edit `src/main.cpp` and update the WiFi credentials in the config.h include section

### 2. Build and Upload

Using PlatformIO:
```bash
# Build the project
platformio run

# Upload to ESP32-S3
platformio run --target upload

# Monitor serial output
platformio device monitor
```

Using Arduino IDE:
1. Install ESP32 board support
2. Select "ESP32S3 Dev Module" as the board
3. Set upload speed to 115200
4. Compile and upload

### 3. Hardware Assembly

1. **Connect the 7-inch display** to your ESP32-S3 board using the 50-pin RGB connector
2. **Power the display** - ensure adequate power supply (5V/2A recommended)
3. **Connect touch controller** via SPI interface
4. **Upload the firmware** via USB

### 4. First Boot

1. The device will attempt to connect to your configured WiFi network
2. Once connected, it will fetch the initial Bitcoin price
3. The display will show the price with trend indicators
4. Price updates automatically every 30 seconds

## Usage

### Display Elements
- **Main Price**: Large central display showing current Bitcoin price in USD
- **Trend Arrow**: ↗ (green) for increases, ↘ (red) for decreases  
- **Percentage Change**: Shows price change percentage with color-coded background
- **Status Bar**: Shows "Live Price • Updated Xs ago" at the bottom
- **Visual Arcs**: Decorative progress arcs in Bitcoin orange

### Network Requirements
- **Internet Connection**: Required for fetching price data
- **Firewall**: Ensure access to `api.coinlore.net` (port 443/80)
- **DNS**: Device needs working DNS resolution

## Customization

### Update Frequency
Change the update interval in `src/main.cpp`:
```cpp
const unsigned long PRICE_UPDATE_INTERVAL = 30000; // 30 seconds
```

### API Configuration
The project uses CoinLore API with automatic HTTPS/HTTP fallback:
- Primary: `https://api.coinlore.net/api/ticker/?id=90`
- Fallback: `http://api.coinlore.net/api/ticker/?id=90`

### Colors and Styling
Modify colors in the UI files:
- **Bitcoin Orange**: `0xF7931A`
- **Success Green**: `0x00FF88`
- **Error Red**: `0xFF4444`
- **Background**: Dark theme with accent colors

## Troubleshooting

### WiFi Connection Issues
1. **Check credentials**: Verify SSID and password in config.h
2. **Signal strength**: Ensure ESP32 is within WiFi range
3. **Network compatibility**: Some enterprise networks may block IoT devices

### Price Update Issues
1. **Check serial monitor**: Look for HTTP error codes
2. **Firewall**: Ensure access to api.coinlore.net
3. **DNS**: Try using Google DNS (8.8.8.8) in router settings

### Display Issues
1. **Check connections**: Verify all ribbon cables are properly seated
2. **Power supply**: Ensure adequate power (5V/2A minimum)
3. **Backlight**: GPIO 2 controls backlight - check connections

### Touch Issues
1. **Calibration**: Touch calibration values may need adjustment
2. **SPI connections**: Verify touch controller SPI wiring
3. **Ground loops**: Ensure proper grounding between display and ESP32

## Development

### Project Structure
```
├── src/
│   ├── main.cpp           # Main application code
│   ├── config.h           # WiFi configuration
│   └── UI/                # LVGL UI components
├── include/
│   ├── lv_conf.h         # LVGL configuration
│   └── ui.h              # UI declarations  
├── platformio.ini        # PlatformIO configuration
└── squareline_files/     # SquareLine Studio project files
```

### Adding Features
1. **New APIs**: Add alternative price sources in main.cpp
2. **UI Changes**: Use SquareLine Studio to modify the interface
3. **Additional Data**: Extend JSON parsing for more cryptocurrency data

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review serial monitor output for error messages
3. Verify hardware connections and power supply
4. Ensure network connectivity and API access