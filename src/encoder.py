"""
Encoder module for hiding messages in images using LSB steganography.
"""

from PIL import Image
from .utils import text_to_binary, calculate_capacity


def hide_message(input_path: str, output_path: str, secret: str) -> bool:
    """
    Hide a secret message in an image using LSB substitution.
    
    Args:
        input_path: Path to the input PNG image
        output_path: Path where the output image will be saved
        secret: The secret message to hide
        
    Returns:
        True if successful, False if the message is too long
    """
    # Load the image
    image = Image.open(input_path)
    
    # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Check capacity
    max_chars = calculate_capacity(image)
    if len(secret) > max_chars:
        return False
    
    # Convert message to binary and add null terminator
    binary_message = text_to_binary(secret) + '00000000'  # Null byte as delimiter
    
    # Get image dimensions and pixel data
    width, height = image.size
    pixels = list(image.getdata())
    
    # Modify pixels to hide the message
    new_pixels = []
    bit_index = 0
    total_bits = len(binary_message)
    
    for pixel in pixels:
        r, g, b = pixel[0], pixel[1], pixel[2]
        
        # Modify R component
        if bit_index < total_bits:
            r = (r & 0xFE) | int(binary_message[bit_index])
            bit_index += 1
        
        # Modify G component
        if bit_index < total_bits:
            g = (g & 0xFE) | int(binary_message[bit_index])
            bit_index += 1
        
        # Modify B component
        if bit_index < total_bits:
            b = (b & 0xFE) | int(binary_message[bit_index])
            bit_index += 1
        
        new_pixels.append((r, g, b))
    
    # Create new image with modified pixels
    new_image = Image.new('RGB', (width, height))
    new_image.putdata(new_pixels)
    
    # Save as PNG (lossless format)
    new_image.save(output_path, 'PNG')
    
    return True

