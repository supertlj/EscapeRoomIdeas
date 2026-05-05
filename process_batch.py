import os
import json
import subprocess
import shutil

batch_data = [
  {
    "level": 1,
    "room_description": "A dark, rundown brick room with exposed pipes, an old AC unit on the wall, wooden crates on the left, a piece of old electronic equipment on the ground, and a sealed wooden door.",
    "key_moments": [
      {"description": "Establishing shot of the room and introduction.", "timestamp_seconds": 0.0},
      {"description": "Zooming in on the AC unit to collect a screwdriver.", "timestamp_seconds": 9.0},
      {"description": "Picking up the empty monitor casing from the debris.", "timestamp_seconds": 11.0},
      {"description": "Inspecting the '1P' block on the ground.", "timestamp_seconds": 19.0},
      {"description": "Removing the '1P' cover to reveal a remote control.", "timestamp_seconds": 22.0},
      {"description": "Inspecting the rusty '2P' panel on the brick wall.", "timestamp_seconds": 26.0},
      {"description": "Connecting the power cord to the monitor casing.", "timestamp_seconds": 34.0},
      {"description": "Using the remote to turn on the monitor, revealing a clue with four dials.", "timestamp_seconds": 36.0},
      {"description": "Opening the '2P' panel to reveal four physical dials.", "timestamp_seconds": 44.0},
      {"description": "Adjusting the dials to match the pattern shown on the monitor.", "timestamp_seconds": 54.0}
    ],
    "puzzles": [
      {"puzzle_name": "Gathering Basic Supplies", "items_used": [], "solution_steps": ["Find the screwdriver stuck in the AC unit.", "Pick up the empty monitor casing from the pile of wood on the ground."], "reward": "Screwdriver, Monitor Casing", "timestamp_seconds": 9.0},
      {"puzzle_name": "The '1P' Box", "items_used": [], "solution_steps": ["Locate the dark grey block marked '1P' on the ground.", "Remove its lid."], "reward": "Remote Control", "timestamp_seconds": 22.0},
      {"puzzle_name": "Powering the Monitor Clue", "items_used": ["Monitor Casing", "Remote Control"], "solution_steps": ["Place the monitor casing back down.", "Plug the loose power cord into the monitor.", "Use the remote control to turn it on and observe the dial orientation clue."], "reward": "Visual clue (Dial orientations: top-left, bottom-left, top-right, bottom-right)", "timestamp_seconds": 36.0},
      {"puzzle_name": "Unlocking the '2P' Door Mechanism", "items_used": ["Screwdriver"], "solution_steps": ["Use the screwdriver to remove the screws on the rusty '2P' panel.", "Adjust the four dials to match the visual clue from the monitor."], "reward": "Opens the exit door", "timestamp_seconds": 54.0}
    ],
    "final_action": "The player successfully aligns the 4 dials behind the '2P' panel, causing the secret door hidden in the wall behind the wooden crates to swing open, allowing escape."
  },
  {
    "level": 2,
    "room_description": "A modern living room with beige walls, a patterned brown and gold rug, a wooden door, a desk with a laptop, a potted plant, a wooden glass-paneled display cabinet, and a white sofa.",
    "key_moments": [
      {"description": "Establishing shot of the living room.", "timestamp_seconds": 0.0},
      {"description": "Checking the laptop on the desk, which requires a text password.", "timestamp_seconds": 4.0},
      {"description": "Zooming into the potted plant to find a hidden key.", "timestamp_seconds": 8.0},
      {"description": "Approaching the lower wooden cabinet doors.", "timestamp_seconds": 11.0},
      {"description": "Unlocking the cabinet and finding a piece of paper.", "timestamp_seconds": 15.0},
      {"description": "Examining the paper to read the word 'TAKI'.", "timestamp_seconds": 18.0},
      {"description": "Entering 'TAKI' into the laptop's password prompt.", "timestamp_seconds": 21.0},
      {"description": "Laptop screen displaying the numeric code '1886'.", "timestamp_seconds": 26.0},
      {"description": "Finding a wooden box with a digital keypad inside the upper cabinet.", "timestamp_seconds": 31.0},
      {"description": "Using the keycard on the electronic door lock.", "timestamp_seconds": 38.0}
    ],
    "puzzles": [
      {"puzzle_name": "Plant Pot Key", "items_used": [], "solution_steps": ["Investigate the soil base of the potted plant near the desk."], "reward": "Silver Key", "timestamp_seconds": 8.0},
      {"puzzle_name": "Cabinet Paper Clue", "items_used": ["Silver Key"], "solution_steps": ["Use the silver key to unlock the bottom doors of the wooden display cabinet.", "Retrieve and examine the paper inside."], "reward": "Password clue 'TAKI'", "timestamp_seconds": 18.0},
      {"puzzle_name": "Laptop Password", "items_used": [], "solution_steps": ["Go to the laptop on the desk.", "Type the password 'TAKI' using the keyboard."], "reward": "Numeric code '1886'", "timestamp_seconds": 26.0},
      {"puzzle_name": "Keypad Safe Box", "items_used": [], "solution_steps": ["Open the upper section of the wooden cabinet.", "Interact with the digital keypad on the wooden box.", "Enter the code '1886'."], "reward": "Keycard", "timestamp_seconds": 34.0}
    ],
    "final_action": "The player inserts the retrieved keycard into the electronic lock on the main wooden door to unlock it and escape."
  },
  {
    "level": 3,
    "room_description": "A brightly lit room featuring blue wallpaper with yellow stars, a teal sofa, an abstract painting, a modern white desk setup with a laptop, and a patterned rug on the floor.",
    "key_moments": [
      {"description": "Establishing shot of the star-wallpapered room.", "timestamp_seconds": 0.0},
      {"description": "Lifting the pillow on the teal sofa.", "timestamp_seconds": 2.0},
      {"description": "Finding a silver key hidden behind the sofa pillow.", "timestamp_seconds": 3.0},
      {"description": "Approaching the white desk drawer.", "timestamp_seconds": 7.0},
      {"description": "Unlocking the drawer to find a compact disc (CD).", "timestamp_seconds": 8.0},
      {"description": "Inspecting the laptop which asks for a numeric password.", "timestamp_seconds": 12.0},
      {"description": "Examining the abstract wall art to find hidden numbers.", "timestamp_seconds": 13.0},
      {"description": "Entering the code '739' into the laptop.", "timestamp_seconds": 18.0},
      {"description": "Viewing the red dot pattern on the laptop screen.", "timestamp_seconds": 20.0},
      {"description": "Inputting the pattern into the metal pegboard on the wall to reveal the final key.", "timestamp_seconds": 29.0}
    ],
    "puzzles": [
      {"puzzle_name": "Sofa Key", "items_used": [], "solution_steps": ["Tap on the teal sofa to zoom in.", "Lift the left decorative pillow to reveal the item."], "reward": "Silver Key", "timestamp_seconds": 3.0},
      {"puzzle_name": "Desk Drawer CD", "items_used": ["Silver Key"], "solution_steps": ["Navigate to the white desk.", "Use the silver key on the lock of the top drawer to open it."], "reward": "Compact Disc (CD)", "timestamp_seconds": 8.0},
      {"puzzle_name": "Painting Code", "items_used": [], "solution_steps": ["Look closely at the abstract painting hanging on the wall.", "Identify the faint numbers embedded in the corners and design."], "reward": "Numeric code '739'", "timestamp_seconds": 13.0},
      {"puzzle_name": "Laptop Pattern Game", "items_used": ["Compact Disc (CD)"], "solution_steps": ["Access the laptop.", "Use the on-screen keypad to enter the code '739'.", "Observe the 5x4 grid pattern with specific red dots."], "reward": "Grid pattern visual clue", "timestamp_seconds": 20.0},
      {"puzzle_name": "Metal Pegboard Unlock", "items_used": [], "solution_steps": ["Locate the metal panel with circular holes.", "Tap the corresponding holes to turn them red, matching the pattern exactly as seen on the laptop screen."], "reward": "Final Door Key", "timestamp_seconds": 29.0}
    ],
    "final_action": "The player takes the key revealed from the hidden compartment behind the metal pegboard and uses it to unlock the main brown door and exit the room."
  },
  {
    "level": 4,
    "room_description": "A modern kitchen featuring dark brown lower cabinets, white upper cabinets, a black marble countertop island with a fruit bowl, a stove, a microwave, and a strange burger-themed machine built into the tiled right wall.",
    "key_moments": [
      {"description": "Establishing shot of the kitchen.", "timestamp_seconds": 0.0},
      {"description": "Retrieving the bottom half of a burger bun from inside the microwave.", "timestamp_seconds": 5.0},
      {"description": "Taking a cooked meat patty from the frying pan on the stove.", "timestamp_seconds": 9.0},
      {"description": "Collecting a plate of shredded lettuce from the counter next to the sink.", "timestamp_seconds": 12.0},
      {"description": "Placing the bottom bun onto the red tray on the kitchen island.", "timestamp_seconds": 16.0},
      {"description": "Finding a bottle of mustard/sauce inside the upper kitchen cabinet.", "timestamp_seconds": 42.0},
      {"description": "Completing the burger assembly by adding the top bun.", "timestamp_seconds": 47.0},
      {"description": "The burger-themed machine on the wall automatically opens its compartment.", "timestamp_seconds": 49.0},
      {"description": "Retrieving the door key from the opened wall machine.", "timestamp_seconds": 53.0},
      {"description": "Unlocking the main kitchen door with the key.", "timestamp_seconds": 56.0}
    ],
    "puzzles": [
      {"puzzle_name": "Gathering Ingredients", "items_used": [], "solution_steps": ["Check the microwave for the bottom bun.", "Check the stove pan for the meat patty.", "Check the sink area for the lettuce.", "Open the upper cabinet to find the sauce bottle."], "reward": "Burger Ingredients (Bun, Patty, Lettuce, Sauce)", "timestamp_seconds": 42.0},
      {"puzzle_name": "Burger Assembly", "items_used": ["Bottom Bun", "Meat Patty", "Lettuce", "Sauce"], "solution_steps": ["Go to the red tray on the kitchen island.", "Stack the ingredients in the correct order: Bottom Bun, Patty, Lettuce, Sauce, Top Bun (already on tray area)."], "reward": "Triggers the wall machine to open", "timestamp_seconds": 47.0},
      {"puzzle_name": "Burger Machine Reward", "items_used": [], "solution_steps": ["Walk over to the newly opened compartment in the burger-themed wall machine."], "reward": "Door Key", "timestamp_seconds": 53.0}
    ],
    "final_action": "The player uses the key obtained from the burger machine to unlock the main wooden door and escape the kitchen."
  },
  {
    "level": 5,
    "room_description": "A cozy bedroom with patterned beige wallpaper, a large bed with a brown runner and throw pillows, a wooden wardrobe, a TV stand with a DVD player, and a hidden wall safe located behind a mirror adorned with red rose petals.",
    "key_moments": [
      {"description": "Establishing shot of the bedroom.", "timestamp_seconds": 0.0},
      {"description": "Lifting the cylindrical bolster pillow on the bed to collect a TV remote.", "timestamp_seconds": 2.0},
      {"description": "Opening the white drawer under the TV to collect a DVD disc.", "timestamp_seconds": 14.0},
      {"description": "Collecting a battery from the shelves inside the wooden wardrobe.", "timestamp_seconds": 24.0},
      {"description": "The TV screen turns on, displaying a color test pattern and the red numbers '1096'.", "timestamp_seconds": 29.0},
      {"description": "Entering the code '1096' into the digital keypad of the hidden wall safe.", "timestamp_seconds": 35.0},
      {"description": "Retrieving a small silver key from inside the safe.", "timestamp_seconds": 36.0},
      {"description": "Using the silver key to unlock the glass-front bedside cabinet to find a blue keycard.", "timestamp_seconds": 44.0},
      {"description": "Swiping the blue keycard on the electronic door handle.", "timestamp_seconds": 48.0}
    ],
    "puzzles": [
      {"puzzle_name": "Powering the TV", "items_used": ["TV Remote", "DVD Disc", "Battery"], "solution_steps": ["Find the remote under the bed pillow.", "Find the DVD in the TV stand drawer.", "Find the battery in the wardrobe.", "Combine items to turn on the TV and reveal the code."], "reward": "Code '1096'", "timestamp_seconds": 29.0},
      {"puzzle_name": "Wall Safe Code", "items_used": [], "solution_steps": ["Locate the safe hidden in the wall cubby next to the mirror.", "Input the code '1096' seen on the TV screen."], "reward": "Silver Key", "timestamp_seconds": 35.0},
      {"puzzle_name": "Bedside Cabinet Lock", "items_used": ["Silver Key"], "solution_steps": ["Use the silver key from the safe to unlock the small nightstand/cabinet next to the bed."], "reward": "Blue Keycard", "timestamp_seconds": 44.0}
    ],
    "final_action": "The player inserts the blue keycard into the slot on the electronic door handle to unlock it and exit."
  },
  {
    "level": 6,
    "room_description": "A rundown, rustic room with boarded-up windows, stone flooring, a simple metal-framed bed, a worn armchair, a wooden door, and a wall poster showing animals made out of numbers.",
    "key_moments": [
      {"description": "Establishing shot of the rundown room.", "timestamp_seconds": 0.0},
      {"description": "Lifting the bed pillow to collect a wooden hammer handle.", "timestamp_seconds": 1.5},
      {"description": "Retrieving a metal hammer head from the floor beneath the bed.", "timestamp_seconds": 7.5},
      {"description": "Examining the wall poster displaying animals integrated with numbers.", "timestamp_seconds": 14.0},
      {"description": "Approaching a wooden box that is nailed shut with wooden planks.", "timestamp_seconds": 36.5},
      {"description": "Using the assembled hammer to pry the nailed planks off the box.", "timestamp_seconds": 37.5},
      {"description": "Entering the 3-digit combination '532' into the wooden box dials.", "timestamp_seconds": 43.0},
      {"description": "Retrieving the silver key from the opened box.", "timestamp_seconds": 44.5},
      {"description": "Unlocking the wooden exit door with the key.", "timestamp_seconds": 48.0}
    ],
    "puzzles": [
      {"puzzle_name": "Assemble the Hammer", "items_used": ["Wooden Handle", "Metal Hammer Head"], "solution_steps": ["Find the handle under the pillow.", "Find the head under the bed.", "Combine them in the inventory to create a usable hammer."], "reward": "Hammer", "timestamp_seconds": 7.5},
      {"puzzle_name": "Unseal the Box", "items_used": ["Hammer"], "solution_steps": ["Use the hammer on the wooden planks crossing the front of the box to pry out the nails."], "reward": "Access to combination dials", "timestamp_seconds": 37.5},
      {"puzzle_name": "Animal Code Box", "items_used": [], "solution_steps": ["Observe the animal poster to correlate animals to numbers: Elephant=5, Cat=3, Zebra=2.", "Enter the code '532' into the dials on the front of the box."], "reward": "Door Key", "timestamp_seconds": 43.0}
    ],
    "final_action": "The player uses the key found inside the combination box to unlock the room's central door and escape."
  },
  {
    "level": 7,
    "room_description": "An Egyptian tomb-themed room with walls covered in hieroglyphics, two golden Sphinx statues guarding the exit door, and various stone pedestals and artifacts scattered around.",
    "key_moments": [
      {"description": "Establishing shot of the Egyptian tomb room.", "timestamp_seconds": 0.0},
      {"description": "Finding a feather duster/brush behind a tilted stone block.", "timestamp_seconds": 8.5},
      {"description": "Collecting a chisel from the shelf beneath a small wooden chest.", "timestamp_seconds": 17.0},
      {"description": "Using the brush to clean off a dusty, blank stone panel on a pedestal.", "timestamp_seconds": 38.0},
      {"description": "Retrieving a wooden mallet from the newly revealed compartment.", "timestamp_seconds": 39.5},
      {"description": "Using the mallet and chisel to break open the clay pot on the floor.", "timestamp_seconds": 58.0},
      {"description": "Unrolling the scroll found in the pot to reveal Arabic numerals (١٥٢٢).", "timestamp_seconds": 61.5},
      {"description": "Entering the corresponding symbols (1-5-2-2) into the slots on the wall panel.", "timestamp_seconds": 75.0},
      {"description": "Retrieving the key from the compartment that opens below the wall panel.", "timestamp_seconds": 76.5},
      {"description": "Unlocking the main door between the Sphinxes using the key.", "timestamp_seconds": 81.0}
    ],
    "puzzles": [
      {"puzzle_name": "Dusty Compartment", "items_used": ["Brush"], "solution_steps": ["Find the brush hidden behind a stone.", "Use the brush on the blank, dusty square panel on the left pedestal."], "reward": "Wooden Mallet", "timestamp_seconds": 38.0},
      {"puzzle_name": "Breaking the Pot", "items_used": ["Mallet", "Chisel"], "solution_steps": ["Find the chisel on the shelf.", "Combine the mallet and chisel to break the round clay pot on the floor."], "reward": "Scroll with a clue", "timestamp_seconds": 58.0},
      {"puzzle_name": "Hieroglyphic Number Lock", "items_used": ["Scroll"], "solution_steps": ["Read the scroll to see the Arabic numerals '١٥٢٢' (1522).", "Locate the wall panel with 4 vertical slots.", "Change the slots to match the symbols for 1, 5, 2, and 2."], "reward": "Door Key", "timestamp_seconds": 75.0}
    ],
    "final_action": "The player takes the key from the stone wall compartment and uses it to unlock the large door located in the center of the room."
  },
  {
    "level": 8,
    "room_description": "An elegant, luxurious bedroom featuring a large bed, patterned wallpaper, an armoire, a grandfather clock, a wooden chest resting on a bench, and a framed jigsaw puzzle on the wall.",
    "key_moments": [
      {"description": "Establishing shot of the bedroom.", "timestamp_seconds": 0.0},
      {"description": "Collecting a puzzle piece from inside the ice bucket on the bed tray.", "timestamp_seconds": 3.5},
      {"description": "Collecting a second puzzle piece pinned to the black coat hanging on the mannequin.", "timestamp_seconds": 5.5},
      {"description": "Collecting a third puzzle piece from the top of the chest, revealing the red text '6:15'.", "timestamp_seconds": 7.5},
      {"description": "Completing the framed jigsaw puzzle on the wall.", "timestamp_seconds": 176.0},
      {"description": "The completed jigsaw puzzle morphs into a clue showing an arrangement of dots and lines.", "timestamp_seconds": 177.0},
      {"description": "Arranging the wooden sliders on the chest to match the dot pattern from the puzzle clue.", "timestamp_seconds": 208.0},
      {"description": "Retrieving two metal rings from inside the opened chest.", "timestamp_seconds": 209.0},
      {"description": "Placing the rings onto the two pegs of the grandfather clock face to open the glass cover.", "timestamp_seconds": 214.0},
      {"description": "Setting the hands on the clock face to '6:15', causing the bottom cabinet door to swing open.", "timestamp_seconds": 222.0},
      {"description": "Retrieving the main door key from the bottom of the grandfather clock.", "timestamp_seconds": 239.0},
      {"description": "Unlocking the exit door with the key.", "timestamp_seconds": 243.0}
    ],
    "puzzles": [
      {"puzzle_name": "Jigsaw Puzzle Assembly", "items_used": ["Puzzle Piece 1", "Puzzle Piece 2", "Puzzle Piece 3"], "solution_steps": ["Find the 3 missing puzzle pieces around the room (ice bucket, coat, chest).", "Interact with the painting frame.", "Assemble the pieces to form a complete picture of a Venetian canal."], "reward": "Slider pattern visual clue", "timestamp_seconds": 176.0},
      {"puzzle_name": "Chest Slider Lock", "items_used": [], "solution_steps": ["Observe the line and dot pattern revealed after finishing the jigsaw puzzle.", "Interact with the front of the wooden chest.", "Move the three wooden sliders so they align perfectly with the dot positions shown on the clue."], "reward": "Two Rings", "timestamp_seconds": 208.0},
      {"puzzle_name": "Grandfather Clock Mechanism", "items_used": ["Two Rings"], "solution_steps": ["Attach the two rings to the small pegs on the grandfather clock face to act as handles.", "Open the glass cover.", "Set the clock hands to read '6:15', using the clue written in red on top of the chest."], "reward": "Door Key", "timestamp_seconds": 222.0}
    ],
    "final_action": "The player takes the key revealed in the bottom compartment of the grandfather clock and uses it to unlock the main door."
  },
  {
    "level": 11,
    "room_description": "A vibrant and colorful child's or teenager's bedroom. It features a bunk bed with blue and yellow bedding, a red suitcase, a desk with a computer and a green swivel chair, and several posters and shelving units with toys. The walls are light blue and the floor is wooden.",
    "key_moments": [
      {"description": "Establishing shot showing the overall view of the bedroom", "timestamp_seconds": 0.0},
      {"description": "Zooming in on the blue wall poster with glowing symbols", "timestamp_seconds": 9.5},
      {"description": "Assembling the pliers from two separate parts", "timestamp_seconds": 33.5},
      {"description": "Solving the color wheel puzzle on the bunk bed shelf", "timestamp_seconds": 45.8},
      {"description": "Combining two halves of a torn paper to reveal a code", "timestamp_seconds": 50.5}
    ],
    "puzzles": [
      {"puzzle_name": "Assembling the Tool", "items_used": ["Pliers handle", "Pliers head"], "solution_steps": ["Find the pliers handle in the lower bunk bed area", "Find the pliers head inside the wall shelving", "Combine the handle and the head in the inventory"], "reward": "Pliers", "timestamp_seconds": 33.5},
      {"puzzle_name": "Red Suitcase Lock", "items_used": ["Pliers"], "solution_steps": ["Use the pliers to cut the metal wire lock on the red suitcase lying on the floor"], "reward": "A blue triangle block", "timestamp_seconds": 38.2},
      {"puzzle_name": "Color Wheel Logic", "items_used": ["Numerical clue from poster"], "solution_steps": ["Examine the poster on the wall to see the number sequence '3917'", "Adjust the four colored dials on the shelf box to match the sequence: Red (3), Blue (9), Yellow (1), Green (7)"], "reward": "A torn half piece of paper", "timestamp_seconds": 48.3},
      {"puzzle_name": "Alarm Clock Time Code", "items_used": ["Two combined pieces of paper"], "solution_steps": ["Collect the first piece of paper from the wall lamp on the left", "Collect the second piece of paper from the color wheel drawer", "Combine both pieces to see the numbers 0, 7, 4, 5 highlighted", "Set the green alarm clock's time to 07:45"], "reward": "Door Key", "timestamp_seconds": 58.5}
    ],
    "final_action": "The player uses the silver key obtained from the alarm clock to unlock and open the white door, exiting the room."
  }
]

