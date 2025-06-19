#!/usr/bin/env python3
"""
Create a better, simpler Bitcoin logo BMP file
"""
import struct

def create_better_bitcoin_logo():
    # Create a 48x48 16-bit BMP (RGB565 format for ESP32)
    width = 48
    height = 48
    
    # Bitcoin orange in RGB565: #F7931A -> 0xF793
    bitcoin_orange = 0xF793
    white = 0xFFFF
    black = 0x0000
    
    # Much simpler Bitcoin logo - just a circle with a "B"
    # Create the pattern programmatically
    pixels = [black] * (width * height)
    
    center_x, center_y = width // 2, height // 2
    radius = 20
    
    # Draw filled circle
    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            if dx*dx + dy*dy <= radius*radius:
                pixels[y * width + x] = bitcoin_orange
    
    # Draw a simple "B" in white on the orange circle
    # Vertical line of the B
    for y in range(center_y - 12, center_y + 13):
        if 0 <= y < height:
            x = center_x - 6
            if 0 <= x < width:
                pixels[y * width + x] = white
                pixels[y * width + x + 1] = white
    
    # Top horizontal line
    for x in range(center_x - 6, center_x + 4):
        if 0 <= x < width:
            y = center_y - 12
            if 0 <= y < height:
                pixels[y * width + x] = white
                pixels[(y + 1) * width + x] = white
    
    # Middle horizontal line
    for x in range(center_x - 6, center_x + 2):
        if 0 <= x < width:
            y = center_y - 1
            if 0 <= y < height:
                pixels[y * width + x] = white
                pixels[(y + 1) * width + x] = white
    
    # Bottom horizontal line
    for x in range(center_x - 6, center_x + 4):
        if 0 <= x < width:
            y = center_y + 11
            if 0 <= y < height:
                pixels[y * width + x] = white
                pixels[(y + 1) * width + x] = white
    
    # Right curves (simplified vertical lines)
    for y in range(center_y - 10, center_y - 1):
        if 0 <= y < height:
            x = center_x + 2
            if 0 <= x < width:
                pixels[y * width + x] = white
                pixels[y * width + x + 1] = white
    
    for y in range(center_y + 2, center_y + 11):
        if 0 <= y < height:
            x = center_x + 2
            if 0 <= x < width:
                pixels[y * width + x] = white
                pixels[y * width + x + 1] = white
    
    # BMP header for 16-bit RGB565
    file_size = 14 + 40 + (width * height * 2)
    
    # BMP file header (14 bytes)
    bmp_header = struct.pack('<2sIHHI',
        b'BM',          # Signature
        file_size,      # File size
        0,              # Reserved
        0,              # Reserved  
        54              # Offset to pixel data
    )
    
    # DIB header (40 bytes)
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
    
    print(f"Better Bitcoin logo BMP created! ({width}x{height})")
    print("File: /home/burns/7inchHackCart/squareline_files/assets/bitcoin_logo.bmp")

if __name__ == "__main__":
    create_better_bitcoin_logo()