from PIL import Image
import os

paths = [
    r"f:\AntiGravity\EscapeRoomIdeas\game\assets\rooms\room_01\background.png",
    r"f:\AntiGravity\EscapeRoomIdeas\game\assets\rooms\room_01\zoom_guestbook.png",
    r"f:\AntiGravity\EscapeRoomIdeas\game\assets\rooms\room_01\zoom_safe_closed.png"
]

for p in paths:
    if os.path.exists(p):
        with Image.open(p) as img:
            print(f"{os.path.basename(p)}: {img.width}x{img.height}")
    else:
        print(f"{os.path.basename(p)}: Not found")
