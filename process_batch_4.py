import os
import json
import subprocess

batch_data = [
  {
    "level": 15,
    "room_description": "A rustic wooden cabin or office room featuring a desk, bookshelf, a vintage globe, a small safe, plants, and puzzle panels integrated into the floor and walls.",
    "key_moments": [
      {"description": "Establishing shot of the wooden office room.", "timestamp_seconds": 0.0},
      {"description": "Inspects the metal dot puzzle integrated into the wooden floor.", "timestamp_seconds": 1.0},
      {"description": "Checks the desk and moves magazines to reveal the equation 'Z=Y-X'.", "timestamp_seconds": 5.5},
      {"description": "Examines a glowing sun puzzle panel mounted on the wall.", "timestamp_seconds": 11.0},
      {"description": "Solves the floor dot puzzle by recreating a specific pattern, turning dots gold.", "timestamp_seconds": 20.0},
      {"description": "Collects a wooden ruler from the newly opened floor compartment.", "timestamp_seconds": 25.0},
      {"description": "Uses the ruler on the chalkboard to measure the sides of a drawn triangle.", "timestamp_seconds": 27.5},
      {"description": "Weighs a black ball on the red scale to determine its numerical value.", "timestamp_seconds": 59.0},
      {"description": "Enters the calculated 3-digit code into the desk drawer lock.", "timestamp_seconds": 104.5},
      {"description": "Retrieves the door key from the unlocked drawer.", "timestamp_seconds": 108.0}
    ],
    "puzzles": [
      {"puzzle_name": "Floor Dot Grid", "items_used": [], "solution_steps": ["Observe the pattern from the other wall grids.", "Press the corresponding metal dots on the floor panel until they turn gold to match the pattern."], "reward": "Wooden ruler", "timestamp_seconds": 20.0},
      {"puzzle_name": "Symbol Drawer", "items_used": [], "solution_steps": ["Find the correct sequence of four symbols (Magnet, Telescope, Lightbulb, Magnifying Glass).", "Input the symbols into the four square panels on the cabinet."], "reward": "Heavy black ball", "timestamp_seconds": 56.0},
      {"puzzle_name": "Math Code (X, Y, Z)", "items_used": ["Wooden ruler", "Heavy black ball"], "solution_steps": ["Use the ruler on the chalkboard to find the value of Y.", "Weigh the black ball on the scale to find the value of X.", "Calculate Z using the desk formula 'Z=Y-X'.", "Enter the resulting 3-digit combination into the drawer."], "reward": "Door key", "timestamp_seconds": 104.5}
    ],
    "final_action": "Uses the acquired key to unlock the main wooden door and escape the room."
  },
  {
    "level": 16,
    "room_description": "An elegant, well-lit study room containing a desk, a large vintage globe, a white sofa, decorative wall shelves, picture frames, and an attached bathroom.",
    "key_moments": [
      {"description": "Establishing shot of the elegant study room.", "timestamp_seconds": 0.0},
      {"description": "Inspects the cushions on the white sofa.", "timestamp_seconds": 1.0},
      {"description": "Finds and collects a metal pin/handle resting on a book on the desk.", "timestamp_seconds": 3.5},
      {"description": "Examines the decorative shelving unit on the wall.", "timestamp_seconds": 8.0},
      {"description": "Uses the metal pin to unlock the vintage globe.", "timestamp_seconds": 11.5},
      {"description": "Enters the attached bathroom and attaches the handle to a blank drawer.", "timestamp_seconds": 20.5},
      {"description": "Opens the bathroom drawer and collects a red towel and a spray bottle.", "timestamp_seconds": 26.0},
      {"description": "Sprays cleaning fluid on the dirty bathroom mirror and wipes it with the towel.", "timestamp_seconds": 28.5},
      {"description": "Reveals the hidden code '7649' written in red on the mirror.", "timestamp_seconds": 31.0},
      {"description": "Enters the mirrored code into the keypad on the dark wooden cabinet.", "timestamp_seconds": 35.0}
    ],
    "puzzles": [
      {"puzzle_name": "Globe Unlock", "items_used": ["Metal pin/handle"], "solution_steps": ["Locate the metal pin on the desk.", "Insert it into the slot on the vintage globe to pop it open."], "reward": "Glass lens/coin", "timestamp_seconds": 11.5},
      {"puzzle_name": "Dirty Mirror Code", "items_used": ["Metal drawer handle", "Spray bottle", "Red towel"], "solution_steps": ["Attach the handle to the bathroom drawer to access the cleaning supplies.", "Spray the clouded mirror with the bottle.", "Wipe the mirror clean with the red towel to reveal the hidden 4-digit code."], "reward": "Code '7649'", "timestamp_seconds": 28.5},
      {"puzzle_name": "Cabinet Keypad", "items_used": [], "solution_steps": ["Take the code '7649' found on the bathroom mirror.", "Type it into the electronic keypad on the main room's dark cabinet."], "reward": "Blue keycard", "timestamp_seconds": 35.0}
    ],
    "final_action": "Retrieves the blue keycard from the opened cabinet and swipes it to unlock the exit door."
  },
  {
    "level": 17,
    "room_description": "A storage pantry or break room equipped with wire shelves, a water dispenser, a red microwave over a mini-fridge, a computer desk, and wooden cabinets.",
    "key_moments": [
      {"description": "Establishing shot of the storage pantry room.", "timestamp_seconds": 0.0},
      {"description": "Inspects the computer desk, monitors, and mouse.", "timestamp_seconds": 2.0},
      {"description": "Opens the red microwave to check inside.", "timestamp_seconds": 7.0},
      {"description": "Finds a token resting on top of the wooden cabinet.", "timestamp_seconds": 13.0},
      {"description": "Opens the mini-fridge to find a row of red apples inside.", "timestamp_seconds": 18.0},
      {"description": "Places a block of butter into the microwave and melts it.", "timestamp_seconds": 21.0},
      {"description": "Collects a hidden token/coin from the melted butter.", "timestamp_seconds": 26.0},
      {"description": "Retrieves an electric kettle from the opened cabinet drawer.", "timestamp_seconds": 32.5},
      {"description": "Turns on the kettle to steam a blank piece of crumpled paper.", "timestamp_seconds": 46.0},
      {"description": "Enters the code '572' into the combination lock inside the mini-fridge.", "timestamp_seconds": 109.0}
    ],
    "puzzles": [
      {"puzzle_name": "Melted Butter", "items_used": ["Block of butter"], "solution_steps": ["Take the frozen block of butter.", "Place it inside the red microwave and turn it on to melt it away."], "reward": "Hidden token/coin", "timestamp_seconds": 21.0},
      {"puzzle_name": "Steaming the Paper", "items_used": ["Electric kettle", "Blank paper"], "solution_steps": ["Place the electric kettle on the counter and turn it on.", "Hold the blank piece of paper over the steam to reveal hidden ink symbols."], "reward": "Clue revealing a Mask, Apple, and Rose", "timestamp_seconds": 46.0},
      {"puzzle_name": "Fridge Drawer Lock", "items_used": [], "solution_steps": ["Count the corresponding items hidden around the room (Masks, Apples, Roses).", "Enter the final tallied combination (572) into the 3-digit lock on the fridge drawer."], "reward": "Door key", "timestamp_seconds": 109.0}
    ],
    "final_action": "Takes the key from the fridge compartment and uses it to unlock the main door."
  },
  {
    "level": 18,
    "room_description": "A classic dining room featuring a long table set with candles, a sofa, a green potted plant, a large birdcage holding a parrot, and a white sideboard cabinet.",
    "key_moments": [
      {"description": "Establishing shot of the classic dining room.", "timestamp_seconds": 0.0},
      {"description": "Inspects the decorative brown cushions on the sofa.", "timestamp_seconds": 1.5},
      {"description": "Finds a small key sitting inside a bowl on the white cabinet.", "timestamp_seconds": 11.0},
      {"description": "Uses the key to unlock the top drawer of the white cabinet.", "timestamp_seconds": 16.0},
      {"description": "Collects a loaf of bread resting on a plate on the dining table.", "timestamp_seconds": 19.5},
      {"description": "Holds a large green leaf over a lit candle on the dining table.", "timestamp_seconds": 30.0},
      {"description": "Reveals a hidden pattern of glowing green dashes on the leaf.", "timestamp_seconds": 35.0},
      {"description": "Enters the dash pattern into the lock at the bottom of the cabinet.", "timestamp_seconds": 38.0},
      {"description": "Completes a sliding jigsaw puzzle on a tablet found inside the drawer.", "timestamp_seconds": 41.0},
      {"description": "Enters the calculated code '835' into the padlock on the birdcage.", "timestamp_seconds": 118.0}
    ],
    "puzzles": [
      {"puzzle_name": "Leaf over Candle", "items_used": ["Green leaf"], "solution_steps": ["Collect the large green leaf from the potted plant.", "Hold the leaf over the heat of the lit candle on the dining table to reveal a dash pattern."], "reward": "Dash code for the cabinet lock", "timestamp_seconds": 30.0},
      {"puzzle_name": "Tablet Jigsaw & Item Count", "items_used": ["Tablet device"], "solution_steps": ["Solve the Roman ruins jigsaw puzzle on the tablet.", "The tablet then displays three items: a chair, a cushion, and a candle.", "Count these specific items in the room (8 chairs, 3 cushions, 5 candles) to form the code."], "reward": "Code '835'", "timestamp_seconds": 41.0},
      {"puzzle_name": "Birdcage Lock", "items_used": ["Bread"], "solution_steps": ["Enter the code '835' into the padlock to open the birdcage.", "Feed the bread to the parrot inside so it drops the key from its beak."], "reward": "Door key", "timestamp_seconds": 118.0}
    ],
    "final_action": "Collects the key dropped by the parrot and uses it to unlock the main door."
  },
  {
    "level": 19,
    "room_description": "A dimly lit room decorated with musical and historical items, including a piano, a suit of knight's armor, a mounted moose head, tribal masks, and a white cabinet.",
    "key_moments": [
      {"description": "Establishing shot of the music and armor room.", "timestamp_seconds": 0.0},
      {"description": "Inspects the piano, noting the red roses scattered on the keys.", "timestamp_seconds": 1.0},
      {"description": "Opens the white cabinet drawer and collects a pair of clippers.", "timestamp_seconds": 13.5},
      {"description": "Uses the clippers to cut the metal latch securing the knight's armor.", "timestamp_seconds": 20.0},
      {"description": "Discovers a crumpled piece of paper showing colored, overlapping numbers '2508'.", "timestamp_seconds": 36.0},
      {"description": "Enters the code '2508' into the 4-digit lock on the wooden box.", "timestamp_seconds": 40.0},
      {"description": "Opens the box to reveal a tablet requiring a swipe pattern.", "timestamp_seconds": 45.0},
      {"description": "Solves the colored floor pad puzzle, which likely reveals the swipe pattern.", "timestamp_seconds": 58.0},
      {"description": "Draws an hourglass/X swipe pattern on the tablet screen.", "timestamp_seconds": 108.0},
      {"description": "Retrieves the gold key from the opened chest plate of the knight armor.", "timestamp_seconds": 114.5}
    ],
    "puzzles": [
      {"puzzle_name": "Armor Latch", "items_used": ["Clippers"], "solution_steps": ["Find the clippers in the cabinet drawer.", "Use them to cut the metal lock keeping the knight's chest plate shut."], "reward": "Access to the inside of the armor", "timestamp_seconds": 20.0},
      {"puzzle_name": "Colored Numbers Box", "items_used": [], "solution_steps": ["Examine the crumpled paper clue to read the overlapping colored numbers (2508).", "Input the digits into the wooden box."], "reward": "Access to the tablet", "timestamp_seconds": 40.0},
      {"puzzle_name": "Tablet Swipe Pattern", "items_used": ["Tablet"], "solution_steps": ["Solve the colored circles on the floor to deduce the lock pattern.", "Swipe the corresponding hourglass/X shape on the tablet's 9-dot grid.", "View the X-ray on the tablet to confirm the key is inside the armor."], "reward": "Unlocks the armor compartment", "timestamp_seconds": 108.0}
    ],
    "final_action": "Takes the gold key found inside the knight's armor and uses it to unlock the exit door."
  },
  {
    "level": 20,
    "room_description": "A vibrant, futuristic robot or toy factory room filled with various robotic figures, colorful building blocks, digital monitors, and metal paneling.",
    "key_moments": [
      {"description": "Establishing shot of the colorful robot room.", "timestamp_seconds": 0.0},
      {"description": "Finds a green number '7' printed on the back of a black monitor.", "timestamp_seconds": 2.5},
      {"description": "Inspects a 3x3 circular grid on a white wall panel.", "timestamp_seconds": 4.5},
      {"description": "Finds a purple number '5' on the chest of a grey plush robot.", "timestamp_seconds": 21.0},
      {"description": "Presses 'play' on the central white monitor to start a sequence.", "timestamp_seconds": 25.5},
      {"description": "Watches the three TV-head robots perform a randomized color sequence.", "timestamp_seconds": 45.0},
      {"description": "Inputs the memorized color sequence into the 3x3 wall grid.", "timestamp_seconds": 103.0},
      {"description": "Collects a metal crowbar from the opened wall panel.", "timestamp_seconds": 131.0},
      {"description": "Uses the crowbar to pry off a metal plate on the wall, revealing a keypad.", "timestamp_seconds": 134.0},
      {"description": "Enters the numerical code '953' into the robot keypad.", "timestamp_seconds": 155.0}
    ],
    "puzzles": [
      {"puzzle_name": "Robot Emotion Match", "items_used": [], "solution_steps": ["Press play on the monitor and observe the sequence of face emojis.", "Change the faces on the row of red robots to match the monitor's sequence."], "reward": "Triggers the TV robots sequence", "timestamp_seconds": 37.0},
      {"puzzle_name": "TV Colors Grid", "items_used": [], "solution_steps": ["Watch the three TV-head robots flash different colors.", "Go to the 3x3 wall panel and input the corresponding colors in the correct order."], "reward": "Metal crowbar", "timestamp_seconds": 103.0},
      {"puzzle_name": "Hidden Numbers Keypad", "items_used": ["Metal crowbar"], "solution_steps": ["Pry off the metal plate using the crowbar.", "Find the hidden numbers associated with three specific robots around the room (White/Grey = 9, Blue = 5, Red = 3).", "Enter the code '953' into the keypad."], "reward": "Unlocks the main door", "timestamp_seconds": 150.0}
    ],
    "final_action": "Entering the final correct code into the wall keypad automatically unlocks the main door, allowing escape."
  }
]

video_mapping = {
    15: r"Videos\Escape Game 50 Rooms 1\15 - Escape Game 50 Rooms 1 ｜ Level 15.f271.webm",
    16: r"Videos\Escape Game 50 Rooms 1\16 - Escape Game 50 Rooms 1 I Level 16.f271.webm",
    17: r"Videos\Escape Game 50 Rooms 1\17 - Escape Game 50 Rooms 1 I Level 17.f271.webm",
    18: r"Videos\Escape Game 50 Rooms 1\18 - Escape Game 50 Rooms 1 I Level 18.f271.webm",
    19: r"Videos\Escape Game 50 Rooms 1\19 - Escape Game 50 Rooms 1 I Level 19.f271.webm",
    20: r"Videos\Escape Game 50 Rooms 1\20 - Escape game 50 rooms 1 ｜ Level 20.f271.webm"
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
