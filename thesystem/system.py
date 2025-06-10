import ujson
import csv
import subprocess
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageTk, ImageFilter
from datetime import datetime, timedelta, date
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import sys
import random
import cv2
import os
import queue
import thesystem.misc
import numpy as np
from multiprocessing import Pool, cpu_count
import tkinter as tk
from tkinter import Label
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial

last_run = 0 
tk_images = []

def fin_pen():
    today = datetime.now().date()

    yesterday = today - timedelta(days=1)
    with open('Files/Checks/Daily_time_check.csv', 'r', newline='') as fout:
        fr=csv.reader(fout)
        for k in fr:
            status=k[1]
            dates=k[0]

    p_date=datetime.strptime(dates, "%Y-%m-%d").date()
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    with open("Files/Player Data/Settings.json", 'r') as settings_open:
        setting_data=ujson.load(settings_open)
    if yesterday==p_date and status=="UNDONE" and setting_data["Settings"]["Main_Penalty"]!="False":
        subprocess.Popen(['python', f'{theme} Version/Penalty Quest/gui.py'])
        with open('Files/Checks/Daily_time_check.csv', 'w', newline='') as fout_final:
            fout_final_wr=csv.writer(fout_final)
            fout_final_wr.writerow([dates,"DONE","Complete"])
    elif yesterday!=p_date or status=="UNDONE" and setting_data["Settings"]["Main_Penalty"]!="False":
        subprocess.Popen(['python', f'{theme} Version/Penalty Quest/gui.py'])
        with open('Files/Checks/Daily_time_check.csv', 'w', newline='') as fout_final:
            fout_final_wr=csv.writer(fout_final)
            fout_final_wr.writerow([dates,"DONE","Complete"])

    #! ===================================================================
    with open("Files/Data/Calorie_Count.json", 'r') as calorie_add_file:
        calorie_add_data=ujson.load(calorie_add_file)
        calorie_add_key=list(calorie_add_data.keys())[0]
        cal_tdy_val=calorie_add_data[calorie_add_data]
    
    # Get today's date
    current_date = date.today()
    current_date_t = date.now()

    # Format the date as a string
    formatted_date = current_date.strftime("%Y-%m-%d")
    day_of_week = (current_date_t.strftime("%A"))
    try:
        with open("Files/Workout/Cal_Count.json", 'r') as calorie_val_search_file:
            calorie_val_search_data=ujson.load(calorie_val_search_file)
            cal_val=calorie_val_search_data[day_of_week]
            
        with open("Files/Player Data/Status.json", 'r') as stat_first_fson:
            stat_first_fson_data=ujson.load(stat_first_fson)
            result=stat_first_fson_data["cal_data"][0]["result"]
    
    except:
        result='MILD WEIGHT LOSS'
        cal_tdy_val=0


    '''
    global last_run
    cal_pen = False
    cooldown = 24 * 60 * 60  # 24 hours in seconds
    

    if result=='MILD WEIGHT LOSS':
        cal_30=cal_val+(cal_val*0.25)
        if cal_tdy_val>cal_30 or cal_tdy_val==0:
            cal_pen=True

    elif result=='MILD WEIGHT GAIN':
        cal_30=cal_val-(cal_val*0.25)
        if cal_tdy_val<cal_30 or cal_tdy_val==0:
            cal_pen=True

    current_time = time.time()
    if cal_pen and (current_time - last_run > cooldown):
        subprocess.Popen(['python', 'First/Calorie Penalty/gui.py'])
        last_run = current_time  # Update the last run time

    '''
    #! ===================================================================

def penalty_check(win):
    with open("Files/Player Data/Penalty_Info.json", "r") as pen_info_file:
        data0=ujson.load(pen_info_file)
        target_time_str=data0["Penalty Time"]

    now=datetime.now()
    if target_time_str == "24:00":
        target_time_str = "00:00"
    target_time=datetime.strptime(target_time_str, "%H:%M").time()
    target_datetime=datetime.combine(now.date(), target_time)
    
    if target_datetime<now:
        target_datetime+=timedelta(days=1)
    
    wait_time_ms = int((target_datetime - now).total_seconds() * 1000)
    
    win.after(wait_time_ms, fin_pen)

def close(stp_eve, thrd):
    stp_eve.set()

    # Wait for the thread to finish
    thrd.join()

    sys.exit()

