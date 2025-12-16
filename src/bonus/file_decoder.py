"""
BONUS FEATURE: Extract hidden files from images using LSB steganography.

This module extracts files that were hidden using the file_encoder module.
"""

from PIL import Image
import os


def extract_file(image_path: str, output_path: str = None) -> tuple[bool, str]:
    """
    Extract a hidden file from an image using LSB extraction.
    
    Args:
        image_path: Path to the PNG image containing the hidden file
        output_path: Optional path where to save the extracted file.
                    If not provided, uses the original filename.
        
    Returns:
        Tuple of (success: bool, filename_or_error: str)
    """
    # Load the image
    image = Image.open(image_path)
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Get pixel data
    pixels = list(image.getdata())
    
    # Extract all LSB bits
    all_bits = ''
    for pixel in pixels:
        r, g, b = pixel[0], pixel[1], pixel[2]
        all_bits += str(r & 1)
        all_bits += str(g & 1)
        all_bits += str(b & 1)
    
    # Convert bits to bytes
    def bits_to_bytes(bits: str) -> bytes:
        return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    
    try:
        # Read filename length (first 4 bytes = 32 bits)
        filename_length = int(all_bits[:32], 2)
        
        if filename_length <= 0 or filename_length > 256:
            return False, "Invalid file format or no hidden file found"
        
        # Read filename
        filename_start = 32
        filename_end = filename_start + (filename_length * 8)
        filename_bits = all_bits[filename_start:filename_end]
        filename = bits_to_bytes(filename_bits).decode('utf-8')
        
        # Read file size (4 bytes = 32 bits)
        filesize_start = filename_end
        filesize_end = filesize_start + 32
        file_size = int(all_bits[filesize_start:filesize_end], 2)
        
        if file_size <= 0:
            return False, "Invalid file size"
        
        # Read file data
        data_start = filesize_end
        data_end = data_start + (file_size * 8)
        
        if data_end > len(all_bits):
            return False, "File data corrupted or incomplete"
        
        file_data = bits_to_bytes(all_bits[data_start:data_end])
        
        # Determine output path
        if output_path:
            final_path = output_path
        else:
            # Use original filename in current directory
            final_path = filename
        
        # Create output directory if needed
        output_dir = os.path.dirname(final_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Write the file
        with open(final_path, 'wb') as f:
            f.write(file_data)
        
        return True, filename
        
    except Exception as e:
        return False, f"Error extracting file: {str(e)}"

