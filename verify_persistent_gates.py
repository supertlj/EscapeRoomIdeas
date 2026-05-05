"""
Verify that all persistent items are on the critical escape path.
A persistent item is 'gated' if the puzzle that rewards it is in the
dependency chain required to reach the final_action/escape.
"""
import os, json

rooms_dir = "Output/OurRooms"

for room_dir in sorted(os.listdir(rooms_dir)):
    if not room_dir.startswith("Room_"):
        continue
    path = os.path.join(rooms_dir, room_dir, "design.json")
    with open(path, "r", encoding="utf-8") as f:
        room = json.load(f)

    rnum = room["room_number"]
    persistent = room.get("persistent_items_found", [])
    if not persistent:
        continue

    puzzles = room.get("puzzles", [])
    puzzle_names = [p["puzzle_name"]["en"] for p in puzzles]

    # Build dependency chain — find which puzzles are on the critical path
    # Critical path = puzzles in the chain leading to the LAST puzzle (which gates escape)
    last_puzzle = puzzles[-1]["puzzle_name"]["en"]

    # Walk backwards through depends_on to find all critical path puzzles
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

    print(f"\nRoom {rnum}: {room['room_name']['en']}")
    print(f"  Critical path: {' -> '.join([p for p in puzzle_names if p in critical_path])}")
    print(f"  Non-critical:  {[p for p in puzzle_names if p not in critical_path]}")

    for item in persistent:
        item_id = item["id"]
        # Find which puzzle rewards this item
        rewarding_puzzle = None
        for p in puzzles:
            reward_text = p.get("reward", {}).get("en", "").lower()
            if item_id.replace("_", " ") in reward_text or item["name"]["en"].lower() in reward_text:
                rewarding_puzzle = p["puzzle_name"]["en"]
                break

        if rewarding_puzzle:
            on_critical = rewarding_puzzle in critical_path
            status = "ON CRITICAL PATH" if on_critical else "NOT ON CRITICAL PATH - NEEDS FIX"
            print(f"  Item '{item_id}': rewarded by '{rewarding_puzzle}' -> {status}")
        else:
            print(f"  Item '{item_id}': NOT tied to any puzzle reward -> NEEDS FIX (story-only?)")
            if item.get("narrative_only"):
                print(f"    (narrative_only=true, could auto-collect with story fragment)")
