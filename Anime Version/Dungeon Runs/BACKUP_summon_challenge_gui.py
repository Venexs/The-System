# Enhanced Dungeon System
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, StringVar, Frame, Label, RIGHT, LEFT, X, Y, BOTTOM, TOP, END, NORMAL, HIDDEN, BOTH, VERTICAL, HORIZONTAL, SOLID, Scrollbar
import ujson
import csv
import subprocess
import random
import cv2
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import threading
import sys
import os
import time
import math
import json

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

stop_event=threading.Event()




class DungeonSystem:
    def __init__(self, window):
        self.window = window
        self.initial_height = 0
        self.target_height = 369
        self.window_width = 879
        
        self.window.geometry(f"{self.window_width}x{self.initial_height}")
        
        self.job = thesystem.misc.return_status()["status"][1]["job"]
        self.setup_window_style()
        
        # Dungeon state tracking
        self.waves = {}
        self.XP_val = 0
        self.wave_completion_percentages = {}  # Track completion % for each wave
        self.mob = 1
        self.current_wave = 1
        self.total_waves = 0
        self.boss_defeated = False
        self.rank = ""
        self.rew_rank = 'X'
        self.type_of_dun = ""
        self.time_remaining = None  # Will be set in setup_dungeon_timer
        self.timer_active = False
        self.activity_completed = [False, False, False, False]
        self.boss_phase = 0
        self.boss_max_phases = 0
        self.dungeon_modifiers = []
        self.dungeon_events = []
        self.current_event = None
        self.dungeon_seed = random.randint(1, 10000)
        
        # Setup UI elements
        self.create_canvas()
        self.setup_video_player()
        self.load_images()
        self.create_ui_elements()
        self.setup_animation()
        self.start_dungeon()
        
        # Generate dungeon events and modifiers after rank is set
        self.roll_dungeon_modifiers()

            
    def setup_window_style(self):
        top_val='dailyquest.py'
        self.all_prev=''
        self.video='Video'
        self.transp_clr='#0C679B'

        if self.job!='None':
            top_val=''
            self.all_prev='alt_'
            self.video='Alt Video'
            self.transp_clr='#652AA3'

        thesystem.system.make_window_transparent(self.window, self.transp_clr)

        with open("Files/Player Data/Settings.json", 'r') as settings_open:
            setting_data=ujson.load(settings_open)

        if setting_data["Settings"]["Performernce (ANIME):"] == "True":
            self.top_images = [f"thesystem/{self.all_prev}top_bar/{top_val}{str(2).zfill(4)}.png"]
            self.bottom_images = [f"thesystem/{self.all_prev}bottom_bar/{str(2).zfill(4)}.png"]

        else:
            self.top_images = [f"thesystem/{self.all_prev}top_bar/{top_val}{str(i).zfill(4)}.png" for i in range(2, 501, 4)]
            self.bottom_images = [f"thesystem/{self.all_prev}bottom_bar/{str(i).zfill(4)}.png" for i in range(2, 501, 4)]


        thesystem.system.animate_window_open(self.window, self.target_height, self.window_width, step=30, delay=1)

        self.window.configure(bg="#FFFFFF")
        self.window.attributes('-alpha', 0.8)
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)

    def create_canvas(self):
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=369,
            width=879,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
    def load_images(self):
        # Preload top and bottom images
        self.top_preloaded_images = thesystem.system.preload_images(self.top_images, (970, 40))
        self.bottom_preloaded_images = thesystem.system.preload_images(self.bottom_images, (970, 40))

        
        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(199.99966430664062, 61.0, image=self.image_image_3)
        
        # Load button images
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.ex_close(),
            relief="flat"
        )
        self.button_1.place(x=669.0, y=295.0, width=127.0, height=22.0)
        
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.next_wave(),
            relief="flat"
        )
        self.button_2.place(x=646.0, y=264.0, width=150.0, height=22.0)
        
        # Load side bars
        self.side = PhotoImage(file=relative_to_assets("blue.png"))
        if self.job.upper() != "NONE":
            self.side = PhotoImage(file=relative_to_assets("purple.png"))
            
        self.canvas.create_image(4.0, 180.0, image=self.side)
        self.canvas.create_image(850.0, 196.0, image=self.side)
        
        self.image_40 = thesystem.system.side_bar("left_bar.png", (75, 320))
        self.canvas.create_image(12.0, 180.0, image=self.image_40)
        
        self.image_50 = thesystem.system.side_bar("right_bar.png", (80, 340))
        self.canvas.create_image(833.0, 190.0, image=self.image_50)
        
    def setup_video_player(self):
        with open("Files/Mod/presets.json", 'r') as pres_file:
            pres_file_data = ujson.load(pres_file)
            self.normal_font_col = pres_file_data["Anime"]["Normal Font Color"]
            video_path = pres_file_data["Anime"][self.video]
        self.player = thesystem.system.VideoPlayer(self.canvas, video_path, 478.0, 213.0)
        
    def create_ui_elements(self):
        # Create UI text elements
        self.canvas.create_rectangle(0.0, -30.0, 957.0, 30.0, fill=self.transp_clr, outline="")
        self.canvas.create_rectangle(0.0, 353.0, 925.0, 555.0, fill=self.transp_clr, outline="")
        
        # Create dungeon information text
        self.dungeon_info_text = self.canvas.create_text(
            65.99966430664062, 88.0,
            anchor="nw",
            text="Loading Dungeon...",
            fill=self.normal_font_col,
            font=("Montserrat Bold", 13 * -1)
        )
        
        # Create wave text
        self.waves_txt = self.canvas.create_text(
            89.99966430664062, 122.0,
            anchor="nw",
            text="[Wave - ?]",
            fill=self.normal_font_col,
            font=("Montserrat Medium", 14 * -1)
        )
        
        # Create enemy text
        self.enemy = self.canvas.create_text(
            89.99966430664062, 152.0,
            anchor="nw",
            text="Preparing to enter dungeon...",
            fill=self.normal_font_col,
            font=("Montserrat Medium", 14 * -1)
        )
        
        # Create instruction text
        self.instruction_text = self.canvas.create_text(
            89.99966430664062, 172.0,
            anchor="nw",
            text="Do the activities below to generate enough [STR/AGI] to defeat them",
            fill=self.normal_font_col,
            font=("Montserrat Medium", 14 * -1)
        )
        
        # Create activity texts
        self.activity1 = self.canvas.create_text(
            109.99966430664062, 204.0,
            anchor="nw",
            text="-Activity 0",
            fill=self.normal_font_col,
            font=("Montserrat Regular", 14 * -1)
        )
        
        self.activity2 = self.canvas.create_text(
            109.99966430664062, 224.0,
            anchor="nw",
            text="-Activity 1",
            fill=self.normal_font_col,
            font=("Montserrat Regular", 14 * -1)
        )
        
        self.activity3 = self.canvas.create_text(
            109.99966430664062, 244.0,
            anchor="nw",
            text="-Activity 2",
            fill=self.normal_font_col,
            font=("Montserrat Regular", 14 * -1)
        )
        
        self.activity4 = self.canvas.create_text(
            109.99966430664062, 264.0,
            anchor="nw",
            text="-Activity 3",
            fill=self.normal_font_col,
            font=("Montserrat Regular", 14 * -1)
        )

        self.checkbox_image_unchecked = PhotoImage(file=relative_to_assets("checkbox_unchecked.png"))
        self.checkbox_image_checked = PhotoImage(file=relative_to_assets("checkbox_checked.png"))
        
        self.checkbox1 = self.canvas.create_image(
            90.99966430664062, 204.0,
            image=self.checkbox_image_unchecked,
            anchor="nw",
            tags="checkbox1"
        )
        
        self.checkbox2 = self.canvas.create_image(
            90.99966430664062, 224.0,
            image=self.checkbox_image_unchecked,
            anchor="nw",
            tags="checkbox2"
        )
        
        self.checkbox3 = self.canvas.create_image(
            90.99966430664062, 244.0,
            image=self.checkbox_image_unchecked,
            anchor="nw",
            tags="checkbox3"
        )
        
        self.checkbox4 = self.canvas.create_image(
            90.99966430664062, 264.0,
            image=self.checkbox_image_unchecked,
            anchor="nw",
            tags="checkbox4"
        )
        
        # Bind click events to checkboxes
        self.canvas.tag_bind("checkbox1", "<ButtonPress-1>", lambda event: self.toggle_activity(0))
        self.canvas.tag_bind("checkbox2", "<ButtonPress-1>", lambda event: self.toggle_activity(1))
        self.canvas.tag_bind("checkbox3", "<ButtonPress-1>", lambda event: self.toggle_activity(2))
        self.canvas.tag_bind("checkbox4", "<ButtonPress-1>", lambda event: self.toggle_activity(3))
        
        # Create timer text (visible by default now)
        self.timer_label = self.canvas.create_text(
            621.9996337890625, 53.0,
            anchor="nw",
            text="Time Left:",
            fill=self.normal_font_col,
            font=("Montserrat Regular", 12 * -1),
            state="normal"  # Make visible
        )
        
        self.timer_text = self.canvas.create_text(
            621.9996337890625, 65.0,
            anchor="nw",
            text="10:00",  # Initial display set to 10 minutes
            fill=self.normal_font_col,
            font=("Montserrat Bold", 32 * -1),
            state="normal"  # Make visible
        )
        
        # Create event text (hidden by default)
        self.event_text = self.canvas.create_text(
            89.99966430664062, 284.0,
            anchor="nw",
            text="",
            fill="#FF5733",
            font=("Montserrat Bold", 14 * -1),
            state="hidden"
        )
        
        # Create progress bar (for boss phases) - Moved to top (y=40)
        self.boss_progress_bg = self.canvas.create_rectangle(
            90, 40, 290, 50,
            fill="#333333",
            outline="",
            state="hidden"
        )

        self.boss_progress_fg = self.canvas.create_rectangle(
            90, 40, 290, 50,  # Start full and will deplete to the left
            fill="#FF0000",
            outline="",
            state="hidden"
        )

        self.boss_progress_text = self.canvas.create_text(
            190, 38,
            anchor="s",
            text="BOSS HEALTH",
            fill="#FFFFFF",
            font=("Montserrat Bold", 10 * -1),
            state="hidden"
        )

    def toggle_activity(self, activity_index):
        """Toggle completion status of an activity"""
        self.activity_completed[activity_index] = not self.activity_completed[activity_index]
        checkboxes = [self.checkbox1, self.checkbox2, self.checkbox3, self.checkbox4]
        if self.activity_completed[activity_index]:
            self.canvas.itemconfig(checkboxes[activity_index], image=self.checkbox_image_checked)
        else:
            self.canvas.itemconfig(checkboxes[activity_index], image=self.checkbox_image_unchecked)

    def setup_animation(self):
        self.image_index = 0
        self.bot_image_index = 0
        
        self.top_image = self.canvas.create_image(
            510.0,
            10.0,
            image=self.top_preloaded_images[self.image_index]
        )  
        self.canvas.tag_bind(self.top_image, "<ButtonPress-1>", self.start_move)
        self.canvas.tag_bind(self.top_image, "<B1-Motion>", self.move_window)
        
        self.bottom_image = self.canvas.create_image(
            500.0,
            353.0,
            image=self.bottom_preloaded_images[self.bot_image_index]
        )
        
    def update_images(self):
        self.image_index = (self.image_index + 1) % len(self.top_preloaded_images)
        self.canvas.itemconfig(self.top_image, image=self.top_preloaded_images[self.image_index])
        self.bot_image_index = (self.bot_image_index + 1) % len(self.bottom_preloaded_images)
        self.canvas.itemconfig(self.bottom_image, image=self.bottom_preloaded_images[self.bot_image_index])
        self.window.after(1000 // 24, self.update_images)
        
    def start_move(self, event):
        self.lastx = event.x_root
        self.lasty = event.y_root
        
    def move_window(self, event):
        deltax = event.x_root - self.lastx
        deltay = event.y_root - self.lasty
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry("+%s+%s" % (x, y))
        self.lastx = event.x_root
        self.lasty = event.y_root
        
    def ex_close(self):
        stop_event.set()
        update_thread.join()
        threading.Thread(target=thesystem.system.fade_out, args=(self.window, 0.8)).start()
        subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
        thesystem.system.animate_window_close(self.window, 0, self.window_width, step=20, delay=1)
        subprocess.Popen(['python', 'Anime Version/Message/gui.py'])
        
    def start_dungeon(self):
        self.hide_activities_and_checkboxes()
        self.canvas.itemconfig(self.instruction_text, state="hidden")
        self.canvas.itemconfig(self.enemy, text="Scanning dungeon environment...")
        self.window.after(1000, lambda: self.canvas.itemconfig(self.enemy, text="Detecting enemy signatures..."))
        self.window.after(2000, lambda: self.canvas.itemconfig(self.enemy, text="Evaluating dungeon difficulty..."))
        self.window.after(3000, self.determine_dungeon_type)
        
    def hide_activities_and_checkboxes(self):
        self.canvas.itemconfig(self.activity1, state="hidden")
        self.canvas.itemconfig(self.activity2, state="hidden")
        self.canvas.itemconfig(self.activity3, state="hidden")
        self.canvas.itemconfig(self.activity4, state="hidden")
        self.canvas.itemconfig(self.checkbox1, state="hidden")
        self.canvas.itemconfig(self.checkbox2, state="hidden")
        self.canvas.itemconfig(self.checkbox3, state="hidden")
        self.canvas.itemconfig(self.checkbox4, state="hidden")

    def show_activities_and_checkboxes(self):
        self.canvas.itemconfig(self.activity1, state="normal")
        self.canvas.itemconfig(self.activity2, state="normal")
        self.canvas.itemconfig(self.activity3, state="normal")
        self.canvas.itemconfig(self.activity4, state="normal")
        self.canvas.itemconfig(self.checkbox1, state="normal")
        self.canvas.itemconfig(self.checkbox2, state="normal")
        self.canvas.itemconfig(self.checkbox3, state="normal")
        self.canvas.itemconfig(self.checkbox4, state="normal")

    def determine_dungeon_type(self):
        with open("Files/Data/Dungeon_Rank.csv", 'r') as rank_file:
            rank_file_reader = csv.reader(rank_file)
            for k in rank_file_reader:
                self.rank = k[0]
                self.type_of_dun = k[1]
                self.rew_rank = self.rank
                
        themes = {
            "E": ["Novice's Path", "Training Grounds", "Beginner's Trial"],
            "D": ["Warrior's Test", "Proving Grounds", "Challenger's Path"],
            "C": ["Veteran's Trial", "Battle Arena", "Survival Gauntlet"],
            "B": ["Elite Proving", "Master's Challenge", "Champion's Trial"],
            "A": ["Hero's Journey", "Legend's Path", "Ultimate Challenge"],
            "S": ["Godslayer's Trial", "Mythic Realm", "Transcendent Domain"],
            "Red": ["Crimson Nightmare", "Bloodthirsty Abyss", "Scarlet Doom"]
        }
        
        dungeon_name = random.choice(themes.get(self.rank, ["Unknown Dungeon"]))
        self.canvas.itemconfig(
            self.dungeon_info_text, 
            text=f"{self.rank}-Rank │ {self.type_of_dun} Dungeon: {dungeon_name}"
        )
        self.generate_waves()
        self.show_current_wave()
        # Start the timer after dungeon type is determined
        self.setup_dungeon_timer()
        
    def generate_waves(self):
        if self.rank == "Red":
            return
            
        base_waves = 3
        if self.rank in ["D", "C"]:
            base_waves = 6
        elif self.rank in ["B", "A"]:
            base_waves = 8
        elif self.rank == "S":
            base_waves = 10
            
        wave_variation = random.choice([-1, 0, 0, 0, 1])
        total_waves = max(3, base_waves + wave_variation)
        self.total_waves = total_waves
        
        with open("Files/Data/Dungeon_Boss_List.json", 'r') as monster_file:
            monster_file_data = ujson.load(monster_file)
            monster_names = list(monster_file_data.keys())
            
        normal_monsters = {}
        elite_monsters = {}
        boss_candidates = {}
        
        if self.rank == 'E': boss_rank = 'D'
        elif self.rank == 'D': boss_rank = 'C'
        elif self.rank == 'C': boss_rank = 'B'
        elif self.rank == 'B': boss_rank = 'A'
        elif self.rank == 'A': boss_rank = 'S'
        elif self.rank == 'S': boss_rank = 'S'
        
        for monster_name in monster_names:
            monster = monster_file_data[monster_name]
            if monster["rank"] == self.rank and monster["type"] == 'Normal':
                normal_monsters[monster_name] = monster
            if monster["rank"] == self.rank and monster["type"] == 'Elite':
                elite_monsters[monster_name] = monster
            if monster["rank"] == boss_rank and monster["type"] == 'Boss':
                boss_candidates[monster_name] = monster
                
        if not elite_monsters:
            elite_monsters = normal_monsters
        
        self.waves = {}
        first_monster = random.choice(list(normal_monsters.keys()))
        self.waves['1'] = {first_monster: monster_file_data[first_monster]}
        self.XP_val += monster_file_data[first_monster]['XP']
        
        for wave_num in range(2, total_waves):
            elite_chance = (wave_num - 1) / total_waves
            if random.random() < elite_chance and elite_monsters:
                monster_name = random.choice(list(elite_monsters.keys()))
                self.waves[str(wave_num)] = {monster_name: monster_file_data[monster_name]}
                self.XP_val += int(monster_file_data[monster_name]['XP'] * 1.5)
            else:
                monster_name = random.choice(list(normal_monsters.keys()))
                self.waves[str(wave_num)] = {monster_name: monster_file_data[monster_name]}
                self.XP_val += monster_file_data[monster_name]['XP']
        
        boss_name = random.choice(list(boss_candidates.keys()))
        self.waves['Final'] = {boss_name: monster_file_data[boss_name]}
        self.XP_val += monster_file_data[boss_name]['XP'] * 2
        
        boss_monster = monster_file_data[boss_name]
        if self.rank in ["A", "S"]:
            self.boss_max_phases = 3
        elif self.rank in ["B", "C"]:
            self.boss_max_phases = 2
        else:
            self.boss_max_phases = 1
        
    def roll_dungeon_modifiers(self):
        all_modifiers = [
            {"name": "Poisonous Mist", "description": "The air is filled with poisonous mist. Each exercise feels harder than normal."},
            {"name": "Reinforced Enemies", "description": "Enemies have increased health and require more effort to defeat."},
            {"name": "Sacred Ground", "description": "This holy ground increases your strength by 20%."},
            {"name": "Treasure Hoard", "description": "This dungeon contains extra treasures, increasing coin rewards by 50%."},
            {"name": "Unstable Reality", "description": "Reality shifts around you. Activities may change unexpectedly."},
            {"name": "Darkness", "description": "Visibility is reduced. You must rely on your other senses."},
            {"name": "Time Distortion", "description": "Time flows differently here. Timer may speed up or slow down."},
            {"name": "Elemental Influence", "description": "The dungeon is infused with elemental energy, changing exercise requirements."}
        ]
        
        all_events = [
            {"name": "Ambush", "description": "You've been ambushed! Complete an extra exercise to escape!"},
            {"name": "Treasure Chest", "description": "You found a treasure chest! Extra rewards available."},
            {"name": "Collapsing Ceiling", "description": "The ceiling is collapsing! Complete the next exercise faster!"},
            {"name": "Healing Spring", "description": "You found a healing spring. Take a short rest before continuing."},
            {"name": "Environmental Hazard", "description": "Watch out for traps! Modify your exercise approach."},
            {"name": "Reinforcements", "description": "Enemy reinforcements have arrived! Additional challenge ahead."},
            {"name": "Magical Surge", "description": "A magical surge empowers you! Next exercise has increased effect."},
            {"name": "Hidden Passage", "description": "You found a hidden passage! Choose which enemy to skip."}
        ]
        
        num_modifiers = 0
        if self.rank in ["E", "D"]:
            num_modifiers = 2
        elif self.rank in ["C", "B"]:
            num_modifiers = 3
        elif self.rank in ["A"]:
            num_modifiers = 4
        elif self.rank in ["S"]:
            num_modifiers = 6

        self.dungeon_modifiers = random.sample(all_modifiers, min(num_modifiers, len(all_modifiers)))
        
        event_chance = {
            "E": 0.2,
            "D": 0.3,
            "C": 0.4,
            "B": 0.5,
            "A": 0.6,
            "S": 0.7,
        }
        
        available_events = all_events
        if self.rank in ["E", "D"]:
            available_events = all_events[:4]
        
        self.dungeon_events = []
        for wave in range(1, self.total_waves):
            if random.random() < event_chance.get(self.rank, 0.3):
                event = random.choice(available_events)
                self.dungeon_events.append({"wave": wave, "event": event})
    
    def setup_dungeon_timer(self):
        # Set timer to 10 minutes (600 seconds) for all ranks
        self.time_remaining = 600  # 10 minutes in seconds
        self.timer_active = True
        # Make timer visible
        self.canvas.itemconfig(self.timer_label, state="normal")
        self.canvas.itemconfig(self.timer_text, state="normal")
        self.update_timer()
    
    def update_timer(self):
        if not self.timer_active or self.time_remaining is None:
            return
            
        minutes, seconds = divmod(self.time_remaining, 60)
        time_str = f"{minutes:02}:{seconds:02}"
        self.canvas.itemconfig(self.timer_text, text=time_str)
        
        if self.time_remaining <= 0:
            self.timer_active = False
            self.fail_dungeon("Time has run out! Dungeon failed.")
            return
            
        if self.time_remaining <= 60:  # Last minute
            self.canvas.itemconfig(self.timer_text, fill="#FF0000")
        elif self.time_remaining <= 180:  # Last 3 minutes
            self.canvas.itemconfig(self.timer_text, fill="#FFA500")
            
        self.time_remaining -= 1
        self.window.after(1000, self.update_timer)  # Update every second
    
    def fail_dungeon(self, message):
        self.canvas.itemconfig(self.enemy, text=message)
        self.canvas.itemconfig(self.instruction_text, text="Dungeon failed. Return to prepare better.")
        self.canvas.itemconfig(self.activity1, text="")
        self.canvas.itemconfig(self.activity2, text="")
        self.canvas.itemconfig(self.activity3, text="")
        self.canvas.itemconfig(self.activity4, text="")
        self.button_2.destroy()
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.ex_close(),
            relief="flat"
        )
        self.button_2.place(x=646.0, y=264.0, width=150.0, height=22.0)
    
    def show_current_wave(self):
        if self.mob > len(self.waves) - 1:
            self.show_boss_wave()
            return

        wave_num = str(self.mob)
        if wave_num not in self.waves:
            print(f"Error: Wave {wave_num} not found in waves dictionary: {self.waves.keys()}")
            if 'Final' in self.waves:
                self.show_boss_wave()
            else:
                self.mob = int(list(self.waves.keys())[0])
                wave_num = str(self.mob)
        
        self.canvas.itemconfig(self.waves_txt, text=f"[Wave - {wave_num}/{len(self.waves)}]")
        
        monster_name = list(self.waves[wave_num].keys())[0]
        monster = self.waves[wave_num][monster_name]
        
        if monster.get('swarm', 'No') == 'Yes':
            group_text = "A Swarm"
        else:
            group_text = "A Group"
            
        monster_desc = monster.get('description', '')
        if monster_desc:
            enemy_text = f"{group_text} of {monster_name} has appeared. {monster_desc}"
        else:
            enemy_text = f"{group_text} of {monster_name} has appeared in front of you."
            
        self.canvas.itemconfig(self.enemy, text=enemy_text)
        
        monster_type = monster.get('attribute', 'STR')
        if monster_type == "STR":
            stat_text = "STR"
        elif monster_type == "AGI":
            stat_text = "AGI"
        else:
            stat_text = "STR/AGI"
            
        self.canvas.itemconfig(
            self.instruction_text, 
            text=f"Do the activities below to generate enough {stat_text} to defeat them",
            state="normal"
        )
        
        # Add skip notification
        if hasattr(self, 'skip_notification_text'):
            self.canvas.delete(self.skip_notification_text)
        
        self.skip_notification_text = self.canvas.create_text(
            721.0, 246.0,  # Position above the button
            anchor="center",
            text="Partially complete activities to skip with reduced XP",
            fill="#FFD700",  # Gold color
            font=("Montserrat Regular", 10 * -1)
        )
        
        self.generate_activities(monster_type)
        self.show_activities_and_checkboxes()
        self.check_for_events()
        
    def show_boss_wave(self):
        self.canvas.itemconfig(self.waves_txt, text=f"[Wave - FINAL]")
        boss_name = list(self.waves["Final"].keys())[0]
        boss = self.waves["Final"][boss_name]
        
        if self.boss_max_phases > 1:
            phase_text = f" - PHASE {self.boss_phase + 1}/{self.boss_max_phases}"
        else:
            phase_text = ""
            
        boss_desc = boss.get('description', '')
        if boss_desc:
            enemy_text = f"BOSS: {boss_name}{phase_text} has appeared! {boss_desc}"
        else:
            enemy_text = f"BOSS: {boss_name}{phase_text} has appeared before you!"
            
        self.canvas.itemconfig(self.enemy, text=enemy_text)
        
        boss_type = boss.get('attribute', 'STR')
        if boss_type == "STR":
            stat_text = "STR"
        elif boss_type == "AGI":
            stat_text = "AGI"
        else:
            stat_text = "STR/AGI"
            
        self.canvas.itemconfig(
            self.instruction_text, 
            text=f"The final challenge! Generate enough {stat_text} to defeat the boss!",
            state="normal"
        )
        
        # Add boss warning notification
        if hasattr(self, 'skip_notification_text'):
            self.canvas.delete(self.skip_notification_text)
        
        self.skip_notification_text = self.canvas.create_text(
            721.0, 246.0,  # Position above the button
            anchor="center",
            text="BOSS FIGHT: All activities must be completed",
            fill="#FF0000",  # Red color
            font=("Montserrat Bold", 10 * -1)
        )
        
        if self.boss_max_phases > 1:
            self.canvas.itemconfig(self.boss_progress_bg, state="normal")
            self.canvas.itemconfig(self.boss_progress_fg, state="normal")
            self.canvas.itemconfig(self.boss_progress_text, state="normal")
            progress = 1.0 - (self.boss_phase / self.boss_max_phases)
            progress_width = 200 * progress
            self.canvas.coords(self.boss_progress_fg, 90, 40, 90 + progress_width, 50)
            
        self.generate_activities(boss_type, is_boss=True)
        self.show_activities_and_checkboxes()

    def generate_activities(self, monster_type, is_boss=False):
        self.activity_completed = [False, False, False, False]
        self.canvas.itemconfig(self.checkbox1, image=self.checkbox_image_unchecked)
        self.canvas.itemconfig(self.checkbox2, image=self.checkbox_image_unchecked)
        self.canvas.itemconfig(self.checkbox3, image=self.checkbox_image_unchecked)
        self.canvas.itemconfig(self.checkbox4, image=self.checkbox_image_unchecked)
        
        # Load STR exercises
        with open('Files/Workout/STR_based.json', 'r') as file:
            str_data = ujson.load(file)
        
        # Load AGI exercises
        with open('Files/Workout/AGI_based.json', 'r') as file:
            agi_data = ujson.load(file)
        
        # Format STR exercises
        str_activities = []
        for exercise_name, exercise_details in str_data.items():
            for detail in exercise_details:
                if "amt" in detail:
                    str_activities.append(f"Do {detail['amt']} {exercise_name}")
                elif "time" in detail:
                    str_activities.append(f"Do {exercise_name} for {detail['time']} {detail['timeval']}")
        
        # Format AGI exercises
        agi_activities = []
        for exercise_name, exercise_details in agi_data.items():
            for detail in exercise_details:
                if "amt" in detail:
                    agi_activities.append(f"Do {detail['amt']} {exercise_name}")
                elif "time" in detail:
                    agi_activities.append(f"Do {exercise_name} for {detail['time']} {detail['timeval']}")
        
        # Apply boss modifier if needed
        if is_boss:
            str_activities = [act.replace("10", "15").replace("15", "20").replace("20", "25").replace("30", "45") for act in str_activities]
            agi_activities = [act.replace("10", "15").replace("15", "20").replace("20", "25").replace("30", "45") for act in agi_activities]
        


        if monster_type == "STR":
            activities = random.sample(str_activities, 4)
        elif monster_type == "AGI":
            activities = random.sample(agi_activities, 4)
        else:
            activities = random.sample(str_activities, 2) + random.sample(agi_activities, 2)
            random.shuffle(activities)
        
        self.canvas.itemconfig(self.activity1, text=f"- {activities[0]}")
        self.canvas.itemconfig(self.activity2, text=f"- {activities[1]}")
        self.canvas.itemconfig(self.activity3, text=f"- {activities[2]}")
        self.canvas.itemconfig(self.activity4, text=f"- {activities[3]}")
    
    def check_for_events(self):
        self.current_event = None
        self.canvas.itemconfig(self.event_text, text="", state="hidden")
        for event_info in self.dungeon_events:
            if event_info["wave"] == self.mob:
                self.current_event = event_info["event"]
                self.canvas.itemconfig(
                    self.event_text, 
                    text=f"EVENT: {self.current_event['name']} - {self.current_event['description']}",
                    state="normal"
                )
                break
    
    def next_wave(self):
        is_boss_wave = self.mob > self.total_waves
        
        # For boss waves, require all activities to be completed
        if is_boss_wave:
            if not all(self.activity_completed):
                incomplete_indices = [i for i, completed in enumerate(self.activity_completed) if not completed]
                activity_widgets = [self.activity1, self.activity2, self.activity3, self.activity4]
                for idx in incomplete_indices:
                    self.canvas.itemconfig(activity_widgets[idx], fill="#FF0000")
                self.window.after(500, lambda: [self.canvas.itemconfig(activity_widgets[idx], fill=self.normal_font_col) for idx in incomplete_indices])
                return
        
        # For non-boss waves, calculate completion percentage
        else:
            completed_count = sum(self.activity_completed)
            total_activities = len(self.activity_completed)
            completion_percentage = completed_count / total_activities
            
            # Store the completion percentage for this wave
            self.wave_completion_percentages[self.mob] = completion_percentage
            
            # Show a warning if activities are incomplete
            if completion_percentage < 1.0:
                reduced_xp_percent = int(completion_percentage * 100)
                warning_text = f"Skipping with {reduced_xp_percent}% completion. Reduced XP for this wave!"
                temp_warning = self.canvas.create_text(
                    400, 300,
                    anchor="center",
                    text=warning_text,
                    fill="#FFA500",  # Orange color
                    font=("Montserrat Bold", 14 * -1)
                )
                self.window.after(1500, lambda: self.canvas.delete(temp_warning))
        
        # Proceed to next wave
        if self.mob > self.total_waves:
            self.boss_phase += 1
            if self.boss_phase >= self.boss_max_phases:
                self.complete_dungeon()
            else:
                self.show_boss_wave()
            return
        
        self.mob += 1
        if str(self.mob) not in self.waves and 'Final' not in self.waves:
            print(f"Error: Wave {self.mob} not found and no final boss wave")
            self.complete_dungeon()
            return
        
        if str(self.mob) not in self.waves:
            self.boss_phase = 0
            self.show_boss_wave()
        else:
            self.show_current_wave()
        
    def complete_dungeon(self):
        self.boss_defeated = True
        self.timer_active = False  # Stop the timer when dungeon is completed
        self.canvas.itemconfig(self.boss_progress_bg, state="hidden")
        self.canvas.itemconfig(self.boss_progress_fg, state="hidden")
        self.canvas.itemconfig(self.boss_progress_text, state="hidden")
        self.canvas.itemconfig(self.enemy, text="Victory! All enemies defeated!")
        self.canvas.itemconfig(self.instruction_text, state="hidden")
        self.hide_activities_and_checkboxes()
        
        # Remove skip notification if it exists
        if hasattr(self, 'skip_notification_text'):
            self.canvas.delete(self.skip_notification_text)
        
        # Calculate average completion percentage across all waves
        original_xp = self.XP_val
        
        # If no waves were skipped or partially completed, default to 100%
        if not self.wave_completion_percentages:
            avg_completion = 1.0
        else:
            # Calculate the average completion percentage
            avg_completion = sum(self.wave_completion_percentages.values()) / len(self.wave_completion_percentages)
        
        # Calculate adjusted XP based on completion percentage
        adjusted_xp = int(original_xp * avg_completion)
        
        # Display completion info
        completion_text = self.canvas.create_text(
            400, 250,
            anchor="center",
            text=f"Dungeon Completed with {int(avg_completion * 100)}% activity completion",
            fill="#00FF00",
            font=("Montserrat Bold", 14 * -1)
        )
        
        xp_text = self.canvas.create_text(
            400, 300,
            anchor="center",
            text=f"XP Earned: {adjusted_xp} ({int(avg_completion * 100)}% of {original_xp})",
            fill="#00FF00",
            font=("Montserrat Bold", 14 * -1)
        )
        
        # Update XP and rewards in records with adjusted values
        try:
            with open("Files/Player Data/Status.json", 'r') as status_read_file:
                status_read_data = ujson.load(status_read_file)

            # Define rewards based on rank
            if self.rew_rank == 'E':
                coin = 100
                avp = 1
            elif self.rew_rank == 'D':
                coin = 500
                avp = 2
            elif self.rew_rank == 'C':
                coin = 1000
                avp = 3
            elif self.rew_rank == 'B':
                coin = 5000
                avp = 4
            elif self.rew_rank == 'A':
                coin = 10000
                avp = 5
            elif self.rew_rank == 'S':
                coin = 20000
                avp = 6

            # Apply completion percentage to rewards
            adjusted_coin = int(coin * avg_completion)
            adjusted_avp = max(1, int(avp * avg_completion))  # Ensure at least 1 avp

            # Apply rewards based on dungeon type
            if self.type_of_dun == 'Normal':
                status_read_data["avail_eq"][0]['str_based'] += adjusted_avp
                status_read_data["avail_eq"][0]['int_based'] += adjusted_avp
                status_read_data["status"][0]['XP'] += adjusted_xp
                status_read_data["status"][0]['coins'] += adjusted_coin
                with open("Files/Player Data/status.json", 'w') as fson:
                    ujson.dump(status_read_data, fson, indent=4)
                with open("Files/Checks/Message.csv", 'w', newline='') as check_file:
                    check_fw = csv.writer(check_file)
                    check_fw.writerow(["Quest Completed"])
            elif self.type_of_dun == 'Instance':
                status_read_data["status"][0]['XP'] += (adjusted_xp * 2)
                status_read_data["status"][0]['coins'] += (adjusted_coin * 2)
                status_read_data["avail_eq"][0]['str_based'] += (adjusted_avp * 2)
                status_read_data["avail_eq"][0]['int_based'] += (adjusted_avp * 2)
                with open("Files/Player Data/status.json", 'w') as fson:
                    ujson.dump(status_read_data, fson, indent=4)
                with open("Files/Checks/Message.csv", 'w', newline='') as check_file:
                    check_fw = csv.writer(check_file)
                    check_fw.writerow(["Instance Reward"])

            thesystem.system.get_fin_xp()

        except Exception as e:
            print(f"Error updating records: {e}")
        
        self.button_2.destroy()
        self.button_1.destroy()
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.ex_close(),
            relief="flat"
        )
        self.button_2.place(x=646.0, y=264.0, width=150.0, height=22.0)




