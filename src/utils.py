"""
Utility functions for steganography operations.
"""

from PIL import Image


def text_to_binary(text: str) -> str:
    """
    Convert a text string to its binary representation.
    Each character is converted to 8 bits.
    
    Args:
        text: The text to convert
        
    Returns:
        Binary string representation of the text
    """
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary


def binary_to_text(binary: str) -> str:
    """
    Convert a binary string back to text.
    
    Args:
        binary: Binary string (multiple of 8 bits)
        
    Returns:
        The decoded text string
    """
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            char_code = int(byte, 2)
            if char_code == 0:  # Null terminator
                break
            text += chr(char_code)
    return text


def calculate_capacity(image: Image.Image) -> int:
    """
    Calculate the maximum number of characters that can be hidden in an image.
    
    Each pixel has 3 color components (R, G, B), and we can store 1 bit per component.
    So we get 3 bits per pixel. Each character needs 8 bits.
    
    Args:
        image: PIL Image object
        
    Returns:
        Maximum number of characters that can be stored
    """
    width, height = image.size
    total_bits = width * height * 3  # 3 bits per pixel (1 per RGB component)
    # Subtract 8 bits for the null terminator
    max_chars = (total_bits - 8) // 8
    return max_chars


def get_image_mode(image: Image.Image) -> str:
    """
    Get the image mode and ensure it's compatible with our steganography.
    
    Args:
        image: PIL Image object
        
    Returns:
        The image mode (RGB or RGBA)
    """
    if image.mode not in ('RGB', 'RGBA'):
        return 'RGB'
    return image.mode

