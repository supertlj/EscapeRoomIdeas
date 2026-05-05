"""
Aggregate and analyze all 50 room analysis.json files
to build a comprehensive design reference report.
"""
import os
import json
from collections import Counter, defaultdict

output_dir = "Output"
all_rooms = []

# Load all analysis files
for i in range(1, 51):
    path = os.path.join(output_dir, f"Level_{i}", "analysis.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_rooms.append(data)
    else:
        print(f"WARNING: Missing Level_{i}/analysis.json")

print(f"Loaded {len(all_rooms)} rooms\n")

# --- 1. PUZZLE COUNTS ---
puzzle_counts = Counter()
for room in all_rooms:
    n = len(room.get("puzzles", []))
    puzzle_counts[n] += 1

print("=" * 60)
print("PUZZLE COUNT DISTRIBUTION")
print("=" * 60)
for count in sorted(puzzle_counts.keys()):
    levels = [str(r["level"]) for r in all_rooms if len(r.get("puzzles", [])) == count]
    print(f"  {count} puzzles: {puzzle_counts[count]} rooms — Levels: {', '.join(levels)}")

# --- 2. KEY MOMENT COUNTS ---
km_counts = Counter()
for room in all_rooms:
    n = len(room.get("key_moments", []))
    km_counts[n] += 1

print(f"\n{'=' * 60}")
print("KEY MOMENTS COUNT DISTRIBUTION")
print("=" * 60)
for count in sorted(km_counts.keys()):
    print(f"  {count} moments: {km_counts[count]} rooms")

# --- 3. ALL PUZZLE NAMES ---
print(f"\n{'=' * 60}")
print("ALL PUZZLE NAMES (by level)")
print("=" * 60)
for room in all_rooms:
    level = room["level"]
    puzzles = [p["puzzle_name"] for p in room.get("puzzles", [])]
    print(f"  L{level:02d}: {' | '.join(puzzles)}")

# --- 4. ALL ITEMS USED ---
all_items = []
for room in all_rooms:
    for puzzle in room.get("puzzles", []):
        for item in puzzle.get("items_used", []):
            all_items.append(item)

item_counts = Counter(all_items)
print(f"\n{'=' * 60}")
print(f"ALL ITEMS USED (total unique: {len(item_counts)})")
print("=" * 60)
for item, count in item_counts.most_common():
    print(f"  {item}: used {count}x")

# --- 5. ROOM DESCRIPTIONS ---
print(f"\n{'=' * 60}")
print("ALL ROOM DESCRIPTIONS")
print("=" * 60)
for room in all_rooms:
    print(f"  L{room['level']:02d}: {room['room_description']}")

# --- 6. FINAL ACTIONS / ESCAPE MECHANISMS ---
print(f"\n{'=' * 60}")
print("ALL FINAL ACTIONS (Escape Mechanisms)")
print("=" * 60)
for room in all_rooms:
    print(f"  L{room['level']:02d}: {room.get('final_action', 'N/A')}")

# --- 7. PUZZLE REWARD TYPES ---
reward_keywords = defaultdict(list)
for room in all_rooms:
    for puzzle in room.get("puzzles", []):
        reward = puzzle.get("reward", "").lower()
        level = room["level"]
        if "key" in reward:
            reward_keywords["Key"].append(level)
        if "code" in reward:
            reward_keywords["Code/Number"].append(level)
        if "token" in reward or "emblem" in reward:
            reward_keywords["Token/Emblem"].append(level)
        if "unlock" in reward or "open" in reward:
            reward_keywords["Unlocks Something"].append(level)
        if "clue" in reward or "reveal" in reward:
            reward_keywords["Visual Clue/Reveal"].append(level)
        if "tool" in reward or "screwdriver" in reward or "hammer" in reward or "knife" in reward:
            reward_keywords["Tool"].append(level)

print(f"\n{'=' * 60}")
print("PUZZLE REWARD CATEGORIES")
print("=" * 60)
for cat, levels in sorted(reward_keywords.items(), key=lambda x: -len(x[1])):
    print(f"  {cat}: {len(levels)} occurrences")

# --- 8. PUZZLE MECHANIC CLASSIFICATION ---
print(f"\n{'=' * 60}")
print("PUZZLE SOLUTION STEP KEYWORDS (frequency analysis)")
print("=" * 60)

step_keywords = Counter()
keyword_list = [
    "code", "enter", "count", "color", "match", "sequence", "rotate",
    "slide", "connect", "key", "unlock", "combine", "place", "insert",
    "observe", "cut", "use", "open", "find", "examine", "tap",
    "align", "press", "arrange", "swap", "puzzle", "pattern",
    "number", "symbol", "dial", "grid", "pipe", "circuit", "wire",
    "memory", "simon", "jigsaw", "peg", "jump"
]

for room in all_rooms:
    for puzzle in room.get("puzzles", []):
        steps_text = " ".join(puzzle.get("solution_steps", [])).lower()
        for kw in keyword_list:
            if kw in steps_text:
                step_keywords[kw] += 1

for kw, count in step_keywords.most_common():
    print(f"  '{kw}': appears in {count} puzzles")

print(f"\n{'=' * 60}")
print("TOTAL STATS")
print("=" * 60)
total_puzzles = sum(len(r.get("puzzles", [])) for r in all_rooms)
total_moments = sum(len(r.get("key_moments", [])) for r in all_rooms)
print(f"  Total Rooms: {len(all_rooms)}")
print(f"  Total Puzzles: {total_puzzles}")
print(f"  Total Key Moments: {total_moments}")
print(f"  Avg Puzzles/Room: {total_puzzles / len(all_rooms):.1f}")
print(f"  Avg Key Moments/Room: {total_moments / len(all_rooms):.1f}")
