#!/usr/bin/env python3
"""
NPY Creator - Recreates all npy files used by thesystem.system.load_or_cache_images function
and video files

This script analyzes all the places where load_or_cache_images is called and recreates
the corresponding npy files with the correct dimensions and job types, plus processes video files.
"""

import os
import sys
import numpy as np
from PIL import Image
from pathlib import Path
import time
import cv2

def video_to_npy(video_path, output_path, resize_factor=None, rotate=False):
    """
    Convert video to NPY format.
    
    Args:
        video_path: Path to input video file
        output_path: Path where npy file should be saved
        resize_factor: Factor to resize frames (None for no resize)
        rotate: Whether to rotate frames 90 degrees clockwise
    """
    if not os.path.exists(video_path):
        print(f"[ERROR] Video file not found: {video_path}")
        return False
    
    try:
        cap = cv2.VideoCapture(video_path)
        frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"[INFO] Processing video: {video_path} ({total_frames} frames)")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if rotate:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            if resize_factor and resize_factor != 1:
                h, w = frame.shape[:2]
                new_w = int(w * resize_factor)
                new_h = int(h * resize_factor)
                frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

            frames.append(frame)

        cap.release()

        if frames:
            frames_array = np.array(frames)
            np.save(output_path, frames_array)
            print(f"[SUCCESS] Saved {len(frames)} video frames → {output_path}")
            return True
        else:
            print(f"[ERROR] No frames extracted from video: {video_path}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Failed to process video {video_path}: {e}")
        return False

def images_to_npy_with_mode(folder_path, output_path, resize=None, sort=True):
    """
    Convert images in a folder to npy format with mode information.
    
    Args:
        folder_path: Path to folder containing images
        output_path: Path where npy file should be saved
        resize: Tuple of (width, height) to resize images
        sort: Whether to sort files alphabetically
    """
    if not os.path.exists(folder_path):
        print(f"[ERROR] Folder not found: {folder_path}")
        return False
    
    files = [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not files:
        print(f"[WARNING] No image files found in: {folder_path}")
        return False
    
    if sort:
        files.sort()
    
    data_to_save = []
    
    print(f"[INFO] Processing {len(files)} images from {folder_path}")
    
    for filename in files:
        path = os.path.join(folder_path, filename)
        if not os.path.exists(path):
            continue
            
        try:
            img = Image.open(path)
            mode = img.mode
            img = img.convert("RGBA")
            
            if resize:
                img = img.resize(resize, Image.Resampling.LANCZOS)
            
            data_to_save.append((np.array(img), mode))
        except Exception as e:
            print(f"[ERROR] Failed to process {filename}: {e}")
            continue
    
    if data_to_save:
        try:
            np.save(output_path, np.array(data_to_save, dtype=object), allow_pickle=True)
            print(f"[SUCCESS] Saved {len(data_to_save)} images → {output_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save {output_path}: {e}")
            return False
    else:
        print(f"[ERROR] No valid images processed from {folder_path}")
        return False

def create_npy_for_config(folder_path, resize, job, type_):
    """
    Create npy file for a specific configuration.
    
    Args:
        folder_path: Base path to image folder
        resize: Tuple of (width, height)
        job: Job type ("NONE" or other)
        type_: Type of bar ("top" or "bottom")
    """
    width, height = resize
    job_upper = job.upper()
    type_lower = type_.lower()
    
    # Build cache filename (same logic as load_or_cache_images)
    if job_upper == "NONE":
        cache_name = f"{type_lower}_frame_stack {width} {height}.npy"
    else:
        cache_name = f"alt_{type_lower}_frame_stack {width} {height}.npy"
    
    cache_path = os.path.join(folder_path, cache_name)
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"[ERROR] Image folder not found: {folder_path}")
        return False
    
    # Create npy file
    return images_to_npy_with_mode(folder_path, cache_path, resize=resize)

