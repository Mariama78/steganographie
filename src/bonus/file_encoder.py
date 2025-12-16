"""
BONUS FEATURE: Hide files in images using LSB steganography.

This module extends the basic text steganography to support hiding
any type of file (PDF, ZIP, images, etc.) inside a PNG image.
"""

from PIL import Image
import os


def calculate_file_capacity(image: Image.Image) -> int:
    """
    Calculate the maximum file size (in bytes) that can be hidden in an image.
    
    We reserve space for:
    - 4 bytes for filename length
    - 256 bytes max for filename
    - 4 bytes for file size
    - The actual file data
    
    Args:
        image: PIL Image object
        
    Returns:
        Maximum file size in bytes that can be stored
    """
    width, height = image.size
    total_bits = width * height * 3  # 3 bits per pixel
    total_bytes = total_bits // 8
    # Reserve 264 bytes for metadata (4 + 256 + 4)
    return max(0, total_bytes - 264)


def hide_file(input_image_path: str, output_image_path: str, file_path: str) -> bool:
    """
    Hide a file inside an image using LSB substitution.
    
    Data format stored in image:
    - 4 bytes: filename length (big-endian)
    - N bytes: filename (UTF-8 encoded)
    - 4 bytes: file size (big-endian)
    - M bytes: file data
    
    Args:
        input_image_path: Path to the input PNG image
        output_image_path: Path where the output image will be saved
        file_path: Path to the file to hide
        
    Returns:
        True if successful, False if the file is too large
    """
    # Load the image
    image = Image.open(input_image_path)
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Read the file
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # Get filename only (not full path)
    filename = os.path.basename(file_path)
    filename_bytes = filename.encode('utf-8')
    
    if len(filename_bytes) > 256:
        filename_bytes = filename_bytes[:256]
    
    # Check capacity
    max_file_size = calculate_file_capacity(image)
    if len(file_data) > max_file_size:
        return False
    
    # Build the data to hide:
    # [filename_length (4 bytes)] [filename] [file_size (4 bytes)] [file_data]
    data_to_hide = bytearray()
    
    # Filename length (4 bytes, big-endian)
    data_to_hide.extend(len(filename_bytes).to_bytes(4, 'big'))
    
    # Filename
    data_to_hide.extend(filename_bytes)
    
    # File size (4 bytes, big-endian)
    data_to_hide.extend(len(file_data).to_bytes(4, 'big'))
    
    # File data
    data_to_hide.extend(file_data)
    
    # Convert to binary string
    binary_data = ''.join(format(byte, '08b') for byte in data_to_hide)
    
    # Get image dimensions and pixel data
    width, height = image.size
    pixels = list(image.getdata())
    
    # Check if we have enough pixels
    if len(binary_data) > len(pixels) * 3:
        return False
    
    # Modify pixels to hide the data
    new_pixels = []
    bit_index = 0
    total_bits = len(binary_data)
    
    for pixel in pixels:
        r, g, b = pixel[0], pixel[1], pixel[2]
        
        # Modify R component
        if bit_index < total_bits:
            r = (r & 0xFE) | int(binary_data[bit_index])
            bit_index += 1
        
        # Modify G component
        if bit_index < total_bits:
            g = (g & 0xFE) | int(binary_data[bit_index])
            bit_index += 1
        
        # Modify B component
        if bit_index < total_bits:
            b = (b & 0xFE) | int(binary_data[bit_index])
            bit_index += 1
        
        new_pixels.append((r, g, b))
    
    # Create new image with modified pixels
    new_image = Image.new('RGB', (width, height))
    new_image.putdata(new_pixels)
    
    # Save as PNG (lossless format)
    new_image.save(output_image_path, 'PNG')
    
    return True

