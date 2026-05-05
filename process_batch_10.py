import os
import json
import subprocess

batch_data = [
  {
    "level": 46,
    "room_description": "A colorful classroom with a green chalkboard showing a line graph, a teacher's desk, and several student desks arranged in rows.",
    "key_moments": [
      {"description": "Establishing shot of the classroom.", "timestamp_seconds": 0.0},
      {"description": "Inspecting a cloth doll lying on the floor between the student desks.", "timestamp_seconds": 2.5},
      {"description": "Looking at musical notes painted on the right wall.", "timestamp_seconds": 5.5},
      {"description": "Zooming in on the colorful ball pit seen through the classroom door.", "timestamp_seconds": 9.5},
      {"description": "Examining a toy crib and shelves in the adjacent playroom.", "timestamp_seconds": 13.0},
      {"description": "Finding a 3x3 grid lock panel hidden behind a poster.", "timestamp_seconds": 43.5},
      {"description": "Entering a combination sequence of shapes on the grid panel.", "timestamp_seconds": 46.5},
      {"description": "Retrieving a key half from the unlocked panel.", "timestamp_seconds": 52.0},
      {"description": "Completing the Lights Out style puzzle game on a tablet.", "timestamp_seconds": 64.0},
      {"description": "Picking up the full key to escape.", "timestamp_seconds": 67.5}
    ],
    "puzzles": [
      {"puzzle_name": "Alphabet Block Code", "items_used": [], "solution_steps": ["Examine the abacus/block toy in the playroom.", "Note the position of the blank spots to figure out the missing letters.", "Input the letters 'G', 'I', 'R', 'L' onto the four interactive blocks on the abacus."], "reward": "A key half", "timestamp_seconds": 15.5},
      {"puzzle_name": "Wall Symbols", "items_used": [], "solution_steps": ["Look at the symbols painted on the wall.", "Go to the three-panel combination lock behind the poster.", "Match the symbols found on the wall on the lock."], "reward": "The second key half", "timestamp_seconds": 46.5},
      {"puzzle_name": "Square Tile Game", "items_used": [], "solution_steps": ["Access the tablet device.", "Tap the tiles to turn them all blue. Tapping a tile changes its color and the color of adjacent tiles."], "reward": "A key", "timestamp_seconds": 64.0}
    ],
    "final_action": "Using the acquired key to unlock the main door and escape the classroom."
  },
  {
    "level": 47,
    "room_description": "A dark, mysterious underground cave with glowing green moss, a pool of water, and strange carvings on the walls.",
    "key_moments": [
      {"description": "Establishing shot of the dark cave environment.", "timestamp_seconds": 0.0},
      {"description": "Finding a beetle on a mossy rock.", "timestamp_seconds": 3.0},
      {"description": "Inspecting a small pool of glowing water.", "timestamp_seconds": 5.0},
      {"description": "Using a knife to scrape fungus off a rock.", "timestamp_seconds": 14.0},
      {"description": "Examining a piece of cloth with red symbols (a pickaxe and numbers).", "timestamp_seconds": 34.0},
      {"description": "Entering symbols into a lock on a wooden box.", "timestamp_seconds": 47.0},
      {"description": "Finding a coil of rope inside the opened box.", "timestamp_seconds": 54.0},
      {"description": "Looking at an analog clock with colored hands.", "timestamp_seconds": 31.0},
      {"description": "Combining items in the inventory.", "timestamp_seconds": 56.5},
      {"description": "Using the rope to climb out.", "timestamp_seconds": 58.0}
    ],
    "puzzles": [
      {"puzzle_name": "Clock Color Code", "items_used": ["Piece of paper with colored lines"], "solution_steps": ["Find the paper showing a yellow, purple, blue, and red line intersecting.", "Look at the clock on the wall and note the numbers each colored hand points to.", "Enter the corresponding code (9246) into the lock."], "reward": "Unlocks a panel/compartment", "timestamp_seconds": 31.0},
      {"puzzle_name": "Cloth Symbol Box", "items_used": ["Piece of cloth"], "solution_steps": ["Examine the cloth to see the red symbols.", "Enter those exact symbols into the combination lock on the wooden box found in the dark crevice."], "reward": "A coil of rope", "timestamp_seconds": 47.0}
    ],
    "final_action": "Using the rope combined with another item (likely a hook) to climb up and out of the cave."
  },
  {
    "level": 48,
    "room_description": "A sophisticated living room with a grand piano, decorative wall shelving, a large rug, and classical artwork.",
    "key_moments": [
      {"description": "Establishing shot of the living room with the piano.", "timestamp_seconds": 0.0},
      {"description": "Inspecting a toy car on a book on the coffee table.", "timestamp_seconds": 2.5},
      {"description": "Taking a matchbox from the wall shelf.", "timestamp_seconds": 6.5},
      {"description": "Looking closely at the grandfather clock.", "timestamp_seconds": 15.0},
      {"description": "Finding a key hidden in the clock mechanism.", "timestamp_seconds": 16.5},
      {"description": "Examining a clue on a leaf showing white worm-like shapes.", "timestamp_seconds": 28.5},
      {"description": "Entering a pattern of dashes on a lock panel.", "timestamp_seconds": 39.0},
      {"description": "Solving a pipe/wire connection mini-game.", "timestamp_seconds": 63.5},
      {"description": "Unlocking a cabinet door with a silver key.", "timestamp_seconds": 78.5},
      {"description": "Using a knife to cut open a sofa cushion.", "timestamp_seconds": 88.0}
    ],
    "puzzles": [
      {"puzzle_name": "Leaf Pattern Lock", "items_used": ["Leaf clue"], "solution_steps": ["Examine the leaf to see the pattern of the white shapes.", "Input that pattern of dashes into the lock panel."], "reward": "Opens a compartment", "timestamp_seconds": 39.0},
      {"puzzle_name": "Pipe Connection Game", "items_used": [], "solution_steps": ["Play the mini-game on the panel.", "Rotate the pipe pieces so that all the red connections are linked properly across the board."], "reward": "Unlocks a mechanism", "timestamp_seconds": 63.5},
      {"puzzle_name": "Sofa Patch", "items_used": ["Knife"], "solution_steps": ["Find the knife.", "Use the knife to cut the stitched patch on the sofa cushion."], "reward": "A hidden item (likely a key or token)", "timestamp_seconds": 88.0}
    ],
    "final_action": "Using the final key obtained from the puzzles to unlock the main door."
  },
  {
    "level": 49,
    "room_description": "A modern, luxurious bedroom with a large bed, flat-screen TV, glass coffee table, and an ornate mirror.",
    "key_moments": [
      {"description": "Establishing shot of the luxury bedroom.", "timestamp_seconds": 0.0},
      {"description": "Finding a clue card on a sofa pillow.", "timestamp_seconds": 4.5},
      {"description": "Inspecting the ornate mirror and an image inside it.", "timestamp_seconds": 10.0},
      {"description": "Playing a sliding tile puzzle on a wall panel.", "timestamp_seconds": 17.5},
      {"description": "Examining a clue showing colored numbers '2694'.", "timestamp_seconds": 23.5},
      {"description": "Entering a date '1991.12.07' into a lock on a suitcase on the bed.", "timestamp_seconds": 34.0},
      {"description": "Opening the suitcase to reveal a tablet.", "timestamp_seconds": 41.5},
      {"description": "Entering a 5-digit code into a wall safe.", "timestamp_seconds": 45.0},
      {"description": "Playing a peg-jumping game on a red panel.", "timestamp_seconds": 47.5},
      {"description": "Solving a slider puzzle with colored tiles.", "timestamp_seconds": 58.0}
    ],
    "puzzles": [
      {"puzzle_name": "Suitcase Date Code", "items_used": ["Clue card"], "solution_steps": ["Find the clue card (possibly near the Russian nesting dolls) that shows a date.", "Enter '1991.12.07' into the combination lock on the suitcase on the bed."], "reward": "Access to the tablet inside", "timestamp_seconds": 34.0},
      {"puzzle_name": "Peg Jumping Game", "items_used": [], "solution_steps": ["Access the mini-game on the red panel.", "Jump the pegs to clear the board or reach a specific configuration."], "reward": "Unlocks a compartment", "timestamp_seconds": 47.5},
      {"puzzle_name": "Colored Slider Puzzle", "items_used": [], "solution_steps": ["Access the slider puzzle.", "Move the colored squares into the correct positions based on a color clue found elsewhere in the room."], "reward": "The exit key", "timestamp_seconds": 58.0}
    ],
    "final_action": "Using the key obtained to unlock the exit door."
  },
  {
    "level": 50,
    "room_description": "An ornate Asian-style temple or meditation room. It features wooden furniture, lit candles, large golden bells, and statues.",
    "key_moments": [
      {"description": "Establishing shot of the temple room.", "timestamp_seconds": 0.0},
      {"description": "Lighting the candles on the table.", "timestamp_seconds": 2.5},
      {"description": "Looking at the framed picture of a potted plant with an IP address.", "timestamp_seconds": 5.5},
      {"description": "Examining a lock with four rotating dials.", "timestamp_seconds": 8.0},
      {"description": "Finding a sequence of colored circles on a plate.", "timestamp_seconds": 11.5},
      {"description": "Entering a symbol code into a lock.", "timestamp_seconds": 18.0},
      {"description": "Striking the large hanging bells in a specific sequence.", "timestamp_seconds": 23.5},
      {"description": "Lighting more candles to reveal a glowing pattern.", "timestamp_seconds": 27.5},
      {"description": "Observing glowing symbols on the Buddha statue.", "timestamp_seconds": 38.5},
      {"description": "Completing a wiring puzzle on a wall panel.", "timestamp_seconds": 63.5}
    ],
    "puzzles": [
      {"puzzle_name": "Bell Striking Sequence", "items_used": [], "solution_steps": ["Find the clue that dictates the order in which to hit the bells.", "Strike the bells in the correct order to trigger a mechanism."], "reward": "Reveals a hidden item or opens a panel", "timestamp_seconds": 23.5},
      {"puzzle_name": "Buddha Symbol Lock", "items_used": [], "solution_steps": ["Observe the sequence of glowing symbols that appear on the chest of the Buddha statue.", "Input those exact symbols into the corresponding combination lock."], "reward": "Opens a compartment", "timestamp_seconds": 38.5},
      {"puzzle_name": "Red Wiring Game", "items_used": [], "solution_steps": ["Access the wiring panel.", "Connect the red wires so that all nodes are properly linked across the board."], "reward": "Unlocks the final door mechanism", "timestamp_seconds": 63.5}
    ],
    "final_action": "Completing the final puzzle sequence unlocks the ornate double doors, allowing escape from the final level."
  }
]

