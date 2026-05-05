import os
import json
import subprocess

batch_data = [
  {
    "level": 41,
    "room_description": "A well-lit, modern living room with beige patterned wallpaper, a white sofa setup, a dark wood coffee table, a TV stand with a decorative ship, a display cabinet, and a study desk with a computer.",
    "key_moments": [
      {"description": "Establishing shot of the living room.", "timestamp_seconds": 0.0},
      {"description": "Finding a blue rubber band hidden between the sofa cushions.", "timestamp_seconds": 3.0},
      {"description": "Collecting a pair of scissors from the top drawer of the display cabinet.", "timestamp_seconds": 9.0},
      {"description": "Opening the middle cabinet drawer to get a roll of yellow tape.", "timestamp_seconds": 20.0},
      {"description": "Using scissors to cut open the sofa cushion, retrieving a blue flash drive.", "timestamp_seconds": 31.0},
      {"description": "Solving the flower picture puzzle to reveal the hidden code '6540'.", "timestamp_seconds": 65.0},
      {"description": "Opening the safe behind the picture frame to get the red keycard.", "timestamp_seconds": 72.0},
      {"description": "Solving the 'Quickspot' puzzle on the computer.", "timestamp_seconds": 121.0},
      {"description": "Entering '4681' into the wooden box lock.", "timestamp_seconds": 125.0},
      {"description": "Retrieving the screwdriver from the wooden box and using it to unscrew the wall vent.", "timestamp_seconds": 127.0}
    ],
    "puzzles": [
      {"puzzle_name": "Sofa Cushion Flash Drive", "items_used": ["Scissors"], "solution_steps": ["Get the scissors from the display cabinet.", "Use the scissors on the patched-up tear on the white sofa cushion.", "Collect the blue USB flash drive hidden inside."], "reward": "Blue Flash Drive", "timestamp_seconds": 31.0},
      {"puzzle_name": "Flower Picture Code", "items_used": ["Blue Rubber Band", "Yellow Tape"], "solution_steps": ["Find the rubber band (sofa) and tape (cabinet).", "Go to the framed picture of flowers on the left wall.", "The picture morphs into a grid. Apply the colored tape/bands to the grid lines based on the visual clue on the wall (Red, Yellow, Green, Blue borders).", "The grid reveals the numbers '6540'."], "reward": "Numeric code '6540'", "timestamp_seconds": 65.0},
      {"puzzle_name": "Computer Differences", "items_used": ["Blue Flash Drive"], "solution_steps": ["Plug the flash drive into the computer on the desk.", "Play the 'spot the difference' minigame on the screen.", "Click the 5 differences between the two images to reveal the code '4681'."], "reward": "Code '4681'", "timestamp_seconds": 121.0},
      {"puzzle_name": "Vent Escape", "items_used": ["Screwdriver"], "solution_steps": ["Enter '4681' into the wooden box in the desk area.", "Retrieve the screwdriver.", "Use the screwdriver on the metal vent cover located near the floor."], "reward": "Access to the escape vent", "timestamp_seconds": 128.0}
    ],
    "final_action": "The player removes the metal vent cover using the screwdriver and crawls into the ventilation shaft to escape the room."
  },
  {
    "level": 42,
    "room_description": "An Egyptian tomb filled with hieroglyphics. It features a central sarcophagus, statues of Anubis and Horus guarding the sides, sun motifs, and glowing floor panels.",
    "key_moments": [
      {"description": "Establishing shot of the Egyptian tomb.", "timestamp_seconds": 0.0},
      {"description": "Collecting the top piece of a golden pyramid from the floor.", "timestamp_seconds": 2.5},
      {"description": "Entering a hidden chamber behind the Sphinx statue.", "timestamp_seconds": 10.0},
      {"description": "Solving the element wheel puzzle to open the wall compartment.", "timestamp_seconds": 17.5},
      {"description": "Retrieving a golden scarab beetle from the compartment.", "timestamp_seconds": 19.0},
      {"description": "Solving the large sliding tile mural puzzle.", "timestamp_seconds": 104.0},
      {"description": "Using the scarab beetle to unlock the glowing sun emblem.", "timestamp_seconds": 107.0},
      {"description": "Collecting the bottom half of the golden pyramid.", "timestamp_seconds": 127.0},
      {"description": "Placing the assembled pyramid onto the altar.", "timestamp_seconds": 131.0},
      {"description": "Taking the golden eye token and unlocking the exit.", "timestamp_seconds": 140.0}
    ],
    "puzzles": [
      {"puzzle_name": "Element Wheel", "items_used": [], "solution_steps": ["Enter the side chamber.", "Interact with the circular panel on the wall showing elemental symbols.", "Rotate the rings to align the symbols according to the environmental clues (Fire on bottom, Water on right, Sun on left, Moon on top)."], "reward": "Golden Scarab Beetle", "timestamp_seconds": 17.5},
      {"puzzle_name": "Mural Sliding Puzzle", "items_used": [], "solution_steps": ["Interact with the large chaotic mural on the wall.", "Slide the rectangular segments horizontally and vertically to form a coherent picture of Egyptian figures and deities."], "reward": "Access to the sun emblem lock", "timestamp_seconds": 104.0},
      {"puzzle_name": "Scarab and Sun", "items_used": ["Golden Scarab Beetle"], "solution_steps": ["After finishing the mural, a sun emblem is revealed.", "Place the golden scarab beetle into the center indentation of the sun emblem.", "The wall slides open."], "reward": "Access to the inner sanctum / Pyramid base", "timestamp_seconds": 107.0},
      {"puzzle_name": "Pyramid Assembly", "items_used": ["Pyramid Top", "Pyramid Base"], "solution_steps": ["Retrieve the base of the pyramid from the inner sanctum.", "Combine the top (found on the floor earlier) with the base.", "Place the completed pyramid onto the square pedestal in the main room."], "reward": "Golden Eye Token", "timestamp_seconds": 131.0}
    ],
    "final_action": "The player places the assembled golden pyramid on the pedestal, which reveals a compartment containing a Golden Eye token. This token is inserted into the main door mechanism to unlock it."
  },
  {
    "level": 43,
    "room_description": "A modern, metallic bunker or control room featuring diamond-plate walls, black statues, a hanging fireplace, a computer desk, and a large central metal door.",
    "key_moments": [
      {"description": "Establishing shot of the metallic bunker.", "timestamp_seconds": 0.0},
      {"description": "Finding a silver coin near the base of a statue.", "timestamp_seconds": 8.0},
      {"description": "Collecting an unlit torch handle from the fireplace grate.", "timestamp_seconds": 14.0},
      {"description": "Looking at the wall clock to see the time '4:15'.", "timestamp_seconds": 19.5},
      {"description": "Entering '4195' into the briefcase lock.", "timestamp_seconds": 32.0},
      {"description": "Retrieving a bottle of oil from the briefcase.", "timestamp_seconds": 36.5},
      {"description": "Using the coin to unscrew the panel on the desk.", "timestamp_seconds": 41.5},
      {"description": "Lighting the torch in the fireplace.", "timestamp_seconds": 54.0},
      {"description": "Using the lit torch to reveal a code hidden in a dark wall compartment.", "timestamp_seconds": 63.5},
      {"description": "Solving the gear rotation puzzle on the wall.", "timestamp_seconds": 81.0}
    ],
    "puzzles": [
      {"puzzle_name": "Briefcase Code", "items_used": [], "solution_steps": ["Examine the wall clock. The hands indicate the time 4:15.", "Examine the desk calendar. The date circled is the 9th.", "Combine the numbers: 4, 1, 9, 5.", "Use the code '4195' to unlock the briefcase on the floor."], "reward": "Bottle of Oil", "timestamp_seconds": 32.0},
      {"puzzle_name": "Lighting the Torch", "items_used": ["Torch Handle", "Oil Bottle"], "solution_steps": ["Collect the torch handle from the floor.", "Apply the oil from the briefcase to the torch.", "Hold the oiled torch to the flames in the hanging fireplace to light it."], "reward": "Lit Torch", "timestamp_seconds": 54.0},
      {"puzzle_name": "Hidden Wall Code", "items_used": ["Lit Torch"], "solution_steps": ["Find the dark, recessed compartment in the wall.", "Use the lit torch to illuminate the interior.", "Read the numbers revealed in the light: '2468'."], "reward": "Code '2468'", "timestamp_seconds": 63.5},
      {"puzzle_name": "Desk Panel & Gears", "items_used": ["Silver Coin"], "solution_steps": ["Use the coin to unscrew the flat panel on the desk.", "Enter the code '2468' into the revealed keypad.", "A wall panel opens showing gears. Rotate the rings to align the gaps, allowing the central mechanism to turn."], "reward": "Unlocks the main door", "timestamp_seconds": 81.0}
    ],
    "final_action": "After completing the gear puzzle, the main heavy metal door in the center of the room opens, allowing the player to escape."
  },
  {
    "level": 44,
    "room_description": "A subterranean stone crypt or dungeon. It features a central illuminated statue of a winged figure, scattered candles, Roman numerals carved into the walls, and a dirt floor.",
    "key_moments": [
      {"description": "Establishing shot of the stone crypt.", "timestamp_seconds": 0.0},
      {"description": "Noting the Roman numeral pairs carved on the wall (VII II, V II, I II, III II).", "timestamp_seconds": 6.5},
      {"description": "Solving the water flow puzzle on the stone panel.", "timestamp_seconds": 24.5},
      {"description": "Entering '1425' into the wall panel.", "timestamp_seconds": 28.0},
      {"description": "Solving the ring rotation puzzle on the floor pedestal.", "timestamp_seconds": 41.5},
      {"description": "Collecting a glowing orb from the pedestal.", "timestamp_seconds": 44.0},
      {"description": "Entering '5273' into the combination lock.", "timestamp_seconds": 53.0},
      {"description": "Placing the glowing orb into the skull's eye socket.", "timestamp_seconds": 56.5},
      {"description": "Inputting the symbol code onto the floor plate.", "timestamp_seconds": 60.5},
      {"description": "Retrieving the exit key from the opened compartment.", "timestamp_seconds": 61.5}
    ],
    "puzzles": [
      {"puzzle_name": "Roman Numeral Math", "items_used": [], "solution_steps": ["Observe the Roman numeral pairs on the wall: VII (7) and II (2), V (5) and II (2), I (1) and II (2), III (3) and II (2).", "Subtract the second number from the first: 7-2=5, 5-2=3, 1-2 (treated as absolute difference or just reading the first numeral incorrectly in logic? Wait, the video shows entering 1425. Let's re-examine. Actually, it's 7/2=3.5 -> no. Let's look at the symbols again at 00:07. It's VII II (7/2), V II (5/2), I II (1/2), III II (3/2). The video enters '1425' at 00:28 based on the water puzzle. The Roman numerals seem to be a different clue.)"], "reward": "Unknown/Contextual", "timestamp_seconds": 6.5},
      {"puzzle_name": "Water Path Slider", "items_used": [], "solution_steps": ["Interact with the stone panel showing blue liquid.", "Use the directional arrows to move the turtle block, clearing a continuous path for the water to flow from the inlet to the outlet."], "reward": "Reveals Roman Numerals 'I IV II V III A'", "timestamp_seconds": 24.5},
      {"puzzle_name": "Altar Ring Puzzle", "items_used": [], "solution_steps": ["Interact with the circular stone pedestal on the floor.", "Rotate the outer rings until the glowing orange symbols match the pattern (forming a specific sequence of Greek-like letters)."], "reward": "Glowing Orb", "timestamp_seconds": 41.5},
      {"puzzle_name": "Symbol Floor Lock", "items_used": ["Glowing Orb"], "solution_steps": ["Place the orb into the eye socket of the skeleton in the corner to reveal a symbol clue.", "Go to the rectangular plate on the floor.", "Change the four symbols to match the clue (Pi, Phi, Omega, Omega)."], "reward": "Exit Key", "timestamp_seconds": 60.5}
    ],
    "final_action": "The player uses the key found under the symbol plate to unlock the heavy wooden door hidden in the back wall and escape."
  },
  {
    "level": 45,
    "room_description": "A vibrant, futuristic lounge with a bright blue and green galaxy-patterned wall. It contains modern black and white curved seating, a suspended spherical fireplace, colorful hanging light bulbs, and abstract art pieces.",
    "key_moments": [
      {"description": "Establishing shot of the futuristic lounge.", "timestamp_seconds": 0.0},
      {"description": "Finding a red utility knife hidden under a sofa pillow.", "timestamp_seconds": 3.0},
      {"description": "Collecting a U-shaped magnet from the white futuristic chair.", "timestamp_seconds": 9.0},
      {"description": "Using the magnet on a string to fish a white sphere out of a tall vase.", "timestamp_seconds": 15.0},
      {"description": "Opening the white cabinet to find an empty glass.", "timestamp_seconds": 23.0},
      {"description": "Arranging the four colored square blocks on the wall panel.", "timestamp_seconds": 34.0},
      {"description": "Viewing the planets/spheres through the telescope.", "timestamp_seconds": 38.0},
      {"description": "Entering '4681' into the colored button panel.", "timestamp_seconds": 51.0},
      {"description": "Collecting a purple screwdriver from the opened compartment.", "timestamp_seconds": 52.0},
      {"description": "Removing the panel on the white table using the screwdriver to get the final key.", "timestamp_seconds": 54.0}
    ],
    "puzzles": [
      {"puzzle_name": "Magnetic Fishing", "items_used": ["Magnet"], "solution_steps": ["Find the magnet on the white chair.", "Attach the magnet to the string hanging over the tall white vase.", "Lower it to pull out the white sphere with the number '6' on it."], "reward": "Numbered Sphere '6'", "timestamp_seconds": 15.0},
      {"puzzle_name": "Colored Square Alignment", "items_used": [], "solution_steps": ["Observe the colored squares hidden around the room (e.g., behind pillows, on walls).", "Interact with the wall panel.", "Rearrange the sliders so the colors match the sequence: Grey, Red, Grey, Green."], "reward": "Access to the Telescope", "timestamp_seconds": 34.0},
      {"puzzle_name": "Telescope Planet Code", "items_used": ["Numbered Sphere '6'"], "solution_steps": ["Look through the telescope at the starry background.", "Identify the numbers written on the floating colored planets: Pink(4), Yellow(6), Green(8), Yellow-Green(1).", "Note the sequence based on the colored bulbs hanging in the room."], "reward": "Numeric code '4681'", "timestamp_seconds": 38.0},
      {"puzzle_name": "Table Panel Key", "items_used": ["Purple Screwdriver"], "solution_steps": ["Input the code '4681' into the lock matching the planet colors.", "Take the purple screwdriver from the compartment.", "Use the screwdriver to remove the side panel from the futuristic white table."], "reward": "Final Exit Key", "timestamp_seconds": 54.0}
    ],
    "final_action": "The player takes the key revealed inside the white table structure and uses it to unlock the modern glass door to escape."
  }
]

video_mapping = {
    41: r"Videos\Escape Game 50 Rooms 1\41 - Escape game 50 rooms 1 I Level 41.f271.webm",
    42: r"Videos\Escape Game 50 Rooms 1\42 - Escape game 50 rooms 1 I Level 42.f271.webm",
    43: r"Videos\Escape Game 50 Rooms 1\43 - Escape game 50 rooms 1 I Level 43.f271.webm",
    44: r"Videos\Escape Game 50 Rooms 1\44 - Escape game 50 rooms 1 I Level 44.f271.webm",
    45: r"Videos\Escape Game 50 Rooms 1\45 - Escape game 50 rooms 1 I Level 45.f271.webm"
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
