import os
from PIL import Image

def convert_to_webp(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.png') and not file.lower().endswith('.bak'):
                png_path = os.path.join(subdir, file)
                webp_path = os.path.splitext(png_path)[0] + '.webp'
                try:
                    with Image.open(png_path) as img:
                        print(f"Converting {png_path} to WebP...")
                        # Ensure we resize to 1024 if not already done (safety check)
                        if img.width > 1024 or img.height > 1024:
                            img = img.resize((1024, 1024), Image.Resampling.LANCZOS)
                        
                        # Save as WebP with quality 80 (great balance)
                        img.save(webp_path, "WEBP", quality=80, method=6)
                        
                        old_size = os.path.getsize(png_path)
                        new_size = os.path.getsize(webp_path)
                        reduction = (old_size - new_size) / old_size * 100
                        print(f"Done: {old_size/1024:.1f}KB -> {new_size/1024:.1f}KB ({reduction:.1f}% reduction)")
                        
                        # Optional: Delete the original PNG if successful
                        # os.remove(png_path)
                except Exception as e:
                    print(f"Error converting {png_path}: {e}")

if __name__ == "__main__":
    convert_to_webp('game/assets/rooms')
    convert_to_webp('game/assets/items')
