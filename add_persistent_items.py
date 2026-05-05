"""
Add persistent_items_found and persistent_items_required fields
to all Act 1 room design.json files.
"""
import os
import json

rooms_dir = "Output/OurRooms"

# Define which rooms introduce persistent items and which require them
persistent_config = {
    1: {
        "found": [],
        "required": []
    },
    2: {
        "found": [],
        "required": []
    },
    3: {
        "found": [],
        "required": []
    },
    4: {
        "found": [
            {
                "id": "postcard_to_margaret",
                "name": {"en": "Unsent Postcard to Margaret", "zh": "未寄出的给玛格丽特的明信片"},
                "found_in_room": 4,
                "used_in_room": 27,
                "narrative_only": True,
                "description": {
                    "en": "A postcard revealing Edmund's sister Margaret and his reason for disappearing.",
                    "zh": "一张明信片，揭示了埃德蒙的姐姐玛格丽特以及他消失的原因。"
                }
            }
        ],
        "required": []
    },
    5: {
        "found": [
            {
                "id": "basement_map_fragment",
                "name": {"en": "Basement Map Fragment", "zh": "地下室地图碎片"},
                "found_in_room": 5,
                "used_in_room": 29,
                "narrative_only": False,
                "description": {
                    "en": "A hand-drawn map of the hotel basement with an X marking a specific location. Required to navigate the Underground Spring in Room 29.",
                    "zh": "一张手绘的酒店地下室地图，X标记了一个特定位置。在第29间房间的地下泉水中需要用来导航。"
                }
            }
        ],
        "required": []
    },
    6: {
        "found": [],
        "required": []
    },
    7: {
        "found": [
            {
                "id": "swimming_club_card",
                "name": {"en": "Swimming Club Membership Card", "zh": "游泳俱乐部会员卡"},
                "found_in_room": 7,
                "used_in_room": None,
                "narrative_only": True,
                "description": {
                    "en": "Edmund's founding member card for Grandview Aquatics. Shows arrows pointing under the deep end.",
                    "zh": "埃德蒙的格兰德维尤水上俱乐部创始会员卡。显示箭头指向深水区下方。"
                }
            }
        ],
        "required": []
    },
    8: {
        "found": [],
        "required": []
    },
    9: {
        "found": [],
        "required": []
    },
    10: {
        "found": [
            {
                "id": "hotel_blueprint",
                "name": {"en": "Hotel Blueprint (Hidden Floor -1.5)", "zh": "酒店蓝图（隐藏地下1.5层）"},
                "found_in_room": 10,
                "used_in_room": 21,
                "narrative_only": False,
                "description": {
                    "en": "Architectural cross-section revealing a hidden floor between basement and sub-basement, labeled 'Level -1.5: The Workshop.' Note reads: 'The way down opens from the clock tower.'",
                    "zh": "建筑横截面图，揭示了地下室和地下二层之间的一个隐藏楼层，标注为'地下1.5层：工作室。'注释写道：'通往下方的路从钟楼打开。'"
                }
            }
        ],
        "required": []
    }
}

# Update each room
for room_dir in sorted(os.listdir(rooms_dir)):
    if not room_dir.startswith("Room_"):
        continue
    path = os.path.join(rooms_dir, room_dir, "design.json")
    if not os.path.exists(path):
        continue

    with open(path, "r", encoding="utf-8") as f:
        room = json.load(f)

    rnum = room["room_number"]
    config = persistent_config.get(rnum, {"found": [], "required": []})

    # Add the new fields right after escape_mechanism
    room["persistent_items_found"] = config["found"]
    room["persistent_items_required"] = config["required"]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(room, f, ensure_ascii=False, indent=2)

    found_count = len(config["found"])
    req_count = len(config["required"])
    status = ""
    if found_count > 0:
        items = ", ".join([i["id"] for i in config["found"]])
        status = f" -> FOUND: {items}"
    if req_count > 0:
        items = ", ".join([i["id"] for i in config["required"]])
        status += f" -> REQUIRES: {items}"
    if not status:
        status = " (no persistent items)"

    print(f"Room {rnum:>2}: Updated{status}")

print("\nDone! All rooms updated with persistent inventory tracking.")
