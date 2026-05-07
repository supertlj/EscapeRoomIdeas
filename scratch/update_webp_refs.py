import os

def update_extensions(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('.js', '.json')) and not file.lower().endswith('.bak'):
                filepath = os.path.join(subdir, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if '.png' in content.lower():
                        print(f"Updating references in {filepath}...")
                        # Case insensitive replace for .png to .webp
                        import re
                        new_content = re.sub(r'\.png', '.webp', content, flags=re.IGNORECASE)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error updating {filepath}: {e}")

if __name__ == "__main__":
    update_extensions('game/js')
    update_extensions('game/data')
