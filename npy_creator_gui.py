
"""
NPY Creator GUI - Tkinter-based interface for recreating all npy files
used by thesystem.system.load_or_cache_images function and video files

This script provides a beautiful GUI interface that matches the aesthetic
style of the update.py file and starts automatically.
"""

import os
import sys
import numpy as np
from PIL import Image, ImageTk
import time
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import queue
import cv2

class NPYCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NPY Creator")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#f0f0f0"
        self.accent_color = "#0078d4"
        self.success_color = "#107c10"
        self.warning_color = "#d83b01"
        self.error_color = "#d13438"
        
        self.root.configure(bg=self.bg_color)
        
        # Message queue for thread communication
        self.message_queue = queue.Queue()
        
        # Processing state
        self.is_processing = False
        self.current_config = 0
        self.total_configs = 0
        
        self.setup_ui()
        self.setup_configurations()
        self.update_ui()
        
        # Auto-start the process
        self.root.after(1000, self.auto_start_processing)
    
    def setup_ui(self):
        """Setup the user interface components."""
        # Main canvas
        self.canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)
        
        # Title
        title_label = tk.Label(
            self.canvas, 
            text="NPY Creator", 
            font=("Segoe UI", 20, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.place(relx=0.5, rely=0.08, anchor="center")
        
        # Subtitle
        subtitle_label = tk.Label(
            self.canvas,
            text="Recreating cached image files and video files for thesystem",
            font=("Segoe UI", 10),
            fg="#666666",
            bg=self.bg_color
        )
        subtitle_label.place(relx=0.5, rely=0.15, anchor="center")
        
        # Status frame
        status_frame = tk.Frame(self.canvas, bg=self.bg_color)
        status_frame.place(relx=0.5, rely=0.28, anchor="center", relwidth=0.8)
        
        # Status label
        self.status_label = tk.Label(
            status_frame,
            text="Starting NPY creation process...",
            font=("Segoe UI", 11),
            fg="#333333",
            bg=self.bg_color,
            wraplength=450
        )
        self.status_label.pack(pady=(0, 10))
        
        # Progress frame
        progress_frame = tk.Frame(self.canvas, bg=self.bg_color)
        progress_frame.place(relx=0.5, rely=0.42, anchor="center", relwidth=0.8)
        
        # Overall progress
        overall_label = tk.Label(
            progress_frame,
            text="Overall Progress:",
            font=("Segoe UI", 10, "bold"),
            fg="#333333",
            bg=self.bg_color
        )
        overall_label.pack(anchor="w", pady=(0, 5))
        
        self.overall_progress = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            mode="determinate",
            length=450
        )
        self.overall_progress.pack(fill="x", pady=(0, 15))
        
        # Current item progress
        current_label = tk.Label(
            progress_frame,
            text="Current Item:",
            font=("Segoe UI", 10, "bold"),
            fg="#333333",
            bg=self.bg_color
        )
        current_label.pack(anchor="w", pady=(0, 5))
        
        self.current_progress = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            mode="determinate",
            length=450
        )
        self.current_progress.pack(fill="x", pady=(0, 15))
        
        # Progress text
        self.progress_text = tk.Label(
            progress_frame,
            text="0 / 0 configurations",
            font=("Segoe UI", 9),
            fg="#666666",
            bg=self.bg_color
        )
        self.progress_text.pack()
        
        # Log frame
        log_frame = tk.Frame(self.canvas, bg=self.bg_color)
        log_frame.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.8)
        
        # Log label
        log_label = tk.Label(
            log_frame,
            text="Log:",
            font=("Segoe UI", 10, "bold"),
            fg="#333333",
            bg=self.bg_color
        )
        log_label.pack(anchor="w", pady=(0, 5))
        
        # Log text widget
        self.log_text = tk.Text(
            log_frame,
            height=4,
            width=60,
            font=("Consolas", 8),
            bg="#f8f8f8",
            fg="#333333",
            relief="solid",
            borderwidth=1
        )
        self.log_text.pack(fill="x")
        
        # Scrollbar for log
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
    
    def auto_start_processing(self):
        """Automatically start the NPY creation process."""
        self.start_processing()
    
    def setup_configurations(self):
        """Setup all the configurations to process."""
        # Image configurations
        self.image_configurations = [
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

            ("thesystem/bottom_bar", (609, 33), "NONE", "bottom"),
            ("thesystem/alt_bottom_bar", (609, 33), "JOB", "bottom"),

            ("thesystem/bottom_bar", (1053, 43), "NONE", "bottom"),
            ("thesystem/alt_bottom_bar", (1053, 43), "JOB", "bottom"),
            
            # Special configurations
            ("thesystem/top_bar", (332, 30), "NONE", "top"),
            ("thesystem/bottom_bar", (322, 25), "NONE", "bottom"),
            ("thesystem/alt_top_bar", (332, 30), "JOB", "top"),
            ("thesystem/alt_bottom_bar", (322, 25), "JOB", "bottom"),
        ]
        
        # Video configurations
        self.video_configurations = [
            ("Files/Mod/default/Anime/alt1.mp4", "Files/Mod/default/Anime/alt1.npy", 1, False),
            ("Files/Mod/default/Anime/0001-0200.mp4", "Files/Mod/default/Anime/default.npy", 1, False),
            ("Files/Mod/default/Manwha/0001-1000.mp4", "Files/Mod/default/Manwha/0001-1000.npy", 1, False),
        ]
        
        # Combine all configurations
        self.configurations = self.image_configurations + self.video_configurations
        self.total_configs = len(self.configurations)
        self.overall_progress["maximum"] = self.total_configs
        self.progress_text.config(text=f"0 / {self.total_configs} configurations")
    
    def video_to_npy(self, video_path, output_path, resize_factor=None, rotate=False):
        """Convert video to NPY format."""
        if not os.path.exists(video_path):
            self.log_message(f"❌ Video file not found: {video_path}", "ERROR")
            return False
        
        try:
            cap = cv2.VideoCapture(video_path)
            frames = []
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            processed_frames = 0
            
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
                processed_frames += 1
                
                # Update progress
                progress = (processed_frames / total_frames) * 100
                self.message_queue.put(("update_current", progress))

            cap.release()

            if frames:
                frames_array = np.array(frames)
                np.save(output_path, frames_array)
                self.log_message(f"✅ Saved {len(frames)} video frames to {output_path}", "SUCCESS")
                return True
            else:
                self.log_message(f"❌ No frames extracted from video: {video_path}", "ERROR")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Error processing video {video_path}: {str(e)}", "ERROR")
            return False
    
    def log_message(self, message, level="INFO"):
        """Add a message to the log with timestamp and level."""
        timestamp = time.strftime("%H:%M:%S")
        level_colors = {
            "INFO": "#333333",
            "SUCCESS": self.success_color,
            "WARNING": self.warning_color,
            "ERROR": self.error_color
        }
        
        color = level_colors.get(level, "#333333")
        
        # Add to log text widget
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        
        # Limit log size
        if int(self.log_text.index("end-1c").split('.')[0]) > 50:
            self.log_text.delete("1.0", "2.0")
    
    def start_processing(self):
        """Start the NPY creation process in a separate thread."""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.current_config = 0
        self.overall_progress["value"] = 0
        self.current_progress["value"] = 0
        
        # Clear log
        self.log_text.delete("1.0", "end")
        
        # Start processing thread
        processing_thread = threading.Thread(target=self.process_configurations, daemon=True)
        processing_thread.start()
    
    def process_configurations(self):
        """Process all configurations in a separate thread."""
        successful = 0
        failed = 0
        
        self.log_message("Starting NPY creation process...", "INFO")
        self.log_message(f"Found {self.total_configs} configurations to process", "INFO")
        self.log_message(f"- {len(self.image_configurations)} image configurations", "INFO")
        self.log_message(f"- {len(self.video_configurations)} video configurations", "INFO")
        
        start_time = time.time()
        
        for i, config in enumerate(self.configurations, 1):
            if not self.is_processing:  # Check if cancelled
                break
                
            self.current_config = i
            self.message_queue.put(("update_overall", i))
            
            # Determine if this is an image or video configuration
            if len(config) == 4 and isinstance(config[0], str) and config[0].endswith('.mp4'):
                # Video configuration
                video_path, output_path, resize_factor, rotate = config
                self.message_queue.put(("update_progress", i, f"Video: {os.path.basename(video_path)}", "VIDEO", "PROCESSING"))
                
                success = self.video_to_npy(video_path, output_path, resize_factor, rotate)
                
            else:
                # Image configuration
                folder_path, resize, job, type_ = config
                self.message_queue.put(("update_progress", i, f"Images: {folder_path} ({resize[0]}x{resize[1]}) - {job} {type_}", "IMAGES", "PROCESSING"))
                
                # Convert relative path to absolute
                current_dir = os.path.dirname(os.path.abspath(__file__))
                abs_folder_path = os.path.join(current_dir, folder_path)
                
                # Process this configuration
                success = self.create_npy_for_config(abs_folder_path, resize, job, type_)
            
            if success:
                successful += 1
            else:
                failed += 1
            
            # Update progress
            self.message_queue.put(("update_overall", i))
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Final status
        if failed > 0:
            self.log_message(f"⚠️ Process completed with {failed} failures. Check the log above.", "WARNING")
        else:
            self.log_message(f"🎉 All {successful} NPY files created successfully!", "SUCCESS")
        
        self.log_message(f"Total processing time: {total_time:.2f} seconds", "INFO")
        
        # Reset UI
        self.message_queue.put(("finish_processing", successful, failed))
    
    def create_npy_for_config(self, folder_path, resize, job, type_):
        """Create NPY file for a specific configuration."""
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
            return False
        
        # Create npy file
        return self.images_to_npy_with_mode(folder_path, cache_path, resize=resize)
    
    def images_to_npy_with_mode(self, folder_path, output_path, resize=None, sort=True):
        """Convert images in a folder to npy format with mode information."""
        if not os.path.exists(folder_path):
            return False
        
        files = [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        if not files:
            return False
        
        if sort:
            files.sort()
        
        data_to_save = []
        total_files = len(files)
        
        for i, filename in enumerate(files):
            if not self.is_processing:  # Check if cancelled
                break
                
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
                
                # Update current progress
                current_progress = (i + 1) / total_files * 100
                self.message_queue.put(("update_current", current_progress))
                
            except Exception as e:
                continue
        
        if data_to_save and self.is_processing:
            try:
                np.save(output_path, np.array(data_to_save, dtype=object), allow_pickle=True)
                return True
            except Exception as e:
                return False
        
        return False
    
    def update_ui(self):
        """Update the UI based on messages from the processing thread."""
        try:
            while True:
                message_type, *args = self.message_queue.get_nowait()
                
                if message_type == "update_progress":
                    i, description, config_type, status = args
                    self.status_label.config(
                        text=f"Processing: {description}"
                    )
                    self.progress_text.config(text=f"{i} / {self.total_configs} configurations")
                
                elif message_type == "update_overall":
                    i = args[0]
                    self.overall_progress["value"] = i
                
                elif message_type == "update_current":
                    progress = args[0]
                    self.current_progress["value"] = progress
                
                elif message_type == "finish_processing":
                    successful, failed = args
                    self.is_processing = False
                    
                    if failed > 0:
                        self.status_label.config(
                            text=f"Completed with {failed} failures. Check the log below.",
                            fg=self.warning_color
                        )
                    else:
                        self.status_label.config(
                            text=f"Successfully created {successful} NPY files!",
                            fg=self.success_color
                        )
                        os.remove("thesystem/temp 7x2.txt")
                    
                    # Auto-close after 5 seconds if successful
                    if failed == 0:
                        self.root.after(5000, self.root.destroy)
                    else:
                        # Keep open longer if there were failures so user can see the log
                        self.root.after(10000, self.root.destroy)
        
        except queue.Empty:
            pass
        
        # Schedule next update
        self.root.after(100, self.update_ui)

def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = NPYCreatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
