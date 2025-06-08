import tkinter as tk
from tkinter import Tk, Frame, Label, Button, Canvas, PhotoImage
from PIL import Image, ImageTk
import json
import random
import os
import ujson
import sys
from pathlib import Path
import threading
import subprocess
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

import thesystem.dungeon
import thesystem.system
import thesystem.misc

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Create a Tabs.json entry for Shadow Summon
try:
    with open("Files/Player Data/Tabs.json", 'r') as tab_son:
        tab_son_data = ujson.load(tab_son)

    with open("Files/Player Data/Tabs.json", 'w') as fin_tab_son:
        tab_son_data["ShadowSummon"] = 'Open'
        ujson.dump(tab_son_data, fin_tab_son, indent=4)
except Exception as e:
    print(f"Error updating Tabs.json: {e}")

window = None
stop_event = threading.Event()
initial_height = 0
target_height = 369
window_width = 879

class ShadowSummonSystem:
    def __init__(self):
        global window, stop_event
        
        # Try to load boss data from temp file
        self.boss_name = "Unknown Shadow"
        self.boss_data = {"type": "Normal", "attribute": "STR"}
        self.rank = "E"
        
        try:
            if os.path.exists("Files/Temp Files/boss_data.json"):
                with open("Files/Temp Files/boss_data.json", "r") as f:
                    boss_data = json.load(f)
                    self.boss_name = boss_data.get("boss_name", "Unknown Boss")
                    self.boss_data = boss_data.get("boss_data", {"type": "Normal", "attribute": "STR"})
                    self.rank = boss_data.get("rank", "E")
        except Exception as e:
            print(f"Error loading boss data: {e}")
        
        # Setup window
        window = Tk()
        window.geometry(f"{window_width}x{initial_height}")
        
        # Get job type for theming
        self.job = thesystem.misc.return_status()["status"][1]["job"]
        self.transp_clr = '#0C679B' if self.job == 'None' else '#652AA3'
        
        # Configure window
        thesystem.system.make_window_transparent(window, self.transp_clr)
        
        # Load settings
        with open("Files/Player Data/Settings.json", 'r') as settings_open:
            self.setting_data = ujson.load(settings_open)
                
        # Setup window properties
        window.configure(bg="#FFFFFF")
        window.attributes('-alpha', 0.8)
        window.overrideredirect(True)
        window.wm_attributes("-topmost", True)
        
        # Animate window opening
        thesystem.system.animate_window_open(window, target_height, window_width, step=40, delay=1)
        
        # Setup animated top and bottom bars
        self.setup_animations()
        
        # Create main canvas
        self.canvas = Canvas(
            window,
            bg="#FFFFFF",
            height=369,
            width=879,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Initialize variables
        self.attempts_remaining = 3
        self.current_state = "main"
        self.success_rate = self.calculate_success_rate()
        self.summons = self.load_summons()
        
        # Setup UI
        self.setup_ui()
        
        # Start animation if performance setting allows
        if self.setting_data["Settings"]["Performernce (ANIME):"] != "True":
            self.update_thread = threading.Thread(target=self.update_images)
            self.update_thread.daemon = True
            self.update_thread.start()
        
        # Show main state initially
        self.show_state("main")
        
        # Set window to non-resizable and start main loop
        window.resizable(False, False)
        window.mainloop()
        
    def setup_animations(self):
        """Setup animations and video player"""
        # Setup animated top and bottom bars
        all_prev = '' if self.job == 'None' else 'alt_'
        top_val = 'dailyquest.py' if self.job == 'None' else ''
        self.video = 'Video' if self.job == 'None' else 'Alt Video'
        
        if self.setting_data["Settings"]["Performernce (ANIME):"] == "True":
            self.top_images = [f"thesystem/{all_prev}top_bar/{top_val}{str(2).zfill(4)}.png"]
            self.bottom_images = [f"thesystem/{all_prev}bottom_bar/{str(2).zfill(4)}.png"]
        else:
            self.top_images = [f"thesystem/{all_prev}top_bar/{top_val}{str(i).zfill(4)}.png" for i in range(2, 501, 4)]
            self.bottom_images = [f"thesystem/{all_prev}bottom_bar/{str(i).zfill(4)}.png" for i in range(2, 501, 4)]
            
        # Preload top and bottom images
        self.top_preloaded_images = thesystem.system.preload_images(self.top_images, (970, 40))
        self.bottom_preloaded_images = thesystem.system.preload_images(self.bottom_images, (970, 40))
        
    def setup_ui(self):
        """Setup the main UI elements"""
        try:
            # Background image (same as inventory)
            self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
            self.image_1 = self.canvas.create_image(479.0, 184.0, image=self.image_image_1)
        except Exception as e:
            print(f"Error loading image_1.png: {e}")
            # Create fallback background
            self.canvas.create_rectangle(0, 0, 879, 369, fill="#2E2E2E")
            
        # Try to setup video player
        try:
            with open("Files/Mod/presets.json", 'r') as pres_file:
                pres_file_data = ujson.load(pres_file)
                self.normal_font_col = pres_file_data["Anime"]["Normal Font Color"]
                video_path = pres_file_data["Anime"][self.video]
            self.player = thesystem.system.VideoPlayer(self.canvas, video_path, 479.0, 184.0, pause_duration=0.5)
        except Exception as e:
            print(f"Error setting up video player: {e}")
        
        # Create side bars
        try:
            self.side = PhotoImage(file=relative_to_assets("blue.png"))
            if self.job.upper() != "NONE":
                self.side = PhotoImage(file=relative_to_assets("purple.png"))
            
            self.canvas.create_image(4.0, 180.0, image=self.side)
            self.canvas.create_image(850.0, 196.0, image=self.side)
            
            self.image_40 = thesystem.system.side_bar("left_bar.png", (75, 320))
            self.canvas.create_image(12.0, 180.0, image=self.image_40)
            
            self.image_50 = thesystem.system.side_bar("right_bar.png", (80, 340))
            self.canvas.create_image(833.0, 190.0, image=self.image_50)
        except Exception as e:
            print(f"Error loading side bars: {e}")
        
        # Create transparent top and bottom bars
        self.canvas.create_rectangle(0, 0, 879, 34, fill=self.transp_clr, outline="")
        self.canvas.create_rectangle(0, 335, 879, 369, fill=self.transp_clr, outline="")
        
        # Create animated top and bottom bars
        self.image_index = 0
        self.bot_image_index = 0

        self.top_image = self.canvas.create_image(
            472.0,
            20.0,
            image=self.top_preloaded_images[self.image_index]
        )

        self.bottom_image = self.canvas.create_image(
            427.0,
            350.0,
            image=self.bottom_preloaded_images[self.bot_image_index]
        )
        
        # Setup window movement controls
        self.canvas.tag_bind(self.top_image, "<ButtonPress-1>", self.start_move)
        self.canvas.tag_bind(self.top_image, "<B1-Motion>", self.move_window)
        
        # Add close button
        try:
            self.button_image_close = PhotoImage(file=relative_to_assets("button_26.png"))
            self.button_close = Button(
                image=self.button_image_close,
                borderwidth=0,
                highlightthickness=0,
                command=self.ex_close,
                relief="flat"
            )
            self.button_close.place(x=830.0, y=64.0, width=20.0, height=20.0)
        except Exception as e:
            print(f"Error loading button image: {e}")
            # Create fallback close button
            self.button_close = Button(
                window,
                text="X",
                bg="#FF3333",
                fg="#FFFFFF",
                font=("Montserrat Bold", 10),
                command=self.ex_close,
                relief="flat"
            )
            self.button_close.place(x=830.0, y=64.0, width=20.0, height=20.0)
            
        # Create Shadow title
        self.shadow_title_bg = self.canvas.create_rectangle(
            200, 70, 666, 104,
            fill="#1E1E1E",
            outline=self.transp_clr,
            width=2
        )

        self.shadow_title = self.canvas.create_text(
            433.0, 87.0,
            text="SHADOW EXTRACTION SYSTEM",
            fill="#FFFFFF",
            font=("Montserrat Bold", 20)
        )
        
        # Create UI states
        self.create_main_ui()
        self.create_extraction_ui()
        self.create_success_ui()
        self.create_failure_ui()
        self.create_dialog_ui()
        
    def create_main_ui(self):
        """Create the main UI elements with 'main' tag"""
        # Create main panel for content
        self.main_panel_bg = self.canvas.create_rectangle(
            150, 120, 729, 320,
            fill="#1E1E1E",
            outline=self.transp_clr,
            width=1,
            tags="main"
        )
        
        # Create main content text
        self.main_text = self.canvas.create_text(
            439.0, 150.0,
            text="Extract a shadow from a defeated enemy",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14),
            tags="main"
        )
        
        self.sub_text = self.canvas.create_text(
            439.0, 180.0,
            text=f"Attempt to extract shadow from: {self.boss_name}",
            fill="#AAAAAA",
            font=("Montserrat Regular", 12),
            tags="main"
        )
        
        self.rank_text = self.canvas.create_text(
            439.0, 210.0,
            text=f"Rank: {self.rank}",
            fill="#FFAA00",
            font=("Montserrat Bold", 14),
            tags="main"
        )
        
        # Create buttons
        self.extract_button_bg = self.canvas.create_rectangle(
            270, 240, 420, 280,
            fill="#333333",
            outline="",
            tags="main"
        )
        
        self.extract_button_text = self.canvas.create_text(
            345, 260,
            text="Extract Shadow",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12),
            tags="main"
        )
        
        # Make button clickable
        self.canvas.tag_bind(self.extract_button_bg, "<Button-1>", 
                            lambda e: self.show_state("extraction"))
        self.canvas.tag_bind(self.extract_button_text, "<Button-1>", 
                            lambda e: self.show_state("extraction"))
        
        self.cancel_button_bg = self.canvas.create_rectangle(
            450, 240, 600, 280,
            fill="#333333",
            outline="",
            tags="main"
        )
        
        self.cancel_button_text = self.canvas.create_text(
            525, 260,
            text="Cancel",
            fill="#FFFFFF",
            font=("Montserrat Regular", 12),
            tags="main"
        )
        
        # Make button clickable
        self.canvas.tag_bind(self.cancel_button_bg, "<Button-1>", 
                            lambda e: self.ex_close())
        self.canvas.tag_bind(self.cancel_button_text, "<Button-1>", 
                            lambda e: self.ex_close())
                            
    def create_extraction_ui(self):
        """Create the extraction UI elements with 'extraction' tag"""
        # Create main panel for content
        self.extraction_panel_bg = self.canvas.create_rectangle(
            180, 120, 699, 320,
            fill="#1E1E1E",
            outline=self.transp_clr,
            width=1,
            tags="extraction"
        )
        
        # Boss info
        self.boss_info_text = self.canvas.create_text(
            439.0, 150.0,
            text=f"Attempt to extract shadow from: {self.boss_name}",
            fill="#AAAAAA",
            font=("Montserrat Regular", 12),
            tags="extraction"
        )
        
        # Rank info
        self.rank_info_text = self.canvas.create_text(
            439.0, 175.0,
            text=f"Rank: {self.rank}",
            fill="#FFAA00",
            font=("Montserrat Bold", 14),
            tags="extraction"
        )
        
        # Success rate and attempts
        self.stats_text = self.canvas.create_text(
            439.0, 200.0,
            text=f"Success Rate: {int(self.success_rate * 100)}% | Attempts: {self.attempts_remaining}",
            fill="#FFAA00",
            font=("Montserrat Regular", 12),
            tags="extraction"
        )
        
        # Attempt animation area
        self.animation_rect = self.canvas.create_rectangle(
            319, 220, 559, 250,
            fill="#2A2A2A",
            outline="#652AA3",
            tags="extraction"
        )
        
        self.animation_text = self.canvas.create_text(
            439.0, 235.0,
            text="Ready to extract",
            fill="#FFFFFF",
            font=("Montserrat Regular", 12),
            tags="extraction"
        )
        
        # Extract button
        self.extract_now_bg = self.canvas.create_rectangle(
            270, 270, 420, 300,
            fill="#652AA3",
            outline="",
            tags="extraction"
        )
        
        self.extract_now_text = self.canvas.create_text(
            345, 285,
            text="Extract Shadow",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12),
            tags="extraction"
        )
        
        # Make button clickable
        self.canvas.tag_bind(self.extract_now_bg, "<Button-1>", 
                            lambda e: self.attempt_summon())
        self.canvas.tag_bind(self.extract_now_text, "<Button-1>", 
                            lambda e: self.attempt_summon())
        
        # Cancel button
        self.cancel_extract_bg = self.canvas.create_rectangle(
            450, 270, 600, 300,
            fill="#333333",
            outline="",
            tags="extraction"
        )
        
        self.cancel_extract_text = self.canvas.create_text(
            525, 285,
            text="Cancel",
            fill="#FFFFFF",
            font=("Montserrat Regular", 12),
            tags="extraction"
        )
        
        # Make button clickable
        self.canvas.tag_bind(self.cancel_extract_bg, "<Button-1>", 
                            lambda e: self.show_state("main"))
        self.canvas.tag_bind(self.cancel_extract_text, "<Button-1>", 
                            lambda e: self.show_state("main"))
        
    def create_success_ui(self):
        """Create the success UI elements with 'success' tag"""
        # Create main panel
        self.success_panel_bg = self.canvas.create_rectangle(
            180, 120, 699, 320,
            fill="#1E1E1E",
            outline="#00AA44",
            width=2,
            tags="success"
        )
        
        # Success message
        self.success_header = self.canvas.create_text(
            439.0, 150.0,
            text="SHADOW EXTRACTION SUCCESSFUL",
            fill="#00FF00",
            font=("Montserrat Bold", 16),
            tags="success"
        )
        
        # Boss name
        self.success_info = self.canvas.create_text(
            439.0, 190.0,
            text=f"{self.boss_name} has been added to your collection",
            fill="#FFFFFF",
            font=("Montserrat Regular", 12),
            tags="success"
        )
        
        # Continue button
        self.success_button_bg = self.canvas.create_rectangle(
            340, 240, 540, 280,
            fill="#652AA3",
            outline="",
            tags="success"
        )
        
        self.success_button_text = self.canvas.create_text(
            440, 260,
            text="View Shadow",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12),
            tags="success"
        )
        
        # Make button clickable
        self.canvas.tag_bind(self.success_button_bg, "<Button-1>", 
                            lambda e: self.show_state("dialog"))
        self.canvas.tag_bind(self.success_button_text, "<Button-1>", 
                            lambda e: self.show_state("dialog"))
                            
    def create_failure_ui(self):
        """Create the failure UI elements with 'failure' tag"""
        # Create main panel
        self.failure_panel_bg = self.canvas.create_rectangle(
            180, 120, 699, 320,
            fill="#1E1E1E",
            outline="#AA0000",
            width=2,
            tags="failure"
        )
        
        # Failure message
        self.failure_header = self.canvas.create_text(
            439.0, 150.0,
            text="SHADOW EXTRACTION FAILED",
            fill="#FF0000",
            font=("Montserrat Bold", 16),
            tags="failure"
        )
        
        # Explanation
        self.failure_info = self.canvas.create_text(
            439.0, 180.0,
            text=f"The shadow of {self.boss_name} resisted extraction",
            fill="#FFFFFF",
            font=("Montserrat Regular", 12),
            tags="failure"
        )
        
        # Advice
        self.failure_advice = self.canvas.create_text(
            439.0, 210.0,
            text="Try again with a different enemy or after becoming stronger",
            fill="#AAAAAA",
            font=("Montserrat Regular", 10),
            tags="failure"
        )
        
        # Close button
        self.failure_button_bg = self.canvas.create_rectangle(
            340, 250, 540, 280,
            fill="#333333",
            outline="",
            tags="failure"
        )
        
        self.failure_button_text = self.canvas.create_text(
            440, 265,
            text="Close",
            fill="#FFFFFF",
            font=("Montserrat Regular", 12),
            tags="failure"
        )
        
        # Make button clickable
        self.canvas.tag_bind(self.failure_button_bg, "<Button-1>", 
                            lambda e: self.show_state("main"))
        self.canvas.tag_bind(self.failure_button_text, "<Button-1>", 
                            lambda e: self.show_state("main"))
                            
    def create_dialog_ui(self):
        """Create the dialog UI elements with 'dialog' tag"""
        # Dialog panel
        self.dialog_panel_bg = self.canvas.create_rectangle(
            130, 120, 749, 320,
            fill="#0A0A0A",
            outline="#652AA3",
            width=2,
            tags="dialog"
        )
        
        # Name plate
        self.dialog_title_bg = self.canvas.create_rectangle(
            130, 120, 749, 150,
            fill="#652AA3",
            outline="",
            tags="dialog"
        )
        
        self.dialog_title_text = self.canvas.create_text(
            439.0, 135.0,
            text=f"{self.boss_name} - Shadow Soldier",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14),
            tags="dialog"
        )
        
        
        # Loyalty dialog phrases
        dialog_options = [
            f"My Liege, I pledge myself to you. I, {self.boss_name} shall serve as your shadow.",
            f"I am yours to command. My strength is now your strength, Shadow Monarch.",
            f"My Liege, I shall fight for you until the end.",
            f"My Liege, most humbly, I shall destroy all who oppose you.",
            f"My defeat was honorable. I serve a strong and worthy master. Command me as you will My Liege."
        ]
        
        # Dialog text
        self.dialog_text = self.canvas.create_text(
            439.0, 265.0,
            text=random.choice(dialog_options),
            fill="#FFFFFF",
            font=("Montserrat", 11, "italic"),
            width=550,
            tags="dialog"
        )
        
        # Continue button
        self.dialog_button_bg = self.canvas.create_rectangle(
            340, 290, 540, 315,
            fill="#652AA3",
            outline="",
            tags="dialog"
        )
        
        self.dialog_button_text = self.canvas.create_text(
            440, 302.5,
            text="Add to Collection",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12),
            tags="dialog"
        )
        
        # Make button clickable
        self.canvas.tag_bind(self.dialog_button_bg, "<Button-1>", 
                            lambda e: self.show_state("main"))
        self.canvas.tag_bind(self.dialog_button_text, "<Button-1>", 
                            lambda e: self.show_state("main"))
    
    def show_state(self, state):
        """Show a specific UI state and hide others"""
        # Hide all states
        self.canvas.itemconfigure("main", state="hidden")
        self.canvas.itemconfigure("extraction", state="hidden")
        self.canvas.itemconfigure("success", state="hidden")
        self.canvas.itemconfigure("failure", state="hidden")
        self.canvas.itemconfigure("dialog", state="hidden")
        
        # Show requested state
        self.canvas.itemconfigure(state, state="normal")
        self.current_state = state
        
        # Reset extraction state if going back to main
        if state == "main" and self.attempts_remaining < 3:
            self.attempts_remaining = 3
            self.canvas.itemconfig(
                self.stats_text, 
                text=f"Success Rate: {int(self.success_rate * 100)}% | Attempts: {self.attempts_remaining}"
            )
            self.canvas.itemconfig(self.animation_text, text="Ready to extract")
            self.canvas.itemconfig(self.animation_rect, outline="#652AA3", fill="#2A2A2A")
            
    def update_images(self):
        """Update animated images for top and bottom bars"""
        try:
            while not stop_event.is_set():
                # Update top image
                self.image_index = (self.image_index + 1) % len(self.top_preloaded_images)
                self.canvas.itemconfig(self.top_image, image=self.top_preloaded_images[self.image_index])

                # Update bottom image
                self.bot_image_index = (self.bot_image_index + 1) % len(self.bottom_preloaded_images)
                self.canvas.itemconfig(self.bottom_image, image=self.bottom_preloaded_images[self.bot_image_index])

                # Sleep for animation timing (24 FPS)
                time.sleep(1/24)
        except Exception as e:
            print(f"Error in animation thread: {e}")
    
    def attempt_summon(self):
        """Try to summon the boss"""
        self.attempts_remaining -= 1
        
        # Update animation to show attempt in progress
        self.canvas.itemconfig(self.animation_text, text="Extracting shadow...")
        self.canvas.itemconfig(self.animation_rect, outline="#FF00FF")
        
        # Update stats display
        self.canvas.itemconfig(
            self.stats_text, 
            text=f"Success Rate: {int(self.success_rate * 100)}% | Attempts: {self.attempts_remaining}"
        )
        
        # Schedule animations and result check
        window.after(500, self.animation_stage1)
        window.after(1000, self.animation_stage2)
        window.after(1500, self.check_summon_result)
    
    def animation_stage1(self):
        """First stage of summoning animation"""
        self.canvas.itemconfig(self.animation_text, text="⚡ Extracting... ⚡")
        self.canvas.itemconfig(self.animation_rect, fill="#3A2A4A")
    
    def animation_stage2(self):
        """Second stage of summoning animation"""
        self.canvas.itemconfig(self.animation_text, text="⚡⚡ Extracting... ⚡⚡")
        self.canvas.itemconfig(self.animation_rect, fill="#4A2A6A")
    
    def check_summon_result(self):
        """Determine if summon is successful based on probability"""
        # Determine if summon is successful
        is_successful = random.random() < self.success_rate
        
        if is_successful:
            self.canvas.itemconfig(self.animation_text, text="EXTRACTION SUCCESSFUL!")
            self.canvas.itemconfig(self.animation_rect, fill="#00AA44", outline="#00FF00")
            window.after(1000, lambda: self.handle_success())
        elif self.attempts_remaining <= 0:
            self.canvas.itemconfig(self.animation_text, text="EXTRACTION FAILED!")
            self.canvas.itemconfig(self.animation_rect, fill="#AA0000", outline="#FF0000")
            window.after(1000, lambda: self.show_state("failure"))
        else:
            self.canvas.itemconfig(self.animation_text, text="Failed - Try again")
            self.canvas.itemconfig(self.animation_rect, fill="#2A2A2A", outline="#AA5500")
    
    def handle_success(self):
        """Handle a successful shadow extraction"""
        self.add_summon_to_collection()
        self.show_state("success")
    
    def calculate_success_rate(self):
        """Calculate success rate for shadow extraction"""
        # Base success rate depends on boss rank
        rank_rates = {
            "E": 0.70,  # 70% success rate for E-rank
            "D": 0.55,
            "C": 0.40, 
            "B": 0.30,
            "A": 0.20,
            "S": 0.10,  # 10% success rate for S-rank
            "Red": 0.05  # 5% success rate for Red-rank
        }
        return rank_rates.get(self.rank, 0.50)
    
    def load_summons(self):
        """Load all shadow summons from JSON"""
        try:
            os.makedirs("Files/Player Data", exist_ok=True)
            if os.path.exists("Files/Player Data/Summons.json"):
                with open("Files/Player Data/Summons.json", 'r') as summon_file:
                    return json.load(summon_file)
            # Create default structure if it doesn't exist
            default_data = {
                "summons": [],
                "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "total_summons": 0,
                "max_summons_allowed": 20,
                "active_summons_limit": 3
            }
            with open("Files/Player Data/Summons.json", 'w') as summon_file:
                json.dump(default_data, summon_file, indent=4)
            return default_data
        except Exception as e:
            print(f"Error loading summons: {e}")
            return {"summons": []}
    
    def save_summons(self):
        """Save summons to JSON file"""
        try:
            with open("Files/Player Data/Summons.json", 'w') as summon_file:
                json.dump(self.summons, summon_file, indent=4)
        except Exception as e:
            print(f"Error saving summons: {e}")
    
    def add_summon_to_collection(self):
        """Add the boss to the shadow summons collection"""
        # Create a new summon entry
        new_summon = {
            "name": self.boss_name,
            "rank": self.rank,
            "type": self.boss_data.get("type", "Boss"),
            "attribute": self.boss_data.get("attribute", "STR"),
            "power": self.calculate_summon_power(),
            "loyalty": 100,
            "level": 1,
            "experience": 0,
            "active": False
        }
        
        # Check if this summon already exists
        for i, summon in enumerate(self.summons["summons"]):
            if summon["name"] == self.boss_name:
                # Update existing summon
                self.summons["summons"][i] = new_summon
                break
        else:
            # Add to collection if it doesn't exist
            self.summons["summons"].append(new_summon)
        
        # Update total summons count
        self.summons["total_summons"] = len(self.summons["summons"])
        
        # Save updated collection
        self.save_summons()
    
    def calculate_summon_power(self):
        """Calculate the power level of the summoned shadow soldier"""
        # Base power based on rank
        rank_power = {
            "E": 10,
            "D": 20,
            "C": 30,
            "B": 50,
            "A": 80,
            "S": 120,
            "Red": 200
        }
        
        base_power = rank_power.get(self.rank, 10)
        
        # Add some randomness to power (-10% to +20%)
        variance_factor = random.uniform(0.9, 1.2)
        return int(base_power * variance_factor)
        
    def start_move(self, event):
        """Start window movement"""
        global window
        window.lastx, window.lasty = event.widget.winfo_pointerxy()

    def move_window(self, event):
        """Move window when dragged"""
        global window
        x_root, y_root = event.widget.winfo_pointerxy()
        deltax, deltay = x_root - window.lastx, y_root - window.lasty

        if deltax != 0 or deltay != 0:  # Update only if there is actual movement
            window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")
            window.lastx, window.lasty = x_root, y_root

    def ex_close(self):
        """Close the window"""
        global stop_event, window
        stop_event.set()
        
        try:
            with open("Files/Player Data/Tabs.json", 'r') as tab_son:
                tab_son_data = ujson.load(tab_son)

            with open("Files/Player Data/Tabs.json", 'w') as fin_tab_son:
                tab_son_data["ShadowSummon"] = 'Close'
                ujson.dump(tab_son_data, fin_tab_son, indent=4)
        except Exception as e:
            print(f"Error updating Tabs.json: {e}")
            
        threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
        subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
        thesystem.system.animate_window_close(window, initial_height, window_width, step=50, delay=1)