def run_once_prog(stp_eve, thrd):
    try:
        with open("Files/Player Data/First_open.csv", 'r') as first_open_check_file:
            first_open_check_data=csv.reader(first_open_check_file)
            first_run_file_check=False
            try:
                for k in first_open_check_data:
                    if k[0]!="True":
                        first_run_file_check=True
            except:
                first_run_file_check=True
    except:
        first_run_file_check=True

    try:
        with open("Files/Player Data/Prove_file.csv", 'r') as second_open_check_file:
            second_open_check_data=csv.reader(second_open_check_file)
            second_run_file_check=False
            try:
                for k in second_open_check_data:
                    if k[0]!="True":
                        second_run_file_check=True
            except:
                second_run_file_check=True
    except:
        second_run_file_check=True

    if first_run_file_check==True and second_run_file_check==True:
        requirements_file='requirements.txt'
        #try:
        #    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
        #    print(f"Installed packages from {requirements_file} successfully.")
        #except subprocess.CalledProcessError as e:
        #    print(f"Failed to install packages from {requirements_file}. Error: {e}")
        stp_eve.set()

        # Wait for the thread to finish
        thrd.join()
    
        subprocess.Popen(['python', 'First/Check/gui.py'])

        sys.exit()
    
    elif first_run_file_check==True and second_run_file_check==False:
        stp_eve.set()

        # Wait for the thread to finish
        thrd.join()

        subprocess.Popen(['python', 'First/Check/gui.py'])

        sys.exit()

def run_once_misc_inv():
    with open("Files/Player Data/Inventory.json", 'r') as inv_file:
        inv_data=ujson.load(inv_file)
    try:
        if inv_data["Veg Maggi"]:
            del inv_data["Veg Maggi"]
            with open("Files/Player Data/Inventory.json", 'w') as inv_file:
                ujson.dump(inv_data, inv_file, indent=6)
    except:
        pass

    with open("Files/Data/Inventory_List.json", 'r') as inv_file:
        inv_data=ujson.load(inv_file)
    try:
        if inv_data["Veg Maggi"]:
            del inv_data["Veg Maggi"]
            with open("Files/Data/Inventory_List.json", 'w') as inv_file:
                ujson.dump(inv_data, inv_file, indent=6)
    except:
        pass

def random_skill_check():
    # Load the primary status file and extract player's data.
    with open("Files/Player Data/Status.json", 'r') as f:
        data = ujson.load(f)
    player = data["status"][0]
    meta = data["status"][1]

    # Convert numeric stats to integers.
    lvl = int(player['level'])
    stre = int(player['str'])
    intel = int(player['int'])
    agi = int(player['agi'])
    vit = int(player['vit'])
    per = int(player['per'])
    man = int(player['man'])

    # Check if level-up is eligible (every 5 levels).
    if lvl % 5 == 0:
        # Load old stats.
        with open("Files/Player Data/Skill_old_check.json", 'r') as f:
            old_lvl_data = ujson.load(f)
        old_stat = old_lvl_data["old_stat"][0]

        # Proceed only if the level has changed.
        if lvl != int(old_stat["lvl"]):
            # Calculate stat differences.
            comp_rec = {
                "STR": stre - int(old_stat["str"]),
                "INT": intel - int(old_stat["int"]),
                "AGI": agi - int(old_stat["agi"]),
                "VIT": vit - int(old_stat["vit"]),
                "PER": per - int(old_stat["per"]),
                "MAN": man - int(old_stat["man"])
            }
            max_val = max(comp_rec.values())
            # Get at most two alphabetically first keys with the max difference.
            max_keys = sorted([key for key, value in comp_rec.items() if value == max_val])[:2]

            # Load the available skills from the skill list.
            with open("Files/Data/Skill_List.json", 'r') as f:
                skill_list_data = ujson.load(f)
            # Find skills whose condition is met by the max_keys.
            available_skills = [
                skill for skill, details in skill_list_data.items()
                if set(details[1].get("Condition", [])).issubset(max_keys)
            ]
            choosen_skill = random.choice(available_skills) if available_skills else "Dash"

            # Load current skills.
            with open("Files/Player Data/Skill.json", 'r') as f:
                main_skill_data = ujson.load(f)

            # If the chosen skill exists, attempt an upgrade.
            if choosen_skill in main_skill_data:
                if main_skill_data[choosen_skill][0]["lvl"] != "MAX":
                    main_skill_data[choosen_skill][0]["lvl"] += 1
                    # Write updated skills.
                    with open("Files/Player Data/Skill.json", 'w') as f:
                        ujson.dump(main_skill_data, f, indent=6)
                    # Log the skill upgrade to a temporary CSV.
                    with open("Files/Temp Files/Skill Up Temp.csv", 'w', newline='') as csvfile:
                        csv.writer(csvfile).writerow([choosen_skill])
                    # Update the New Updates file.
                    new_updates = {"Skills": "False", "Quests": "False", "Upgrade": "True", "Lines": "False"}
                    with open("Files/Data/New_Updates.json", 'w') as f:
                        ujson.dump(new_updates, f, indent=4)
            else:
                # Add the new skill from the skill list.
                new_skill_entry = skill_list_data.get(choosen_skill, [])
                entry = new_skill_entry.pop(0) if new_skill_entry else {}
                entry["pl_point"] = 0
                main_skill_data[choosen_skill] = [entry]
                with open("Files/Player Data/Skill.json", 'w') as f:
                    ujson.dump(main_skill_data, f, indent=6)
                new_updates = {"Skills": "True", "Quests": "False", "Upgrade": "False", "Lines": "False"}
                with open("Files/Data/New_Updates.json", 'w') as f:
                    ujson.dump(new_updates, f, indent=4)

            # Update the stored old stats.
            old_stat.update({
                "lvl": lvl,
                "str": stre,
                "int": intel,
                "agi": agi,
                "vit": vit,
                "per": per,
                "man": man,
            })
            with open("Files/Player Data/Skill_old_check.json", 'w') as f:
                ujson.dump(old_lvl_data, f, indent=4)