class SkillSystem:
    def __init__(self, parent, canvas, normal_font_col):
        self.parent = parent
        self.canvas = canvas
        self.normal_font_col = normal_font_col
        self.active_skills = {}
        self.passive_skills = {}
        self.cooldowns = {}
        self.skill_frame = None
        self.skill_buttons = []
        self.skill_icons = {}
        self.skill_ui_elements = []
        self.skill_panel_visible = False
        
        # Load skills from JSON
        self.load_skills()
        
        # Create skill button in main UI
        self.create_skill_button()
    
    def load_skills(self):
        """Load player skills from Skill.json and all possible skills from Skill_List.json"""
        try:
            with open("Files/Player Data//Skill.json", 'r') as skill_file:
                self.player_skills = json.load(skill_file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.player_skills = {}
        
        try:
            with open("Files/Data/Skill_List.json", 'r') as skill_list_file:
                self.all_skills = json.load(skill_list_file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create default skill list if file doesn't exist
            self.all_skills = {
                "Rush": {
                    "type": "Passive",
                    "cooldown": "24h",
                    "desc": "When your body health decreases and fatigue is high, the skill activates to push adrenaline allowing you to keep going on",
                    "base": "STR"
                },
                "Dash": {
                    "type": "Active",
                    "cooldown": "1h",
                    "desc": "Gives the user the ability to get a faster start in a sprint/run",
                    "base": "STR"
                },
                "Negotiation": {
                    "type": "Active",
                    "cooldown": "12h",
                    "desc": "Allows negotiation with dungeon creatures for better rewards or peaceful passage",
                    "base": "INT"
                },
                "Tactical": {
                    "type": "Active",
                    "cooldown": "6h",
                    "desc": "Analyzes enemy patterns to find weaknesses",
                    "base": "INT"
                },
                "Iron Fist": {
                    "type": "Passive",
                    "cooldown": "24h",
                    "desc": "Increases damage from strength-based activities by 10%",
                    "base": "STR"
                },
                "Iron Warrior": {
                    "type": "Passive",
                    "cooldown": "24h",
                    "desc": "Increases HP by 5% below 50% Max HP for every level upgrade",
                    "base": "STR"
                },
                "Resourceful Adaptation": {
                    "type": "Active",
                    "cooldown": "1h",
                    "desc": "Change workouts in dungeons if needed (random)",
                    "base": "INT"
                },
                "Charismatic Aura": {
                    "type": "Passive",
                    "cooldown": "12h",
                    "desc": "Increases rewards from dungeons by 5% per level",
                    "base": "CHA"
                },
                "Fatal Strike": {
                    "type": "Active",
                    "cooldown": "1h",
                    "desc": "Reduces workout values for oneself by 10% for each level upgrade",
                    "base": "STR"
                },
                "Nimble Endurance": {
                    "type": "Passive",
                    "cooldown": "12h",
                    "desc": "Increases time limit in dungeons by 5% per level",
                    "base": "AGI"
                },
                "Mind Over Matter": {
                    "type": "Active",
                    "cooldown": "3h",
                    "desc": "Convert INT to temporary STR/AGI for one workout wave",
                    "base": "INT"
                },
                "Brute Force Mastery": {
                    "type": "Active",
                    "cooldown": "1h",
                    "desc": "Higher STR stat and Lower AGI stat for a period of time",
                    "base": "STR"
                }
            }
        
        # Sort skills into active and passive
        for skill_name, skill_data in self.player_skills.items():
            if skill_data[0]["type"] == "Active":
                self.active_skills[skill_name] = skill_data
            else:
                self.passive_skills[skill_name] = skill_data
    
    def create_skill_button(self):
        """Create the main skill button in the UI"""
        try:
            self.skill_icon = PhotoImage(file=relative_to_assets("skill_icon.png"))
        except:
            # Create a default skill icon if file not found
            self.skill_icon = PhotoImage(file=relative_to_assets("button_4.png"))
        
        self.skill_button = Button(
            self.parent.window,
            image=self.skill_icon,
            borderwidth=0,
            highlightthickness=0,
            command=self.toggle_skill_panel,
            relief="flat"
        )
        self.skill_button.place(x=650.0, y=32.0, width=150.0, height=22.0)
        
        # Add skill count indicator
        active_count = len(self.active_skills)
        self.skill_count_text = self.canvas.create_text(
            752.0, 40.0,
            anchor="nw",
            text=f"{active_count}",
            fill="#FFFFFF",
            font=("Montserrat Bold", 10 * -1)
        )
    
    def toggle_skill_panel(self):
        """Show or hide the skill panel"""
        if self.skill_panel_visible:
            self.hide_skill_panel()
        else:
            self.show_skill_panel()

    def show_skill_panel(self):
        """Display the skill panel with all player skills and scrollbar"""
        self.skill_panel_visible = True
        
        # Create panel background
        self.skill_panel_bg = self.canvas.create_rectangle(
            500, 60, 800, 250,
            fill="#1E1E1E",
            outline="#333333",
            width=2
        )
        
        # Create panel title
        self.skill_panel_title = self.canvas.create_text(
            650, 70,
            text="SKILLS",
            fill="#FFFFFF",
            font=("Montserrat Bold", 16 * -1),
            anchor="center"
        )
        
        # Create close button
        self.close_panel_button = self.canvas.create_rectangle(
            780, 60, 800, 80,
            fill="#FF3333",
            outline=""
        )
        self.close_panel_x = self.canvas.create_text(
            790, 70,
            text="X",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12 * -1),
            anchor="center"
        )
        self.canvas.tag_bind(self.close_panel_button, "<ButtonPress-1>", lambda e: self.hide_skill_panel())
        self.canvas.tag_bind(self.close_panel_x, "<ButtonPress-1>", lambda e: self.hide_skill_panel())
        
        # Add these to UI elements list
        self.skill_ui_elements.extend([
            self.skill_panel_bg,
            self.skill_panel_title,
            self.close_panel_button,
            self.close_panel_x
        ])
        
        # Create a frame to hold the canvas and scrollbar
        self.skill_frame = Frame(self.parent.window, bg="#1E1E1E")
        self.skill_frame.place(x=510, y=90, width=280, height=150)
        
        # Create a canvas inside the frame
        self.skill_canvas = Canvas(
            self.skill_frame,
            bg="#1E1E1E",
            bd=0,
            highlightthickness=0,
            width=330,
            height=150
        )
        self.skill_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Create a scrollbar and connect it to the canvas
        self.skill_scrollbar = Scrollbar(self.skill_frame, orient=VERTICAL, command=self.skill_canvas.yview)
        self.skill_scrollbar.pack(side=RIGHT, fill=Y)
        self.skill_canvas.configure(yscrollcommand=self.skill_scrollbar.set)
        
        # Create a frame inside the canvas to hold the skill elements
        self.skills_container = Frame(self.skill_canvas, bg="#1E1E1E")
        self.skill_canvas.create_window((0, 0), window=self.skills_container, anchor="nw")
        
        # Add section titles and skills to the container frame
        Label(
            self.skills_container,
            text="ACTIVE SKILLS",
            fg="#00AAFF",
            bg="#1E1E1E",
            font=("Montserrat Bold", 12),
            anchor="w"
        ).pack(fill=X, padx=5, pady=(5, 2))
        
        # Display active skills
        for skill_name, skill_data in self.active_skills.items():
            skill_info = skill_data[0]
            skill_level = skill_info["lvl"]
            
            # Create skill frame
            skill_frame = Frame(self.skills_container, bg="#2A2A2A", bd=1, relief=SOLID)
            skill_frame.pack(fill=X, padx=5, pady=2)
            
            # Create skill name and level
            Label(
                skill_frame,
                text=f"{skill_name} (Lvl {skill_level})",
                fg="#FFFFFF",
                bg="#2A2A2A",
                font=("Montserrat Bold", 12),
                anchor="w"
            ).pack(fill=X, padx=5, pady=(5, 0))
            
            # Create skill description
            Label(
                skill_frame,
                text=skill_info["desc"],
                fg="#CCCCCC",
                bg="#2A2A2A",
                font=("Montserrat Regular", 10),
                anchor="w",
                wraplength=200,
                justify=LEFT
            ).pack(fill=X, padx=5, pady=(0, 5))
            
            # Create use button frame
            btn_frame = Frame(skill_frame, bg="#2A2A2A")
            btn_frame.pack(fill=X, padx=150, pady=(0, 5))
            
            # Create spacer to push button to the right
            Label(btn_frame, bg="#2A2A2A").pack(side=LEFT, expand=True)
            
            # Create use button if not on cooldown
            if skill_name in self.cooldowns and self.cooldowns[skill_name] > datetime.now():
                cooldown_time = self.cooldowns[skill_name] - datetime.now()
                minutes = int(cooldown_time.total_seconds() // 60)
                seconds = int(cooldown_time.total_seconds() % 60)
                cooldown_text = f"CD: {minutes}m {seconds}s"
                
                use_btn = Label(
                    btn_frame,
                    text=cooldown_text,
                    fg="#AAAAAA",
                    bg="#555555",
                    font=("Montserrat Regular", 10),
                    padx=10,
                    pady=5
                )
                use_btn.pack(side=RIGHT)
            else:
                use_btn = Label(
                    btn_frame,
                    text="USE",
                    fg="#FFFFFF",
                    bg="#00AA44",
                    font=("Montserrat Bold", 12),
                    padx=10,
                    pady=5
                )
                use_btn.pack(side=RIGHT)
                
                # Bind click event
                use_btn.bind("<ButtonPress-1>", lambda e, s=skill_name: self.use_skill(s))
        
        # Display passive skills section
        Label(
            self.skills_container,
            text="PASSIVE SKILLS",
            fg="#FFAA00",
            bg="#1E1E1E",
            font=("Montserrat Bold", 12),
            anchor="w"
        ).pack(fill=X, padx=5, pady=(10, 2))
        
        # Display passive skills
        for skill_name, skill_data in self.passive_skills.items():
            skill_info = skill_data[0]
            skill_level = skill_info["lvl"]
            
            # Create skill frame
            skill_frame = Frame(self.skills_container, bg="#2A2A2A", bd=1, relief=SOLID)
            skill_frame.pack(fill=X, padx=5, pady=2)
            
            # Create skill name and level
            Label(
                skill_frame,
                text=f"{skill_name} (Lvl {skill_level}) - Always Active",
                fg="#FFFFFF",
                bg="#2A2A2A",
                font=("Montserrat Bold", 11),
                anchor="w"
            ).pack(fill=X, padx=5, pady=(5, 0))
            
            # Create skill description
            Label(
                skill_frame,
                text=skill_info["desc"],
                fg="#CCCCCC",
                bg="#2A2A2A",
                font=("Montserrat Regular", 9),
                anchor="w",
                wraplength=250,
                justify=LEFT
            ).pack(fill=X, padx=5, pady=(0, 5))
        
        # Update the scrollable region
        self.skills_container.update_idletasks()
        self.skill_canvas.config(scrollregion=self.skill_canvas.bbox("all"))
        
        # Add mousewheel scrolling
        self.skill_canvas.bind_all("<MouseWheel>", lambda event: self.skill_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    def hide_skill_panel(self):
        """Hide the skill panel"""
        self.skill_panel_visible = False
        
        # Delete canvas elements
        for element in self.skill_ui_elements:
            self.canvas.delete(element)
        self.skill_ui_elements = []
        
        # Destroy the skill frame with scrollbar
        if hasattr(self, 'skill_frame') and self.skill_frame is not None:
            self.skill_frame.destroy()
            self.skill_frame = None
        
        # Unbind mousewheel
        self.skill_canvas.unbind_all("<MouseWheel>")
    
    def use_skill(self, skill_name):
        """Use an active skill"""
        if skill_name not in self.active_skills:
            return
            
        # Get cooldown from skill data
        all_skill_data = self.all_skills.get(skill_name, {})
        cooldown_str = self.all_skills.get("cooldown", "5m")
        
        # Parse cooldown time
        minutes = 1
        if "m" in cooldown_str:
            minutes = int(cooldown_str.replace("m", ""))
        
        # Set cooldown
        self.cooldowns[skill_name] = datetime.now() + timedelta(minutes=minutes)
        
        # Apply skill effect
        self.apply_skill_effect(skill_name)
        
        # Hide and show panel to refresh
        self.hide_skill_panel()
        self.show_skill_panel()
        
    def apply_skill_effect(self, skill_name):
        """Apply the effect of the selected skill"""
        # Get the skill level for scaling effects
        skill_level = self.player_skills[skill_name][0]["lvl"] if skill_name in self.player_skills else 1

        if skill_name == "Resourceful Adaptation":
            # Change workout activities randomly
            if hasattr(self.parent, 'generate_activities'):
                monster_type = random.choice(["STR", "AGI", "MIXED"])
                self.parent.generate_activities(monster_type)
                notification = self.parent.canvas.create_text(
                    400, 320,
                    anchor="center",
                    text="Resourceful Adaptation: Activities changed randomly!",
                    fill="#00FFFF",
                    font=("Montserrat Bold", 14 * -1)
                )
                self.parent.window.after(3000, lambda: self.parent.canvas.delete(notification))
                
        elif skill_name == "Fatal Strike":
            # Base reduction: 15% at level 1, +5% per level
            reduction_percent = 15 + (5 * (skill_level - 1))
            reduction_percent = min(50, reduction_percent)  # Cap at 50% reduction
            reduction_factor = reduction_percent / 100.0
            
            # Apply to all activities (both STR and VIT)
            modified_activities = []
            
            for activity_widget in [self.parent.activity1, self.parent.activity2, 
                                self.parent.activity3, self.parent.activity4]:
                activity_text = self.parent.canvas.itemcget(activity_widget, "text")
                
                # Skip empty activities
                if not activity_text or activity_text.startswith("-Activity"):
                    continue
                    
                # Find and reduce the numeric value
                import re
                numbers = re.findall(r'\d+', activity_text)
                if numbers:
                    for num_str in numbers:
                        value = int(num_str)
                        reduced = max(1, int(value * (1 - reduction_factor)))
                        # Only replace the first occurrence of this number
                        new_text = activity_text.replace(str(value), str(reduced), 1)
                        self.parent.canvas.itemconfig(activity_widget, text=new_text, fill="#FF9900")
                        modified_activities.append(activity_widget)
                        break
            
            # After 3 seconds, reset color
            if modified_activities:
                self.parent.window.after(3000, lambda widgets=modified_activities: 
                                    [self.parent.canvas.itemconfig(w, fill=self.parent.normal_font_col) 
                                        for w in widgets])
            
            # Feedback notification
            notification = self.parent.canvas.create_text(
                400, 320,
                anchor="center",
                text=f"Fatal Strike Lvl {skill_level}: All activities reduced by {reduction_percent}%!",
                fill="#FF9900",
                font=("Montserrat Bold", 14 * -1)
            )
            self.parent.window.after(3000, lambda: self.parent.canvas.delete(notification))
            
        elif skill_name == "Brute Force Mastery":
            # Calculate STR buff and AGI debuff based on level
            str_buff_percent = 20 + (10 * (skill_level - 1))  # 20% at lvl 1, +10% per level
            agi_debuff_percent = 10 + (5 * (skill_level - 1))  # 10% at lvl 1, +5% per level
            
            str_buff_percent = min(70, str_buff_percent)  # Cap at 70% buff
            agi_debuff_percent = min(35, agi_debuff_percent)  # Cap at 35% debuff
            
            str_factor = 1 - (str_buff_percent / 100.0)  # Reduction factor for STR (making activities easier)
            agi_factor = 1 + (agi_debuff_percent / 100.0)  # Increase factor for AGI (making activities harder)
            
            modified_activities = []
            
            # Process all activities
            for activity_widget in [self.parent.activity1, self.parent.activity2, 
                                self.parent.activity3, self.parent.activity4]:
                activity_text = self.parent.canvas.itemcget(activity_widget, "text")
                
                # Skip empty activities
                if not activity_text or activity_text.startswith("-Activity"):
                    continue
                    
                is_agi = "Seconds" in activity_text or "seconds" in activity_text
                
                # Apply appropriate factor based on activity type
                import re
                numbers = re.findall(r'\d+', activity_text)
                if numbers:
                    for num_str in numbers:
                        value = int(num_str)
                        
                        if is_agi:
                            # AGI activities get harder (values increase)
                            modified = max(1, int(value * agi_factor))
                            color = "#FF6666"  # Red for debuff
                            self.parent.canvas.itemconfig(activity_widget, text=activity_text.replace(
                                str(value), str(modified), 1), fill=color)
                        else:
                            # STR activities get easier (values decrease)
                            modified = max(1, int(value * str_factor))
                            color = "#66FF66"  # Green for buff
                            self.parent.canvas.itemconfig(activity_widget, text=activity_text.replace(
                                str(value), str(modified), 1), fill=color)
                        
                        modified_activities.append((activity_widget, color))
                        break
            
            # After 3 seconds, reset color
            if modified_activities:
                self.parent.window.after(3000, lambda activities=modified_activities: 
                                    [self.parent.canvas.itemconfig(w[0], fill=self.parent.normal_font_col) 
                                        for w in activities])
            
            # Feedback notification
            notification = self.parent.canvas.create_text(
                400, 320,
                anchor="center",
                text=f"Brute Force Mastery Lvl {skill_level}: STR +{str_buff_percent}%, AGI -{agi_debuff_percent}%",
                fill="#FFCC00",
                font=("Montserrat Bold", 14 * -1)
            )
            self.parent.window.after(3000, lambda: self.parent.canvas.delete(notification))
            
        elif skill_name == "Dash":
            # Calculate reduction based on dungeon rank and skill level
            base_reduction = 30 + (5 * (skill_level - 1))  # 30% at level 1, +5% per level
            
            # Rank penalty (higher ranks get less reduction)
            rank_penalty = {
                "E": 0,    # No penalty for E rank
                "D": 5,    # 5% less reduction
                "C": 10,   # 10% less reduction
                "B": 15,   # 15% less reduction
                "A": 20,   # 20% less reduction
                "S": 25    # 25% less reduction (still usable on S rank in this implementation)
            }
            
            # Get current dungeon rank
            current_rank = self.parent.rank if hasattr(self.parent, 'rank') else "E"
            
            # Calculate final reduction (clamp between 25% and 75%)
            reduction_percent = base_reduction - rank_penalty.get(current_rank, 0)
            reduction_percent = max(25, min(75, reduction_percent))
            reduction_factor = reduction_percent / 100.0
            
            # Find and modify all activities with "Seconds" in them
            modified_activities = []
            
            for activity_widget in [self.parent.activity1, self.parent.activity2, 
                                self.parent.activity3, self.parent.activity4]:
                activity_text = self.parent.canvas.itemcget(activity_widget, "text")
                
                # Skip empty activities
                if not activity_text or activity_text.startswith("-Activity"):
                    continue
                    
                # Check if this is a time-based (AGI) activity
                if "Seconds" in activity_text or "seconds" in activity_text:
                    # Extract the time value
                    import re
                    numbers = re.findall(r'\d+', activity_text)
                    if numbers:
                        for num_str in numbers:
                            value = int(num_str)
                            reduced = max(1, int(value * (1 - reduction_factor)))
                            # Replace just the first occurrence of this number
                            new_text = activity_text.replace(str(value), str(reduced), 1)
                            self.parent.canvas.itemconfig(activity_widget, text=new_text, fill="#FF00FF")
                            modified_activities.append(activity_widget)
                            break
            
            # After 3 seconds, reset color
            if modified_activities:
                self.parent.window.after(3000, lambda widgets=modified_activities: 
                                    [self.parent.canvas.itemconfig(w, fill=self.parent.normal_font_col) 
                                        for w in widgets])
            
            # Feedback notification
            count = len(modified_activities)
            if count > 0:
                feedback = f"Dash Lvl {skill_level}: Reduced {count} time-based activities by {reduction_percent}%!"
            else:
                feedback = "No time-based activities found to reduce!"
                
            notification = self.parent.canvas.create_text(
                400, 320,
                anchor="center",
                text=feedback,
                fill="#FF00FF",
                font=("Montserrat Bold", 14 * -1)
            )
            self.parent.window.after(3000, lambda: self.parent.canvas.delete(notification))
            
        else:
            # Generic skill effect message for other skills
            notification = self.parent.canvas.create_text(
                400, 320,
                anchor="center",
                text=f"Skill '{skill_name}' activated!",
                fill="#FFFFFF",
                font=("Montserrat Bold", 14 * -1)
            )
            self.parent.window.after(3000, lambda: self.parent.canvas.delete(notification))
    
    def remove_brute_force_buff(self):
        """Remove the Brute Force buff after duration expires"""
        if hasattr(self.parent, 'str_buff_active'):
            self.parent.str_buff_active = False
            self.parent.agi_debuff_active = False
            
            # Remove buff text elements
            for element in self.parent.skill_ui_elements:
                self.parent.canvas.delete(element)
            self.parent.skill_ui_elements = []







# Shadow Manager Class for Dungeons
class ShadowManager:
    def __init__(self, parent, canvas, normal_font_col):
        self.parent = parent
        self.canvas = canvas
        self.normal_font_col = normal_font_col
        self.active_summons = []
        self.summon_selection_window = None
        
    def load_summons(self):
        """Load all available shadow soldiers"""
        try:
            import os
            import json
            if os.path.exists("Files/Player Data/Summons.json"):
                with open("Files/Player Data/Summons.json", 'r') as summon_file:
                    summons_data = json.load(summon_file)
                    return summons_data.get("summons", [])
            else:
                # Create default structure if it doesn't exist
                default_data = {
                    "summons": [],
                    "last_updated": "",
                    "total_summons": 0,
                    "max_summons_allowed": 20,
                    "active_summons_limit": 3
                }
                os.makedirs(os.path.dirname("Files/Player Data/Summons.json"), exist_ok=True)
                with open("Files/Player Data/Summons.json", 'w') as summon_file:
                    json.dump(default_data, summon_file, indent=4)
                return []
        except Exception as e:
            print(f"Error loading summons: {e}")
            return []
    
    def show_summon_selection(self):
        """Display a window to select shadow soldiers for the dungeon"""
        import tkinter as tk
        from tkinter import Toplevel, Frame, Label, Button, Canvas, Scrollbar
        
        all_summons = self.load_summons()
        
        if not all_summons:
            # No summons available, just return
            return
        
        # Create summon selection window
        self.summon_selection_window = Toplevel(self.parent.window)
        self.summon_selection_window.title("Select Shadow Soldiers")
        self.summon_selection_window.geometry("600x400")
        self.summon_selection_window.configure(bg="#1E1E1E")
        self.summon_selection_window.overrideredirect(True)
        
        # Create canvas
        canvas = Canvas(
            self.summon_selection_window,
            bg="#1E1E1E",
            height=400,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Top and bottom colored bars
        canvas.create_rectangle(0.0, 0.0, 600.0, 30.0, fill=self.parent.transp_clr, outline="")
        canvas.create_rectangle(0.0, 370.0, 600.0, 400.0, fill=self.parent.transp_clr, outline="")
        
        # Title
        canvas.create_text(
            300, 50,
            text="SELECT SHADOW SOLDIERS",
            fill="#FFFFFF",
            font=("Montserrat Bold", 16),
            anchor="center"
        )
        
        # Instructions
        canvas.create_text(
            300, 80,
            text="Choose up to 3 shadow soldiers to assist you in the dungeon",
            fill="#AAAAAA",
            font=("Montserrat Regular", 12),
            anchor="center"
        )
        
        # Create frame for summons list
        list_frame = Frame(self.summon_selection_window, bg="#2A2A2A")
        list_frame.place(x=50, y=100, width=500, height=200)
        
        # Create a canvas and scrollbar for the list
        list_canvas = Canvas(list_frame, bg="#2A2A2A", highlightthickness=0)
        scrollbar = Scrollbar(list_frame, orient="vertical", command=list_canvas.yview)
        
        list_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        list_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create inner frame for summons
        inner_frame = Frame(list_canvas, bg="#2A2A2A")
        list_canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        # Selected summons list and selection variables
        selected_summons = []
        select_buttons = {}
        max_selected = 3
        
        # Function to handle selection
        def toggle_selection(summon_name):
            if summon_name in selected_summons:
                selected_summons.remove(summon_name)
                select_buttons[summon_name].config(bg="#652AA3", text="Select")
            elif len(selected_summons) < max_selected:
                selected_summons.append(summon_name)
                select_buttons[summon_name].config(bg="#00AA44", text="Selected")
            else:
                # Show max selection message
                canvas.create_text(
                    300, 310,
                    text="You can only select up to 3 shadow soldiers",
                    fill="#FF5555",
                    font=("Montserrat Regular", 12),
                    anchor="center",
                    tags="error_message"
                )
                self.summon_selection_window.after(2000, lambda: canvas.delete("error_message"))
        
        # Add each summon to the list
        for i, summon in enumerate(all_summons):
            summon_frame = Frame(inner_frame, bg="#333333", padx=10, pady=10)
            summon_frame.pack(fill="x", pady=5)
            
            # Name and rank
            name_label = Label(
                summon_frame,
                text=f"{summon['name']} ({summon['rank']}-Rank)",
                fg="#FFFFFF",
                bg="#333333",
                font=("Montserrat Bold", 12),
                anchor="w"
            )
            name_label.pack(fill="x")
            
            # Power and attribute
            stats_label = Label(
                summon_frame,
                text=f"Power: {summon['power']} | Type: {summon['attribute']} | Level: {summon['level']}",
                fg="#AAAAAA",
                bg="#333333",
                font=("Montserrat Regular", 10),
                anchor="w"
            )
            stats_label.pack(fill="x")
            
            # Loyalty
            loyalty_label = Label(
                summon_frame,
                text=f"Loyalty: {summon['loyalty']}%",
                fg="#FFAA00",
                bg="#333333",
                font=("Montserrat Regular", 10),
                anchor="w"
            )
            loyalty_label.pack(fill="x")
            
            # Check if already active
            is_active = summon.get('active', False)
            
            # Select button
            select_button = Button(
                summon_frame,
                text="Selected" if is_active else "Select",
                bg="#00AA44" if is_active else "#652AA3",
                fg="#FFFFFF",
                font=("Montserrat Bold", 10),
                command=lambda name=summon['name']: toggle_selection(name),
                width=10
            )
            select_button.pack(anchor="e", pady=5)
            
            # Store button reference
            select_buttons[summon['name']] = select_button
            
            # Pre-select active summons
            if is_active:
                selected_summons.append(summon['name'])
        
        # Update canvas scroll region
        inner_frame.update_idletasks()
        list_canvas.config(scrollregion=list_canvas.bbox("all"))
        
        # Continue button
        def continue_to_dungeon():
            # Store selected summons for use in dungeon
            self.active_summons = []
            for summon in all_summons:
                if summon['name'] in selected_summons:
                    summon_copy = summon.copy()  # Create a copy to avoid modifying original
                    summon_copy['active'] = True
                    self.active_summons.append(summon_copy)
                    
                    # Also update the original summon in the JSON file
                    try:
                        import json
                        import os
                        if os.path.exists("Files/Player Data/Summons.json"):
                            with open("Files/Player Data/Summons.json", 'r') as summon_file:
                                summons_data = json.load(summon_file)
                                
                            # Update the active status
                            for s in summons_data["summons"]:
                                if s["name"] == summon['name']:
                                    s["active"] = True
                                elif s["name"] not in selected_summons and s.get("active", False):
                                    s["active"] = False
                                    
                            # Save changes
                            with open("Files/Player Data/Summons.json", 'w') as summon_file:
                                json.dump(summons_data, summon_file, indent=4)
                    except Exception as e:
                        print(f"Error updating summons: {e}")
            
            # Close window and continue
            self.summon_selection_window.destroy()
            self.summon_selection_window = None
        
        continue_button = Button(
            self.summon_selection_window,
            text="Continue to Dungeon",
            bg="#00AA44",
            fg="#FFFFFF",
            font=("Montserrat Bold", 12),
            command=continue_to_dungeon,
            width=20,
            height=1
        )
        continue_button.place(x=100, y=330)
        
        # Skip button
        skip_button = Button(
            self.summon_selection_window,
            text="Continue Without Summons",
            bg="#333333",
            fg="#FFFFFF",
            font=("Montserrat Regular", 12),
            command=lambda: self.summon_selection_window.destroy(),
            width=20,
            height=1
        )
        skip_button.place(x=320, y=330)
        
        # Center the window and make it modal
        self.summon_selection_window.transient(self.parent.window)
        self.summon_selection_window.grab_set()
        self.summon_selection_window.geometry("+%d+%d" % (
            self.parent.window.winfo_rootx() + 50,
            self.parent.window.winfo_rooty() + 50
        ))
    
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
                font=("Montserrat Bold", 12 * -1)
            )
            self.parent.window.after(5000, lambda: self.canvas.delete(notification))
    
    def apply_modifier_to_activities(self, modifier, activities):
        """Apply summon modifier to reduce exercise requirements"""
        # Calculate percent reduction (capped at 60%)
        percent_reduction = min(0.60, modifier / 200.0)
        
        # Apply to all activities
        for activity in activities:
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
                    self.parent.window.after(3000, lambda act=activity: self.canvas.itemconfig(
                        act, fill=self.normal_font_col
                    ))
                    break
    
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
        
        try:
            import json
            import os
            if os.path.exists("Files/Player Data/Summons.json"):
                with open("Files/Player Data/Summons.json", 'r') as summon_file:
                    summons_data = json.load(summon_file)
                
                updated_summons = []
                
                # Update each active summon
                for summon in summons_data["summons"]:
                    # Check if this summon was used
                    was_active = False
                    for active_summon in self.active_summons:
                        if active_summon['name'] == summon['name']:
                            was_active = True
                            break
                    
                    if was_active:
                        # Add experience
                        summon['experience'] = summon.get('experience', 0) + gained_xp
                        
                        # Check for level up
                        xp_required = summon.get('level', 1) * 100
                        if summon['experience'] >= xp_required:
                            summon['level'] = summon.get('level', 1) + 1
                            summon['experience'] -= xp_required
                            
                            # Show level up notification
                            level_up_text = self.canvas.create_text(
                                400, 200 + len(updated_summons) * 20,
                                anchor="center",
                                text=f"{summon['name']} leveled up to {summon['level']}!",
                                fill="#00FF00",
                                font=("Montserrat Bold", 12 * -1)
                            )
                            self.parent.window.after(4000, lambda t=level_up_text: self.canvas.delete(t))
                        
                        # Increase loyalty (capped at 100%)
                        summon['loyalty'] = min(100, summon.get('loyalty', 50) + loyalty_gain)
                        
                        updated_summons.append(summon['name'])
                
                # Save updated summons data
                with open("Files/Player Data/Summons.json", 'w') as summon_file:
                    json.dump(summons_data, summon_file, indent=4)
                
                # Show update notification if any summons were updated
                if updated_summons:
                    summon_names = ", ".join(updated_summons)
                    update_text = self.canvas.create_text(
                        400, 180,
                        anchor="center",
                        text=f"Shadow Soldiers gained experience: {summon_names}",
                        fill="#FFAA00",
                        font=("Montserrat Bold", 12 * -1)
                    )
                    self.parent.window.after(4000, lambda: self.canvas.delete(update_text))
        except Exception as e:
            print(f"Error updating summons after completion: {e}")


# Shadow Summon extraction system (minimal implementation)
class ShadowSummonSystem:
    def __init__(self, parent_window, boss_name, boss_data, rank, transp_clr):
        self.parent_window = parent_window
        self.boss_name = boss_name
        self.boss_data = boss_data
        self.rank = rank
        self.transp_clr = transp_clr
        self.attempts_remaining = 3
        self.summon_window = None
        self.success_rate = self.calculate_success_rate()
        self.summons = self.load_summons()
        
    def calculate_success_rate(self):
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
        try:
            import os
            import json
            os.makedirs("Files/Player Data/", exist_ok=True)
            if os.path.exists("Files/Player Data/Summons.json"):
                with open("Files/Player Data/Summons.json", 'r') as summon_file:
                    return json.load(summon_file)
            # Create default structure if file doesn't exist
            return {"summons": []}
        except (FileNotFoundError, json.JSONDecodeError):
            return {"summons": []}
    
    def save_summons(self):
        import json
        with open("Files/Player Data/Summons.json", 'w') as summon_file:
            json.dump(self.summons, summon_file, indent=4)
    
    def show_summon_window(self):
        from tkinter import Toplevel, Canvas, Button
        
        # Create a new window for summoning
        self.summon_window = Toplevel(self.parent_window)
        self.summon_window.title("Shadow Extraction")
        self.summon_window.geometry("500x300")
        self.summon_window.configure(bg="#1E1E1E")
        self.summon_window.overrideredirect(True)
        
        # Create canvas for UI elements
        canvas = Canvas(
            self.summon_window,
            bg="#1E1E1E",
            height=300,
            width=500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Top and bottom colored bars
        canvas.create_rectangle(0.0, 0.0, 500.0, 30.0, fill=self.transp_clr, outline="")
        canvas.create_rectangle(0.0, 270.0, 500.0, 300.0, fill=self.transp_clr, outline="")
        
        # Title
        canvas.create_text(
            250, 50,
            text="SHADOW EXTRACTION SYSTEM",
            fill="#FFFFFF",
            font=("Montserrat Bold", 18),
            anchor="center"
        )
        
        # Boss info
        canvas.create_text(
            250, 90,
            text=f"Attempt to extract shadow from: {self.boss_name}",
            fill="#AAAAAA",
            font=("Montserrat Regular", 12),
            anchor="center"
        )
        
        # Rank info
        canvas.create_text(
            250, 110,
            text=f"Rank: {self.rank}",
            fill="#FFAA00",
            font=("Montserrat Bold", 14),
            anchor="center"
        )
        
        # Success rate and attempts
        self.stats_text = canvas.create_text(
            250, 140,
            text=f"Success Rate: {int(self.success_rate * 100)}% | Attempts Remaining: {self.attempts_remaining}",
            fill="#FFAA00",
            font=("Montserrat Regular", 12),
            anchor="center"
        )
        
        # Attempt animation area
        self.animation_rect = canvas.create_rectangle(
            150, 160, 350, 190,
            fill="#2A2A2A",
            outline="#652AA3"
        )
        
        self.animation_text = canvas.create_text(
            250, 175,
            text="Ready to extract",
            fill="#FFFFFF",
            font=("Montserrat Regular", 12),
            anchor="center"
        )
        
        # Extract button
        extract_button = Button(
            self.summon_window,
            text="Extract Shadow",
            bg="#652AA3",
            fg="#FFFFFF",
            font=("Montserrat Bold", 12),
            command=self.attempt_summon,
            width=15,
            height=1
        )
        extract_button.place(x=100, y=220)
        
        # Cancel button
        cancel_button = Button(
            self.summon_window,
            text="Cancel",
            bg="#333333",
            fg="#FFFFFF",
            font=("Montserrat Regular", 12),
            command=self.close_summon_window,
            width=15,
            height=1
        )
        cancel_button.place(x=280, y=220)
        
        # Center the window and make it modal
        self.summon_window.transient(self.parent_window)
        self.summon_window.grab_set()
        self.summon_window.geometry("+%d+%d" % (
            self.parent_window.winfo_rootx() + 50,
            self.parent_window.winfo_rooty() + 50
        ))
        
        # Store canvas for updates
        self.canvas = canvas
    
    def attempt_summon(self):
        """Try to summon the boss"""
        import random
        
        self.attempts_remaining -= 1
        
        # Update animation to show attempt in progress
        self.canvas.itemconfig(self.animation_text, text="Extracting shadow...")
        self.canvas.itemconfig(self.animation_rect, outline="#FF00FF")
        
        # Update stats display
        self.canvas.itemconfig(
            self.stats_text, 
            text=f"Success Rate: {int(self.success_rate * 100)}% | Attempts Remaining: {self.attempts_remaining}"
        )
        
        # Schedule animations and result check
        self.summon_window.after(500, self.animation_stage1)
        self.summon_window.after(1000, self.animation_stage2)
        self.summon_window.after(1500, self.check_summon_result)
    
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
        import random
        
        # Determine if summon is successful
        is_successful = random.random() < self.success_rate
        
        if is_successful:
            self.canvas.itemconfig(self.animation_text, text="EXTRACTION SUCCESSFUL!")
            self.canvas.itemconfig(self.animation_rect, fill="#00AA44", outline="#00FF00")
            self.summon_window.after(1000, self.show_success_notification)
        elif self.attempts_remaining <= 0:
            self.canvas.itemconfig(self.animation_text, text="EXTRACTION FAILED!")
            self.canvas.itemconfig(self.animation_rect, fill="#AA0000", outline="#FF0000")
            self.summon_window.after(1000, self.show_failure_notification)
        else:
            self.canvas.itemconfig(self.animation_text, text="Failed - Try again")
            self.canvas.itemconfig(self.animation_rect, fill="#2A2A2A", outline="#AA5500")
    
    def show_success_notification(self):
        """Display the success notification window"""
        from tkinter import Toplevel, Canvas, Button
        
        self.close_summon_window()
        self.add_summon_to_collection()
        
        # Create success window
        success_window = Toplevel(self.parent_window)
        success_window.title("Summon Successful")
        success_window.geometry("400x250")
        success_window.configure(bg="#1E1E1E")
        success_window.overrideredirect(True)
        
        # Create canvas
        canvas = Canvas(
            success_window,
            bg="#1E1E1E",
            height=250,
            width=400,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Top and bottom colored bars
        canvas.create_rectangle(0.0, 0.0, 400.0, 30.0, fill=self.transp_clr, outline="")
        canvas.create_rectangle(0.0, 220.0, 400.0, 250.0, fill=self.transp_clr, outline="")
        
        # Success message
        canvas.create_text(
            200, 80,
            text="SHADOW EXTRACTION SUCCESSFUL",
            fill="#00FF00",
            font=("Montserrat Bold", 16),
            anchor="center"
        )
        
        # Boss name
        canvas.create_text(
            200, 120,
            text=f"{self.boss_name} has been added to your collection",
            fill="#FFFFFF",
            font=("Montserrat Regular", 12),
            anchor="center"
        )
        
        # Center the window
        success_window.geometry("+%d+%d" % (
            self.parent_window.winfo_rootx() + 100,
            self.parent_window.winfo_rooty() + 100
        ))
        
        # Close after 3 seconds and show dialog
        success_window.after(3000, lambda: self.close_and_show_dialog(success_window))
    
    def close_and_show_dialog(self, window):
        """Close the current window and show the shadow dialog"""
        window.destroy()
        self.show_summon_dialog()
    
    def show_failure_notification(self):
        """Display the failure notification window"""
        from tkinter import Toplevel, Canvas, Button
        
        self.close_summon_window()
        
        # Create failure window
        failure_window = Toplevel(self.parent_window)
        failure_window.title("Summon Failed")
        failure_window.geometry("400x250")
        failure_window.configure(bg="#1E1E1E")
        failure_window.overrideredirect(True)
        
        # Create canvas
        canvas = Canvas(
            failure_window,
            bg="#1E1E1E",
            height=250,
            width=400,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Top and bottom colored bars
        canvas.create_rectangle(0.0, 0.0, 400.0, 30.0, fill="#AA0000", outline="")
        canvas.create_rectangle(0.0, 220.0, 400.0, 250.0, fill="#AA0000", outline="")
        
        # Failure message
        canvas.create_text(
            200, 80,
            text="SHADOW EXTRACTION FAILED",
            fill="#FF0000",
            font=("Montserrat Bold", 16),
            anchor="center"
        )
        
        # Explanation
        canvas.create_text(
            200, 120,
            text=f"The shadow of {self.boss_name} resisted extraction",
            fill="#FFFFFF",
            font=("Montserrat Regular", 12),
            anchor="center"
        )
        
        # Advice
        canvas.create_text(
            200, 160,
            text="Try again with a different enemy or after becoming stronger",
            fill="#AAAAAA",
            font=("Montserrat Regular", 10),
            anchor="center"
        )
        
        # Close button
        close_button = Button(
            failure_window,
            text="Close",
            bg="#333333",
            fg="#FFFFFF",
            font=("Montserrat Regular", 12),
            command=failure_window.destroy,
            width=10,
            height=1
        )
        close_button.place(x=150, y=185)
        
        # Center the window
        failure_window.geometry("+%d+%d" % (
            self.parent_window.winfo_rootx() + 100,
            self.parent_window.winfo_rooty() + 100
        ))
    
    def show_summon_dialog(self):
        """Show the dialog window with the summoned shadow soldier"""
        import random
        from tkinter import Toplevel, Canvas, Button
        
        # Loyalty dialog phrases
        dialog_options = [
            f"My liege, I pledge myself to you. {self.boss_name} shall serve as your shadow.",
            f"I am yours to command. My strength is now your strength, Shadow Monarch.",
            f"The shadows bind me to your will. I shall fight for you until the end.",
            f"As your shadow soldier, I shall destroy all who oppose you.",
            f"My defeat was honorable. Now, I serve a worthy master. Command me as you will."
        ]
        
        # Create dialog window
        dialog_window = Toplevel(self.parent_window)
        dialog_window.title("Shadow Soldier")
        dialog_window.geometry("600x400")
        dialog_window.configure(bg="#0A0A0A")
        dialog_window.overrideredirect(True)
        
        # Create canvas
        canvas = Canvas(
            dialog_window,
            bg="#0A0A0A",
            height=400,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        
        # Name plate
        canvas.create_rectangle(0, 0, 600, 40, fill="#652AA3", outline="")
        
        canvas.create_text(
            300, 20,
            text=f"{self.boss_name} - Shadow Soldier",
            fill="#FFFFFF",
            font=("Montserrat Bold", 14),
            anchor="center"
        )
        
        # Image placeholder
        canvas.create_rectangle(150, 60, 450, 260, fill="#1A1A1A", outline="#652AA3")
        
        canvas.create_text(
            300, 160,
            text="[SHADOW SOLDIER IMAGE PLACEHOLDER]",
            fill="#AAAAAA",
            font=("Montserrat Regular", 12),
            anchor="center"
        )
        
        # Dialog text
        dialog_text = random.choice(dialog_options)
        
        canvas.create_text(
            300, 300,
            text=dialog_text,
            fill="#FFFFFF",
            font=("Montserrat", 14, "italic"),
            width=500,  # Wrap text at 500 pixels
            anchor="center"
        )
        
        # Continue button
        continue_button = Button(
            dialog_window,
            text="Add to Collection",
            bg="#652AA3",
            fg="#FFFFFF",
            font=("Montserrat Bold", 12),
            command=dialog_window.destroy,
            width=15,
            height=1
        )
        continue_button.place(x=225, y=350)
        
        # Center the window
        dialog_window.geometry("+%d+%d" % (
            self.parent_window.winfo_rootx() + 50,
            self.parent_window.winfo_rooty() + 50
        ))
    
    def add_summon_to_collection(self):
        """Add the boss to the shadow summons collection"""
        import random
        from datetime import datetime
        
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
            "active": False,
            "date_acquired": datetime.now().strftime("%Y-%m-%d")
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
        
        # Save updated collection
        self.save_summons()
    
    def calculate_summon_power(self):
        """Calculate the power level of the summoned shadow soldier"""
        import random
        
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
    
    def close_summon_window(self):
        """Close the summoning window"""
        if self.summon_window:
            self.summon_window.grab_release()
            self.summon_window.destroy()
            self.summon_window = None


# Modify the DungeonSystem class to integrate shadow summoning
# Modify the DungeonSystem class to integrate shadow summoning
def modify_dungeon_system():
    # Store original methods to call them in our new methods
    original_init = DungeonSystem.__init__
    original_start_dungeon = DungeonSystem.start_dungeon
    original_show_current_wave = DungeonSystem.show_current_wave
    original_complete_dungeon = DungeonSystem.complete_dungeon
    
    # Extend the __init__ method to add shadow management
    def new_init(self, window):
        # Set the shadow_manager attribute to None initially
        self.shadow_manager = None
        # Call the original __init__ method
        original_init(self, window)
        
        # Only initialize shadow manager if the player has a job
        if self.job != 'None':
            # Initialize shadow manager after original init is done
            self.shadow_manager = ShadowManager(self, self.canvas, self.normal_font_col)
            
    
    # Extend the start_dungeon method to show shadow selection
    def new_start_dungeon(self):
        original_start_dungeon(self)
        # Show shadow soldier selection at start only if player has a job
        if hasattr(self, 'shadow_manager') and self.shadow_manager is not None:
            self.window.after(4000, self.shadow_manager.show_summon_selection)
    
    # Modify show_current_wave to apply shadow soldier effects
    def new_show_current_wave(self):
        original_show_current_wave(self)
        
        # Only apply shadow effects if player has a job and shadow_manager exists
        if hasattr(self, 'shadow_manager') and self.shadow_manager is not None:
            # Get current wave and monster info
            if self.mob > len(self.waves) - 1:
                wave_key = "Final"
            else:
                wave_key = str(self.mob)
                
            if wave_key in self.waves:
                monster_name = list(self.waves[wave_key].keys())[0]
                monster = self.waves[wave_key][monster_name]
                
                # Apply shadow effects to activities
                activities = [self.activity1, self.activity2, self.activity3, self.activity4]
                self.shadow_manager.apply_summon_effects(wave_key, monster_name, monster, activities)
    
    # Modify complete_dungeon to offer shadow extraction and update summons
    def new_complete_dungeon(self):
        original_complete_dungeon(self)
        
        # Only offer shadow extraction if player has a job and shadow_manager exists
        if hasattr(self, 'shadow_manager') and self.shadow_manager is not None:
            # Update shadow soldiers that participated
            self.shadow_manager.update_summons_after_completion(self.rank)
            
            # Offer shadow extraction for the boss after displaying completion info
            self.window.after(2000, self.offer_shadow_extraction)
    
    # Add new method for offering shadow extraction
    def offer_shadow_extraction(self):
        # Don't do anything if player doesn't have a job or shadow_manager doesn't exist
        if not hasattr(self, 'shadow_manager') or self.shadow_manager is None:
            return
        self.extract_button = Button(
            self.window,
            text="Extract Shadow",
            bg="#333333",  # Changed to purple to match theme
            fg="#FFFFFF",
            font=("Montserrat Bold", 12),
            command=self.start_shadow_extraction,  # Just reference the method
            width=15
        )
        self.extract_button.place(x=350, y=335)
        
        self.skip_button = Button(
            self.window,
            text="Skip",
            bg="#333333",
            fg="#FFFFFF",
            font=("Montserrat Regular", 12),
            command=self.skip_extraction,
            width=15
        )
        self.skip_button.place(x=530, y=335)
        
        # Add extraction text
        self.extraction_text = self.canvas.create_text(
            440, 315,
            anchor="center",
            text="Would you like to attempt shadow extraction on the defeated boss?",
            fill="#FFFFFF",
            font=("Montserrat Bold", 12)
        )
    
    def start_shadow_extraction(self):
        print("Shadow extraction started")
        
        # Don't do anything if player doesn't have a job or shadow_manager doesn't exist
        if not hasattr(self, 'shadow_manager') or self.shadow_manager is None:
            print("wtf")
            return
        
        # Get boss data
        try:
            boss_name = list(self.waves["Final"].keys())[0]
            boss_data = self.waves["Final"][boss_name]
            
            # Launch the shadow extraction system in a separate process
            import subprocess
            import json
            import os
            
            # Create temporary data file with boss information
            temp_data = {
                "boss_name": boss_name,
                "boss_data": boss_data,
                "rank": self.rank,
                "transp_clr": self.transp_clr
            }
            
            os.makedirs("Files/Temp Files", exist_ok=True)
            with open("Files/Temp Files/boss_data.json", "w") as f:
                json.dump(temp_data, f)
            
            # Launch the shadow extraction system
            subprocess.Popen(['python', 'shadow_summon_system.py'])
            
        except Exception as e:
            print(f"Error launching shadow extraction: {e}")
            # Show error message
            error_text = self.canvas.create_text(
                440, 315,
                anchor="center",
                text=f"Error: Could not extract shadow",
                fill="#FF0000",
                font=("Montserrat Bold", 12)
            )
            self.window.after(3000, lambda: self.canvas.delete(error_text))
            
    def create_extraction_window(self, boss_name, boss_data, feedback_text):
        """Helper method to create the extraction window after delay"""
        try:
            # Remove feedback text
            self.canvas.delete(feedback_text)
            
            # Initialize and show summon system
            self.summon_system = ShadowSummonSystem(self.window, boss_name, boss_data, self.rank, self.transp_clr)
            self.summon_system.show_summon_window()
        except Exception as e:
            print(f"Error creating extraction window: {e}")
            # Show error message to user
            error_text = self.canvas.create_text(
                440, 315,
                anchor="center",
                text=f"Error: {str(e)}",
                fill="#FF0000",
                font=("Montserrat Bold", 12)
            )
            self.window.after(3000, lambda: self.canvas.delete(error_text))

    # Add method for skipping extraction
    def skip_extraction(self):
        # Don't do anything if player doesn't have a job or shadow_manager doesn't exist
        if not hasattr(self, 'shadow_manager') or self.shadow_manager is None:
            return
            
        # Remove buttons and text
        if hasattr(self, 'extract_button') and self.extract_button:
            self.extract_button.destroy()
            self.extract_button = None
        
        if hasattr(self, 'skip_button') and self.skip_button:
            self.skip_button.destroy()
            self.skip_button = None
        
        if hasattr(self, 'extraction_text'):
            self.canvas.delete(self.extraction_text)
        
        # Show message that shadow extraction was skipped
        skipped_text = self.canvas.create_text(
            440, 315,
            anchor="center",
            text="Shadow extraction skipped",
            fill="#AAAAAA",
            font=("Montserrat Regular", 12)
        )
        # Remove text after 2 seconds
        self.window.after(2000, lambda: self.canvas.delete(skipped_text))
    
    
    # Add method for starting shadow extraction
    def new_start_shadow_extraction(self):
        print("Shadow extraction started")
        
        # Don't do anything if player doesn't have a job or shadow_manager doesn't exist
        if not hasattr(self, 'shadow_manager') or self.shadow_manager is None:
            return
        
        # Get boss data
        try:
            boss_name = list(self.waves["Final"].keys())[0]
            boss_data = self.waves["Final"][boss_name]
            
            # Launch the shadow extraction system in a separate process
            import subprocess
            import json
            import os
            
            # Create temporary data file with boss information
            temp_data = {
                "boss_name": boss_name,
                "boss_data": boss_data,
                "rank": self.rank,
                "transp_clr": self.transp_clr
            }
            
            os.makedirs("Files/Temp Files", exist_ok=True)
            with open("Files/Temp Files/boss_data.json", "w") as f:
                json.dump(temp_data, f)
            
            # Launch the shadow extraction system
            subprocess.Popen(['python', 'Anime Version/Dungeon Runs/shadow_summon_system.py'])
            
        except Exception as e:
            print(f"Error launching shadow extraction: {e}")
            # Show error message
            error_text = self.canvas.create_text(
                440, 315,
                anchor="center",
                text=f"Error: Could not extract shadow",
                fill="#FF0000",
                font=("Montserrat Bold", 12)
            )
            self.window.after(3000, lambda: self.canvas.delete(error_text))
    
    # Now assign all the new methods to the class
    DungeonSystem.__init__ = new_init
    DungeonSystem.start_dungeon = new_start_dungeon
    DungeonSystem.show_current_wave = new_show_current_wave
    DungeonSystem.complete_dungeon = new_complete_dungeon
    DungeonSystem.offer_shadow_extraction = offer_shadow_extraction
    DungeonSystem.start_shadow_extraction = new_start_shadow_extraction
    DungeonSystem.skip_extraction = skip_extraction
    
# Call the modification function at the bottom of the code after all classes are defined
modify_dungeon_system()

def modify_dungeon_system1():
    # Add skill system initialization to __init__ method
    original_init = DungeonSystem.__init__
    
    def new_init(self, window):
        original_init(self, window)
        self.skill_system = SkillSystem(self, self.canvas, self.normal_font_col)
        self.str_buff_active = False
        self.agi_debuff_active = False
        self.skill_ui_elements = []
    
    DungeonSystem.__init__ = new_init
    
    # Modify generate_activities to account for skills
    original_generate_activities = DungeonSystem.generate_activities
    
    def new_generate_activities(self, monster_type, is_boss=False):
        original_generate_activities(self, monster_type, is_boss)
        
        # Apply buffs/debuffs from active skills
        if hasattr(self, 'str_buff_active') and self.str_buff_active and monster_type == "STR":
            # Apply STR buff - make activities easier
            activities = [self.activity1, self.activity2, self.activity3, self.activity4]
            for activity in activities:
                current_text = self.canvas.itemcget(activity, "text")
                if "STR BUFF" not in current_text:
                    import re
                    numbers = re.findall(r'\d+', current_text)
                    if numbers:
                        num = int(numbers[0])
                        reduced_num = max(1, int(num * 0.8))  # 20% reduction
                        new_text = current_text.replace(str(num), str(reduced_num))
                        new_text += " [STR BUFF]"
                        self.canvas.itemconfig(activity, text=new_text)
        
        if hasattr(self, 'agi_debuff_active') and self.agi_debuff_active and monster_type == "AGI":
            # Apply AGI debuff - make activities harder
            activities = [self.activity1, self.activity2, self.activity3, self.activity4]
            for activity in activities:
                current_text = self.canvas.itemcget(activity, "text")
                if "AGI DEBUFF" not in current_text:
                    import re
                    numbers = re.findall(r'\d+', current_text)
                    if numbers:
                        num = int(numbers[0])
                        increased_num = int(num * 1.2)  # 20% increase
                        new_text = current_text.replace(str(num), str(increased_num))
                        new_text += " [AGI DEBUFF]"
                        self.canvas.itemconfig(activity, text=new_text)
    
    DungeonSystem.generate_activities = new_generate_activities
    
    # Add passive skill effect application to start_dungeon
    original_start_dungeon = DungeonSystem.start_dungeon
    
    def new_start_dungeon(self):
        original_start_dungeon(self)
        
        # Apply passive skills effects
        if hasattr(self, 'skill_system'):
            for skill_name, skill_data in self.skill_system.passive_skills.items():
                if skill_name == "Iron Warrior":
                    # Apply Iron Warrior effect (will take effect below 50% HP)
                    skill_level = skill_data[0]["lvl"]
                    hp_bonus = 0.05 * skill_level  # 5% per level
                    
                    # Show passive skill indicator
                    passive_text = self.canvas.create_text(
                        690, 90.0,
                        anchor="nw",
                        text=f"IRON WARRIOR ACTIVE: +{int(hp_bonus*100)}% HP below 50%",
                        fill="#FFAA00",
                        font=("Montserrat Regular", 10 * -1)
                    )
                    self.skill_ui_elements.append(passive_text)
    
    DungeonSystem.start_dungeon = new_start_dungeon
    
    # Update setup_dungeon_timer to account for passive skills
    original_setup_timer = DungeonSystem.setup_dungeon_timer
    
    def new_setup_dungeon_timer(self):
        original_setup_timer(self)
        
        # Apply passive skills that affect time
        if hasattr(self, 'skill_system'):
            for skill_name, skill_data in self.skill_system.passive_skills.items():
                if skill_name == "Nimble Endurance":
                    skill_level = skill_data[0]["lvl"]
                    time_bonus = 0.05 * skill_level  # 5% per level
                    
                    # Apply time bonus
                    self.time_remaining = int(self.time_remaining * (1 + time_bonus))
                    
                    # Show passive skill effect
                    passive_text = self.canvas.create_text(
                        690, 80.0,
                        anchor="nw",
                        text=f"NIMBLE ENDURANCE: +{int(time_bonus*100)}% Time",
                        fill="#FFAA00",
                        font=("Montserrat Regular", 10 * -1)
                    )
                    self.skill_ui_elements.append(passive_text)
    
    DungeonSystem.setup_dungeon_timer = new_setup_dungeon_timer

# Call the modification function at the bottom of the code
modify_dungeon_system1()

if __name__ == "__main__":
    window = Tk()
    window.title("Dungeon System")
    app = DungeonSystem(window)
    update_thread = threading.Thread(target=app.update_images())
    update_thread.start()
    window.mainloop()