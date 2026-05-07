import os
from PIL import Image

def optimize_pngs(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.png') and not file.lower().endswith('.bak'):
                filepath = os.path.join(subdir, file)
                try:
                    with Image.open(filepath) as img:
                        original_size = os.path.getsize(filepath)
                        
                        # 1. Resize if larger than 1024
                        if img.width > 1024 or img.height > 1024:
                            print(f"Resizing {filepath} from {img.size} to 1024x1024")
                            img = img.resize((1024, 1024), Image.Resampling.LANCZOS)
                        
                        # 2. Convert to P (indexed) if it's a large background/zoom
                        # This can save massive space. We'll only do it if the file is > 1MB
                        save_kwargs = {"optimize": True}
                        if original_size > 1024 * 1024:
                             # Convert to RGB first to handle RGBA properly during quantization
                             if img.mode == 'RGBA':
                                 alpha = img.getchannel('A')
                                 img = img.convert('RGB').quantize(colors=256).convert('RGBA')
                                 img.putalpha(alpha)
                             else:
                                 img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
                        
                        img.save(filepath, "PNG", **save_kwargs)
                        new_size = os.path.getsize(filepath)
                        reduction = (original_size - new_size) / original_size * 100
                        print(f"Optimized {file}: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB ({reduction:.1f}% reduction)")
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    optimize_pngs('game/assets/rooms')
    optimize_pngs('game/assets/items')