def check_midnight(window,stop_event):
    while not stop_event.is_set():
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            penalty_check(window)
        time.sleep(1)

def random_quest():
    # ! The Random Quests thing
    with open('Files/Player Data/Random_Quest_Day.json', 'r') as random_quest:
        random_quest_data=ujson.load(random_quest)
        day_num=random_quest_data["Day"]
        tdy_week_num=datetime.today().weekday()
        comp_check=False

        if day_num==tdy_week_num:
            comp_check=True
            rank_val_list=["C","D","E"]
            rank=random.choice(rank_val_list)
            ab_points=["STR","AGI","VIT","INT","PER","MAN"]
            random_ab=ab_points[random.randint(0, 5)]

            # ? Active Quests
            try:
                with open("Files/Player Data/Active_Quests.json", 'r') as active_quests_file:
                    activ_quests=ujson.load(active_quests_file)
                    name_of_activ_quests=list(activ_quests.keys())
                    activ_quests_vals=0
                    for k in name_of_activ_quests:
                        activ_quests_vals+=1
            except:
                name_of_activ_quests=[]

            if activ_quests_vals<13 and activ_quests_vals!=13:
                # ? Quest Name
                with open("Files/Data/Quest_Names.json", 'r') as quest_name_file:
                    quest_names=ujson.load(quest_name_file)
                    if random_ab in ["STR","AGI","VIT"]:
                        names_list=quest_names["STR"]
                        check=True
                        while check:
                            quest_name=random.choice(names_list)
                            if quest_name in name_of_activ_quests:
                                quest_name=random.choice(names_list)
                            else:
                                check=False
                        rew3="STRav"
                    elif random_ab in ["INT","PER","MAN"]:
                        names_list=quest_names["INT"]
                        check=True
                        while check:
                            quest_name=random.choice(names_list)
                            if quest_name in name_of_activ_quests:
                                quest_name=random.choice(names_list)
                            else:
                                check=False
                        rew3="INTav"
                
                # ? Quest Description
                with open("Files/Data/Quest_Desc.json", 'r') as quest_desc_file:
                    quest_desc=ujson.load(quest_desc_file)
                    if rank in ["E", "D"]:
                        desc_list=quest_desc["Easy"]
                        findesc=random.choice(desc_list)
                    elif rank in ["C", "B"]:
                        desc_list=quest_desc["Intermediate"]
                        findesc=random.choice(desc_list)
                    elif rank in ["A", "S"]:
                        desc_list=quest_desc["Hard"]
                        findesc=random.choice(desc_list)

                # ! MAIN INFO
                # ? Rewards
                amt={
                    "S":250000, 
                    "A":130000,
                    "B":80000,
                    "C":5000,
                    "D":500,
                    "E":300
                    }
                
                coinval=amt[rank]
                rew1=f"Coin Bag {coinval}"
                with open("Files/Data/Inventory_List.json", 'r') as rewards_name_file:
                    reward_names=ujson.load(rewards_name_file)
                    reward_names_list=list(reward_names.keys())

                    final_rewards_list=[]
                    for k in reward_names_list:
                        if rank==reward_names[k][0]["rank"]:
                            final_rewards_list.append(k)
                    
                    rew2=random.choice(final_rewards_list)

                # ? Quest Info
                file_name=f"Files/Workout/{random_ab}_based.json"
                with open(file_name, 'r') as quest_file_name:
                    quest_main_names=ujson.load(quest_file_name)
                    quest_main_names_list=list(quest_main_names.keys())
                    final_quest_main_name=random.choice(quest_main_names_list)

                    details=quest_main_names[final_quest_main_name][0]

                # ? Final

                rew_dict={rew1:1, rew2:1}
                if rank in ["S"]:
                    rew_dict["LVLADD"]=8
                    rew_dict[rew3]=10
                elif rank in ["A"]:
                    rew_dict["LVLADD"]=5
                    rew_dict[rew3]=8
                elif rank in ["B"]:
                    rew_dict["LVLADD"]=2
                    rew_dict[rew3]=6

                if details["type"]=='Learn':
                    details["obj_desc"]=details["desc"]

                details["desc"]=findesc
                details["rank"]=rank
                details["ID"]=random.randrange(1,999999)

                if rank=="D":
                    if "amt" in details:
                        if details["amt"]==50:
                            details["amt"]+=10

                        elif details["amt"]==15:
                            details["amt"]+=5

                        elif details["amt"]==2:
                            details["amt"]+=1

                        elif details["amt"]==30:
                            details["amt"]+=15

                    if ("time" in details) and ("amt" not in details):
                        if details["time"]==60:
                            details["time"]+=60

                        elif details["time"]==45:
                            details["time"]+=15

                        elif details["time"]==1:
                            details["time"]+=1

                elif rank=="C":
                    if "amt" in details:
                        if details["amt"]==50:
                            details["amt"]+=20

                        elif details["amt"]==15:
                            details["amt"]+=15

                        elif details["amt"]==2:
                            details["amt"]+=1

                        elif details["amt"]==30:
                            details["amt"]+=30

                    if ("time" in details) and ("amt" not in details):
                        if details["time"]==45:
                            details["time"]+=30

                        elif details["time"]==60:
                            details["time"]+=120

                        elif details["time"]==1:
                            details["time"]+=2

                elif rank=="B":
                    if "amt" in details:
                        if details["amt"]==50:
                            details["amt"]+=50

                        elif details["amt"]==15:
                            details["amt"]+=35

                        elif details["amt"]==2:
                            details["amt"]+=3

                        elif details["amt"]==30:
                            details["amt"]+=60

                    if ("time" in details) and ("amt" not in details):
                        if details["time"]==45:
                            details["time"]+=45

                        elif details["time"]==60:
                            details["time"]+=240

                        elif details["time"]==1:
                            details["time"]+=4

                elif rank=="A":
                    if "amt" in details:
                        if details["amt"]==50:
                            details["amt"]+=100

                        elif details["amt"]==15:
                            details["amt"]+=60

                        elif details["amt"]==2:
                            details["amt"]+=5

                        elif details["amt"]==30:
                            details["amt"]+=70

                    if ("time" in details) and ("amt" not in details):
                        if details["time"]==45:
                            details["time"]+=65

                        elif details["time"]==60:
                            details["time"]+=360

                        elif details["time"]==1:
                            details["time"]+=6

                elif rank=="S":
                    if "amt" in details:
                        if details["amt"]==50:
                            details["amt"]+=150

                        elif details["amt"]==15:
                            details["amt"]+=85

                        elif details["amt"]==2:
                            details["amt"]+=8

                        elif details["amt"]==30:
                            details["amt"]+=90

                    if ("time" in details) and ("amt" not in details):
                        if details["time"]==45:
                            details["time"]+=75

                        elif details["time"]==60:
                            details["time"]+=540

                        elif details["time"]==1:
                            details["time"]+=9

                details["Rewards"]=rew_dict

                acti_name=list(quest_main_names.keys())[0]
                details["skill"]=acti_name
                
                activ_quests[quest_name]=[details]

                with open("Files/Player Data/Active_Quests.json", 'w') as fin_active_quest_file:
                    ujson.dump(activ_quests, fin_active_quest_file, indent=6)

                random_quest_data["Day"]=random.randint(0,6)

    if comp_check==True:
        with open('Files/Player Data/Random_Quest_Day.json', 'w') as finalrandom_quest:
            ujson.dump(random_quest_data, finalrandom_quest, indent=4)

        with open('Files/Data/New_Updates.json', 'w') as updatefile:
            fin_data={
                        "Skills":"False",
                        "Quests":"True",
                        "Upgrade":"False",
                        "Lines":"False"
                    }
            ujson.dump(fin_data, updatefile, indent=4)

