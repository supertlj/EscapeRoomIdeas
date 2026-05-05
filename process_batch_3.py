import os
import json
import subprocess

batch_data = [
  {
    "level": 9,
    "room_description": "A modern living area featuring a beige tufted sofa set, a glass coffee table over a brown rug, a large fish tank against the back wall, a white shelving unit, and a dark wooden exit door.",
    "key_moments": [
      {"description": "Establishing shot of the modern living room.", "timestamp_seconds": 0.0},
      {"description": "Lifting the beige sofa pillow to find a pair of red scissors.", "timestamp_seconds": 2.0},
      {"description": "Using the scissors to cut the string on the rolled paper on the coffee table, revealing a number grid.", "timestamp_seconds": 11.5},
      {"description": "Discovering a small silver key hidden in the soil of the potted plant.", "timestamp_seconds": 16.0},
      {"description": "Unlocking the white drawer to retrieve a yellow fishing line spool.", "timestamp_seconds": 19.5},
      {"description": "Attaching the spool to the fishing rod and using it to fish out a grid mask from the fish tank.", "timestamp_seconds": 25.5},
      {"description": "Overlaying the grid mask onto the number grid to reveal a 4-digit code.", "timestamp_seconds": 28.5},
      {"description": "Entering the code into the digital lock inside the cabinet.", "timestamp_seconds": 36.5},
      {"description": "Solving the sliding puzzle on the laptop to reveal a sequence of colors.", "timestamp_seconds": 100.0},
      {"description": "Inputting the color sequence into the safe to get the keycard and escaping.", "timestamp_seconds": 112.0}
    ],
    "puzzles": [
      {"puzzle_name": "Fishing for the Clue Mask", "items_used": ["Silver Key", "Fishing Line Spool"], "solution_steps": ["Find the key in the plant pot and use it to open the cabinet drawer to get the yellow spool.", "Attach the spool to the fishing rod near the tank.", "Use the rod to extract the black grid mask from the water."], "reward": "Grid Mask", "timestamp_seconds": 26.0},
      {"puzzle_name": "Number Grid Code", "items_used": ["Scissors", "Grid Mask"], "solution_steps": ["Use the scissors to unroll the paper on the table.", "Overlay the grid mask onto the paper's number grid.", "Read the numbers visible through the holes.", "Enter the code into the red digital safe."], "reward": "Access to the laptop", "timestamp_seconds": 36.5},
      {"puzzle_name": "Animal Color Sequence", "items_used": [], "solution_steps": ["Solve the sliding tile puzzle on the laptop.", "Note the background colors of the four animals displayed (Yellow, Purple, Green, White).", "Input this exact color sequence into the 4-panel safe in the cabinet."], "reward": "Blue Keycard", "timestamp_seconds": 112.0}
    ],
    "final_action": "The player swipes the blue keycard on the electronic door handle to unlock the main door and escape."
  },
  {
    "level": 10,
    "room_description": "A bright pink bedroom with white wall paneling, a white metal-framed bed, a wall clock, a vanity table with a chest, a large 'Last Supper' painting, and a locked wooden door.",
    "key_moments": [
      {"description": "Establishing shot of the pink bedroom.", "timestamp_seconds": 0.0},
      {"description": "Lifting the cloth on the table shelf to find a green number '5'.", "timestamp_seconds": 3.5},
      {"description": "Moving the bed pillow to find a red number '2' and a diamond ring.", "timestamp_seconds": 6.5},
      {"description": "Using the diamond ring to cut the glass of the ornate wall mirror.", "timestamp_seconds": 12.0},
      {"description": "Entering the shape sequence from the mirror onto the large wall painting.", "timestamp_seconds": 18.0},
      {"description": "Opening the small chest on the table to find a yellow number '3'.", "timestamp_seconds": 37.5},
      {"description": "Checking the wall clock to see the blue hand pointing to '8'.", "timestamp_seconds": 40.5},
      {"description": "Entering the color-coded number combination into the wall safe.", "timestamp_seconds": 51.0},
      {"description": "Placing the missing puzzle piece into the wooden box under the bed.", "timestamp_seconds": 55.5},
      {"description": "Unlocking the main door after completing the sliding puzzle.", "timestamp_seconds": 331.0}
    ],
    "puzzles": [
      {"puzzle_name": "Mirror Shapes", "items_used": ["Diamond Ring"], "solution_steps": ["Find the ring under the pillow.", "Use the ring to cut the mirror glass, revealing four red symbols.", "Tap the medallions on the 'Last Supper' painting to match the symbols (Circle, Star of David, Eye of Providence, Cross)."], "reward": "Reveals the hidden wall safe", "timestamp_seconds": 23.0},
      {"puzzle_name": "Color-Coded Safe", "items_used": [], "solution_steps": ["Locate the four colored numbers hidden around the room: Red 2 (bed), Yellow 3 (chest), Blue 8 (clock), Green 5 (table).", "Match the numbers to the colored arrows on the wall safe (Red, Yellow, Blue, Green).", "Enter the code '2385'."], "reward": "Puzzle Tile", "timestamp_seconds": 51.0},
      {"puzzle_name": "Starry Night Slider", "items_used": ["Puzzle Tile"], "solution_steps": ["Find the wooden box under the bed.", "Insert the missing tile retrieved from the safe.", "Solve the sliding tile puzzle to form Van Gogh's 'Starry Night'."], "reward": "Silver Key", "timestamp_seconds": 328.0}
    ],
    "final_action": "The player uses the silver key found inside the puzzle box to unlock the main bedroom door and escape."
  },
  {
    "level": 12,
    "room_description": "A bedroom with bold vertical striped wallpaper, a metal bed frame holding a teddy bear, a road bicycle parked on the shiny floor, a wooden cabinet, and a door.",
    "key_moments": [
      {"description": "Establishing shot of the striped bedroom.", "timestamp_seconds": 0.0},
      {"description": "Picking up a yellow pencil from near the bicycle's pedals.", "timestamp_seconds": 2.0},
      {"description": "Lifting the bed pillow to collect a red battery.", "timestamp_seconds": 6.5},
      {"description": "Opening the bottom drawer of the black nightstand to collect a projector component.", "timestamp_seconds": 12.5},
      {"description": "Scribbling on the blank notebook with the pencil to reveal a flower drawing.", "timestamp_seconds": 18.5},
      {"description": "Assembling the projector inside the wooden cabinet to reveal a projection code.", "timestamp_seconds": 27.5},
      {"description": "Entering the projected code '8659' to open the cabinet drawer.", "timestamp_seconds": 34.0},
      {"description": "Retrieving a screwdriver from the opened drawer.", "timestamp_seconds": 36.5},
      {"description": "Entering the color-symbol code on the left cabinet panel.", "timestamp_seconds": 105.0},
      {"description": "Using the retrieved key to unlock the exit door.", "timestamp_seconds": 116.5}
    ],
    "puzzles": [
      {"puzzle_name": "Projecting the Code", "items_used": ["Projector Component", "Red Battery"], "solution_steps": ["Find the projector component in the nightstand.", "Find the battery under the bed pillow.", "Place both items into the slot in the center of the wooden cabinet to project the numbers '8659'."], "reward": "Code '8659'", "timestamp_seconds": 27.5},
      {"puzzle_name": "Symbol & Color Matching", "items_used": ["Pencil", "Screwdriver"], "solution_steps": ["Use the pencil on the notebook to reveal a yellow flower.", "Use the screwdriver to open the locked left panel of the cabinet.", "Match the objects in the room to their colors on the panel dials: White Teddy Bear (bed), Green Trash Can (floor), Red Flower (vase), Yellow Flower (notebook)."], "reward": "Silver Key", "timestamp_seconds": 113.0}
    ],
    "final_action": "The player uses the silver key obtained from the symbol panel compartment to unlock the main door."
  },
  {
    "level": 13,
    "room_description": "A spacious apartment featuring a living room with a white sofa, black coffee table, and TV console, separated by a sliding door from a dining area with a table and wine bucket.",
    "key_moments": [
      {"description": "Establishing shot of the living and dining area.", "timestamp_seconds": 0.0},
      {"description": "Collecting a pair of wire cutters from under the TV console.", "timestamp_seconds": 5.5},
      {"description": "Collecting a corkscrew from the upper drawer of the dining cabinet.", "timestamp_seconds": 11.5},
      {"description": "Using the cutters to snip the padlock on the black chest.", "timestamp_seconds": 16.0},
      {"description": "Opening the hidden wall compartment behind the picture frame to get a key.", "timestamp_seconds": 29.5},
      {"description": "Using the key to unlock the sliding door, accessing the dining table.", "timestamp_seconds": 32.0},
      {"description": "Using the corkscrew to open the wine bottle and extract a paper clue.", "timestamp_seconds": 40.0},
      {"description": "Unrolling the wine bottle paper to reveal the number '1462'.", "timestamp_seconds": 53.0},
      {"description": "Entering the mathematical sum into the TV console keypad.", "timestamp_seconds": 59.5},
      {"description": "Using the keycard to unlock the final exit door.", "timestamp_seconds": 103.5}
    ],
    "puzzles": [
      {"puzzle_name": "First Half of the Equation", "items_used": ["Wire Cutters"], "solution_steps": ["Find the wire cutters under the TV stand.", "Use them to cut the metal lock on the black chest.", "Open the chest and unroll the paper."], "reward": "Clue '4325 +'", "timestamp_seconds": 21.0},
      {"puzzle_name": "Message in a Bottle", "items_used": ["Corkscrew", "Silver Key"], "solution_steps": ["Find the silver key behind the wall painting.", "Use the key to open the sliding door to the dining area.", "Use the corkscrew (from the cabinet) to open the wine bottle in the ice bucket."], "reward": "Clue '1462'", "timestamp_seconds": 53.0},
      {"puzzle_name": "Console Keypad Sum", "items_used": [], "solution_steps": ["Combine the clues to form an equation: 4325 + 1462.", "Calculate the sum (5787).", "Enter '5787' into the digital keypad on the TV console drawer."], "reward": "Blue Keycard", "timestamp_seconds": 59.5}
    ],
    "final_action": "The player takes the blue keycard from the console drawer and inserts it into the electronic lock of the main door to escape."
  },
  {
    "level": 14,
    "room_description": "A dimly lit home office or study containing a desk with a laptop, a wooden bookshelf, a patterned chaise lounge, an overturned chair, and a wastebasket.",
    "key_moments": [
      {"description": "Establishing shot of the office room.", "timestamp_seconds": 0.0},
      {"description": "Moving the sofa cushion to find a silver key.", "timestamp_seconds": 2.0},
      {"description": "Using the key to unlock the bookshelf drawer, revealing a green box cutter.", "timestamp_seconds": 15.5},
      {"description": "Opening the desk drawer to collect a USB flash drive.", "timestamp_seconds": 19.5},
      {"description": "Plugging the USB drive into the laptop to activate the screen.", "timestamp_seconds": 27.5},
      {"description": "Examining the black notebook to see a grid of red numbers.", "timestamp_seconds": 31.0},
      {"description": "Unfolding the crumpled paper on the desk to reveal a grid with red dots.", "timestamp_seconds": 47.0},
      {"description": "Entering the derived PIN code into the laptop.", "timestamp_seconds": 104.0},
      {"description": "Completing the 'Quickspot' minigame on the laptop.", "timestamp_seconds": 115.5},
      {"description": "Entering '311' into the desk drawer lock and escaping with the key.", "timestamp_seconds": 126.5}
    ],
    "puzzles": [
      {"puzzle_name": "Accessing the Laptop", "items_used": ["USB Drive"], "solution_steps": ["Open the unlocked desk drawer to get the USB drive.", "Insert it into the laptop to bring up the keypad screen."], "reward": "Activates Laptop Password Prompt", "timestamp_seconds": 27.5},
      {"puzzle_name": "Dot Grid Overlay", "items_used": [], "solution_steps": ["Examine the crumpled paper to see the positions of 5 red dots.", "Cross-reference these positions with the grid of numbers in the black notebook.", "Extract the corresponding numbers to form the code."], "reward": "Code to unlock laptop", "timestamp_seconds": 104.0},
      {"puzzle_name": "Spot the Difference", "items_used": [], "solution_steps": ["Play the 'Quickspot' game on the laptop.", "Find and click all 5 differences between the two classic portraits."], "reward": "Code '311'", "timestamp_seconds": 116.0},
      {"puzzle_name": "Desk Drawer Lock", "items_used": [], "solution_steps": ["Look at the combination lock on the lower desk drawer.", "Enter the code '311' provided by the laptop."], "reward": "Final Silver Key", "timestamp_seconds": 123.5}
    ],
    "final_action": "The player uses the silver key from the locked desk drawer to open the main door and escape the room."
  }
]

video_mapping = {
    9: r"Videos\Escape Game 50 Rooms 1\09 - Escape game 50 rooms 1 - Level 9.f271.webm",
    10: r"Videos\Escape Game 50 Rooms 1\10 - Escape game 50 rooms 1 - Level 10 [ Kindly Check Description].f271.webm",
    12: r"Videos\Escape Game 50 Rooms 1\12 - Escape game 50 rooms 1 - Level 12.f271.webm",
    13: r"Videos\Escape Game 50 Rooms 1\13 - Escape game 50 rooms 1 - Level 13.f271.webm",
    14: r"Videos\Escape Game 50 Rooms 1\14 - Escape Game 50 Rooms 1 ｜ Level 14.f400.mp4"
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
