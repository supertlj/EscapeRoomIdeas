import cv2
import os
import sys

def extract_key_screenshots(video_path, output_dir, num_screenshots=4):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video stream or file: {video_path}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    print(f"Video duration: {duration:.2f} seconds. Total frames: {total_frames}")

    # Calculate frame indices to extract
    frame_indices = [int(total_frames * (i + 1) / (num_screenshots + 1)) for i in range(num_screenshots)]

    for i, frame_idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret:
            # Save the frame as an image
            output_path = os.path.join(output_dir, f"screenshot_{i+1}.jpg")
            cv2.imwrite(output_path, frame)
            print(f"Saved screenshot {i+1} to {output_path}")
        else:
            print(f"Error reading frame {frame_idx}")

    cap.release()
    print("Done extracting screenshots.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_screenshots.py <video_path>")
        sys.exit(1)
        
    video_path = sys.argv[1]
    output_dir = "Screenshots"
    extract_key_screenshots(video_path, output_dir)