def make_window_transparent(window,color="#0C679B"):
    window.wm_attributes('-transparentcolor', color)

def animate_window_open(window, target_height, width, step=2, delay=5, doners=False, cached_dims=None):
    current_height = window.winfo_height()
    if current_height >= target_height:
        return

    # Increase height by step.
    new_height = min(current_height + step, target_height)
    
    # Cache screen dimensions if not already provided.
    if cached_dims is None:
        cached_dims = (window.winfo_screenwidth(), window.winfo_screenheight())
    screen_width, screen_height = cached_dims

    # Compute new coordinates to keep the window centered.
    new_x = (screen_width - width) // 2
    new_y = (screen_height - new_height) // 2

    # Update geometry.
    window.geometry(f"{width}x{new_height}+{new_x}+{new_y}")
    
    # Trigger a one-time action when passing the 20% threshold.
    if not doners:
        threshold = 0.2 * target_height
        if current_height < threshold <= new_height:
            # Trigger side effect, e.g. play a sound:
            # subprocess.Popen(['python', 'Files\\Mod\\default\\sfx.py'])
            doners = True

    # Schedule the next update using the cached screen dimensions.
    window.after(max(1, delay // 2), animate_window_open, window, target_height, width, step, delay, doners, cached_dims)

def animate_window_close(window, target_height, width, step=2, delay=5, cached_dims=None):
    current_height = window.winfo_height()
    new_height = max(current_height - step, target_height)
    
    if cached_dims is None:
        cached_dims = (window.winfo_screenwidth(), window.winfo_screenheight())
    screen_width, screen_height = cached_dims

    # Compute new coordinates to keep the window centered.
    new_x = (screen_width - width) // 2
    new_y = (screen_height - new_height) // 2

    # Update geometry.
    window.geometry(f"{width}x{new_height}+{new_x}+{new_y}")

    if new_height > target_height:
        window.after(delay, animate_window_close, window, target_height, width, step, delay, cached_dims)
    else:
        window.quit()

class VideoPlayer:
    def __init__(self, canvas, video_path, del_x=0, del_y=0, resize_factor=0.7, buffer_size=4, pause_duration=0, fps=12):
        self.canvas = canvas
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.image_id = self.canvas.create_image(0, 0, anchor='nw')
        self.frame_queue = queue.Queue(maxsize=buffer_size)
        self.stop_event = threading.Event()
        self.pause_duration = float(pause_duration)
        self.fps = fps
        self.first_frame_displayed = False
        self.rotate_video = False  # Flag to check if rotation is needed

        # Wait for valid canvas dimensions.
        self.canvas.update_idletasks()
        while self.canvas.winfo_width() <= 1 or self.canvas.winfo_height() <= 1:
            self.canvas.update_idletasks()
            time.sleep(0.01)

        ret, frame = self.cap.read()
        if not ret:
            raise ValueError("Unable to read video file.")

        # Check if the canvas is taller than it is wide
        if self.canvas.winfo_height() > self.canvas.winfo_width():
            self.rotate_video = True  # Set flag to rotate frames
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        self.original_width = frame.shape[1]
        self.original_height = frame.shape[0]
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Cache canvas dimensions.
        self.last_canvas_width = None
        self.last_canvas_height = None
        self.last_new_width = None
        self.last_new_height = None
        self.new_dimensions = self._calculate_new_dimensions()

        # Start the background thread for reading frames.
        self.read_thread = threading.Thread(target=self._read_frames, daemon=True)
        self.read_thread.start()

        # Start the update loop on the main thread.
        self.update_frame()

    def _calculate_new_dimensions(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if self.last_canvas_width == canvas_width and self.last_canvas_height == canvas_height:
            return self.last_new_width, self.last_new_height

        # "Cover" effect: scale so that one edge exactly matches.
        scaling_factor = max(canvas_width / self.original_width, canvas_height / self.original_height)
        new_width = int(self.original_width * scaling_factor)
        new_height = int(self.original_height * scaling_factor)

        self.last_canvas_width = canvas_width
        self.last_canvas_height = canvas_height
        self.last_new_width = new_width
        self.last_new_height = new_height
        return new_width, new_height

    def _read_frames(self):
        while not self.stop_event.is_set():
            ret, frame = self.cap.read()
            if not ret:
                # Loop video by resetting the frame pointer.
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
                if not ret:
                    continue
            
            # Rotate frame if necessary
            if self.rotate_video:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            new_width, new_height = self.new_dimensions
            # Choose interpolation based on resizing direction.
            interp = cv2.INTER_LINEAR if (new_width > self.original_width or new_height > self.original_height) else cv2.INTER_AREA
            frame = cv2.resize(frame, (new_width, new_height), interpolation=interp)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Use non-blocking put; drop frame if the queue is full.
            try:
                self.frame_queue.put_nowait(frame)
            except queue.Full:
                pass

    def update_frame(self):
        self.new_dimensions = self._calculate_new_dimensions()
        try:
            frame = self.frame_queue.get_nowait()
        except queue.Empty:
            frame = None

        if frame is not None:
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            # Center the frame on the canvas.
            x_center = (canvas_width - frame.shape[1]) // 2
            y_center = (canvas_height - frame.shape[0]) // 2
            self.canvas.coords(self.image_id, x_center, y_center)
            self.canvas.itemconfig(self.image_id, image=imgtk)
            self.canvas.imgtk = imgtk  # Keep a reference to avoid garbage collection.

            if not self.first_frame_displayed:
                self.first_frame_displayed = True
                self.canvas.after(int(self.pause_duration * 1000), self.update_frame)
                return

        # Schedule next frame update based on fps.
        self.canvas.after(int(1000 / self.fps), self.update_frame)

    def __del__(self):
        try:
            self.stop_event.set()
            self.read_thread.join(timeout=1)
            if self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass

def set_preview_temp(o_name1,qt1):
    with open("Files/Temp Files/Inventory temp.csv", 'w', newline='') as new_csv_open:
        rec=[o_name1, qt1, "Preview"]
        writer=csv.writer(new_csv_open)
        writer.writerow(rec)
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
            theme_data=ujson.load(themefile)
            theme=theme_data["Theme"]
    subprocess.Popen(['python', f'{theme} Version/Item Data/gui.py/gui.py'])

def center_window(root, width, height):
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate position x, y to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set the dimensions of the window and the position
    root.geometry(f'{width}x{height}+{x}+{y}')

def update_penalty_countdown(duration_seconds, countdown_label, canvas, window):
    # Calculate end time
    end_time = datetime.now() + timedelta(seconds=duration_seconds)

    # Update the countdown every second
    def update_timer():
        # Get the remaining time
        remaining_time = end_time - datetime.now()

        # If time is up, perform the necessary actions
        if remaining_time.total_seconds() <= 0:
            with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
                theme_data = ujson.load(themefile)
                theme = theme_data["Theme"]
            subprocess.Popen(['python', f'{theme} Version/Penalty Quest Rewards/gui.py'])
            window.quit()
            return

        # Format the remaining time (hours:minutes:seconds)
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        timer_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        canvas.itemconfig(countdown_label, text=timer_text)

        # Schedule the function to run again after 1 second
        window.after(1000, update_timer)

    # Start the countdown
    update_timer()

def start_job(canvas):
    with open("Files/Player Data/Job_info.json", 'r') as stat_fson:
        data=ujson.load(stat_fson)

    canvas.itemconfig("Jobs", state="hidden")
    data["status"][1]["job_confirm"]='True'

    with open("Files/Player Data/Job_info.json", 'w') as fson:
        ujson.dump(data, fson, indent=4)

def three_val(val):
    values=f"{val:03d}:"
    new_value=''
    for k in values:
        if k!=':':
            new_value+=k
    return new_value

def sign(num):
    if num<0:
        return "-"
    elif num>0:
        return "+"
    elif num==0:
        return ""

def pos_fix(num):
    if num<0:
        num=abs(num)
        return str(num)
    elif num==0:
        return ""
    else:
        return str(num)

def get_fin_xp():
    # Load the status file
    with open("Files/Player Data/Status.json", 'r') as fson:
        data = ujson.load(fson)
        lvl = int(data["status"][0]['level'])  # Current level
        old_lvl=lvl
        xp = float(data["status"][0]['XP'])  # Current XP value
        last_lvl = int(data["status"][0]['last_level'])  # Last processed level

    # Load level-up values
    with open("Files/Data/Level_Up_Values.json", 'r') as fron2:
        level_up_values = ujson.load(fron2)["XP Check"]

    leveled_up = False
    new_lvl = lvl

    # Check for level-ups
    for k, v in level_up_values.items():
        level_threshold = int(k)
        if xp >= float(v) and level_threshold > new_lvl:
            new_lvl = level_threshold
            leveled_up = True

    if leveled_up:
        level_difference = new_lvl - lvl
        data["status"][0]['level'] = new_lvl
        data["status"][0]['last_level'] = new_lvl

        # Increment stats based on the number of levels gained
        data["status"][0]['hp'] += 10 * level_difference
        data["status"][0]['mp'] += 10 * level_difference
        data["status"][0]['str'] += 1 * level_difference
        data["status"][0]['int'] += 1 * level_difference
        data["status"][0]['agi'] += 1 * level_difference
        data["status"][0]['vit'] += 1 * level_difference
        data["status"][0]['per'] += 1 * level_difference
        data["status"][0]['man'] += 1 * level_difference
        data["status"][0]['fatigue_max'] += 10 * level_difference

        # Save updated status to file
        with open("Files/Player Data/Status.json", 'w') as up_fson:
            ujson.dump(data, up_fson, indent=4)

        rank_up(old_lvl, new_lvl)
    fin_xp = None
    if str(lvl + 1) in level_up_values:
        next_level_xp = float(level_up_values[str(lvl + 1)])
        fin_xp = next_level_xp - xp  # Difference between next level XP and current XP

    return [leveled_up,fin_xp]

def rank_up(old_lvl, new_lvl):
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data = ujson.load(themefile)
        theme = theme_data["Theme"]

    old_rank=give_ranking(old_lvl)
    new_rank=give_ranking(new_lvl)
    if old_rank==new_rank:
        subprocess.Popen(['python', f'{theme} Version/Leveled up/gui.py'])
    else:
        with open("Files/Temp Files/Rank file.csv", "w", newline="") as f:
            writer=csv.writer(f)
            writer.writerow([f"{old_lvl}"])
        subprocess.Popen(['python', f'{theme} Version/Rank up/gui.py'])

def return_back_to_tab(loc,window):
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
        fin_loc=f'{theme} Version/{loc}/gui.py'
    subprocess.Popen(['python', fin_loc])
    window.quit()   

def fade_out(window, alpha):
    if alpha > 0:
        window.attributes('-alpha', alpha)
        alpha -= 0.08
        window.after(1, fade_out, window, alpha)
    else:
        window.attributes('-alpha', 0)

def give_ranking(level):
    if level>=101:
        return "National"
    elif level>=91 and level<=100:
        return "SSS"
    elif level>=81 and level<=90:
        return "SS"
    elif level>=66 and level<=80:
        return "S"
    elif level>=46 and level<=65:
        return "A"
    elif level>=31 and level<=45:
        return "B"
    elif level>=21 and level<=30:
        return "C"
    elif level>=11 and level<=20:
        return "D"
    elif level>=1 and level<=10:
        return "E"

def give_ranking_from_daily(daily_lvl):
    if daily_lvl>=91 and daily_lvl<=100:
        return 1300
    elif daily_lvl>=71 and daily_lvl<=90:
        return 600
    elif daily_lvl>=56 and daily_lvl<=70:
        return 285
    elif daily_lvl>=41 and daily_lvl<=55:
        return 175
    elif daily_lvl>=21 and daily_lvl<=40:
        return 80
    elif daily_lvl>=1 and daily_lvl<=20:
        return 40
    
def give_fatigue_from_rank(rank):
    if rank=='E':
        return 40
    elif rank=='D':
        return 80
    elif rank=='C':
        return 175
    elif rank=='B':
        return 285
    elif rank=='A':
        return 600
    elif rank=='S':
        return 1300
 
def message_open(message):
    fout=open('Files/Checks/Message.csv', 'w', newline='')
    fw=csv.writer(fout)
    rec=[message]
    fw.writerow(rec)
    fout.close()
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    subprocess.Popen(['python', f"{theme} Version/Message/gui.py"])

def resize_image_cv(image_path, size):
    """
    Resize an image using OpenCV for faster performance.
    It preserves the alpha channel if present.
    """
    try:
        # Read image; IMREAD_UNCHANGED ensures the alpha channel is preserved.
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"Error reading image: {image_path}")
            return None

        # Resize image using INTER_AREA interpolation (optimized for downscaling)
        resized = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

        # Convert color channels: OpenCV loads images in BGR or BGRA order.
        if resized.ndim == 3:
            channels = resized.shape[2]
            if channels == 3:
                # Convert BGR to RGB.
                resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            elif channels == 4:
                # Convert BGRA to RGBA.
                resized = cv2.cvtColor(resized, cv2.COLOR_BGRA2RGBA)
        return resized
    except Exception as e:
        print(f"Error resizing {image_path}: {e}")
        return None

def preload_images(image_paths, size, max_workers=None):
    """
    Preload images by resizing them in parallel using OpenCV
    and converting them to ImageTk.PhotoImage objects.
    
    Parameters:
      image_paths: List of image file paths.
      size: Desired size (width, height) tuple.
      max_workers: Maximum number of threads to use. If None, it is set to a safe default.
      
    Returns:
      A list of ImageTk.PhotoImage objects.
    """
    # Set max_workers to a safe default if not provided.
    if max_workers is None:
        max_workers = min(32, (os.cpu_count() or 1) + 4)
    
    preloaded_images = []
    
    # Use ThreadPoolExecutor to parallelize resizing.
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        func = partial(resize_image_cv, size=size)
        resized_images = list(executor.map(func, image_paths))
    
    # Convert each resized NumPy image to a PIL Image then to PhotoImage.
    for img in resized_images:
        if img is None:
            continue
        pil_img = Image.fromarray(img)
        preloaded_images.append(ImageTk.PhotoImage(pil_img))
    
    return preloaded_images

def side_bar(image, size, alt=False):
    # Construct the path to the image
    s = 'thesystem/side_bars/' + image
    job=thesystem.misc.return_status()["status"][1]["job"]

    if alt or job!="None": 
        s = 'thesystem/alt_side_bars/' + image
    # Check if the image exists
    if os.path.exists(s):
        # Open and resize the image
        s_m = Image.open(s).resize(size)
        # Convert the image to a format Tkinter can use
        return ImageTk.PhotoImage(s_m)
    else:
        print(f"Image {s} not found.")
        return None

def info_open(message):
    subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])
    fout=open('Files/Temp Files/help.csv', 'w', newline='')
    fw=csv.writer(fout)
    rec=[message]
    fw.writerow(rec)
    fout.close()
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    subprocess.Popen(['python', f"{theme} Version/Info/gui.py"])

def event_tracker():
    while True:
        today_day = datetime.today().strftime('%A')
        current_time = datetime.now().strftime("%H:%M")
        
        with open("Files/Player Data/Player Events.json", "r") as f:
            data = ujson.load(f)
        data_keys=data.keys()
        for key in data_keys:
            if today_day in data[key]["days"]:
                if data[key]["time"]==current_time:
                    with open("Files/Temp Files/Event.csv", "w", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([key])
                    data[key]["begun"]=True
                    with open("Files/Player Data/Player Events.json", "w") as f:
                        ujson.dump(data, f, indent=6)
                    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
                        theme_data=ujson.load(themefile)
                        theme=theme_data["Theme"]
                    subprocess.Popen(['python', f"{theme} Version/Urgent Quest PVE/gui.py"])
                elif current_time > data[key]["time"]:
                    if data[key]["begun"]==False:
                        print()
        time.sleep(3)
