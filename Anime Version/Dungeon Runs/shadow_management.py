# Shadow Management System styled to match inventory GUI frame with custom content
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, Label, Scrollbar, StringVar, OptionMenu, Toplevel
import ujson
import csv
import subprocess
import cv2
from PIL import Image, ImageTk
import threading
import sys
import os
import json
import random
import time
from datetime import datetime, timedelta

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

import thesystem.system
import thesystem.misc

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

# Create a Tabs.json entry for Shadows
try:
    with open("Files/Player Data/Tabs.json", 'r') as tab_son:
        tab_son_data = ujson.load(tab_son)

    with open("Files/Player Data/Tabs.json", 'w') as fin_tab_son:
        tab_son_data["Shadows"] = 'Open'
        ujson.dump(tab_son_data, fin_tab_son, indent=4)
except Exception as e:
    print(f"Error updating Tabs.json: {e}")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_directory_if_not_exists(directory_path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)

# Ensure Shadow assets directory exists
shadow_assets_dir = OUTPUT_PATH / "shadow_assets"
create_directory_if_not_exists(shadow_assets_dir)

window = Tk()
stop_event = threading.Event()

initial_height = 0
target_height = 592
window_width = 855

window.geometry(f"{window_width}x{initial_height}")

# Get job type for theming
job = thesystem.misc.return_status()["status"][1]["job"]

top_val = 'dailyquest.py'
all_prev = ''
video = 'Video'
transp_clr = '#0C679B'

if job != 'None':
    top_val = ''
    all_prev = 'alt_'
    video = 'Alt Video'
    transp_clr = '#652AA3'

thesystem.system.make_window_transparent(window, transp_clr)

with open("Files/Player Data/Settings.json", 'r') as settings_open:
    setting_data = ujson.load(settings_open)

if setting_data["Settings"]["Performernce (ANIME):"] == "True":
    top_images = [f"thesystem/{all_prev}top_bar/{top_val}{str(2).zfill(4)}.png"]
    bottom_images = [f"thesystem/{all_prev}bottom_bar/{str(2).zfill(4)}.png"]
else:
    top_images = [f"thesystem/{all_prev}top_bar/{top_val}{str(i).zfill(4)}.png" for i in range(2, 501, 4)]
    bottom_images = [f"thesystem/{all_prev}bottom_bar/{str(i).zfill(4)}.png" for i in range(2, 501, 4)]

thesystem.system.animate_window_open(window, target_height, window_width, step=40, delay=1)

window.configure(bg="#FFFFFF")
window.attributes('-alpha', 0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

# Preload top and bottom images
top_preloaded_images = thesystem.system.preload_images(top_images, (970, 40))
bottom_preloaded_images = thesystem.system.preload_images(bottom_images, (970, 40))

subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])

def start_move(event):
    window.lastx, window.lasty = event.widget.winfo_pointerxy()

def move_window(event):
    x_root, y_root = event.widget.winfo_pointerxy()
    deltax, deltay = x_root - window.lastx, y_root - window.lasty

    if deltax != 0 or deltay != 0:  # Update only if there is actual movement
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")
        window.lastx, window.lasty = x_root, y_root

def ex_close():
    if setting_data["Settings"]["Performernce (ANIME):"] != "True":
        stop_event.set()
        update_thread.join()

    with open("Files/Player Data/Tabs.json", 'r') as tab_son:
        tab_son_data = ujson.load(tab_son)

    with open("Files/Player Data/Tabs.json", 'w') as fin_tab_son:
        tab_son_data["Shadows"] = 'Close'
        ujson.dump(tab_son_data, fin_tab_son, indent=4)
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=50, delay=1)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=592,
    width=855,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

# Background image (same as inventory)
try:
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(479.0, 364.0, image=image_image_1)
except Exception as e:
    print(f"Error loading image_1.png: {e}")
    # Create fallback background
    canvas.create_rectangle(0, 0, 855, 592, fill="#2E2E2E")

# Setup video player
try:
    with open("Files/Mod/presets.json", 'r') as pres_file:
        pres_file_data = ujson.load(pres_file)
        video_path = pres_file_data["Anime"][video]
    player = thesystem.system.VideoPlayer(canvas, video_path, 479.0, 364.0, pause_duration=0.5)
except Exception as e:
    print(f"Error setting up video player: {e}")

# Load background overlay
try:
    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(470.0, 311.0, image=image_image_2)
except Exception as e:
    print(f"Error loading image_2.png: {e}")

# Create Shadow title
shadow_title_bg = canvas.create_rectangle(
    200, 100, 666, 134,
    fill="#1E1E1E",
    outline=transp_clr,
    width=2
)

