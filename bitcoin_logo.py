#!/usr/bin/env python3
"""
Generate a Bitcoin logo BMP file for the ESP32 display
"""
from PIL import Image, ImageDraw
import os

def create_bitcoin_logo():
    # Create a 64x64 image with transparent background
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Bitcoin orange color
    bitcoin_orange = (247, 147, 26, 255)  # #F7931A
    
    # Draw outer circle
    margin = 4
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=bitcoin_orange, outline=None)
    
    # Draw the Bitcoin "B" symbol in white
    # This is a simplified version of the Bitcoin logo
    white = (255, 255, 255, 255)
    
    # Vertical line for the B
    line_width = 4
    x_center = size // 2
    y_start = size // 4
    y_end = 3 * size // 4
    
    # Main vertical line
    draw.rectangle([x_center - 10, y_start, x_center - 10 + line_width, y_end], fill=white)
    
    # Top horizontal lines for the B
    draw.rectangle([x_center - 10, y_start, x_center + 8, y_start + line_width], fill=white)
    draw.rectangle([x_center - 10, y_start + 12, x_center + 6, y_start + 12 + line_width], fill=white)
    draw.rectangle([x_center - 10, y_end - line_width, x_center + 8, y_end], fill=white)
    
    # Right curves (simplified as rectangles)
    draw.rectangle([x_center + 4, y_start + line_width, x_center + 8, y_start + 12], fill=white)
    draw.rectangle([x_center + 2, y_start + 16, x_center + 6, y_end - line_width], fill=white)
    
    # Convert to RGB (remove alpha) for BMP
    rgb_img = Image.new('RGB', img.size, (0, 0, 0))
    rgb_img.paste(img, mask=img.split()[-1])  # Use alpha as mask
    
    return rgb_img

def main():
    print("Creating Bitcoin logo...")
    logo = create_bitcoin_logo()
    
    # Save as BMP
    bmp_path = "/home/burns/7inchHackCart/squareline_files/assets/bitcoin_logo.bmp"
    logo.save(bmp_path, "BMP")
    print(f"Bitcoin logo saved as: {bmp_path}")
    
    # Also save a copy for easy viewing
    logo.save("/home/burns/7inchHackCart/bitcoin_logo_preview.png", "PNG")
    print("Preview saved as: bitcoin_logo_preview.png")

if __name__ == "__main__":
    main()