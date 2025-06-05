# Enhanced Dungeon System
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, StringVar, Frame
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
        self.load_images()
        self.setup_video_player()
        self.create_ui_elements()
        self.setup_animation()
        self.start_dungeon()
        
        # Generate dungeon events and modifiers after rank is set
        self.roll_dungeon_modifiers()
            
    def setup_window_style(self):
        self.top_val = 'dailyquest.py'
        self.all_prev = ''
        self.video = 'Video'
        self.transp_clr = '#0C679B'

        if self.job != 'None':
            self.top_val = ''
            self.all_prev = 'alt_'
            self.video = 'Alt Video'
            self.transp_clr = '#652AA3'

        thesystem.system.make_window_transparent(self.window, self.transp_clr)

        self.top_images = [f"thesystem/{self.all_prev}top_bar/{self.top_val}{str(i).zfill(4)}.png" for i in range(1, 501)]
        self.bottom_images = [f"thesystem/{self.all_prev}bottom_bar/{str(i).zfill(4)}.png" for i in range(1, 501)]

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
        self.top_preloaded_images = thesystem.system.preload_images(self.top_images, (1167, 47))
        self.bottom_preloaded_images = thesystem.system.preload_images(self.bottom_images, (1053, 43))
        
        # Load main images
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(675.0, 375.0, image=self.image_image_1)
        
        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(435.0, 180.52554321289062, image=self.image_image_2)
        
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
        with open("Files\Mod\presets.json", 'r') as pres_file:
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
        with open("Files\Data\Dungeon_Rank.csv", 'r') as rank_file:
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
            base_waves = 4
        elif self.rank in ["B", "A"]:
            base_waves = 5
        elif self.rank == "S":
            base_waves = 6
            
        wave_variation = random.choice([-1, 0, 0, 0, 1])
        total_waves = max(3, base_waves + wave_variation)
        self.total_waves = total_waves
        
        with open("Files\Data\Dungeon_Boss_List.json", 'r') as monster_file:
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
            num_modifiers = 1
        elif self.rank in ["C", "B"]:
            num_modifiers = 2
        elif self.rank in ["A", "S"]:
            num_modifiers = 3
            
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
        
        str_activities = [
            "Do 10 push-ups",
            "Perform 15 squats",
            "Complete 20 jumping jacks",
            "Hold a plank for 30 seconds",
            "Do 12 lunges (each leg)",
            "Complete 8 burpees",
            "Do 15 mountain climbers",
            "Perform 20 arm circles",
            "Complete 12 tricep dips",
            "Do 15 calf raises"
        ]
        
        agi_activities = [
            "Balance on one foot for 30 seconds",
            "Do 20 high knees",
            "Perform 10 side lunges (each side)",
            "Complete a quick dance routine",
            "Do 15 lateral jumps",
            "Walk 30 steps heel-to-toe",
            "Complete 10 agility ladder drills",
            "Do 10 quick directional changes",
            "Perform 15 toe touches",
            "Complete 20 ankle rotations"
        ]
        
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
        if not all(self.activity_completed):
            incomplete_indices = [i for i, completed in enumerate(self.activity_completed) if not completed]
            activity_widgets = [self.activity1, self.activity2, self.activity3, self.activity4]
            for idx in incomplete_indices:
                self.canvas.itemconfig(activity_widgets[idx], fill="#FF0000")
            self.window.after(500, lambda: [self.canvas.itemconfig(activity_widgets[idx], fill=self.normal_font_col) for idx in incomplete_indices])
            return
        
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
        self.canvas.itemconfig(self.button_image_1, state="hidden")
        self.canvas.itemconfig(self.button_image_2, state="hidden")
        self.hide_activities_and_checkboxes()
        
        # Update XP and rewards in records
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

            # Apply rewards based on dungeon type
            if self.type_of_dun == 'Normal':
                status_read_data["avail_eq"][0]['str_based'] += avp
                status_read_data["avail_eq"][0]['int_based'] += avp
                status_read_data["status"][0]['XP'] += self.XP_val
                status_read_data["status"][0]['coins'] += coin
                with open("Files/Player Data/Status.json", 'w') as fson:
                    ujson.dump(status_read_data, fson, indent=4)
                with open("Files/Checks/Message.csv", 'w', newline='') as check_file:
                    check_fw = csv.writer(check_file)
                    check_fw.writerow(["Quest Completed"])
            elif self.type_of_dun == 'Instance':
                status_read_data["status"][0]['XP'] += (self.XP_val * 2)
                status_read_data["status"][0]['coins'] += (coin * 2)
                status_read_data["avail_eq"][0]['str_based'] += (avp * 2)
                status_read_data["avail_eq"][0]['int_based'] += (avp * 2)
                with open("Files/Player Data/Status.json", 'w') as fson:
                    ujson.dump(status_read_data, fson, indent=4)
                with open("Files/Checks/Message.csv", 'w', newline='') as check_file:
                    check_fw = csv.writer(check_file)
                    check_fw.writerow(["Instance Reward"])

            thesystem.system.get_fin_xp()

        except Exception as e:
            print(f"Error updating records: {e}")
        
        self.button_2.destroy()
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.ex_close(),
            relief="flat"
        )
        self.button_2.place(x=646.0, y=264.0, width=150.0, height=22.0)

if __name__ == "__main__":
    window = Tk()
    window.title("Dungeon System")
    app = DungeonSystem(window)
    update_thread = threading.Thread(target=app.update_images())
    update_thread.start()
    window.mainloop()