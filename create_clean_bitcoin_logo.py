#!/usr/bin/env python3
"""
Create a clean, professional Bitcoin logo
"""
import struct
import math

def create_clean_bitcoin_logo():
    """
    Create a clean 48x48 Bitcoin logo with modern design
    """
    width = 48
    height = 48
    
    # Colors
    bitcoin_orange = 0xF793  # #f7931a in RGB565
    white = 0xFFFF
    black = 0x0000
    
    # Create pixel array with transparent background
    pixels = [black] * (width * height)
    
    center_x, center_y = 24, 24
    radius = 22
    
    # Create a clean circle
    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            distance_sq = dx*dx + dy*dy
            
            if distance_sq <= radius*radius:
                pixels[y * width + x] = bitcoin_orange
    
    # Create a very clean, simple "B" - more geometric and modern
    # B parameters
    b_left = center_x - 8
    b_right = center_x + 6
    b_top = center_y - 12
    b_bottom = center_y + 12
    b_middle = center_y
    
    # Main vertical line (left side of B)
    for y in range(b_top, b_bottom + 1):
        if 0 <= y < height:
            for x in range(b_left, b_left + 3):
                if 0 <= x < width:
                    pixels[y * width + x] = white
    
    # Top horizontal line
    for x in range(b_left, b_right):
        if 0 <= x < width:
            for y in range(b_top, b_top + 3):
                if 0 <= y < height:
                    pixels[y * width + x] = white
    
    # Middle horizontal line
    for x in range(b_left, b_right - 2):
        if 0 <= x < width:
            for y in range(b_middle - 1, b_middle + 2):
                if 0 <= y < height:
                    pixels[y * width + x] = white
    
    # Bottom horizontal line
    for x in range(b_left, b_right):
        if 0 <= x < width:
            for y in range(b_bottom - 2, b_bottom + 1):
                if 0 <= y < height:
                    pixels[y * width + x] = white
    
    # Right side curves (simplified)
    # Top curve
    for y in range(b_top + 3, b_middle - 3):
        if 0 <= y < height:
            for x in range(b_right - 3, b_right):
                if 0 <= x < width:
                    pixels[y * width + x] = white
    
    # Bottom curve
    for y in range(b_middle + 3, b_bottom - 2):
        if 0 <= y < height:
            for x in range(b_right - 3, b_right):
                if 0 <= x < width:
                    pixels[y * width + x] = white
    
    # Add the characteristic Bitcoin vertical lines above and below
    # Top line
    for y in range(b_top - 4, b_top):
        if 0 <= y < height:
            for x in range(center_x - 1, center_x + 2):
                if 0 <= x < width:
                    pixels[y * width + x] = white
    
    # Bottom line
    for y in range(b_bottom + 1, b_bottom + 5):
        if 0 <= y < height:
            for x in range(center_x - 1, center_x + 2):
                if 0 <= x < width:
                    pixels[y * width + x] = white
    
    return pixels, width, height

def save_as_bmp(pixels, width, height, filename):
    """Save the pixel data as a BMP file"""
    
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
    with open(filename, 'wb') as f:
        f.write(bmp_header)
        f.write(dib_header)
        
        # Write pixels (BMP is bottom-up, so reverse rows)
        for y in range(height-1, -1, -1):
            for x in range(width):
                pixel = pixels[y * width + x]
                f.write(struct.pack('<H', pixel))

def main():
    print("Creating clean, professional Bitcoin logo...")
    pixels, width, height = create_clean_bitcoin_logo()
    
    # Save as BMP
    bmp_path = "/home/burns/7inchHackCart/squareline_files/assets/bitcoin_logo.bmp"
    save_as_bmp(pixels, width, height, bmp_path)
    print(f"Clean Bitcoin logo saved as: {bmp_path}")
    print(f"Size: {width}x{height}")

if __name__ == "__main__":
    main()