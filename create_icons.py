#!/usr/bin/env python3
"""
Create different icon formats from nna.png for various platforms
"""

from PIL import Image
import os

def create_icons():
    """Create icon files for different platforms"""
    
    # Load the source image
    if not os.path.exists('nna.png'):
        print("❌ nna.png not found!")
        return
    
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Load and process the image
    img = Image.open('nna.png')
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    print(f"📐 Source image size: {img.size}")
    
    # Create different sizes and formats
    sizes = [16, 32, 48, 64, 128, 256, 512, 1024]
    
    # Create PNG icons in different sizes
    for size in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f'assets/icon_{size}x{size}.png')
        print(f"✅ Created icon_{size}x{size}.png")
    
    # Create ICO file for Windows (multiple sizes in one file)
    ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    ico_images = []
    for size in ico_sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        ico_images.append(resized)
    
    # Save as ICO
    ico_images[0].save('assets/icon.ico', format='ICO', sizes=ico_sizes)
    print("✅ Created icon.ico for Windows")
    
    # Create ICNS for macOS (requires pillow-heif or just use PNG)
    try:
        # For macOS, we'll use a high-res PNG
        mac_icon = img.resize((1024, 1024), Image.Resampling.LANCZOS)
        mac_icon.save('assets/icon.icns.png')  # macOS can use PNG as icon
        print("✅ Created icon.icns.png for macOS")
    except Exception as e:
        print(f"⚠️  Could not create ICNS: {e}")
    
    # Copy the original as the main icon
    img.save('assets/icon.png')
    print("✅ Created assets/icon.png")
    
    print("\n🎉 Icon creation complete!")
    print("📁 Available icons:")
    for file in sorted(os.listdir('assets')):
        if file.startswith('icon'):
            size = os.path.getsize(f'assets/{file}')
            print(f"   - {file} ({size:,} bytes)")

if __name__ == "__main__":
    create_icons()