video_mapping = {
    1: r"Videos\Escape Game 50 Rooms 1\01 - Escape game 50 rooms 1 - Puzzle Game - Level 1.f271.webm",
    2: r"Videos\Escape Game 50 Rooms 1\02 - Escape game 50 rooms 1 - Level 2.f271.webm",
    3: r"Videos\Escape Game 50 Rooms 1\03 - Escape game 50 rooms 1 - Level 3.f271.webm",
    4: r"Videos\Escape Game 50 Rooms 1\04 - Escape game 50 rooms 1 - Level 4.f271.webm",
    5: r"Videos\Escape Game 50 Rooms 1\05 - Escape game 50 rooms 1 - Level 5.f271.webm",
    6: r"Videos\Escape Game 50 Rooms 1\06 - Escape game 50 rooms 1 - Level 6.f271.webm",
    7: r"Videos\Escape Game 50 Rooms 1\07 - Escape game 50 rooms 1 - Level 7.f271.webm",
    8: r"Videos\Escape Game 50 Rooms 1\08 - Escape game 50 rooms 1 - Level 8 [Check description if any trouble].f271.webm",
    11: r"Videos\Escape Game 50 Rooms 1\11 - Escape game 50 rooms 1 - Level 11.f271.webm"
}

for room in batch_data:
    level = room["level"]
    video_path = video_mapping.get(level)
    if not video_path:
        print(f"Skipping Level {level}: Video path not found.")
        continue
    
    print(f"\n--- Processing Level {level} ---")
    
    # Wipe the existing screenshots folder to ensure a clean deduplicated run
    level_dir = os.path.join("Output", f"Level_{level}")
    screenshots_dir = os.path.join(level_dir, "Screenshots")
    if os.path.exists(screenshots_dir):
        print(f"Cleaning up old screenshots in {screenshots_dir}...")
        shutil.rmtree(screenshots_dir)
    
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

print("\nFull Clean Re-Processing Complete!")
