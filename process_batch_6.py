import os
import json
import subprocess

batch_data = [
  {
    "level": 26,
    "room_description": "A luxury master bedroom featuring a large bed, fireplace, mounted deer head, and several pieces of white ornate furniture.",
    "key_moments": [
      {"description": "Establishing shot of the luxury bedroom.", "timestamp_seconds": 0.0},
      {"description": "Inspecting the pillows on the left side of the bed to find a gold coin.", "timestamp_seconds": 1.5},
      {"description": "Checking under the pillows on the right side of the bed.", "timestamp_seconds": 5.0},
      {"description": "Examining the mounted deer head with colored dots on its neck.", "timestamp_seconds": 10.5},
      {"description": "Opening the bottom drawer of the long white sideboard.", "timestamp_seconds": 16.5},
      {"description": "Retrieving a metal rod from the ice bucket containing a wine bottle.", "timestamp_seconds": 23.0},
      {"description": "Unlocking a small ornate chest inside a desk drawer to find a scroll.", "timestamp_seconds": 27.0},
      {"description": "Using a coin to reveal a hidden compartment behind a portrait.", "timestamp_seconds": 44.5},
      {"description": "Viewing a color-coded number clue on a piece of paper: 2694.", "timestamp_seconds": 49.0},
      {"description": "Entering a 4-digit code into a wall-mounted keypad.", "timestamp_seconds": 53.5}
    ],
    "puzzles": [
      {"puzzle_name": "Colored Deer Sequence", "items_used": ["Metal rod"], "solution_steps": ["Observe the color sequence on the deer head's neck (White, White, Yellow, White).", "Use the metal rod to poke the fireplace screen in a specific spot to release a mechanism."], "reward": "Small key", "timestamp_seconds": 11.0},
      {"puzzle_name": "Color-Coded Keypad", "items_used": ["Color clue scroll"], "solution_steps": ["Find the scroll showing 2 (Blue), 6 (Green), 9 (Red), 4 (Yellow).", "Correlate the numbers with the dot colors on the deer head or portraits.", "Input the resulting sequence 9426 (based on room clues) into the keypad."], "reward": "A blue keycard", "timestamp_seconds": 54.0}
    ],
    "final_action": "Using the blue keycard on the electronic lock next to the exit door."
  },
  {
    "level": 27,
    "room_description": "A grimy, yellow-tiled basement or locker room with blood stains, a skeleton, and various cleaning equipment.",
    "key_moments": [
      {"description": "Establishing shot of the grimy room.", "timestamp_seconds": 0.0},
      {"description": "Finding a mop and a bucket on the blood-stained checkered floor.", "timestamp_seconds": 1.5},
      {"description": "Inspecting a skeleton holding a leather briefcase.", "timestamp_seconds": 5.0},
      {"description": "Finding a hidden number '1354' written in blood on the wall tile.", "timestamp_seconds": 13.0},
      {"description": "Entering '1354' into the briefcase combination lock.", "timestamp_seconds": 17.5},
      {"description": "A small monitor on the wall flashes a sequence of Red, White, Yellow, Green.", "timestamp_seconds": 25.5},
      {"description": "Pressing the buttons on the trash bins in the order shown by the monitor.", "timestamp_seconds": 30.5},
      {"description": "Using a hooked pole to retrieve an object from the ceiling rafters.", "timestamp_seconds": 37.5},
      {"description": "Checking the generator/pump in the corner of the room.", "timestamp_seconds": 41.5},
      {"description": "Activating the generator to open the exit door.", "timestamp_seconds": 49.5}
    ],
    "puzzles": [
      {"puzzle_name": "Blood Code Briefcase", "items_used": ["Mop"], "solution_steps": ["Use the mop to clear away grime or blood to reveal the code 1354 on the wall.", "Enter 1354 into the briefcase lock next to the skeleton."], "reward": "Roll of duct tape", "timestamp_seconds": 18.5},
      {"puzzle_name": "TV Color Sequence", "items_used": [], "solution_steps": ["Observe the color sequence on the wall monitor (Red, White, Yellow, Green).", "Press the corresponding color-coded lids of the four trash bins in the same order."], "reward": "Hooked metal pole", "timestamp_seconds": 31.0}
    ],
    "final_action": "Using the duct tape to repair a frayed wire and turning the red valve on the generator to unlock the door."
  },
  {
    "level": 28,
    "room_description": "A Japanese-style living room with tatami mats, shoji sliding doors, and traditional wooden furniture.",
    "key_moments": [
      {"description": "Establishing shot of the Japanese living room.", "timestamp_seconds": 0.0},
      {"description": "Opening a drawer in the side table to find a set of bowls and chopsticks.", "timestamp_seconds": 2.5},
      {"description": "Finding a mahjong tile hidden in a potted plant.", "timestamp_seconds": 6.5},
      {"description": "Retrieving a pair of scissors from a low cabinet drawer.", "timestamp_seconds": 19.5},
      {"description": "Using the scissors to cut a patch on the sofa to reveal a hidden compartment.", "timestamp_seconds": 24.5},
      {"description": "Looking at a wall clock with colored hands and markers.", "timestamp_seconds": 31.5},
      {"description": "Setting the clock hands to specific times based on a color clue scroll.", "timestamp_seconds": 35.5},
      {"description": "Entering '9246' into the digital keypad on the shoji door.", "timestamp_seconds": 43.5},
      {"description": "Solving a slider puzzle involving multi-colored vertical pipes.", "timestamp_seconds": 55.0},
      {"description": "The shoji doors slide open to reveal the exit.", "timestamp_seconds": 110.5}
    ],
    "puzzles": [
      {"puzzle_name": "Clock Time Calculation", "items_used": ["Color clue scroll"], "solution_steps": ["Find the scroll showing a sequence of colored hands/marks.", "Manipulate the clock hands to align with these colors.", "Read the numbers revealed by the clock hands (9, 2, 4, 6)."], "reward": "Keypad code 9246", "timestamp_seconds": 39.5},
      {"puzzle_name": "Pipe Slider Puzzle", "items_used": [], "solution_steps": ["Access the sliding puzzle behind the keypad panel.", "Move the colored segments up and down to align them with the corresponding colored sockets at the top."], "reward": "Unlocks the main exit doors", "timestamp_seconds": 108.0}
    ],
    "final_action": "The shoji doors slide open once the slider puzzle is completed, allowing the player to pass through."
  },
  {
    "level": 29,
    "room_description": "A recreational games room with a pool table, dartboard, arcade machine, and retro gaming decor.",
    "key_moments": [
      {"description": "Establishing shot of the games room.", "timestamp_seconds": 0.0},
      {"description": "Finding a metal slider piece under the billiard balls on the pool table.", "timestamp_seconds": 2.5},
      {"description": "Examining a row of cues and colored billiard balls on the wall rack.", "timestamp_seconds": 10.5},
      {"description": "Opening a toy chest using a 4-digit code (2571) to find a box cutter.", "timestamp_seconds": 45.5},
      {"description": "Using the box cutter to open a stuffed cow toy to find a silver coin.", "timestamp_seconds": 54.5},
      {"description": "Inserting the coin into the arcade machine to play a mini-game.", "timestamp_seconds": 100.5},
      {"description": "Playing a directional arrow game on the arcade screen.", "timestamp_seconds": 110.0},
      {"description": "Revealing the code '495' in Red, Green, and Blue ink on the arcade screen.", "timestamp_seconds": 126.5},
      {"description": "Entering '950' (based on color logic) into a wall safe hidden behind the dartboard.", "timestamp_seconds": 150.0},
      {"description": "Retrieving the exit key from the wall safe.", "timestamp_seconds": 154.0}
    ],
    "puzzles": [
      {"puzzle_name": "Toy Chest Code", "items_used": [], "solution_steps": ["Count the billiard balls of different colors on the rack.", "Check the dartboard for specific numbers hit by darts.", "Combine these counts to derive the code 2571 for the chest."], "reward": "Box cutter", "timestamp_seconds": 47.0},
      {"puzzle_name": "Arcade Directional Puzzle", "items_used": ["Silver coin"], "solution_steps": ["Insert the coin to start the game.", "Press the arrows (Left, Up, Right, Down) in the sequence indicated by the flashing characters on screen."], "reward": "Number code 495", "timestamp_seconds": 125.0}
    ],
    "final_action": "Using the key found in the wall safe to unlock the wooden exit door."
  },
  {
    "level": 30,
    "room_description": "An ancient stone temple or tomb with lion statues, pedestals, and glowing blue energy.",
    "key_moments": [
      {"description": "Establishing shot of the stone temple.", "timestamp_seconds": 0.0},
      {"description": "Finding a stone artifact on a pedestal with an eagle carving.", "timestamp_seconds": 2.5},
      {"description": "Inspecting the left lion statue with glowing green eyes.", "timestamp_seconds": 11.0},
      {"description": "Finding a hammer on the floor near a pillar.", "timestamp_seconds": 14.5},
      {"description": "Using the hammer to break a clay pot to find a golden dragon head.", "timestamp_seconds": 31.0},
      {"description": "Matching stone tiles with eagle, dolphin, and wolf carvings on a wall panel.", "timestamp_seconds": 51.5},
      {"description": "Placing two golden dragon heads into a central stone box.", "timestamp_seconds": 112.5},
      {"description": "Retrieving a wolf emblem from the stone box.", "timestamp_seconds": 114.5},
      {"description": "Inserting various emblems into the main circular door lock.", "timestamp_seconds": 118.0},
      {"description": "Solving a pathfinding mini-game on the door to align helmet and beast icons.", "timestamp_seconds": 122.5}
    ],
    "puzzles": [
      {"puzzle_name": "Animal Tile Wall", "items_used": [], "solution_steps": ["Examine the carvings around the room (Dolphin 4, Eagle 2, etc.).", "Rotate or swap the tiles on the wall panel to match the icons found on the pedestals."], "reward": "Second golden dragon head", "timestamp_seconds": 101.5},
      {"puzzle_name": "Door Hexagon Game", "items_used": ["Wolf emblem", "Eagle emblem", "Lion emblem"], "solution_steps": ["Insert the three gathered emblems into the door slots.", "Slide the beast heads (Left) and the knight helmets (Right) across the hexagonal grid to swap their positions."], "reward": "Unlocks the stone temple door", "timestamp_seconds": 210.0}
    ],
    "final_action": "The large stone door slides open after the hexagon puzzle is complete, revealing the way forward."
  }
]

video_mapping = {
    26: r"Videos\Escape Game 50 Rooms 1\26 - Escape game 50 rooms 1 ｜ Level 26.f271.webm",
    27: r"Videos\Escape Game 50 Rooms 1\27 - Escape game 50 rooms 1 I Level 27.f271.webm",
    28: r"Videos\Escape Game 50 Rooms 1\28 - Escape game 50 rooms 1 I Level 28.f400.mp4",
    29: r"Videos\Escape Game 50 Rooms 1\29 - Escape game 50 rooms 1 I Level 29.f271.webm",
    30: r"Videos\Escape Game 50 Rooms 1\30 - Escape game 50 rooms 1 I Level 30.f271.webm"
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
