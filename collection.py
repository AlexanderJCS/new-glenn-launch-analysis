import os
import time

import cv2
import numpy as np
import pytesseract
from datetime import timedelta
from multiprocessing import Pool, cpu_count
import pickle

from tqdm import tqdm

import download


def img_to_digits(img):
    config = "--oem 3 --psm 7"
    text = pytesseract.image_to_string(img, lang="eng", config=config)
    text = text.strip().replace(",", "")
    try:
        return float(text)
    except ValueError:
        return np.nan


def process_telemetry(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # crop the ROIs
    s1v = gray[325:344,  78:135]
    s1a = gray[325:344, 186:242]
    s2v = gray[325:344, 411:468]
    s2a = gray[325:344, 514:571]

    stage1_vel = img_to_digits(s1v)
    stage1_alt = img_to_digits(s1a)
    stage2_vel = img_to_digits(s2v)
    if stage2_vel == 0:
        stage2_vel, stage2_alt = stage1_vel, stage1_alt
    else:
        stage2_alt = img_to_digits(s2a)

    return stage1_vel, stage1_alt, stage2_vel, stage2_alt


def to_meters(val, miles: bool):
    return (val * 1609.344 if miles  # miles -> meters
            else val * 0.3048)  # feet -> meters


def _worker(args):
    """Unpack a single task: (frame_idx, frame, fps, total_frames)."""
    start = time.time()
    
    frame_idx, frame, fps, total = args
    ts = timedelta(seconds=frame_idx / fps)
    s1v, s1a, s2v, s2a = process_telemetry(frame)
    
    s1v *= 0.44704  # mph -> m/s
    s2v *= 0.44704  # mph -> m/s
    s1a = to_meters(s1a, s1v > 1000 and s1a < 1000)
    s2a = to_meters(s2a, s2v > 1000 and s2a < 1000)
    
    result = {
        "frame": frame_idx,
        "time": str(ts),
        "stage1_vel": s1v,
        "stage1_alt": s1a,
        "stage2_vel": s2v,
        "stage2_alt": s2a
    }
    
    return result


def analyze_video_parallel(video_path):
    # sourcery skip: for-append-to-extend, simplify-generator
    # 1) Read all frames into memory
    print("Loading frames into memory")
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    frame_idx = -1
    while True:
        frame_idx += 1
        
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_idx % 4 != 0:
            continue
        
        frames.append((frame_idx, frame))
    cap.release()
    
    # 2) Build argument list
    print("Building argument list")
    tasks = [(frame_idx, frame, fps, len(frames)) for frame_idx, frame in frames]

    # 3) Spawn a pool of workers
    print("Spawning workers")
    results = []
    with Pool(cpu_count()) as pool:
        results.extend(tqdm(
            pool.imap_unordered(_worker, tasks, chunksize=20),
            total=len(frames),
            desc="OCR frames",
            unit="frame",
        ))

    results.sort(key=lambda x: x["frame"])

    return results


def main():
    video_file = "new_glenn_clipped.mp4"
    if not os.path.isfile(video_file):
        print("Video not found; Downloading video")
        download.download()

    ocr_data = analyze_video_parallel(video_file)

    with open("rocket_data.pickle", "wb") as f:
        pickle.dump(ocr_data, f)


if __name__ == "__main__":
    main()
