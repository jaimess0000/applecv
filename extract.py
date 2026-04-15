import cv2
import os
import argparse

parser = argparse.ArgumentParser(description="Extract frames from a video for scroll animations.")
parser.add_argument('--video', type=str, default='Camera_Moves_Inside_Apple_Store.mp4', help='Path to video file')
parser.add_argument('--width', type=int, default=None, help='Target width to resize frames. Defaults to maintaining original video width.')
parser.add_argument('--quality', type=int, default=65, help='JPEG quality index (0-100). Default is 65.')
args = parser.parse_args()

video_path = args.video
output_folder = 'frames'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error opening video stream or file: {video_path}")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Original Video: {orig_w}x{orig_h} at {fps} fps, Total Frames: {frame_count}")

# Apple usually uses around 150-300 frames to keep the total download size reasonable.
target_frames = 250
skip = max(1, frame_count // target_frames)

count = 0
extracted = 0

print(f"Extracting roughly 1 frame every {skip} frames...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if count % skip == 0:
        h, w = frame.shape[:2]
        
        # Determine target width
        new_w = args.width if args.width else w
        new_h = int(h * (new_w / w))
        
        if new_w != w:
            # Use INTER_AREA for shrinking, INTER_CUBIC for enlarging
            interpolation = cv2.INTER_AREA if new_w < w else cv2.INTER_CUBIC
            resized = cv2.resize(frame, (new_w, new_h), interpolation=interpolation)
        else:
            resized = frame
            
        frame_name = os.path.join(output_folder, f"frame_{extracted:04d}.jpg")
        cv2.imwrite(frame_name, resized, [int(cv2.IMWRITE_JPEG_QUALITY), args.quality])
        extracted += 1
        
    count += 1

cap.release()
print(f"Successfully extracted {extracted} frames to {output_folder}")
