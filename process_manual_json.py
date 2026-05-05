import os
import sys
import json
import cv2

def process_manual(json_path, video_path):
    print(f"Loading JSON from: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    level = data.get("level", "unknown")
    level_dir = os.path.join("Output", f"Level_{level}")
    screenshots_dir = os.path.join(level_dir, "Screenshots")
    
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
        print(f"Created directory: {screenshots_dir}")

    print(f"Opening video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video FPS: {fps}")

    # Cache to avoid duplicate screenshots for the same timestamp
    timestamp_cache = {}

    def extract_frame(item_name, timestamp):
        if timestamp is None:
            return None
            
        ts_float = float(timestamp)
        if ts_float in timestamp_cache:
            print(f"Using cached screenshot for '{item_name}' at {timestamp}s")
            return timestamp_cache[ts_float]

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_idx = int(ts_float * fps)
        
        # Clamp frame_idx to stay within valid range
        if frame_idx >= total_frames:
            frame_idx = total_frames - 1
            print(f"Clamping timestamp {timestamp}s to last frame ({frame_idx})")
            
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret:
            # Only allow ASCII alphanumeric characters in the filename
            item_name_clean = "".join([c if (ord(c) < 128 and c.isalnum()) else "_" for c in item_name])
            img_filename = f"{ts_float:05.1f}s_{item_name_clean}.jpg"
            output_path = os.path.join(screenshots_dir, img_filename)
            cv2.imwrite(output_path, frame)
            print(f"Saved screenshot: {img_filename}")
            
            # Store relative path in cache
            rel_path = f"Screenshots/{img_filename}"
            timestamp_cache[ts_float] = rel_path
            return rel_path
        else:
            print(f"Warning: Failed to read frame at {timestamp}s")
        return None

    print("\nProcessing puzzles...")
    for i, puzzle in enumerate(data.get("puzzles", [])):
        path = extract_frame(puzzle.get("puzzle_name", f"puzzle_{i}"), puzzle.get("timestamp_seconds"))
        if path:
            puzzle["screenshot_path"] = path
            
    print("\nProcessing key moments...")
    for i, moment in enumerate(data.get("key_moments", [])):
        path = extract_frame(moment.get("description", f"moment_{i}"), moment.get("timestamp_seconds"))
        if path:
            moment["screenshot_path"] = path

    cap.release()
    
    output_json = os.path.join(level_dir, "analysis.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"\nDone! Enriched JSON saved to: {output_json}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python process_manual_json.py <json_file> <video_file>")
    else:
        process_manual(sys.argv[1], sys.argv[2])
