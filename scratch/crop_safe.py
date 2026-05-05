from PIL import Image
import os

def crop_safe():
    img_path = 'game/assets/rooms/room_01/background.png'
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found")
        return

    img = Image.open(img_path)
    # The safe is around x:50, y:650, w:450, h:350 in the 1024x1024 art space
    # We'll take a slightly larger crop to give the AI context
    left = 0
    top = 600
    right = 500
    bottom = 1024
    
    crop = img.crop((left, top, right, bottom))
    crop_path = 'game/assets/rooms/room_01/safe_reference.png'
    crop.save(crop_path)
    print(f"Saved reference crop to {crop_path}")

if __name__ == "__main__":
    crop_safe()
