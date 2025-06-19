# Bitcoin Price Display Setup

## What's Changed

Your 7-inch ESP32-S3 display has been transformed into a live Bitcoin price display! 

### Features Added:
- **Live Bitcoin Price**: Fetches real-time price from CoinDesk API
- **Trend Indicators**: Green for price increases, red for decreases
- **Modern UI Design**: Dark theme with Bitcoin orange accents
- **Price Change**: Shows percentage change with arrows
- **Auto-refresh**: Updates every 30 seconds
- **WiFi Connection**: Automatic reconnection if lost

### Visual Design:
- Large central price display ($XX,XXX format)
- Circular progress arc showing price momentum
- Bitcoin logo and branding
- Trend arrows (↗ ↘) with percentage changes
- Corner accent arcs in Bitcoin orange
- Status indicator showing last update time

## Setup Instructions

### 1. WiFi Configuration
Edit `src/main.cpp` and update these lines with your WiFi credentials:
```cpp
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
```

### 2. Build and Upload
```bash
platformio run --target upload
```

### 3. Monitor Output
```bash
platformio device monitor
```

## How It Works

1. **Startup**: Connects to WiFi and fetches initial Bitcoin price
2. **Display**: Shows price with trend colors and indicators
3. **Updates**: Fetches new price every 30 seconds
4. **Trends**: Compares with previous price to show green/red indicators
5. **Arc Animation**: Visual representation of price momentum

## API Used
- **Source**: CoinDesk Bitcoin Price Index API
- **Endpoint**: https://api.coindesk.com/v1/bpi/currentprice.json
- **Rate Limit**: No API key required, reasonable usage expected
- **Update Frequency**: 30 seconds (configurable)

## Customization Options

### Change Update Interval
Modify in `src/main.cpp`:
```cpp
const unsigned long PRICE_UPDATE_INTERVAL = 30000; // milliseconds
```

### Color Scheme
Colors can be modified in `src/UI/screens/ui_ScreenHome.c`:
- Bitcoin Orange: `0xF7931A`
- Success Green: `0x00FF88`
- Error Red: `0xFF4444`

### Font Sizes
- Title: `lv_font_montserrat_24`
- Price: `lv_font_montserrat_48`
- Change: `lv_font_montserrat_18`
- Status: `lv_font_montserrat_14`

Enjoy your new Bitcoin price display! 🚀₿