#!/usr/bin/env python3
"""
Convert the official Bitcoin logo BMP to LVGL format
"""
import struct

def convert_official_logo():
    # Read the BMP file
    with open('/home/burns/7inchHackCart/squareline_files/assets/bitcoin_logo.bmp', 'rb') as f:
        data = f.read()
    
    # Skip BMP headers (54 bytes) and get pixel data
    pixel_data = data[54:]
    
    # Convert to C array format
    c_array = "// Official Bitcoin logo 64x64 RGB565\n"
    c_array += "#include \"lvgl.h\"\n\n"
    c_array += "#ifndef LV_ATTRIBUTE_MEM_ALIGN\n"
    c_array += "#define LV_ATTRIBUTE_MEM_ALIGN\n"
    c_array += "#endif\n\n"
    c_array += "const LV_ATTRIBUTE_MEM_ALIGN uint8_t ui_img_bitcoin_logo_map[] = {\n"
    
    # Convert pixel data to hex
    for i in range(0, len(pixel_data), 16):
        c_array += "  "
        for j in range(16):
            if i + j < len(pixel_data):
                c_array += f"0x{pixel_data[i + j]:02x}, "
            else:
                break
        c_array += "\n"
    
    c_array = c_array.rstrip(", \n") + "\n"
    c_array += "};\n\n"
    
    c_array += "const lv_img_dsc_t ui_img_bitcoin_logo = {\n"
    c_array += "  .header.cf = LV_IMG_CF_TRUE_COLOR,\n"
    c_array += "  .header.always_zero = 0,\n"
    c_array += "  .header.reserved = 0,\n"
    c_array += "  .header.w = 64,\n"
    c_array += "  .header.h = 64,\n"
    c_array += "  .data_size = sizeof(ui_img_bitcoin_logo_map),\n"
    c_array += "  .data = ui_img_bitcoin_logo_map,\n"
    c_array += "};\n"
    
    # Write to C file
    with open('/home/burns/7inchHackCart/src/UI/images/ui_img_bitcoin_logo.c', 'w') as f:
        f.write(c_array)
    
    print("Official Bitcoin logo converted to LVGL C format!")
    print("File: /home/burns/7inchHackCart/src/UI/images/ui_img_bitcoin_logo.c")
    print("Size: 64x64 pixels")

if __name__ == "__main__":
    convert_official_logo()