shadow_title = canvas.create_text(
    433.0, 117.0,
    text="SHADOW ARMY MANAGEMENT",
    fill="#FFFFFF",
    font=("Montserrat Bold", 20)
)

# Create side bars (same as inventory)
side = PhotoImage(file=relative_to_assets("blue.png"))
if job.upper() != "NONE":
    side = PhotoImage(file=relative_to_assets("purple.png"))
canvas.create_image(-10.0, 283.0, image=side)
canvas.create_image(851.0, 308.0, image=side)

# Create top and bottom bars
canvas.create_rectangle(
    0.0,
    0.0,
    101.0,
    21.0,
    fill=transp_clr,
    outline=""
)

canvas.create_rectangle(
    0.0,
    520.0,
    1000.0,
    716.0,
    fill=transp_clr,
    outline=""
)

canvas.create_rectangle(
    0.0,
    0.0,
    1000.0,
    34.0,
    fill=transp_clr,
    outline=""
)

image_40 = thesystem.system.side_bar("left_bar.png", (101, 520))
canvas.create_image(-13.0, 280.0, image=image_40)

image_50 = thesystem.system.side_bar("right_bar.png", (80, 500))
canvas.create_image(851.0, 280.0, image=image_50)

# Create animated top and bottom bars
image_index = 0
bot_image_index = 0

top_image = canvas.create_image(
    472.0,
    20.0,
    image=top_preloaded_images[image_index]
)

canvas.tag_bind(top_image, "<ButtonPress-1>", start_move)
canvas.tag_bind(top_image, "<B1-Motion>", move_window)

bottom_image = canvas.create_image(
    427.0,
    530.0,
    image=bottom_preloaded_images[bot_image_index]
)

