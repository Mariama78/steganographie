"""
Command-line interface for the steganography application.
"""

import argparse
import sys
import os

from .encoder import hide_message
from .decoder import reveal_message


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog='stegano',
        description='Hide and reveal secret messages in PNG images using LSB steganography.'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Hide command
    hide_parser = subparsers.add_parser('hide', help='Hide a secret message in an image')
    hide_parser.add_argument('-i', '--input', required=True, help='Path to the input PNG image')
    hide_parser.add_argument('-o', '--output', required=True, help='Path for the output PNG image')
    hide_parser.add_argument('-s', '--secret', required=True, help='The secret message to hide')
    
    # Reveal command
    reveal_parser = subparsers.add_parser('reveal', help='Reveal a hidden message from an image')
    reveal_parser.add_argument('image', help='Path to the PNG image containing the hidden message')
    
    # ========================================
    # BONUS FEATURES
    # ========================================
    
    # Hide file command (BONUS)
    hidefile_parser = subparsers.add_parser('hidefile', help='[BONUS] Hide a file inside an image')
    hidefile_parser.add_argument('-i', '--input', required=True, help='Path to the input PNG image')
    hidefile_parser.add_argument('-o', '--output', required=True, help='Path for the output PNG image')
    hidefile_parser.add_argument('-f', '--file', required=True, help='Path to the file to hide')
    
    # Extract file command (BONUS)
    extract_parser = subparsers.add_parser('extract', help='[BONUS] Extract a hidden file from an image')
    extract_parser.add_argument('image', help='Path to the PNG image containing the hidden file')
    extract_parser.add_argument('-o', '--output', required=False, help='Optional output path for the extracted file')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'hide':
        # Validate input file exists
        if not os.path.exists(args.input):
            print(f"--> /!\\ Input file not found: {args.input}")
            sys.exit(1)
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Hide the message
        success = hide_message(args.input, args.output, args.secret)
        
        if not success:
            print("--> /!\\ The secret string exceeds the maximum length supported by the image.")
            sys.exit(1)
    
    elif args.command == 'reveal':
        # Validate input file exists
        if not os.path.exists(args.image):
            print(f"--> /!\\ Image file not found: {args.image}")
            sys.exit(1)
        
        # Reveal the message
        message = reveal_message(args.image)
        print(f'--> secret message is: "{message}"')
    
    # ========================================
    # BONUS COMMANDS
    # ========================================
    
    elif args.command == 'hidefile':
        from .bonus.file_encoder import hide_file
        
        # Validate input image exists
        if not os.path.exists(args.input):
            print(f"--> /!\\ Input image not found: {args.input}")
            sys.exit(1)
        
        # Validate file to hide exists
        if not os.path.exists(args.file):
            print(f"--> /!\\ File to hide not found: {args.file}")
            sys.exit(1)
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Hide the file
        success = hide_file(args.input, args.output, args.file)
        
        if success:
            print(f'--> File "{os.path.basename(args.file)}" hidden successfully in {args.output}')
        else:
            print("--> /!\\ The file is too large to be hidden in this image.")
            sys.exit(1)
    
    elif args.command == 'extract':
        from .bonus.file_decoder import extract_file
        
        # Validate input image exists
        if not os.path.exists(args.image):
            print(f"--> /!\\ Image file not found: {args.image}")
            sys.exit(1)
        
        # Extract the file
        success, result = extract_file(args.image, args.output)
        
        if success:
            print(f'--> File extracted successfully: "{result}"')
        else:
            print(f"--> /!\\ {result}")
            sys.exit(1)


if __name__ == '__main__':
    main()

