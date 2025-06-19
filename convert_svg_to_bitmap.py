#!/usr/bin/env python3
"""
Convert the official Bitcoin SVG to a bitmap for LVGL
Since we don't have PIL/Pillow, we'll create a bitmap version by hand
based on the SVG structure
"""
import struct
import math

def create_bitcoin_bitmap_from_svg():
    """
    Create a 64x64 bitmap of the Bitcoin logo based on the official SVG
    """
    width = 64
    height = 64
    
    # Colors from the SVG
    bitcoin_orange = 0xF793  # #f7931a in RGB565
    white = 0xFFFF
    black = 0x0000
    
    # Create pixel array
    pixels = [black] * (width * height)
    
    # The SVG shows a circle with the Bitcoin "B" symbol
    # Let's create a simplified version based on the official design
    
    center_x, center_y = 32, 32
    radius = 30
    
    # Fill the circle with Bitcoin orange
    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            distance_sq = dx*dx + dy*dy
            
            if distance_sq <= radius*radius:
                pixels[y * width + x] = bitcoin_orange
    
    # Now draw the Bitcoin "B" symbol in white
    # Based on the official design, create the "B" shape
    
    # Vertical lines of the B (left side)
    b_center_x = center_x - 2
    b_top = center_y - 16
    b_bottom = center_y + 16
    b_middle = center_y
    
    # Left vertical line
    for y in range(b_top, b_bottom + 1):
        if 0 <= y < height:
            for x_offset in range(3):  # Make it thicker
                x = b_center_x - 6 + x_offset
                if 0 <= x < width:
                    pixels[y * width + x] = white
    
    # Top horizontal line
    for x in range(b_center_x - 6, b_center_x + 8):
        if 0 <= x < width:
            for y_offset in range(3):
                y = b_top + y_offset
                if 0 <= y < height:
                    pixels[y * width + x] = white
    
    # Middle horizontal line (shorter)
    for x in range(b_center_x - 6, b_center_x + 6):
        if 0 <= x < width:
            for y_offset in range(3):
                y = b_middle + y_offset
                if 0 <= y < height:
                    pixels[y * width + x] = white
    
    # Bottom horizontal line
    for x in range(b_center_x - 6, b_center_x + 8):
        if 0 <= x < width:
            for y_offset in range(3):
                y = b_bottom - 2 + y_offset
                if 0 <= y < height:
                    pixels[y * width + x] = white
    
    # Right side curves (simplified as vertical lines)
    # Top right curve
    for y in range(b_top + 3, b_middle - 1):
        if 0 <= y < height:
            for x_offset in range(3):
                x = b_center_x + 5 + x_offset
                if 0 <= x < width:
                    pixels[y * width + x] = white
    
    # Bottom right curve
    for y in range(b_middle + 4, b_bottom - 2):
        if 0 <= y < height:
            for x_offset in range(3):
                x = b_center_x + 6 + x_offset
                if 0 <= x < width:
                    pixels[y * width + x] = white
    
    # Add the two small vertical lines that extend above and below (characteristic of Bitcoin logo)
    # Top extension
    for y in range(b_top - 6, b_top):
        if 0 <= y < height:
            x = b_center_x - 2
            if 0 <= x < width:
                pixels[y * width + x] = white
                pixels[y * width + x + 1] = white
    
    # Bottom extension
    for y in range(b_bottom + 1, b_bottom + 7):
        if 0 <= y < height:
            x = b_center_x - 2
            if 0 <= x < width:
                pixels[y * width + x] = white
                pixels[y * width + x + 1] = white
    
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
    print("Creating official-style Bitcoin logo bitmap...")
    pixels, width, height = create_bitcoin_bitmap_from_svg()
    
    # Save as BMP
    bmp_path = "/home/burns/7inchHackCart/squareline_files/assets/bitcoin_logo.bmp"
    save_as_bmp(pixels, width, height, bmp_path)
    print(f"Bitcoin logo saved as: {bmp_path}")
    print(f"Size: {width}x{height}")

if __name__ == "__main__":
    main()