# Animation update function
def update_images():
    global image_index, bot_image_index

    image_index = (image_index + 1) % len(top_preloaded_images)
    top_img = top_preloaded_images[image_index]
    canvas.itemconfig(top_image, image=top_img)
    canvas.top_img = top_img

    bot_image_index = (bot_image_index + 1) % len(bottom_preloaded_images)
    bot_img = bottom_preloaded_images[bot_image_index]
    canvas.itemconfig(bottom_image, image=bot_img)
    canvas.bot_img = bot_img

    window.after(1000 // 24, update_images)

# Start animation if performance setting allows
if setting_data["Settings"]["Performernce (ANIME):"] != "True":
    update_thread = threading.Thread(target=update_images)
    update_thread.start()

# Shadow Management specific functionality
class ShadowManager:
    def __init__(self, canvas, parent_window, transp_clr):
        self.canvas = canvas
        self.parent_window = parent_window
        self.transp_clr = transp_clr
        self.summons = []
        self.selected_summon = None
        self.filter_attribute = "All"
        self.filter_rank = "All"
        self.filter_type = "All"
        self.shadow_list_items = []
        
        # Load shadows
        self.load_summons()
        
        # Create custom UI for shadow management
        self.create_shadow_ui()
        
    def load_summons(self):
        """Load all shadow summons from JSON"""
        try:
            if os.path.exists("Files/Player Data/Summons.json"):
                with open("Files/Player Data/Summons.json", 'r') as summon_file:
                    summons_data = json.load(summon_file)
                    self.summons = summons_data.get("summons", [])
            else:
                # Create default structure if it doesn't exist
                default_data = {
                    "summons": [],
                    "last_updated": datetime.now().isoformat(),
                    "total_summons": 0,
                    "max_summons_allowed": 20,
                    "active_summons_limit": 3
                }
                os.makedirs(os.path.dirname("Files/Player Data/Summons.json"), exist_ok=True)
                with open("Files/Player Data/Summons.json", 'w') as summon_file:
                    json.dump(default_data, summon_file, indent=4)
                self.summons = []
        except Exception as e:
            print(f"Error loading summons: {e}")
            self.summons = []
    
    def create_shadow_ui(self):
        """Create custom UI for shadow management"""
        # Create main containers
        self.left_frame = Frame(
            self.parent_window, 
            bg="#1E1E1E",
            highlightbackground=self.transp_clr,
            highlightthickness=1
        )
        self.left_frame.place(x=50, y=150, width=350, height=340)
        
        self.right_frame = Frame(
            self.parent_window, 
            bg="#1E1E1E",
            highlightbackground=self.transp_clr,
            highlightthickness=1
        )
        self.right_frame.place(x=420, y=150, width=380, height=340)
        
        # Create filter controls
        self.filter_frame = Frame(self.left_frame, bg="#1E1E1E")
        self.filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Rank filter
        rank_label = Label(
            self.filter_frame,
            text="Rank:",
            fg="#FFFFFF",
            bg="#1E1E1E",
            font=("Montserrat Bold", 10)
        )
        rank_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        rank_options = ["All", "E", "D", "C", "B", "A", "S", "Red"]
        self.rank_var = StringVar(value="All")
        rank_menu = OptionMenu(
            self.filter_frame,
            self.rank_var,
            *rank_options,
            command=self.apply_filters
        )
        rank_menu.config(bg="#333333", fg="#FFFFFF", width=5, font=("Montserrat", 8))
        rank_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Type filter
        type_label = Label(
            self.filter_frame,
            text="Type:",
            fg="#FFFFFF",
            bg="#1E1E1E",
            font=("Montserrat Bold", 10)
        )
        type_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        type_options = ["All", "Boss", "Elite", "Normal"]
        self.type_var = StringVar(value="All")
        type_menu = OptionMenu(
            self.filter_frame,
            self.type_var,
            *type_options,
            command=self.apply_filters
        )
        type_menu.config(bg="#333333", fg="#FFFFFF", width=6, font=("Montserrat", 8))
        type_menu.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Attribute filter
        attr_label = Label(
            self.filter_frame,
            text="Attribute:",
            fg="#FFFFFF",
            bg="#1E1E1E",
            font=("Montserrat Bold", 10)
        )
        attr_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        attr_options = ["All", "STR", "AGI", "INT"]
        self.attr_var = StringVar(value="All")
        attr_menu = OptionMenu(
            self.filter_frame,
            self.attr_var,
            *attr_options,
            command=self.apply_filters
        )
        attr_menu.config(bg="#333333", fg="#FFFFFF", width=5, font=("Montserrat", 8))
        attr_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Status filter
        status_label = Label(
            self.filter_frame,
            text="Status:",
            fg="#FFFFFF",
            bg="#1E1E1E",
            font=("Montserrat Bold", 10)
        )
        status_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        status_options = ["All", "Active", "Inactive"]
        self.status_var = StringVar(value="All")
        status_menu = OptionMenu(
            self.filter_frame,
            self.status_var,
            *status_options,
            command=self.apply_filters
        )
        status_menu.config(bg="#333333", fg="#FFFFFF", width=6, font=("Montserrat", 8))
        status_menu.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        # Create shadow list
        self.list_container = Frame(self.left_frame, bg="#1E1E1E")
        self.list_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.list_canvas = Canvas(
            self.list_container,
            bg="#1E1E1E",
            highlightthickness=0
        )
        self.list_scrollbar = Scrollbar(
            self.list_container,
            orient="vertical",
            command=self.list_canvas.yview
        )
        
        self.list_canvas.pack(side="left", fill="both", expand=True)
        self.list_scrollbar.pack(side="right", fill="y")
        
        self.list_canvas.configure(yscrollcommand=self.list_scrollbar.set)
        
        self.shadow_list_frame = Frame(self.list_canvas, bg="#1E1E1E")
        self.list_canvas.create_window((0, 0), window=self.shadow_list_frame, anchor="nw")
        
        # Populate shadow list
        self.populate_shadow_list()
        
        # Create right side details panel
        self.detail_title = Label(
            self.right_frame,
            text="SHADOW DETAILS",
            fg="#FFFFFF",
            bg="#1E1E1E",
            font=("Montserrat Bold", 12)
        )
        self.detail_title.pack(pady=10)
        
        # Shadow image placeholder
        self.detail_image_frame = Frame(
            self.right_frame,
            bg="#2A2A2A",
            width=150,
            height=150
        )
        self.detail_image_frame.pack(pady=5)
        self.detail_image_frame.pack_propagate(False)
        
        self.detail_image_label = Label(
            self.detail_image_frame,
            text="SHADOW SOLDIER",
            fg="#AAAAAA",
            bg="#2A2A2A",
            font=("Montserrat Bold", 10)
        )
        self.detail_image_label.pack(expand=True)
        
        # Shadow details panel 
        self.detail_panel = Frame(self.right_frame, bg="#1E1E1E")
        self.detail_panel.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create shadow stats display
        self.stats_frame = Frame(self.detail_panel, bg="#1E1E1E")
        self.stats_frame.pack(fill="x", pady=5)
        
        # Setup default/empty detail texts
        self.detail_name = Label(
            self.stats_frame,
            text="Select a Shadow",
            fg="#FFFFFF",
            bg="#1E1E1E",
            font=("Montserrat Bold", 14)
        )
        self.detail_name.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
        
        self.detail_rank = Label(
            self.stats_frame,
            text="Rank: -",
            fg="#AAAAAA",
            bg="#1E1E1E",
            font=("Montserrat Regular", 10)
        )
        self.detail_rank.grid(row=1, column=0, sticky="w")
        
        self.detail_type = Label(
            self.stats_frame,
            text="Type: -",
            fg="#AAAAAA",
            bg="#1E1E1E",
            font=("Montserrat Regular", 10)
        )
        self.detail_type.grid(row=1, column=1, sticky="w")
        
        self.detail_attribute = Label(
            self.stats_frame,
            text="Attribute: -",
            fg="#AAAAAA",
            bg="#1E1E1E",
            font=("Montserrat Regular", 10)
        )
        self.detail_attribute.grid(row=2, column=0, sticky="w")
        
        self.detail_level = Label(
            self.stats_frame,
            text="Level: -",
            fg="#AAAAAA",
            bg="#1E1E1E",
            font=("Montserrat Regular", 10)
        )
        self.detail_level.grid(row=2, column=1, sticky="w")
        
        self.detail_power = Label(
            self.stats_frame,
            text="Power: -",
            fg="#FFAA00",
            bg="#1E1E1E",
            font=("Montserrat Bold", 10)
        )
        self.detail_power.grid(row=3, column=0, sticky="w")
        
        self.detail_loyalty = Label(
            self.stats_frame,
            text="Loyalty: -",
            fg="#AAAAAA",
            bg="#1E1E1E",
            font=("Montserrat Regular", 10)
        )
        self.detail_loyalty.grid(row=3, column=1, sticky="w")
        
        # Create XP progress bar
        self.xp_frame = Frame(self.detail_panel, bg="#1E1E1E")
        self.xp_frame.pack(fill="x", pady=5)
        
        self.xp_label = Label(
            self.xp_frame,
            text="XP: -",
            fg="#AAAAAA",
            bg="#1E1E1E",
            font=("Montserrat Regular", 10)
        )
        self.xp_label.pack(anchor="w")
        
        self.xp_bar_bg = Frame(
            self.xp_frame,
            bg="#333333",
            height=10
        )
        self.xp_bar_bg.pack(fill="x", pady=2)
        
        self.xp_bar_fill = Frame(
            self.xp_bar_bg,
            bg="#00AAFF",
            width=0,
            height=10
        )
        self.xp_bar_fill.place(x=0, y=0, width=0)
        
        # Create loyalty progress bar
        self.loyalty_frame = Frame(self.detail_panel, bg="#1E1E1E")
        self.loyalty_frame.pack(fill="x", pady=5)
        
        self.loyalty_label = Label(
            self.loyalty_frame,
            text="Loyalty: -",
            fg="#AAAAAA",
            bg="#1E1E1E",
            font=("Montserrat Regular", 10)
        )
        self.loyalty_label.pack(anchor="w")
        
        self.loyalty_bar_bg = Frame(
            self.loyalty_frame,
            bg="#333333",
            height=10
        )
        self.loyalty_bar_bg.pack(fill="x", pady=2)
        
        self.loyalty_bar_fill = Frame(
            self.loyalty_bar_bg,
            bg="#00FF00",
            width=0,
            height=10
        )
        self.loyalty_bar_fill.place(x=0, y=0, width=0)
        
        # Create description area
        self.desc_label = Label(
            self.detail_panel,
            text="Description:",
            fg="#FFFFFF",
            bg="#1E1E1E",
            font=("Montserrat Bold", 10),
            anchor="w"
        )
        self.desc_label.pack(anchor="w", pady=(10, 0))
        
        self.description_text = Label(
            self.detail_panel,
            text="Select a shadow to view its details.",
            fg="#AAAAAA",
            bg="#1E1E1E",
            font=("Montserrat Regular", 9),
            wraplength=340,
            justify="left",
            anchor="w"
        )
        self.description_text.pack(fill="x", pady=5)
        
        # Create action buttons frame
        self.buttons_frame = Frame(self.right_frame, bg="#1E1E1E")
        self.buttons_frame.pack(fill="x", padx=10, pady=10)
        
        self.activate_button = Button(
            self.buttons_frame,
            text="Activate Shadow",
            bg="#652AA3",
            fg="#FFFFFF",
            font=("Montserrat Bold", 10),
            command=self.toggle_shadow_active,
            state="disabled",
            width=15
        )
        self.activate_button.pack(side="left", padx=5)
        
        self.rename_button = Button(
            self.buttons_frame,
            text="Rename",
            bg="#333333",
            fg="#FFFFFF",
            font=("Montserrat Regular", 10),
            command=self.rename_shadow,
            state="disabled",
            width=10
        )
        self.rename_button.pack(side="right", padx=5)
        
        # Summary stats panel
        self.summary_frame = Frame(self.parent_window, bg="#1E1E1E")
        self.summary_frame.place(x=50, y=495, width=750, height=30)
        
        # Get active summons limit
        active_limit = 3
        if self.summons and os.path.exists("Files/Player Data/Summons.json"):
            try:
                with open("Files/Player Data/Summons.json", 'r') as summon_file:
                    summons_data = json.load(summon_file)
                    active_limit = summons_data.get("active_summons_limit", 3)
            except:
                active_limit = 3
        
        # Count active summons
        active_count = sum(1 for s in self.summons if s.get("active", False))
        
        # Summary stats
        self.total_label = Label(
            self.summary_frame,
            text=f"Total Shadows: {len(self.summons)}",
            fg="#FFFFFF",
            bg="#1E1E1E",
            font=("Montserrat Regular", 10)
        )
        self.total_label.pack(side="left", padx=10)
        
        self.active_label = Label(
            self.summary_frame,
            text=f"Active: {active_count}/{active_limit}",
            fg="#FFFFFF" if active_count < active_limit else "#FF5555",
            bg="#1E1E1E",
            font=("Montserrat Regular", 10)
        )
        self.active_label.pack(side="left", padx=10)
        
        # Initialize list scrolling
        self.shadow_list_frame.update_idletasks()
        self.list_canvas.config(scrollregion=self.list_canvas.bbox("all"))
        
        # Setup mousewheel scrolling
        self.list_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    
    def populate_shadow_list(self):
        """Populate the shadow list with filtered shadows"""
        # Clear existing items
        for widget in self.shadow_list_frame.winfo_children():
            widget.destroy()
        
        self.shadow_list_items = []
        
        if not self.summons:
            # Show empty state
            empty_label = Label(
                self.shadow_list_frame,
                text="No shadow soldiers found.\nComplete dungeons to extract shadows.",
                fg="#AAAAAA",
                bg="#1E1E1E",
                font=("Montserrat Regular", 10),
                pady=20
            )
            empty_label.pack(fill="x")
            return
        
        # Apply filters
        filtered_summons = self.filter_summons()
        
        # Sort by rank and power
        filtered_summons.sort(key=lambda x: (self.rank_value(x.get('rank', 'E')), -x.get('power', 0)))
        
        # Create a row for each shadow
        for i, summon in enumerate(filtered_summons):
            row_bg = "#2A2A2A" if i % 2 == 0 else "#333333"
            
            row_frame = Frame(
                self.shadow_list_frame,
                bg=row_bg,
                padx=5,
                pady=5,
                highlightbackground=self.transp_clr if summon.get("active", False) else row_bg,
                highlightthickness=1 if summon.get("active", False) else 0
            )
            row_frame.pack(fill="x", pady=1)
            
            # Add rank badge
            rank = summon.get('rank', 'E')
            rank_color = self.rank_color(rank)
            
            rank_frame = Frame(row_frame, bg=rank_color, width=20, height=20)
            rank_frame.grid(row=0, column=0, rowspan=2, padx=(0, 5))
            rank_frame.grid_propagate(False)
            
            rank_label = Label(
                rank_frame,
                text=rank,
                fg="#FFFFFF",
                bg=rank_color,
                font=("Montserrat Bold", 10)
            )
            rank_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Name and level
            name_label = Label(
                row_frame,
                text=summon.get('name', 'Unknown'),
                fg="#FFFFFF",
                bg=row_bg,
                font=("Montserrat Bold", 10),
                anchor="w"
            )
            name_label.grid(row=0, column=1, sticky="w")
            
            level_label = Label(
                row_frame,
                text=f"Lvl {summon.get('level', 1)}",
                fg="#00AAFF",
                bg=row_bg,
                font=("Montserrat Regular", 9),
                anchor="w"
            )
            level_label.grid(row=1, column=1, sticky="w")
            
            # Power
            power_label = Label(
                row_frame,
                text=f"PWR: {summon.get('power', 0)}",
                fg="#FFAA00",
                bg=row_bg,
                font=("Montserrat Bold", 9),
                anchor="w"
            )
            power_label.grid(row=0, column=2, padx=5)
            
            # Attribute indicator
            attr = summon.get('attribute', 'STR')
            attr_color = self.attr_color(attr)
            
            type_label = Label(
                row_frame,
                text=f"{attr} | {summon.get('type', 'Normal')}",
                fg=attr_color,
                bg=row_bg,
                font=("Montserrat Regular", 9),
                anchor="w"
            )
            type_label.grid(row=1, column=2, padx=5)
            
            # Status indicator
            status_text = "ACTIVE" if summon.get("active", False) else "Inactive"
            status_color = "#00FF00" if summon.get("active", False) else "#AAAAAA"
            
            status_label = Label(
                row_frame,
                text=status_text,
                fg=status_color,
                bg=row_bg,
                font=("Montserrat Regular" if not summon.get("active", False) else "Montserrat Bold", 9)
            )
            status_label.grid(row=0, column=3, rowspan=2, padx=5)
            
            # Make the entire row clickable
            for widget in row_frame.winfo_children():
                widget.bind("<Button-1>", lambda e, s=summon: self.select_shadow(s))
            row_frame.bind("<Button-1>", lambda e, s=summon: self.select_shadow(s))
            
            # Store row for later reference
            self.shadow_list_items.append(row_frame)
        
        # Update scrollregion
        self.shadow_list_frame.update_idletasks()
        self.list_canvas.config(scrollregion=self.list_canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def filter_summons(self):
        """Apply filters to the summons list"""
        filtered = self.summons.copy()
        
        # Apply rank filter
        if self.rank_var.get() != "All":
            filtered = [s for s in filtered if s.get('rank', 'E') == self.rank_var.get()]
        
        # Apply type filter
        if self.type_var.get() != "All":
            filtered = [s for s in filtered if s.get('type', 'Normal') == self.type_var.get()]
        
        # Apply attribute filter
        if self.attr_var.get() != "All":
            filtered = [s for s in filtered if s.get('attribute', 'STR') == self.attr_var.get()]
        
        # Apply status filter
        if self.status_var.get() == "Active":
            filtered = [s for s in filtered if s.get('active', False)]
        elif self.status_var.get() == "Inactive":
            filtered = [s for s in filtered if not s.get('active', False)]
        
        return filtered
    
    def apply_filters(self, *args):
        """Apply current filters and update the list"""
        self.populate_shadow_list()
    
    def select_shadow(self, summon):
        """Select a shadow and update the details panel"""
        self.selected_summon = summon
        
        # Update shadow details display
        self.detail_name.config(text=summon.get('name', 'Unknown'))
        
        # Update rank with color
        rank = summon.get('rank', 'E')
        self.detail_rank.config(
            text=f"Rank: {rank}",
            fg=self.rank_color(rank)
        )
        
        # Update type
        self.detail_type.config(text=f"Type: {summon.get('type', 'Normal')}")
        
        # Update attribute with color
        attr = summon.get('attribute', 'STR')
        self.detail_attribute.config(
            text=f"Attribute: {attr}",
            fg=self.attr_color(attr)
        )
        
        # Update level and power
        self.detail_level.config(text=f"Level: {summon.get('level', 1)}")
        self.detail_power.config(text=f"Power: {summon.get('power', 0)}")
        
        # Update loyalty
        loyalty = summon.get('loyalty', 0)
        self.detail_loyalty.config(
            text=f"Loyalty: {loyalty}%",
            fg="#00FF00" if loyalty >= 90 else "#FFFFFF"
        )
        
        # Update XP bar
        level = summon.get('level', 1)
        xp = summon.get('experience', 0)
        xp_required = level * 100
        xp_percent = min(100, int((xp / xp_required) * 100))
        
        self.xp_label.config(text=f"XP: {xp}/{xp_required} ({xp_percent}%)")
        self.xp_bar_fill.place(x=0, y=0, width=int((self.xp_bar_bg.winfo_width() * xp_percent / 100)))
        
        # Update loyalty bar
        self.loyalty_label.config(text=f"Loyalty: {loyalty}%")
        self.loyalty_bar_fill.config(bg="#00FF00" if loyalty >= 90 else "#FFAA00")
        self.loyalty_bar_fill.place(x=0, y=0, width=int((self.loyalty_bar_bg.winfo_width() * loyalty / 100)))
        
        # Update description
        descriptions = {
            "Boss": {
                "S": "A legendary boss that now serves you. Its immense power greatly reduces required exercises.",
                "A": "A powerful boss that now serves you. Its significant strength reduces required exercises.",
                "B": "A formidable boss that now serves you. Its strength noticeably reduces required exercises.",
                "C": "A capable boss that now serves you. Its power moderately reduces required exercises.",
                "D": "A modest boss that now serves you. Its abilities slightly reduce required exercises.",
                "E": "A basic boss that now serves you. Its limited power provides minor assistance."
            },
            "Elite": {
                "S": "An elite shadow soldier with exceptional abilities. Provides significant exercise reduction.",
                "A": "A high-ranking elite shadow with strong abilities. Provides good exercise reduction.",
                "B": "A skilled elite shadow with useful abilities. Provides moderate exercise reduction.",
                "C": "A competent elite shadow with decent abilities. Provides modest exercise reduction.",
                "D": "A basic elite shadow with some abilities. Provides minor exercise reduction.",
                "E": "A novice elite shadow with limited abilities. Provides minimal exercise reduction."
            },
            "Normal": {
                "S": "A shadow soldier with surprising strength. Provides good exercise reduction.",
                "A": "A shadow soldier with notable abilities. Provides decent exercise reduction.",
                "B": "A shadow soldier with reliable abilities. Provides moderate exercise reduction.",
                "C": "A shadow soldier with basic abilities. Provides modest exercise reduction.",
                "D": "A shadow soldier with simple abilities. Provides minor exercise reduction.",
                "E": "A shadow soldier with very limited abilities. Provides minimal exercise reduction."
            }
        }
        
        summon_type = summon.get('type', 'Normal')
        summon_rank = summon.get('rank', 'E')
        
        type_descriptions = descriptions.get(summon_type, descriptions['Normal'])
        description = type_descriptions.get(summon_rank, type_descriptions['E'])
        
        # If Red rank, override description
        if summon_rank == "Red":
            description = "A legendary red-rank shadow of immense power. Dramatically reduces required exercises."
        
        # Add ability text
        if attr == "STR":
            ability_text = "\n\nAbility: Reduces STR exercise requirements by up to 60%."
        elif attr == "AGI":
            ability_text = "\n\nAbility: Reduces AGI exercise requirements by up to 60%."
        else:
            ability_text = "\n\nAbility: Reduces all exercise requirements by up to 50%."
        
        self.description_text.config(text=description + ability_text)
        
        # Update image label
        self.detail_image_label.config(text=f"{summon.get('name', 'Unknown')}\n{rank}-Rank {attr}")
        
        # Enable action buttons
        self.activate_button.config(state="normal")
        self.rename_button.config(state="normal")
        
        # Update activate button text based on current state
        if summon.get("active", False):
            self.activate_button.config(text="Deactivate Shadow")
        else:
            self.activate_button.config(text="Activate Shadow")
    
    def toggle_shadow_active(self):
        """Toggle active status of the selected shadow"""
        if not self.selected_summon:
            return
            
        try:
            if os.path.exists("Files/Player Data/Summons.json"):
                with open("Files/Player Data/Summons.json", 'r') as summon_file:
                    summons_data = json.load(summon_file)
                    
                # Get active summons limit
                active_limit = summons_data.get("active_summons_limit", 3)
                
                # Count current active summons
                active_count = sum(1 for s in summons_data["summons"] if s.get("active", False))
                
                # Find the summon to update
                for i, s in enumerate(summons_data["summons"]):
                    if s["name"] == self.selected_summon["name"]:
                        # Toggle active status
                        if s.get("active", False):
                            s["active"] = False
                            message = f"{self.selected_summon['name']} is no longer active"
                            color = "#AAAAAA"
                            self.activate_button.config(text="Activate Shadow")
                        else:
                            # Check if we've hit the limit
                            if active_count >= active_limit and not self.selected_summon.get("active", False):
                                message = f"Maximum of {active_limit} active shadows reached"
                                color = "#FF5555"
                            else:
                                s["active"] = True
                                message = f"{self.selected_summon['name']} is now active for dungeons"
                                color = "#00FF00"
                                self.activate_button.config(text="Deactivate Shadow")
                        break
                
                # Save changes
                with open("Files/Player Data/Summons.json", 'w') as summon_file:
                    json.dump(summons_data, summon_file, indent=4)
                
                # Show message
                message_label = Label(
                    self.right_frame,
                    text=message,
                    fg=color,
                    bg="#1E1E1E",
                    font=("Montserrat Regular", 10)
                )
                message_label.place(relx=0.5, rely=0.9, anchor="center")
                self.parent_window.after(2000, message_label.destroy)
                
                # Reload summons and update UI
                self.load_summons()
                self.populate_shadow_list()
                
                # Update summary
                active_count = sum(1 for s in self.summons if s.get("active", False))
                self.active_label.config(
                    text=f"Active: {active_count}/{active_limit}",
                    fg="#FFFFFF" if active_count < active_limit else "#FF5555"
                )
                
                # Get the updated shadow for selection
                for s in self.summons:
                    if s["name"] == self.selected_summon["name"]:
                        self.selected_summon = s
                        break
                
        except Exception as e:
            print(f"Error toggling shadow active: {e}")
    
    def rename_shadow(self):
        """Show a dialog to rename the selected shadow"""
        if not self.selected_summon:
            return
            
        # Create rename dialog
        rename_window = Toplevel(self.parent_window)
        rename_window.title("Rename Shadow")
        rename_window.geometry("300x150")
        rename_window.configure(bg="#1E1E1E")
        rename_window.overrideredirect(True)
        
        # Shadow name
        name_label = Label(
            rename_window,
            text=f"Rename {self.selected_summon.get('name', 'Unknown')}",
            fg="#FFFFFF",
            bg="#1E1E1E",
            font=("Montserrat Bold", 12)
        )
        name_label.pack(pady=10)
        
        # Name entry
        name_entry = Entry(
            rename_window,
            bg="#333333",
            fg="#FFFFFF",
            font=("Montserrat Regular", 10),
            width=30
        )
        name_entry.insert(0, self.selected_summon.get('name', 'Unknown'))
        name_entry.pack(pady=10)
        
        # Button frame
        button_frame = Frame(rename_window, bg="#1E1E1E")
        button_frame.pack(pady=10)
        
        # Save button
        def save_name():
            new_name = name_entry.get().strip()
            if not new_name:
                return
                
            # Update name in JSON
            try:
                if os.path.exists("Files/Player Data/Summons.json"):
                    with open("Files/Player Data/Summons.json", 'r') as summon_file:
                        summons_data = json.load(summon_file)
                        
                    # Find the summon to update
                    for i, s in enumerate(summons_data["summons"]):
                        if s["name"] == self.selected_summon["name"]:
                            s["name"] = new_name
                            break
                    
                    # Save changes
                    with open("Files/Player Data/Summons.json", 'w') as summon_file:
                        json.dump(summons_data, summon_file, indent=4)
                    
                    # Update UI
                    self.load_summons()
                    self.populate_shadow_list()
                    
                    # Get the updated shadow for selection
                    for s in self.summons:
                        if s["name"] == new_name:
                            self.select_shadow(s)
                            break
            except Exception as e:
                print(f"Error renaming shadow: {e}")
            
            rename_window.destroy()
        
        save_button = Button(
            button_frame,
            text="Save",
            bg=self.transp_clr,
            fg="#FFFFFF",
            font=("Montserrat Bold", 10),
            command=save_name,
            width=10
        )
        save_button.pack(side="left", padx=5)
        
        # Cancel button
        cancel_button = Button(
            button_frame,
            text="Cancel",
            bg="#333333",
            fg="#FFFFFF",
            font=("Montserrat Regular", 10),
            command=rename_window.destroy,
            width=10
        )
        cancel_button.pack(side="right", padx=5)
        
        # Center window
        rename_window.geometry("+%d+%d" % (
            self.parent_window.winfo_rootx() + 275,
            self.parent_window.winfo_rooty() + 250
        ))
        
        # Set focus to entry
        name_entry.focus_set()
        name_entry.select_range(0, "end")
    
    def rank_value(self, rank):
        """Convert rank letter to numeric value for sorting"""
        rank_values = {
            "E": 1,
            "D": 2,
            "C": 3, 
            "B": 4,
            "A": 5,
            "S": 6,
            "Red": 7
        }
        return rank_values.get(rank, 0)
    
    def rank_color(self, rank):
        """Return color based on rank"""
        rank_colors = {
            "E": "#00AA00",  # Green
            "D": "#00AAAA",  # Cyan
            "C": "#0088FF",  # Blue
            "B": "#AA00AA",  # Purple
            "A": "#FF8800",  # Orange
            "S": "#FF0000",  # Red
            "Red": "#FF0055"  # Crimson
        }
        return rank_colors.get(rank, "#FFFFFF")
    
    def attr_color(self, attr):
        """Return color based on attribute"""
        attr_colors = {
            "STR": "#FF6666",
            "AGI": "#66FF66",
            "INT": "#6666FF"
        }
        return attr_colors.get(attr, "#FFFFFF")

# Create shadow manager
try:
    shadow_manager = ShadowManager(canvas, window, transp_clr)
except Exception as e:
    print(f"Error creating shadow manager: {e}")
    # Show error message
    canvas.create_text(
        433.0, 300.0,
        text=f"Error loading shadow management:\n{str(e)}",
        fill="#FF5555",
        font=("Montserrat Regular", 12),
        justify="center"
    )

# Add close button (same style as inventory)
try:
    button_image_26 = PhotoImage(file=relative_to_assets("button_26.png"))
    button_26 = Button(
        image=button_image_26,
        borderwidth=0,
        highlightthickness=0,
        command=ex_close,
        relief="flat"
    )
    button_26.place(x=806.0, y=64.0, width=20.0, height=20.0)
except Exception as e:
    print(f"Error loading button image: {e}")
    # Create fallback close button
    button_26 = Button(
        window,
        text="X",
        bg="#FF3333",
        fg="#FFFFFF",
        font=("Montserrat Bold", 10),
        command=ex_close,
        relief="flat"
    )
    button_26.place(x=806.0, y=64.0, width=20.0, height=20.0)

window.resizable(False, False)
window.mainloop()