"""
Decoder module for revealing hidden messages from images using LSB steganography.
"""

from PIL import Image
from .utils import binary_to_text


def reveal_message(image_path: str) -> str:
    """
    Reveal a hidden message from an image using LSB extraction.
    
    Args:
        image_path: Path to the PNG image containing the hidden message
        
    Returns:
        The revealed secret message
    """
    # Load the image
    image = Image.open(image_path)
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Get pixel data
    pixels = list(image.getdata())
    
    # Extract LSB from each color component
    binary_message = ''
    
    for pixel in pixels:
        r, g, b = pixel[0], pixel[1], pixel[2]
        
        # Extract LSB from each component
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)
        
        # Check for null terminator every 8 bits (after we have at least 8 bits)
        # This is an optimization to stop early
        if len(binary_message) >= 8 and len(binary_message) % 8 == 0:
            # Check the last byte
            last_byte = binary_message[-8:]
            if last_byte == '00000000':
                # Remove the null terminator and stop
                binary_message = binary_message[:-8]
                break
    
    # Convert binary to text
    message = binary_to_text(binary_message)
    
    return message

