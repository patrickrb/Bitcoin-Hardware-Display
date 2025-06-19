#!/usr/bin/env python3
"""
Create a simple Bitcoin logo BMP file manually
"""
import struct

def create_simple_bmp():
    # Create a 32x32 16-bit BMP (RGB565 format for ESP32)
    width = 32
    height = 32
    
    # Bitcoin orange in RGB565: #F7931A -> R=31, G=18, B=3
    bitcoin_orange = 0xF793  # RGB565
    white = 0xFFFF
    black = 0x0000
    
    # Simple Bitcoin logo pattern (32x32)
    # 1 = orange, 0 = transparent/black
    bitcoin_pattern = [
        "00000000000000000000000000000000",
        "00000000000111111110000000000000",
        "00000000111111111111110000000000",
        "00000001111111111111111000000000",
        "00000111111111111111111100000000",
        "00001111111111111111111110000000",
        "00011111110111111011111111000000",
        "00111111100111110001111111100000",
        "01111111001111100000111111110000",
        "01111110011111000000011111110000",
        "11111110011110000000001111111100",
        "11111100111100000000000111111100",
        "11111100111000111111000111111100",
        "11111100110001111111100111111100",
        "11111100110011111111110111111100",
        "11111100110111111111111111111100",
        "11111100110111111111111111111100",
        "11111100110011111111110111111100",
        "11111100110001111111100111111100",
        "11111100111000111111000111111100",
        "11111100111100000000000111111100",
        "11111110011110000000001111111100",
        "01111110011111000000011111110000",
        "01111111001111100000111111110000",
        "00111111100111110001111111100000",
        "00011111110111111011111111000000",
        "00001111111111111111111110000000",
        "00000111111111111111111100000000",
        "00000001111111111111111000000000",
        "00000000111111111111110000000000",
        "00000000000111111110000000000000",
        "00000000000000000000000000000000"
    ]
    
    # Create pixel data
    pixels = []
    for row in bitcoin_pattern:
        for char in row:
            if char == '1':
                pixels.append(bitcoin_orange)
            else:
                pixels.append(black)
    
    # BMP header for 16-bit RGB565
    file_size = 14 + 40 + (width * height * 2)  # Header + DIB header + pixel data
    
    # BMP file header (14 bytes)
    bmp_header = struct.pack('<2sIHHI',
        b'BM',          # Signature
        file_size,      # File size
        0,              # Reserved
        0,              # Reserved  
        54              # Offset to pixel data
    )
    
    # DIB header (40 bytes) - BITMAPINFOHEADER
    dib_header = struct.pack('<IIIHHIIIIII',
        40,             # DIB header size
        width,          # Image width
        height,         # Image height
        1,              # Planes
        16,             # Bits per pixel (RGB565)
        0,              # Compression (none)
        width * height * 2,  # Image size
        2835,           # X pixels per meter
        2835,           # Y pixels per meter
        0,              # Colors in palette
        0               # Important colors
    )
    
    # Write BMP file
    with open('/home/burns/7inchHackCart/squareline_files/assets/bitcoin_logo.bmp', 'wb') as f:
        f.write(bmp_header)
        f.write(dib_header)
        
        # Write pixels (BMP is bottom-up, so reverse rows)
        for y in range(height-1, -1, -1):
            for x in range(width):
                pixel = pixels[y * width + x]
                f.write(struct.pack('<H', pixel))
    
    print("Bitcoin logo BMP created successfully!")
    print("File: /home/burns/7inchHackCart/squareline_files/assets/bitcoin_logo.bmp")

if __name__ == "__main__":
    create_simple_bmp()