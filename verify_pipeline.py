import os
import json
import cv2

def verify_pipeline():
    with open("level1_analysis.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        
    video_path = "Videos\\Escape Game 50 Rooms 1\\01 - Escape game 50 rooms 1 - Puzzle Game - Level 1.f271.webm"
    
    # Determine level and output directories
    level = data.get("level", "unknown")
    level_dir = os.path.join("Output", f"Level_{level}")
    screenshots_dir = os.path.join(level_dir, "Screenshots")
    
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    def extract_frame(item_name, timestamp):
        if timestamp is not None:
            frame_idx = int(float(timestamp) * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if ret:
                item_name_clean = "".join([c if c.isalnum() else "_" for c in item_name])
                img_filename = f"{float(timestamp):05.1f}s_{item_name_clean}.jpg"
                output_path = os.path.join(screenshots_dir, img_filename)
                cv2.imwrite(output_path, frame)
                print(f"Saved screenshot for '{item_name}' at {timestamp}s -> {output_path}")
                # Return relative path for the JSON
                return f"Screenshots/{img_filename}"
            else:
                print(f"Failed to read frame at {timestamp}s")
        return None

    # Process puzzles
    for i, puzzle in enumerate(data.get("puzzles", [])):
        path = extract_frame(puzzle.get("puzzle_name", f"puzzle_{i}"), puzzle.get("timestamp_seconds"))
        if path:
            puzzle["screenshot_path"] = path
        
    # Process key moments
    for i, moment in enumerate(data.get("key_moments", [])):
        path = extract_frame(moment.get("description", f"moment_{i}"), moment.get("timestamp_seconds"))
        if path:
            moment["screenshot_path"] = path

    cap.release()
    
    # Save enriched JSON
    json_output_path = os.path.join(level_dir, "analysis.json")
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved enriched JSON to {json_output_path}")

if __name__ == "__main__":
    verify_pipeline()
