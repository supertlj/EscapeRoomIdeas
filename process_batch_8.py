import os
import json
import subprocess

batch_data = [
  {
    "level": 36,
    "room_description": "A creepy, abandoned underground hospital room or bunker. It features a rusty bed with a body bag, a medical monitor, an ultrasound machine, and blood stains on the floor.",
    "key_moments": [
      {"description": "Establishing shot of the dark medical room.", "timestamp_seconds": 0.0},
      {"description": "Inspects a combination safe hidden in a floor panel.", "timestamp_seconds": 4.0},
      {"description": "Enters the code '5985' to unlock the floor safe.", "timestamp_seconds": 16.0},
      {"description": "Retrieves a CD/DVD from the opened floor safe.", "timestamp_seconds": 28.0},
      {"description": "Inserts the CD into the laptop resting on the bed.", "timestamp_seconds": 30.0},
      {"description": "Completes a sliding photo puzzle on the laptop screen.", "timestamp_seconds": 46.0},
      {"description": "Checks the newly activated medical monitor on the wall.", "timestamp_seconds": 54.0},
      {"description": "Checks the toe tag on the body bag, reading the number '240'.", "timestamp_seconds": 61.0},
      {"description": "Turns a red valve on a wall pipe until the pressure gauge hits 240.", "timestamp_seconds": 68.0},
      {"description": "Collects a small key that drops from the pressurized pipe.", "timestamp_seconds": 72.0}
    ],
    "puzzles": [
      {"puzzle_name": "Floor Safe", "items_used": [], "solution_steps": ["Determine the 4-digit code (likely deciphered from the ultrasound machine imagery).", "Enter '5985' into the combination lock on the floor."], "reward": "CD/DVD", "timestamp_seconds": 26.0},
      {"puzzle_name": "Laptop Sliding Puzzle", "items_used": ["CD/DVD"], "solution_steps": ["Insert the CD into the laptop to trigger the puzzle.", "Slide the scrambled tiles to form a complete vintage photograph of a group of people.", "Completing the photo powers on the wall-mounted medical monitor."], "reward": "Activates the medical monitor", "timestamp_seconds": 46.0},
      {"puzzle_name": "Pressure Valve", "items_used": [], "solution_steps": ["Find the toe tag on the body bag to get the target number '240'.", "Locate the pipe and turn the red valve to increase the pressure.", "Stop exactly when the gauge needle hits 240."], "reward": "A small key drops from the pipe", "timestamp_seconds": 68.0}
    ],
    "final_action": "Uses the small key dropped from the pipe to unlock the padlock securing the chains on the main exit doors."
  },
  {
    "level": 37,
    "room_description": "The interior of a sunken red car underwater. The player looks out through a cracked windshield into the ocean, with the dashboard, steering wheel, and leather seats visible.",
    "key_moments": [
      {"description": "Establishing shot from the driver's seat of the sunken car.", "timestamp_seconds": 0.0},
      {"description": "Looks at the back seat and finds '689241' pressed into the leather.", "timestamp_seconds": 8.0},
      {"description": "Presses a button to pop open the glovebox, finding a grid clue on paper.", "timestamp_seconds": 13.0},
      {"description": "Enters '689241' into the password prompt on the center console screen.", "timestamp_seconds": 23.0},
      {"description": "Collects a gold disc from the dashboard near the cracked windshield.", "timestamp_seconds": 26.0},
      {"description": "A 3x3 grid puzzle of yellow and blue triangles appears on the screen.", "timestamp_seconds": 42.0},
      {"description": "Successfully matches the grid puzzle pattern to the glovebox clue.", "timestamp_seconds": 72.0},
      {"description": "A secret panel slides down, revealing an arrow button puzzle.", "timestamp_seconds": 76.0},
      {"description": "Solves the jumping arrow puzzle and collects a metal hammer.", "timestamp_seconds": 100.0},
      {"description": "Uses the hammer to violently smash the cracked windshield.", "timestamp_seconds": 105.0}
    ],
    "puzzles": [
      {"puzzle_name": "Console Password", "items_used": [], "solution_steps": ["Examine the red leather back seat to find the indented numbers '689241'.", "Type this exact sequence into the digital keypad on the center console screen."], "reward": "Unlocks the screen to reveal a grid puzzle", "timestamp_seconds": 23.0},
      {"puzzle_name": "Triangle Grid Game", "items_used": [], "solution_steps": ["Look at the paper clue from the glovebox showing a grid with a key icon.", "Tap the squares on the digital 3x3 grid to change their colors (Lights Out style mechanics) until the correct pattern is formed."], "reward": "Reveals a hidden panel under the steering wheel", "timestamp_seconds": 72.0},
      {"puzzle_name": "Arrow Peg Puzzle", "items_used": [], "solution_steps": ["Play the peg solitaire mini-game on the hidden panel.", "Jump the green up-arrows over the blue down-arrows until all green arrows are at the top and blue arrows are at the bottom."], "reward": "A metal hammer", "timestamp_seconds": 100.0}
    ],
    "final_action": "Takes the hammer and repeatedly strikes the cracked windshield until it shatters, allowing the player to swim out and escape."
  },
  {
    "level": 38,
    "room_description": "A festive, brightly lit room decorated for Christmas. It contains a red sofa, a decorated Christmas tree, a snowman, a nutcracker statue, and a large red and black armoire.",
    "key_moments": [
      {"description": "Establishing shot of the colorful Christmas room.", "timestamp_seconds": 0.0},
      {"description": "Opens the nutcracker's mouth to find hidden items.", "timestamp_seconds": 15.0},
      {"description": "Collects a small bottle of lubricating oil from the nutcracker.", "timestamp_seconds": 17.0},
      {"description": "Collects a paper clue from the nutcracker showing the code '5674'.", "timestamp_seconds": 20.0},
      {"description": "Inspects the picture combination lock on the wall.", "timestamp_seconds": 30.0},
      {"description": "Enters '2571' into the lock and retrieves a red box cutter.", "timestamp_seconds": 48.0},
      {"description": "Enters '5674' into the digital lock on the large armoire.", "timestamp_seconds": 66.0},
      {"description": "Uses the box cutter to slice open a wrapped gift box on the floor.", "timestamp_seconds": 74.0},
      {"description": "Retrieves a gold key from inside the sliced gift box.", "timestamp_seconds": 76.0},
      {"description": "Applies the oil to the stuck key inside the exit door lock.", "timestamp_seconds": 82.0}
    ],
    "puzzles": [
      {"puzzle_name": "Butterfly & Flower Lock", "items_used": [], "solution_steps": ["Count the red butterflies, pink flowers, yellow butterflies, and white flowers depicted on the room's wall panels.", "Input the resulting sequence (2571) into the picture combination lock."], "reward": "Red box cutter", "timestamp_seconds": 48.0},
      {"puzzle_name": "Armoire Code", "items_used": ["Paper clue"], "solution_steps": ["Read the code '5674' from the paper found inside the nutcracker's mouth.", "Enter this code into the digital keypad on the large armoire."], "reward": "The armoire slides open, revealing the room's true exit door hidden behind it", "timestamp_seconds": 66.0},
      {"puzzle_name": "Stuck Door Lock", "items_used": ["Box cutter", "Gold key", "Bottle of oil"], "solution_steps": ["Cut open the gift box with the box cutter to find the gold key.", "Insert the key into the exit door, realizing the mechanism is stuck.", "Use the bottle of oil from the nutcracker to lubricate the keyhole."], "reward": "Unlocks the main door", "timestamp_seconds": 84.0}
    ],
    "final_action": "Turns the newly lubricated key to unlock the white door hidden behind the armoire and escapes."
  },
  {
    "level": 39,
    "room_description": "An elegant, luxurious hallway with ornate wallpaper, lounge chairs, a large mirror with red writing, a red fire hose box, a treasure chest, and a set of elevator doors.",
    "key_moments": [
      {"description": "Establishing shot of the elegant elevator lobby.", "timestamp_seconds": 0.0},
      {"description": "Finds a silver key buried in the dirt of a potted plant.", "timestamp_seconds": 8.0},
      {"description": "Reads the code '27583' written in red across the large mirror.", "timestamp_seconds": 32.0},
      {"description": "Enters '27583' into the combination lock on the treasure chest.", "timestamp_seconds": 44.0},
      {"description": "Retrieves a set of metal gears from the unlocked chest.", "timestamp_seconds": 46.0},
      {"description": "Studies a painting depicting colored Greek letters at different angles.", "timestamp_seconds": 52.0},
      {"description": "Adjusts the colored dials on the fire hose box to match the painting.", "timestamp_seconds": 66.0},
      {"description": "Uses the retrieved screwdriver to open the wall's electrical fuse box.", "timestamp_seconds": 74.0},
      {"description": "Places the gears onto a wall puzzle, opening a hidden compartment for fuses.", "timestamp_seconds": 82.0},
      {"description": "Inserts the newly found fuses into the electrical box to restore power.", "timestamp_seconds": 112.0}
    ],
    "puzzles": [
      {"puzzle_name": "Mirror Chest", "items_used": [], "solution_steps": ["Read the 5-digit code '27583' written prominently in red on the large mirror.", "Enter this code into the digital lock on the wooden treasure chest."], "reward": "Metal gears", "timestamp_seconds": 44.0},
      {"puzzle_name": "Fire Hose Dials", "items_used": [], "solution_steps": ["Observe the painting showing Alpha (Red) at 10 o'clock, Beta (Yellow) at 2 o'clock, and Omega (Blue) at 4 o'clock.", "Rotate the three corresponding dials on the fire hose box to match these orientations."], "reward": "Screwdriver", "timestamp_seconds": 66.0},
      {"puzzle_name": "Gear Mechanism & Power", "items_used": ["Metal gears", "Screwdriver"], "solution_steps": ["Place the gears onto the wall mechanism to complete the turning circuit, which opens a compartment containing two fuses.", "Use the screwdriver to unscrew the cover of the electrical box.", "Insert the two fuses to restore power to the room."], "reward": "Restores power to the elevator", "timestamp_seconds": 112.0}
    ],
    "final_action": "Restoring power to the electrical fuse box automatically opens the central elevator doors, allowing the player to escape."
  },
  {
    "level": 40,
    "room_description": "A vibrant Asian temple room decorated with ornate tapestries, hanging bells, a glowing Buddha statue, a wooden chest, and a stone altar.",
    "key_moments": [
      {"description": "Establishing shot of the colorful temple room.", "timestamp_seconds": 0.0},
      {"description": "Inspects a painting showing four rows of birds with specific red markings.", "timestamp_seconds": 9.0},
      {"description": "Solves the 4x4 bell grid puzzle on the wall.", "timestamp_seconds": 34.0},
      {"description": "Collects a golden dragon emblem from the hidden compartment behind the bells.", "timestamp_seconds": 36.0},
      {"description": "Finds a green metal blade/wedge inside the wooden chest's drawer.", "timestamp_seconds": 45.0},
      {"description": "Looks up at the ceiling mandala and discovers a hidden gold chain.", "timestamp_seconds": 52.0},
      {"description": "Notes the four glowing orange symbols appearing on the Buddha statue's chest.", "timestamp_seconds": 58.0},
      {"description": "Adjusts the symbol dials on a hidden panel to match the Buddha.", "timestamp_seconds": 66.0},
      {"description": "Collects a second golden dragon emblem from the symbol panel.", "timestamp_seconds": 70.0},
      {"description": "Solves the node jumping mini-game on the stone altar to reveal a hammer.", "timestamp_seconds": 100.0}
    ],
    "puzzles": [
      {"puzzle_name": "Bird & Bell Grid", "items_used": [], "solution_steps": ["Observe the red birds on the wire painting to get a sequence (Row 1: 2nd, Row 2: 4th, Row 3: 1st, Row 4: 3rd).", "Tap the corresponding bells on the 4x4 wall grid to light them up in this exact pattern."], "reward": "Golden dragon emblem", "timestamp_seconds": 34.0},
      {"puzzle_name": "Buddha Symbols", "items_used": [], "solution_steps": ["Look closely at the glowing symbols cycling or appearing on the chest of the Buddha statue.", "Input this exact sequence of four characters into the dial lock."], "reward": "Second golden dragon emblem", "timestamp_seconds": 106.0},
      {"puzzle_name": "Altar Node Puzzle", "items_used": ["Two golden dragon emblems"], "solution_steps": ["Insert both dragon emblems into the stone altar to activate a puzzle.", "Play the peg-jumping mini-game, moving the blue and red helmet nodes across the board until they have completely swapped sides."], "reward": "A metal hammer", "timestamp_seconds": 140.0}
    ],
    "final_action": "The player retrieves a hammer from the altar. (Note: The video abruptly cuts to footage from another level at this point, so the final escape interaction is not shown)."
  }
]

video_mapping = {
    36: r"Videos\Escape Game 50 Rooms 1\36 - Escape game 50 rooms 1 I Level 36.f271.webm",
    37: r"Videos\Escape Game 50 Rooms 1\37 - Escape game 50 rooms 1 I Level 37.f271.webm",
    38: r"Videos\Escape Game 50 Rooms 1\38 - Escape game 50 rooms 1 I Level 38.f271.webm",
    39: r"Videos\Escape Game 50 Rooms 1\39 - Escape game 50 rooms 1 I Level 39.f271.webm",
    40: r"Videos\Escape Game 50 Rooms 1\40 - Escape game 50 rooms 1 I Level 40.f271.webm"
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
