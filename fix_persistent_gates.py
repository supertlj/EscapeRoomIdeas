"""
Fix persistent item gating:
1. Add acquisition_puzzle and critical_path_guaranteed to each persistent item
2. Fix Room 5's puzzle chain so map_fragment is on the critical path
3. For narrative-only items, set auto_collect=true (collected when story fragment is displayed)
"""
import os, json

rooms_dir = "Output/OurRooms"

# --- Fix definitions ---
fixes = {
    4: {
        "items_update": {
            "postcard_to_margaret": {
                "acquisition_method": "auto_collect_with_story",
                "acquisition_puzzle": None,
                "critical_path_guaranteed": True,
                "gate_note": {
                    "en": "Auto-collected when the player reads the story fragment. Cannot leave without viewing.",
                    "zh": "当玩家阅读故事碎片时自动收集。不查看无法离开。"
                }
            }
        },
        "chain_fix": None
    },
    5: {
        "items_update": {
            "basement_map_fragment": {
                "acquisition_method": "puzzle_reward",
                "acquisition_puzzle": "Room Number Sort",
                "critical_path_guaranteed": True,
                "gate_note": {
                    "en": "Rewarded by 'Room Number Sort' puzzle, which is now on the critical escape path.",
                    "zh": "由'房间号分拣'谜题奖励，该谜题现在在关键逃脱路径上。"
                }
            }
        },
        # Fix: Make "Package Weight Cipher" depend on "Room Number Sort"
        # so the map fragment puzzle is on the critical path
        "chain_fix": {
            "puzzle_name": "Package Weight Cipher",
            "new_depends_on": "Room Number Sort"
        }
    },
    7: {
        "items_update": {
            "swimming_club_card": {
                "acquisition_method": "puzzle_reward",
                "acquisition_puzzle": "Chromatic Numbers",
                "critical_path_guaranteed": True,
                "gate_note": {
                    "en": "Found inside the waterproof pouch rewarded by 'Chromatic Numbers', which is on the critical path.",
                    "zh": "在'彩色数字'谜题奖励的防水袋内找到，该谜题在关键路径上。"
                }
            }
        },
        "chain_fix": None
    },
    10: {
        "items_update": {
            "hotel_blueprint": {
                "acquisition_method": "puzzle_reward",
                "acquisition_puzzle": "Spotlight Reveal",
                "critical_path_guaranteed": True,
                "gate_note": {
                    "en": "Found behind the portrait, revealed by 'Spotlight Reveal' puzzle, which is on the critical path.",
                    "zh": "在肖像画后面找到，由'聚光灯揭秘'谜题揭示，该谜题在关键路径上。"
                }
            }
        },
        "chain_fix": None
    }
}

for room_dir in sorted(os.listdir(rooms_dir)):
    if not room_dir.startswith("Room_"):
        continue
    path = os.path.join(rooms_dir, room_dir, "design.json")
    with open(path, "r", encoding="utf-8") as f:
        room = json.load(f)

    rnum = room["room_number"]
    if rnum not in fixes:
        continue

    fix = fixes[rnum]
    changed = False

    # 1. Update persistent items with acquisition metadata
    for item in room.get("persistent_items_found", []):
        if item["id"] in fix["items_update"]:
            item.update(fix["items_update"][item["id"]])
            changed = True
            print(f"Room {rnum}: Updated persistent item '{item['id']}' with acquisition gate")

    # 2. Fix puzzle chain if needed
    if fix["chain_fix"]:
        target_name = fix["chain_fix"]["puzzle_name"]
        new_dep = fix["chain_fix"]["new_depends_on"]
        for p in room.get("puzzles", []):
            if p["puzzle_name"]["en"] == target_name:
                old_dep = p.get("depends_on")
                p["depends_on"] = new_dep
                changed = True
                print(f"Room {rnum}: Fixed chain — '{target_name}' now depends on '{new_dep}' (was: {old_dep})")

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(room, f, ensure_ascii=False, indent=2)

print("\n--- Verification ---")

# Re-verify all rooms
for room_dir in sorted(os.listdir(rooms_dir)):
    if not room_dir.startswith("Room_"):
        continue
    path = os.path.join(rooms_dir, room_dir, "design.json")
    with open(path, "r", encoding="utf-8") as f:
        room = json.load(f)

    persistent = room.get("persistent_items_found", [])
    if not persistent:
        continue

    rnum = room["room_number"]
    puzzles = room.get("puzzles", [])
    last_puzzle = puzzles[-1]["puzzle_name"]["en"]

    # Rebuild critical path
    critical_path = set()
    queue = [last_puzzle]
    while queue:
        current = queue.pop()
        critical_path.add(current)
        for p in puzzles:
            if p["puzzle_name"]["en"] == current:
                dep = p.get("depends_on")
                if dep and dep not in critical_path:
                    queue.append(dep)

    for item in persistent:
        acq = item.get("acquisition_puzzle")
        method = item.get("acquisition_method", "unknown")
        if method == "auto_collect_with_story":
            print(f"R{rnum} '{item['id']}': AUTO-COLLECT with story -> GUARANTEED")
        elif acq and acq in critical_path:
            print(f"R{rnum} '{item['id']}': puzzle '{acq}' -> ON CRITICAL PATH -> GUARANTEED")
        elif acq:
            print(f"R{rnum} '{item['id']}': puzzle '{acq}' -> NOT ON CRITICAL PATH -> PROBLEM!")
        else:
            print(f"R{rnum} '{item['id']}': no acquisition method -> PROBLEM!")
