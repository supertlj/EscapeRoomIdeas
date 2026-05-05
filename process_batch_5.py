import os
import json
import subprocess

batch_data = [
  {
    "level": 21,
    "room_description": "A modern bedroom with tan wood paneling, a large double bed with a brown and black runner, a desk with a computer on the left, a wall-mounted ship painting, and a vertical heater unit on the right.",
    "key_moments": [
      {"description": "Establishing shot of the bedroom interior.", "timestamp_seconds": 0.0},
      {"description": "Removing the heater grate to find a hidden compartment.", "timestamp_seconds": 1.4},
      {"description": "Lifting the bed runner to find a golden star-shaped token.", "timestamp_seconds": 10.0},
      {"description": "Tapping the wall shelves to collect a small white model bicycle.", "timestamp_seconds": 11.5},
      {"description": "Inspecting the smartphone on the desk to see notification numbers.", "timestamp_seconds": 18.5},
      {"description": "Finding a numeric lock box inside the desk drawer.", "timestamp_seconds": 23.0},
      {"description": "Retreiving a yellow pencil and a screwdriver from a different cabinet section.", "timestamp_seconds": 36.5},
      {"description": "Opening a hidden wall safe behind the heater area using the screwdriver.", "timestamp_seconds": 50.5},
      {"description": "Using tokens to unlock a specialized box hidden in a wall niche.", "timestamp_seconds": 57.0},
      {"description": "Retrieving the exit key and opening the door.", "timestamp_seconds": 63.5}
    ],
    "puzzles": [
      {"puzzle_name": "The Notification Code", "items_used": [], "solution_steps": ["Check the smartphone on the left desk.", "Note the counts: Calls (2), Messages (5), Updates (8).", "Enter '258' into the numeric box inside the desk drawer."], "reward": "Blue token", "timestamp_seconds": 26.5},
      {"puzzle_name": "Wall Grate Secret", "items_used": ["Screwdriver"], "solution_steps": ["Locate the vertical heater/grate on the right wall.", "Use the screwdriver to remove the screws and the grate.", "Collect the half-moon token from inside."], "reward": "Half-moon token", "timestamp_seconds": 50.5},
      {"puzzle_name": "Celestial Token Box", "items_used": ["Star token", "Half-moon token"], "solution_steps": ["Navigate to the hidden wall niche (behind the ship painting).", "Insert the star token and the moon token into the wooden box.", "The box opens to reveal the key."], "reward": "Silver Exit Key", "timestamp_seconds": 59.5}
    ],
    "final_action": "The player uses the silver key on the main wooden door to unlock it and exit the room."
  },
  {
    "level": 22,
    "room_description": "An underwater-themed fantasy room with blue floors, glowing jellyfish lights, hanging shark and dolphin figures, and a spiral staircase.",
    "key_moments": [
      {"description": "Establishing shot of the bioluminescent underwater room.", "timestamp_seconds": 0.0},
      {"description": "Checking the numeric safe box on the left rock formation.", "timestamp_seconds": 2.5},
      {"description": "Counting the colored glowing lights on the hanging fish models.", "timestamp_seconds": 6.0},
      {"description": "Entering '424' into the rock-mounted safe.", "timestamp_seconds": 15.5},
      {"description": "Collecting a purple triangle token from the safe.", "timestamp_seconds": 16.5},
      {"description": "Observing the numbered fish silhouettes on the background wall.", "timestamp_seconds": 28.5},
      {"description": "Setting the color sequence on the barrel-shaped pillar.", "timestamp_seconds": 38.0},
      {"description": "Solving the numeric path puzzle on the exit door console.", "timestamp_seconds": 52.0},
      {"description": "Solving the circuit-style tile rotation puzzle.", "timestamp_seconds": 123.0}
    ],
    "puzzles": [
      {"puzzle_name": "Glow Fish Code", "items_used": [], "solution_steps": ["Observe the hanging fish models: Pink has 4 lights, Yellow has 2, Blue has 4.", "Input '424' into the colored numeric boxes on the left rock."], "reward": "Purple Triangle Token", "timestamp_seconds": 15.5},
      {"puzzle_name": "Fish Silhouette Barrel", "items_used": [], "solution_steps": ["Look at the numbered fish silhouettes on the back wall.", "Match the numbers (1-6) to the colors of the jellyfish near them.", "Adjust the circular buttons on the twin-barrel unit to match the sequence."], "reward": "Teal Pentagon Token", "timestamp_seconds": 38.5},
      {"puzzle_name": "Token Geometric Lock", "items_used": ["Purple Triangle Token", "Teal Pentagon Token"], "solution_steps": ["Go to the golden pentagonal pedestal.", "Place the triangle and pentagon tokens into their matching slots.", "Observe the number code '474' that appears."], "reward": "Code '474'", "timestamp_seconds": 45.5},
      {"puzzle_name": "Pipe Connection Grid", "items_used": [], "solution_steps": ["Enter '474' into the keypad on the green door.", "Solve the puzzle by rotating the square tiles to create a continuous path of light from the power sources."], "reward": "Unlocks the exit door", "timestamp_seconds": 123.0}
    ],
    "final_action": "Once the light path is fully connected, the green door automatically opens, allowing the player to swim through and escape."
  },
  {
    "level": 23,
    "room_description": "A classic study with dark wood paneling, a floral sofa, a coffee table with a newspaper and tea set, and a kitchen counter area on the right.",
    "key_moments": [
      {"description": "Establishing shot of the study.", "timestamp_seconds": 0.0},
      {"description": "Opening the kitchen drawer to find a green hand pump.", "timestamp_seconds": 4.5},
      {"description": "Finding an orange combination box on the floor.", "timestamp_seconds": 7.5},
      {"description": "Lifting the sofa cushions to find a red/blue magnet.", "timestamp_seconds": 14.5},
      {"description": "Using the hand pump to inflate the deflated basketball.", "timestamp_seconds": 27.5},
      {"description": "Observing the color-coded star pattern on the inflated ball.", "timestamp_seconds": 31.0},
      {"description": "Using the magnet to fish a metal item out of the bean barrel.", "timestamp_seconds": 52.0},
      {"description": "Pouring a cup of coffee to reveal the code '7164'.", "timestamp_seconds": 69.5},
      {"description": "Entering '7162' (calculated) into the orange box.", "timestamp_seconds": 120.5},
      {"description": "Solving the fruit-clicking puzzle to get the final key.", "timestamp_seconds": 149.0}
    ],
    "puzzles": [
      {"puzzle_name": "Basketball Inflation", "items_used": ["Hand Pump"], "solution_steps": ["Retrieve the green pump from the kitchen drawer.", "Use the pump on the flat basketball on the rug.", "Identify the color sequence: Red, Yellow, Blue, White."], "reward": "Color Clue", "timestamp_seconds": 31.0},
      {"puzzle_name": "Magnetic Retrieval", "items_used": ["Magnet"], "solution_steps": ["Find the magnet under the sofa pillow.", "Use the magnet on the large wooden barrel filled with beans.", "Pull out the small metal handle."], "reward": "Small Handle", "timestamp_seconds": 52.0},
      {"puzzle_name": "The Coffee Clue", "items_used": [], "solution_steps": ["Interact with the coffee pot on the counter.", "Pour the coffee into the empty white mug.", "The bottom of the mug reveals the code '7164'."], "reward": "Numeric code '7164'", "timestamp_seconds": 69.5},
      {"puzzle_name": "Fruit Plate Elimination", "items_used": [], "solution_steps": ["Enter the code '7162' into the orange chest on the floor.", "In the mini-game, click the fruits one by one to make them disappear until only the key remains."], "reward": "Silver Exit Key", "timestamp_seconds": 149.0}
    ],
    "final_action": "The player takes the silver key from the fruit plate and uses it to unlock the center door and escape."
  },
  {
    "level": 24,
    "room_description": "A vibrant green living room with a large white L-shaped sofa, a zebra-print rug, and a modern TV stand.",
    "key_moments": [
      {"description": "Establishing shot of the green living room.", "timestamp_seconds": 0.0},
      {"description": "Finding a sharp knife hidden under the coffee table.", "timestamp_seconds": 1.5},
      {"description": "Cutting the sofa cushion with the knife to find a red remote.", "timestamp_seconds": 4.5},
      {"description": "Finding a crowbar inside the white cabinet.", "timestamp_seconds": 7.5},
      {"description": "Using the crowbar to pry open the door of the modern fireplace.", "timestamp_seconds": 11.0},
      {"description": "Tapping the toilet tank (oddly placed in wall) to find a clue.", "timestamp_seconds": 16.5},
      {"description": "Using the remote to turn on the TV and see the color bars.", "timestamp_seconds": 26.5},
      {"description": "Counting the colored fish on the wall: 7 Purple, 4 Green, 6 Red.", "timestamp_seconds": 32.5},
      {"description": "Entering '746' into the numeric safe drawer.", "timestamp_seconds": 40.0},
      {"description": "Retrieving the keycard and exiting.", "timestamp_seconds": 44.0}
    ],
    "puzzles": [
      {"puzzle_name": "The Sofa Secret", "items_used": ["Knife"], "solution_steps": ["Find the knife under the triangular coffee table.", "Use the knife to slice the seat of the white sofa.", "Pick up the red TV remote."], "reward": "TV Remote", "timestamp_seconds": 4.5},
      {"puzzle_name": "Fish Wall Tally", "items_used": ["TV Remote"], "solution_steps": ["Use the remote to turn on the TV, which shows color bars: Purple, Green, Red.", "Count the corresponding colored fish decorations on the green wall.", "Purple (7), Green (4), Red (6)."], "reward": "Code '746'", "timestamp_seconds": 40.0}
    ],
    "final_action": "The player takes the blue keycard from the drawer and uses it to unlock the exit door at the back of the room."
  },
  {
    "level": 25,
    "room_description": "A dark, macabre studio featuring gothic armor, a skeleton leaning against the wall, an artist's easel with a sketch, and a large demonic portrait.",
    "key_moments": [
      {"description": "Establishing shot of the dark studio.", "timestamp_seconds": 0.0},
      {"description": "Finding a blue block inside a barrel.", "timestamp_seconds": 3.5},
      {"description": "Collecting a wooden rod from the back of the artist's easel.", "timestamp_seconds": 8.5},
      {"description": "Using the rod to knock down a key hidden above the skeleton.", "timestamp_seconds": 18.0},
      {"description": "Opening a drawer to find another blue block.", "timestamp_seconds": 20.0},
      {"description": "Cleaning the easel sketch with a wet cloth to reveal a code.", "timestamp_seconds": 25.5},
      {"description": "Entering '5273' into the wall panel.", "timestamp_seconds": 38.5},
      {"description": "Placing blue blocks onto the demonic portrait.", "timestamp_seconds": 44.5},
      {"description": "Solving the grid-pattern clicking puzzle on the wall.", "timestamp_seconds": 60.5},
      {"description": "Retrieving the final key and escaping.", "timestamp_seconds": 65.5}
    ],
    "puzzles": [
      {"puzzle_name": "Easel Reveal", "items_used": ["Wet Cloth"], "solution_steps": ["Obtain the wet cloth from the side table.", "Use it to wipe the charcoal sketch on the easel.", "A pattern of numbers on blue squares (4, 5, 2, 8) is revealed."], "reward": "Visual code clue", "timestamp_seconds": 31.5},
      {"puzzle_name": "Demonic Grid", "items_used": ["Blue Blocks"], "solution_steps": ["Look at the demon portrait.", "Interact with the grid on the wall next to it.", "Select the circles to match the pattern from the demon's eyes or the canvas clue (Red dots on the grid)."], "reward": "Final Silver Key", "timestamp_seconds": 62.0}
    ],
    "final_action": "The player uses the silver key found in the wall compartment to unlock the central wooden door and escape."
  }
]

video_mapping = {
    21: r"Videos\Escape Game 50 Rooms 1\21 - Escape Game 50 Rooms 1 I Level 21.f271.webm",
    22: r"Videos\Escape Game 50 Rooms 1\22 - Escape Game 50 Rooms 1 I Level 22.f400.mp4",
    23: r"Videos\Escape Game 50 Rooms 1\23 - Escape Game 50 Rooms 1 I Level 23.f271.webm",
    24: r"Videos\Escape Game 50 Rooms 1\24 - Escape game 50 rooms 1 ｜ Level 24.f271.webm",
    25: r"Videos\Escape Game 50 Rooms 1\25 - Escape game 50 rooms 1 ｜ Level 25.f271.webm"
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
