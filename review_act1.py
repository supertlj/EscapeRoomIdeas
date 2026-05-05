"""
Act 1 Review Script — Validates all Room 1-10 design.json files
Checks: schema completeness, puzzle chains, hint counts, language parity,
        difficulty balance, escape mechanism variety, and narrative continuity.
"""
import os
import json

rooms_dir = "Output/OurRooms"
issues = []
stats = {
    "total_puzzles": 0,
    "total_hints": 0,
    "total_items": 0,
    "escape_mechanisms": [],
    "twists_used": [],
    "difficulty_scores": [],
    "mechanic_families": [],
    "puzzle_types": {"observation": 0, "item_use": 0, "logic_minigame": 0},
    "story_fragments": []
}

room_dirs = sorted([d for d in os.listdir(rooms_dir) if d.startswith("Room_")])
print(f"Found {len(room_dirs)} room directories\n")

for room_dir in room_dirs:
    path = os.path.join(rooms_dir, room_dir, "design.json")
    if not os.path.exists(path):
        issues.append(f"❌ MISSING: {path}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        room = json.load(f)

    rnum = room.get("room_number", "?")
    rname = room.get("room_name", {}).get("en", "Unknown")
    print(f"{'='*60}")
    print(f"Room {rnum}: {rname}")
    print(f"{'='*60}")

    # --- Schema checks ---
    required_fields = ["room_number", "room_name", "hotel_area", "act", "difficulty_tier",
                       "art_style", "perspective", "monetization", "room_description",
                       "story_fragment", "estimated_solve_time_minutes", "items", "puzzles",
                       "final_action", "escape_mechanism"]
    for field in required_fields:
        if field not in room:
            issues.append(f"Room {rnum}: Missing field '{field}'")

    # --- Language parity check ---
    bilingual_fields = ["room_name", "hotel_area", "room_description", "story_fragment", "final_action"]
    for field in bilingual_fields:
        val = room.get(field, {})
        if isinstance(val, dict):
            if "en" not in val:
                issues.append(f"Room {rnum}: '{field}' missing 'en'")
            if "zh" not in val:
                issues.append(f"Room {rnum}: '{field}' missing 'zh'")
            elif val.get("zh", "").strip() == "":
                issues.append(f"Room {rnum}: '{field}' has empty 'zh'")

    # --- Puzzle analysis ---
    puzzles = room.get("puzzles", [])
    puzzle_names = []
    print(f"  Puzzles: {len(puzzles)}")
    stats["total_puzzles"] += len(puzzles)

    for i, p in enumerate(puzzles):
        pname = p.get("puzzle_name", {}).get("en", f"Puzzle {i+1}")
        puzzle_names.append(pname)
        ptype = p.get("puzzle_type", "unknown")
        stats["puzzle_types"][ptype] = stats["puzzle_types"].get(ptype, 0) + 1

        # Check hints
        hints = p.get("hints", [])
        stats["total_hints"] += len(hints)
        if len(hints) != 3:
            issues.append(f"Room {rnum}, '{pname}': Expected 3 hints, got {len(hints)}")

        # Check hint language parity
        for j, hint in enumerate(hints):
            if isinstance(hint, dict):
                if "en" not in hint:
                    issues.append(f"Room {rnum}, '{pname}', hint {j+1}: missing 'en'")
                if "zh" not in hint:
                    issues.append(f"Room {rnum}, '{pname}', hint {j+1}: missing 'zh'")

        # Check solution steps language
        steps = p.get("solution_steps", [])
        for j, step in enumerate(steps):
            if isinstance(step, dict):
                if "en" not in step:
                    issues.append(f"Room {rnum}, '{pname}', step {j+1}: missing 'en'")
                if "zh" not in step:
                    issues.append(f"Room {rnum}, '{pname}', step {j+1}: missing 'zh'")

        # Check dependencies
        dep = p.get("depends_on")
        if dep and dep not in puzzle_names:
            # Check if it refers to a puzzle later in the list
            all_names_in_room = [pp.get("puzzle_name", {}).get("en", "") for pp in puzzles]
            if dep not in all_names_in_room:
                issues.append(f"Room {rnum}, '{pname}': depends_on '{dep}' not found in this room")

        # Collect stats
        diff = p.get("difficulty", 0)
        stats["difficulty_scores"].append(diff)
        twist = p.get("twist_applied")
        if twist:
            stats["twists_used"].append(twist)
        mech = p.get("mechanic_family", "unknown")
        stats["mechanic_families"].append(mech)

        # Print puzzle summary
        dep_str = f" (depends: {dep})" if dep else ""
        twist_str = f" [{twist}]" if twist else ""
        print(f"  [{i+1}] {pname} — {ptype}, diff={diff}{dep_str}{twist_str}")
        print(f"      Steps: {len(steps)}, Hints: {len(hints)}")

    # --- Items check ---
    items = room.get("items", [])
    stats["total_items"] += len(items)
    for item in items:
        if "id" not in item:
            issues.append(f"Room {rnum}: Item missing 'id'")
        name = item.get("name", {})
        if "en" not in name or "zh" not in name:
            issues.append(f"Room {rnum}: Item '{item.get('id', '?')}' missing language key")

    # --- Escape mechanism ---
    esc = room.get("escape_mechanism", "unknown")
    stats["escape_mechanisms"].append(esc)
    print(f"  Escape: {esc}")

    # --- Story fragment preview ---
    frag = room.get("story_fragment", {}).get("en", "")[:80]
    stats["story_fragments"].append(f"R{rnum}: {frag}...")
    print(f"  Story: {frag}...")
    print()

# --- Summary ---
print(f"\n{'='*60}")
print("ACT 1 REVIEW SUMMARY")
print(f"{'='*60}")
print(f"  Total Rooms: {len(room_dirs)}")
print(f"  Total Puzzles: {stats['total_puzzles']}")
print(f"  Total Hints: {stats['total_hints']} (expected: {stats['total_puzzles'] * 3})")
print(f"  Total Items: {stats['total_items']}")
print(f"  Avg Puzzles/Room: {stats['total_puzzles']/max(len(room_dirs),1):.1f}")
print(f"  Avg Difficulty: {sum(stats['difficulty_scores'])/max(len(stats['difficulty_scores']),1):.1f}")

print(f"\n  Puzzle Types:")
for pt, count in stats["puzzle_types"].items():
    print(f"    {pt}: {count}")

print(f"\n  Escape Mechanisms:")
from collections import Counter
for esc, count in Counter(stats["escape_mechanisms"]).items():
    print(f"    {esc}: {count}")

print(f"\n  Twists Used ({len(stats['twists_used'])}):")
for tw in stats["twists_used"]:
    print(f"    {tw}")

print(f"\n  Mechanic Families:")
for mech, count in Counter(stats["mechanic_families"]).most_common():
    print(f"    {mech}: {count}")

print(f"\n{'='*60}")
print(f"ISSUES FOUND: {len(issues)}")
print(f"{'='*60}")
if issues:
    for issue in issues:
        print(f"  ⚠️  {issue}")
else:
    print("  ✅ No issues found!")

print(f"\n{'='*60}")
print("NARRATIVE ARC (Story Fragments in Order)")
print(f"{'='*60}")
for frag in stats["story_fragments"]:
    print(f"  {frag}")
