#!/usr/bin/env python3
"""
Main entry point for the steganography CLI application.
Usage:
    python stegano.py hide -i <input_image> -o <output_image> -s "secret message"
    python stegano.py reveal <image>
"""

from src.cli import main

if __name__ == '__main__':
    main()

