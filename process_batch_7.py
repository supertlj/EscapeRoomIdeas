import os
import json
import subprocess

batch_data = [
  {
    "level": 31,
    "room_description": "A well-lit bedroom featuring beige patterned wallpaper, a white tufted bed with matching pillows, an elegant armchair, a flat-screen TV mounted on the wall with a modern console below, and a fish tank built into the wall near the door.",
    "key_moments": [
      {"description": "Establishing shot of the modern bedroom.", "timestamp_seconds": 0.0},
      {"description": "Collecting a purple pencil from under the armchair.", "timestamp_seconds": 3.0},
      {"description": "Counting the colored fish in the fish tank to get a 4-digit code.", "timestamp_seconds": 16.0},
      {"description": "Entering the code '2133' to open the TV console drawer.", "timestamp_seconds": 25.5},
      {"description": "Scribbling on the blank notebook page with the pencil to reveal a hidden code.", "timestamp_seconds": 47.0},
      {"description": "Entering the code '4325 + 1462' into the laptop.", "timestamp_seconds": 52.0},
      {"description": "Matching the colored shapes from the laptop clue onto the TV console dials.", "timestamp_seconds": 121.0},
      {"description": "Opening the small wooden box inside the console drawer with the silver key.", "timestamp_seconds": 142.5},
      {"description": "Solving the flower puzzle using the battery.", "timestamp_seconds": 146.5},
      {"description": "Unlocking the main door using the silver key.", "timestamp_seconds": 154.5}
    ],
    "puzzles": [
      {"puzzle_name": "Fish Tank Tally", "items_used": [], "solution_steps": ["Observe the fish tank.", "Count the fish by color to find the code: 2 red, 1 yellow, 3 blue, 3 green.", "Enter '2133' into the colored digital lock on the white TV console drawer."], "reward": "Access to the console drawer", "timestamp_seconds": 25.5},
      {"puzzle_name": "Notebook Clue", "items_used": ["Purple Pencil"], "solution_steps": ["Find the pencil under the armchair.", "Open the notebook found in the console drawer.", "Use the pencil on the blank page to reveal the text '4325 + 1462'."], "reward": "Code '4325 + 1462'", "timestamp_seconds": 47.0},
      {"puzzle_name": "Laptop Sum", "items_used": ["Battery"], "solution_steps": ["Calculate the sum of the equation found in the notebook: 4325 + 1462 = 5787.", "Enter '5787' into the laptop on the bed."], "reward": "Visual clue (colored shapes)", "timestamp_seconds": 52.0},
      {"puzzle_name": "Console Shape Dials", "items_used": [], "solution_steps": ["Note the shapes and colors displayed on the laptop: Red Hexagon, Blue Circle, Green Square, Yellow Triangle.", "Adjust the dials on the left console drawer to match this sequence."], "reward": "Silver Key", "timestamp_seconds": 121.0}
    ],
    "final_action": "The player uses the silver key found in the console to unlock the bedroom door."
  },
  {
    "level": 32,
    "room_description": "A children's room with exposed brick walls, a torn wall mural revealing a hidden figure, two large pumpkin-shaped beanbag chairs, a small TV, a pink dresser, and a bed adorned with plush bunnies.",
    "key_moments": [
      {"description": "Establishing shot of the children's room.", "timestamp_seconds": 0.0},
      {"description": "Moving the green frog plushie to find a battery.", "timestamp_seconds": 7.5},
      {"description": "Collecting a magnet piece from the wooden blocks shelf.", "timestamp_seconds": 5.0},
      {"description": "Inserting the battery into the TV remote to turn on the screen.", "timestamp_seconds": 11.5},
      {"description": "Using the magnet on the wall mural to find a key hidden behind the tear.", "timestamp_seconds": 14.5},
      {"description": "Observing the numbered bunny plushies on the bed.", "timestamp_seconds": 23.5},
      {"description": "Opening the pink dresser to find a piece of paper with symbols.", "timestamp_seconds": 25.5},
      {"description": "Aligning the symbol pattern on the wall panel.", "timestamp_seconds": 41.5},
      {"description": "Entering the '8659' code into the final chest.", "timestamp_seconds": 50.0}
    ],
    "puzzles": [
      {"puzzle_name": "Powering the TV", "items_used": ["Battery"], "solution_steps": ["Find the battery under the green frog plushie on the beanbag chair.", "Insert it into the TV remote to turn the TV on."], "reward": "Reveals a visual clue on the TV screen", "timestamp_seconds": 11.5},
      {"puzzle_name": "Magnetic Retrieval", "items_used": ["Magnet"], "solution_steps": ["Find the U-shaped magnet on the shelf with the letter blocks.", "Use the magnet near the torn section of the wall mural to pull out a hidden silver key."], "reward": "Silver Key", "timestamp_seconds": 14.5},
      {"puzzle_name": "Dresser Code", "items_used": [], "solution_steps": ["Observe the numbers written in red on the four white bunny plushies on the bed: 2, 4, 3, 1.", "Input the sequence '2431' into the digital lock on the pink dresser."], "reward": "Paper Clue with Symbols", "timestamp_seconds": 25.5},
      {"puzzle_name": "Symbol Panel Match", "items_used": ["Silver Key", "Paper Clue"], "solution_steps": ["Use the silver key to unlock the wall panel.", "Adjust the slider positions to match the symbol pattern shown on the paper clue found in the dresser."], "reward": "Code '8659'", "timestamp_seconds": 41.5}
    ],
    "final_action": "The player inputs the code '8659' into the chest to retrieve the exit key and unlock the main door."
  },
  {
    "level": 33,
    "room_description": "A dark, green-lit industrial room resembling a control center or bunker, featuring metal panels, electrical boxes, large pipes, and a central metal door.",
    "key_moments": [
      {"description": "Establishing shot of the industrial control room.", "timestamp_seconds": 0.0},
      {"description": "Collecting a blue and yellow keycard from the metal shelf.", "timestamp_seconds": 6.5},
      {"description": "Solving the 'Simon Says' style light pattern puzzle on the control panel.", "timestamp_seconds": 20.0},
      {"description": "Collecting a heavy metal pipe fitting from the opened panel.", "timestamp_seconds": 21.0},
      {"description": "Observing the number sequence on the pipe gauge.", "timestamp_seconds": 38.5},
      {"description": "Entering the color code sequence into the electrical box.", "timestamp_seconds": 49.0},
      {"description": "Solving the circuit connection puzzle on the large metal door.", "timestamp_seconds": 139.0},
      {"description": "Opening the main metal door.", "timestamp_seconds": 141.5}
    ],
    "puzzles": [
      {"puzzle_name": "Color Panel Memory Game", "items_used": [], "solution_steps": ["Interact with the control panel showing a 2x2 grid of colored squares.", "Repeat the sequence of flashing lights exactly as shown."], "reward": "Heavy Metal Pipe Fitting", "timestamp_seconds": 20.0},
      {"puzzle_name": "Electrical Box Code", "items_used": ["Keycard"], "solution_steps": ["Find the keycard on the shelf and examine its color quadrants (Red, Blue, Yellow, Green).", "Match the position of the colors to the input panel on the electrical box to unlock it."], "reward": "Access to the pipe gauge", "timestamp_seconds": 49.0},
      {"puzzle_name": "Gauge Combination", "items_used": [], "solution_steps": ["Observe the pressure gauge to note the sequence of numbers it points to: 6, 2, 8, 3.", "Enter '6283' into the keypad next to the electrical box."], "reward": "Activates the door puzzle", "timestamp_seconds": 54.0},
      {"puzzle_name": "Circuit Connection Door", "items_used": ["Metal Pipe Fitting"], "solution_steps": ["Place the missing pipe fitting onto the door's circuit panel.", "Rotate the tiles to form a continuous line connecting the two active nodes, creating a closed loop."], "reward": "Unlocks the main door", "timestamp_seconds": 139.0}
    ],
    "final_action": "Upon completing the circuit puzzle, the heavy metal door slides open, allowing the player to escape."
  },
  {
    "level": 34,
    "room_description": "An elegant room designed for leisure, featuring dark wood walls, a green billiards table in the center, two suits of armor, an armchair, and playing card suits (Spades, Clubs) displayed on the back wall.",
    "key_moments": [
      {"description": "Establishing shot of the billiards room.", "timestamp_seconds": 0.0},
      {"description": "Collecting a dart from the small round table next to the armchair.", "timestamp_seconds": 2.5},
      {"description": "Finding a blue button hidden in the wooden box.", "timestamp_seconds": 9.0},
      {"description": "Using the dart to pop a balloon on the dartboard, revealing a key.", "timestamp_seconds": 13.5},
      {"description": "Unlocking the lower cabinet to find a rolled piece of paper.", "timestamp_seconds": 17.0},
      {"description": "Arranging the card suit panels on the wall according to the clue.", "timestamp_seconds": 26.5},
      {"description": "Solving the colored ball placement puzzle using the cue ball positions.", "timestamp_seconds": 32.5},
      {"description": "Completing the playing card memory match game.", "timestamp_seconds": 46.5},
      {"description": "Inputting the sequence 'Spade, Heart, Club, Diamond' to open the final drawer.", "timestamp_seconds": 53.0},
      {"description": "Sinking the billiard balls into the pockets in the correct order.", "timestamp_seconds": 111.0}
    ],
    "puzzles": [
      {"puzzle_name": "Dartboard Key", "items_used": ["Dart"], "solution_steps": ["Collect the dart from the side table.", "Use the dart on the dartboard to pop the balloon and retrieve the silver key."], "reward": "Silver Key", "timestamp_seconds": 13.5},
      {"puzzle_name": "Card Suit Wall Panels", "items_used": ["Silver Key"], "solution_steps": ["Use the key to open the cabinet and get the paper clue.", "The paper shows the card suits: Spade, Heart, Club, Diamond.", "Adjust the four wall panels to display these suits in the correct order."], "reward": "Reveals the colored ball puzzle", "timestamp_seconds": 26.5},
      {"puzzle_name": "Billiards Color Match", "items_used": ["Blue Button"], "solution_steps": ["Place the blue button onto the puzzle board.", "Observe the colored billiard balls on the table.", "Arrange the colored buttons on the board to match the positions of the corresponding balls on the pool table."], "reward": "Access to the card matching game", "timestamp_seconds": 32.5},
      {"puzzle_name": "Billiards Pocket Sequence", "items_used": [], "solution_steps": ["After completing the card memory game, observe the numbers associated with the colored balls: Red=4, Yellow=2, Green=1, Blue=3.", "Using the cue stick, hit the balls into the pockets in numerical order (Green, Yellow, Blue, Red)."], "reward": "Exit Key", "timestamp_seconds": 111.0}
    ],
    "final_action": "The player sinks all four billiard balls in the correct sequence, causing a compartment to open containing the exit key, which is used to unlock the main double doors."
  },
  {
    "level": 35,
    "room_description": "A dimly lit, rugged stone cave with uneven terrain. In the background, a bright campfire illuminates the area, and bare tree branches protrude from the ground. A wooden crate sits on the right.",
    "key_moments": [
      {"description": "Establishing shot of the cave interior.", "timestamp_seconds": 0.0},
      {"description": "Collecting a wooden axe handle from the ground.", "timestamp_seconds": 3.0},
      {"description": "Using a knife to cut away the dry branches, revealing a stone code.", "timestamp_seconds": 6.5},
      {"description": "Collecting a torch from near the campfire.", "timestamp_seconds": 10.0},
      {"description": "Using the torch to illuminate a dark alcove, finding a metal axe head.", "timestamp_seconds": 15.0},
      {"description": "Assembling the axe.", "timestamp_seconds": 16.5},
      {"description": "Inputting the colored block sequence from the statue puzzle.", "timestamp_seconds": 34.0},
      {"description": "Completing the Van Gogh 'Starry Night' jigsaw puzzle.", "timestamp_seconds": 64.0},
      {"description": "Entering the final numeric code '7164' to open the chest.", "timestamp_seconds": 118.0}
    ],
    "puzzles": [
      {"puzzle_name": "Assemble the Axe", "items_used": ["Axe Handle", "Torch", "Knife"], "solution_steps": ["Pick up the handle from the ground.", "Use the knife to clear the branches to get the torch.", "Use the torch to light the dark area and find the axe head.", "Combine the handle and head."], "reward": "Axe", "timestamp_seconds": 16.5},
      {"puzzle_name": "Statue Color Code", "items_used": [], "solution_steps": ["Observe the colored gems on the small stone statues: Red, Blue, Yellow, Green.", "Enter this sequence into the colored blocks on the puzzle box."], "reward": "Puzzle Piece", "timestamp_seconds": 34.0},
      {"puzzle_name": "Starry Night Assembly", "items_used": ["Puzzle Piece"], "solution_steps": ["Place the missing piece into the frame.", "Assemble the tiles to form the classic Van Gogh painting 'The Starry Night'."], "reward": "Numeric Code '7164'", "timestamp_seconds": 64.0},
      {"puzzle_name": "Breaking the Crate", "items_used": ["Axe"], "solution_steps": ["Use the assembled axe to smash the wooden crate on the right side of the cave.", "Input the code '7164' into the chest hidden inside."], "reward": "Exit Key", "timestamp_seconds": 118.0}
    ],
    "final_action": "The player retrieves the key from the chest and uses it to unlock the metal grate, allowing them to crawl out of the cave."
  }
]

video_mapping = {
    31: r"Videos\Escape Game 50 Rooms 1\31 - Escape game 50 rooms 1 I Level 31.f271.webm",
    32: r"Videos\Escape Game 50 Rooms 1\32 - Escape game 50 rooms 1 I Level 32.f271.webm",
    33: r"Videos\Escape Game 50 Rooms 1\33 - Escape game 50 rooms 1 I Level 33.f271.webm",
    34: r"Videos\Escape Game 50 Rooms 1\34 - Escape game 50 rooms 1 ｜ Level 34.f271.webm",
    35: r"Videos\Escape Game 50 Rooms 1\35 - Escape game 50 rooms 1 I Level 35.f271.webm"
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