# Shadow Manager class to handle summoned soldiers in dungeons
class ShadowManager:
    def __init__(self, parent, canvas, normal_font_col):
        self.parent = parent
        self.canvas = canvas
        self.normal_font_col = normal_font_col
        self.active_summons = []
        
    def load_summons(self):
        """Load all available shadow soldiers"""
        try:
            with open("Files/Player Data/Summons.json", 'r') as summon_file:
                summons_data = json.load(summon_file)
                return summons_data.get("summons", [])
        except Exception as e:
            print(f"Error loading summons: {e}")
            return []
    
    def apply_summon_effects(self, wave_key, monster_name, monster, activities):
        """Apply the effects of active shadow soldiers to the current wave"""
        if not self.active_summons:
            return
        
        monster_type = monster.get('attribute', 'STR')
        
        # Track which summons are effective
        effective_summons = []
        
        # Check each active summon for effects
        for summon in self.active_summons:
            # Calculate strength modifier based on:
            # 1. Summon power
            # 2. Summon level
            # 3. Type effectiveness (matching attribute gives bonus)
            # 4. Loyalty (higher loyalty = more effective)
            base_modifier = summon['power'] * (1 + (summon['level'] - 1) * 0.2)
            
            # Type effectiveness (25% bonus if attributes match)
            if summon['attribute'] == monster_type:
                type_bonus = 1.25
                effective_summons.append(f"{summon['name']} (Type Advantage)")
            else:
                type_bonus = 1.0
                effective_summons.append(f"{summon['name']}")
            
            # Loyalty factor (100% loyalty = full effect, 0% loyalty = no effect)
            loyalty_factor = summon['loyalty'] / 100.0
            
            # Final modifier
            total_modifier = base_modifier * type_bonus * loyalty_factor
            
            # Apply effects to activities (reduce required counts/times)
            self.apply_modifier_to_activities(total_modifier, activities)
        
        # Display summon effect notification
        if effective_summons:
            effective_text = ", ".join(effective_summons)
            notification = self.canvas.create_text(
                400, 190,
                anchor="center",
                text=f"Shadow Soldiers assisting: {effective_text}",
                fill="#652AA3",
                font=("Montserrat Bold", 12)
            )
            window.after(5000, lambda: self.canvas.delete(notification))
    
    def apply_modifier_to_activities(self, modifier, activities):
        """Apply summon modifier to reduce exercise requirements"""
        # Calculate percent reduction (capped at 60%)
        percent_reduction = min(0.60, modifier / 200.0)
        
        # Apply to all activities
        for activity in activities:
            try:
                current_text = self.canvas.itemcget(activity, "text")
                
                # Skip if already modified by a summon
                if "[Shadow Assist]" in current_text:
                    continue
                
                # Find and reduce the numeric value
                import re
                numbers = re.findall(r'\d+', current_text)
                if numbers:
                    for num_str in numbers:
                        original_value = int(num_str)
                        reduced_value = max(1, int(original_value * (1 - percent_reduction)))
                        
                        # Don't modify if reduction is too small
                        if original_value - reduced_value < 1:
                            continue
                        
                        # Replace with reduced value and add indicator
                        new_text = current_text.replace(str(original_value), str(reduced_value), 1)
                        new_text += f" [Shadow Assist]"
                        self.canvas.itemconfig(activity, text=new_text, fill="#652AA3")
                        
                        # Reset color after 3 seconds
                        window.after(3000, lambda act=activity: self.canvas.itemconfig(
                            act, fill=self.normal_font_col
                        ))
                        break
            except Exception as e:
                print(f"Error applying modifier: {e}")
    
    def update_summons_after_completion(self, dungeon_rank):
        """Update loyalty and experience for summons used in the dungeon"""
        if not self.active_summons:
            return
        
        all_summons = self.load_summons()
        
        # XP gained based on dungeon rank
        rank_xp = {
            "E": 10,
            "D": 20,
            "C": 30,
            "B": 50,
            "A": 80,
            "S": 120,
            "Red": 200
        }
        
        gained_xp = rank_xp.get(dungeon_rank, 10)
        loyalty_gain = 5  # Gain 5% loyalty per dungeon completion
        
        # Update each active summon
        updated_summons = []
        for i, summon in enumerate(all_summons):
            # Check if this summon was used in the dungeon
            was_active = False
            for active_summon in self.active_summons:
                if active_summon['name'] == summon['name']:
                    was_active = True
                    break
            
            if was_active:
                # Add experience
                summon['experience'] += gained_xp
                
                # Check for level up
                xp_required = summon['level'] * 100
                if summon['experience'] >= xp_required:
                    summon['level'] += 1
                    summon['experience'] -= xp_required
                    
                    # Increase power with level up (5% per level)
                    summon['power'] = int(summon['power'] * 1.05)
                    
                    # Show level up notification
                    lvl_up_text = self.canvas.create_text(
                        400, 200 + len(updated_summons) * 20,
                        anchor="center",
                        text=f"{summon['name']} leveled up to {summon['level']}!",
                        fill="#00FF00",
                        font=("Montserrat Bold", 12)
                    )
                    window.after(4000, lambda t=lvl_up_text: self.canvas.delete(t))
                
                # Increase loyalty (capped at 100%)
                summon['loyalty'] = min(100, summon['loyalty'] + loyalty_gain)
                
                updated_summons.append(summon['name'])
        
        # Save updated summons data
        try:
            with open("Files/Player Data/Summons.json", 'r') as summon_file:
                summons_data = json.load(summon_file)
                
            # Update summons in the data
            for i, summon in enumerate(summons_data.get("summons", [])):
                for updated_name in updated_summons:
                    if summon['name'] == updated_name:
                        # Find the updated summon data
                        for updated_summon in all_summons:
                            if updated_summon['name'] == updated_name:
                                summons_data["summons"][i] = updated_summon
                                break
            
            # Save the updated data
            with open("Files/Player Data/Summons.json", 'w') as summon_file:
                json.dump(summons_data, summon_file, indent=4)
        except Exception as e:
            print(f"Error updating summons after completion: {e}")
        
        # Show update notification if any summons were updated
        if updated_summons:
            summon_names = ", ".join(updated_summons)
            update_text = self.canvas.create_text(
                400, 180,
                anchor="center",
                text=f"Shadow Soldiers gained experience: {summon_names}",
                fill="#FFAA00",
                font=("Montserrat Bold", 12)
            )
            window.after(4000, lambda: self.canvas.delete(update_text))

# Main execution
if __name__ == "__main__":
    try:
        ShadowSummonSystem()
    except Exception as e:
        print(f"Error starting shadow summon system: {e}")
        # If there's an error, create a simple error window
        error_root = tk.Tk()
        error_root.title("Shadow System Error")
        error_root.geometry("400x200")
        error_root.configure(bg="#1E1E1E")
        tk.Label(
            error_root, 
            text=f"Error in Shadow Summon System:\n{str(e)}", 
            fg="#FF5555",
            bg="#1E1E1E",
            font=("Montserrat Bold", 12)
        ).pack(pady=20)
        tk.Button(
            error_root, 
            text="Close", 
            command=error_root.destroy,
            bg="#333333",
            fg="#FFFFFF"
        ).pack()
        error_root.mainloop()