def main():
    """Main function to recreate all npy files."""
    print("=" * 60)
    print("NPY Creator - Recreating all cached image and video files")
    print("=" * 60)
    
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = current_dir
    
    # Define all the configurations found in the codebase
    # Format: (folder_path, resize, job, type_) for images
    image_configurations = [
        # Anime Version configurations
        ("thesystem/top_bar", (400, 19), "NONE", "top"),
        ("thesystem/bottom_bar", (400, 16), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (400, 19), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (400, 16), "JOB", "bottom"),
        
        ("thesystem/top_bar", (488, 38), "NONE", "top"),
        ("thesystem/bottom_bar", (488, 33), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (488, 38), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (488, 33), "JOB", "bottom"),
        
        ("thesystem/top_bar", (490, 34), "NONE", "top"),
        ("thesystem/bottom_bar", (490, 34), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (490, 34), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (490, 34), "JOB", "bottom"),
        
        ("thesystem/top_bar", (550, 38), "NONE", "top"),
        ("thesystem/bottom_bar", (550, 33), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (550, 38), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (550, 33), "JOB", "bottom"),
        
        ("thesystem/top_bar", (580, 38), "NONE", "top"),
        ("thesystem/bottom_bar", (580, 33), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (580, 38), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (580, 33), "JOB", "bottom"),
        
        ("thesystem/top_bar", (587, 19), "NONE", "top"),
        ("thesystem/bottom_bar", (587, 16), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (587, 19), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (587, 16), "JOB", "bottom"),
        
        ("thesystem/top_bar", (609, 33), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (609, 33), "JOB", "bottom"),
        
        ("thesystem/top_bar", (695, 39), "NONE", "top"),
        ("thesystem/bottom_bar", (702, 36), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (695, 39), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (702, 36), "JOB", "bottom"),
        
        ("thesystem/top_bar", (715, 41), "NONE", "top"),
        ("thesystem/bottom_bar", (715, 41), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (715, 41), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (715, 41), "JOB", "bottom"),
        
        ("thesystem/top_bar", (727, 38), "NONE", "top"),
        ("thesystem/bottom_bar", (737, 27), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (727, 38), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (737, 27), "JOB", "bottom"),
        
        ("thesystem/top_bar", (748, 39), "NONE", "top"),
        ("thesystem/bottom_bar", (763, 36), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (748, 39), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (763, 36), "JOB", "bottom"),
        
        ("thesystem/top_bar", (840, 47), "NONE", "top"),
        ("thesystem/bottom_bar", (723, 47), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (840, 47), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (723, 47), "JOB", "bottom"),
        
        ("thesystem/top_bar", (957, 43), "NONE", "top"),
        ("thesystem/bottom_bar", (1026, 47), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (957, 43), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (1026, 47), "JOB", "bottom"),
        
        ("thesystem/top_bar", (970, 40), "NONE", "top"),
        ("thesystem/bottom_bar", (970, 40), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (970, 40), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (970, 40), "JOB", "bottom"),
        
        ("thesystem/top_bar", (974, 47), "NONE", "top"),
        ("thesystem/bottom_bar", (983, 52), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (974, 47), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (983, 52), "JOB", "bottom"),
        
        ("thesystem/top_bar", (1053, 43), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (1053, 43), "JOB", "bottom"),
        
        ("thesystem/top_bar", (1120, 47), "NONE", "top"),
        ("thesystem/alt_top_bar", (1120, 47), "JOB", "top"),
        
        ("thesystem/top_bar", (1229, 47), "NONE", "top"),
        ("thesystem/bottom_bar", (1229, 47), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (1229, 47), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (1229, 47), "JOB", "bottom"),
        
        # Special configurations
        ("thesystem/top_bar", (332, 30), "NONE", "top"),
        ("thesystem/bottom_bar", (322, 25), "NONE", "bottom"),
        ("thesystem/alt_top_bar", (332, 30), "JOB", "top"),
        ("thesystem/alt_bottom_bar", (322, 25), "JOB", "bottom"),
    ]
    
    # Video configurations
    # Format: (video_path, output_path, resize_factor, rotate)
    video_configurations = [
        ("Files/Mod/default/Anime/alt1.mp4", "Files/Mod/default/Anime/alt1.npy", 1, False),
        ("Files/Mod/default/Anime/0001-0200.mp4", "Files/Mod/default/Anime/default.npy", 1, False),
        ("Files/Mod/default/Manwha/0001-1000.mp4", "Files/Mod/default/Manwha/0001-1000.npy", 1, False),
    ]
    
    # Combine all configurations
    total_image_configs = len(image_configurations)
    total_video_configs = len(video_configurations)
    total_configs = total_image_configs + total_video_configs
    
    print(f"Found {total_configs} configurations to process:")
    print(f"- {total_image_configs} image configurations")
    print(f"- {total_video_configs} video configurations")
    print()
    
    successful = 0
    failed = 0
    
    start_time = time.time()
    
    # Process image configurations
    print("=" * 40)
    print("PROCESSING IMAGE CONFIGURATIONS")
    print("=" * 40)
    
    for i, (folder_path, resize, job, type_) in enumerate(image_configurations, 1):
        print(f"[{i:3d}/{total_image_configs}] Processing: {folder_path} ({resize[0]}x{resize[1]}) - {job} {type_}")
        
        # Convert relative path to absolute
        abs_folder_path = os.path.join(project_root, folder_path)
        
        if create_npy_for_config(abs_folder_path, resize, job, type_):
            successful += 1
        else:
            failed += 1
        
        print()
    
    # Process video configurations
    print("=" * 40)
    print("PROCESSING VIDEO CONFIGURATIONS")
    print("=" * 40)
    
    for i, (video_path, output_path, resize_factor, rotate) in enumerate(video_configurations, 1):
        print(f"[{i:3d}/{total_video_configs}] Processing video: {video_path}")
        
        if video_to_npy(video_path, output_path, resize_factor, rotate):
            successful += 1
        else:
            failed += 1
        
        print()
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print("=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total configurations: {total_configs}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_time:.2f} seconds")
    
    if failed > 0:
        print(f"\n[WARNING] {failed} configurations failed. Check the error messages above.")
        return 1
    else:
        print(f"\n[SUCCESS] All {successful} NPY files created successfully!")
        return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[INFO] Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1) 