video_mapping = {
    46: r"Videos\Escape Game 50 Rooms 1\46 - Escape game 50 rooms 1 I Level 46.f271.webm",
    47: r"Videos\Escape Game 50 Rooms 1\47 - Escape game 50 rooms 1 I Level 47.f271.webm",
    48: r"Videos\Escape Game 50 Rooms 1\48 - Escape game 50 rooms 1 - Level 48.f271.webm",
    49: r"Videos\Escape Game 50 Rooms 1\49 - Escape game 50 rooms 1 - Level 49.f271.webm",
    50: r"Videos\Escape Game 50 Rooms 1\50 - Escape game 50 rooms 1 - Final Level - Level 50.f271.webm"
}

for room in batch_data:
    level = room["level"]
    video_path = video_mapping.get(level)
    if not video_path:
        print(f"Skipping Level {level}: Video path not found.")
        continue
    
    print(f"\n--- Processing Level {level} ---")
    temp_json = f"temp_level_{level}.json"
    with open(temp_json, "w", encoding="utf-8") as f:
        json.dump(room, f)
    
    try:
        subprocess.run([
            r"C:\Users\super\AppData\Local\Python\pythoncore-3.14-64\python.exe",
            "process_manual_json.py",
            temp_json,
            video_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing Level {level}: {e}")
    finally:
        if os.path.exists(temp_json):
            os.remove(temp_json)

print("\nBatch Processing Complete!")
