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
POSITION_FILE = "Files/Player Data/window_positions.json"

def overwrite_python_file_with_text(py_file_path, txt_file_path):
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
            new_content = txt_file.read()

        with open(py_file_path, 'w', encoding='utf-8') as py_file:
            py_file.write(new_content)

        print(f"✅ Successfully updated: {py_file_path}")
        os.remove(txt_file_path)
    except Exception as e:
        print(f"❌ Failed to update {py_file_path}: {e}")


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

def run_once_setting_chaneg():
    new_file_data={
    "Settings": {
        "Calorie_Penalty": "True",
        "Main_Penalty": "True",
        "Performernce (ANIME):": "False",
        "Transparency": 0.75,
        "SFX Delay": 0,
        "Microphone": "False"
    }
}

    with open("Files/Player Data/Settings.json", 'w') as settings_file:
        ujson.dump(new_file_data, settings_file, indent=4) 

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

def animate_window_open(window,target_height: int, width: int, step: int = 2, delay: int = 16, threshold_triggered: bool = False, cached_dims: tuple = None):
    """
    Animate the opening of a window by gradually increasing its height,
    keeping it centered on the screen. Triggers an optional side effect
    when reaching 20% of target height.

    Args:
        window: The Tkinter window to animate.
        target_height (int): Final height to reach.
        width (int): Fixed width of the window.
        base_step (int, optional): Minimum step increment per frame. Defaults to 2.
        delay (int, optional): Delay between frames in ms (aim for 16ms for ~60fps). Defaults to 16.
        threshold_triggered (bool, optional): Whether the 20% height side effect has fired. Defaults to False.
        cached_dims (tuple, optional): Screen dimensions (width, height). If None, they will be fetched.
    """
    current_height = window.winfo_height()

    if current_height >= target_height:
        return

    # --- Calculate dynamic step for smoother scaling ---
    remaining = target_height - current_height
    dynamic_step = max(step, int(remaining * 0.15))
    new_height = min(current_height + dynamic_step, target_height)

    # --- Get screen size only once ---
    if cached_dims is None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        cached_dims = (screen_width, screen_height)
    else:
        screen_width, screen_height = cached_dims

    # --- Recenter window with new height ---
    new_x = (screen_width - width) // 2
    new_y = (screen_height - new_height) // 2
    window.geometry(f"{width}x{new_height}+{new_x}+{new_y}")

    # --- Trigger one-time effect at 20% progress ---
    if not threshold_triggered and current_height < 0.2 * target_height <= new_height:
        # Example trigger: subprocess.Popen(['python', 'Files\\Mod\\default\\sfx.py'])
        threshold_triggered = True

    # --- Schedule next frame ---
    window.after(
        delay,
        animate_window_open,
        window,
        target_height,
        width,
        step,
        delay,
        threshold_triggered,
        cached_dims
    )

def animate_window_close(window, target_height, width, step=5, delay=10):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    def update_frame():
        current_height = window.winfo_height()
        new_height = max(current_height - step, target_height)

        new_x = (screen_width - width) // 2
        new_y = (screen_height - new_height) // 2

        window.geometry(f"{width}x{new_height}+{new_x}+{new_y}")

        if new_height > target_height:
            window.after(delay, update_frame)
        else:
            # Optional cleanup or sound trigger
            window.quit()

    # Start animation safely
    window.after(0, update_frame)

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

class FastVideoPlayer:
    def __init__(self, canvas, preloaded_frames=None, del_x=0, del_y=0, resize_factor=0.7, buffer_size=4, pause_duration=0, fps=12, video_path=None):
        self.canvas = canvas
        self.del_x = del_x
        self.del_y = del_y
        self.pause_duration = float(pause_duration)
        self.fps = fps
        self.frame_queue = queue.Queue(maxsize=buffer_size)
        self.stop_event = threading.Event()
        self.first_frame_displayed = False
        self.rotate_video = False
        self.preloaded_mode = preloaded_frames is not None
        self.image_id = self.canvas.create_image(0, 0, anchor='nw')

        # Wait for canvas dimensions to initialize
        self.canvas.update_idletasks()
        while self.canvas.winfo_width() <= 1 or self.canvas.winfo_height() <= 1:
            self.canvas.update_idletasks()
            time.sleep(0.01)

        if self.preloaded_mode:
            self.frames = preloaded_frames
            first_frame = self.frames[0]
        else:
            self.video_path = video_path
            self.cap = cv2.VideoCapture(video_path)
            ret, first_frame = self.cap.read()
            if not ret:
                raise ValueError("Unable to read video file.")

        # Auto-rotate if necessary
        if self.canvas.winfo_height() > self.canvas.winfo_width():
            self.rotate_video = True
            first_frame = cv2.rotate(first_frame, cv2.ROTATE_90_CLOCKWISE)

        self.original_width = first_frame.shape[1]
        self.original_height = first_frame.shape[0]
        self.last_canvas_width = None
        self.last_canvas_height = None
        self.last_new_width = None
        self.last_new_height = None
        self.new_dimensions = self._calculate_new_dimensions()

        if self.preloaded_mode:
            self.current_frame_index = 0
            self.read_thread = threading.Thread(target=self._loop_preloaded_frames, daemon=True)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.read_thread = threading.Thread(target=self._read_frames, daemon=True)
        self.read_thread.start()

        self.update_frame()
    
    def _loop_preloaded_frames(self):
        while not self.stop_event.is_set():
            frame_data = self.frames[self.current_frame_index]
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

            # Lazy load: Load frame only when needed
            if isinstance(frame_data, str):  # Assume it's a file path
                frame = cv2.imread(frame_data)
                if frame is None:
                    continue
            else:
                frame = frame_data  # Already-loaded frame

            if self.rotate_video:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            new_width, new_height = self.new_dimensions
            interp = cv2.INTER_LINEAR if (new_width > self.original_width or new_height > self.original_height) else cv2.INTER_AREA
            frame = cv2.resize(frame, (new_width, new_height), interpolation=interp)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            try:
                self.frame_queue.put_nowait(frame)
            except queue.Full:
                pass

            time.sleep(1 / self.fps)

    def _calculate_new_dimensions(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if self.last_canvas_width == canvas_width and self.last_canvas_height == canvas_height:
            return self.last_new_width, self.last_new_height

        scaling_factor = max(canvas_width / self.original_width, canvas_height / self.original_height)
        new_width = int(self.original_width * scaling_factor)
        new_height = int(self.original_height * scaling_factor)

        self.last_canvas_width = canvas_width
        self.last_canvas_height = canvas_height
        self.last_new_width = new_width
        self.last_new_height = new_height

        return new_width, new_height

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
            x_center = (canvas_width - frame.shape[1]) // 2
            y_center = (canvas_height - frame.shape[0]) // 2
            self.canvas.coords(self.image_id, x_center, y_center)
            self.canvas.itemconfig(self.image_id, image=imgtk)
            self.canvas.imgtk = imgtk  # Prevent garbage collection

            if not self.first_frame_displayed:
                self.first_frame_displayed = True
                self.canvas.after(int(self.pause_duration * 1000), self.update_frame)
                return

        self.canvas.after(int(1000 / self.fps), self.update_frame)

class LazyImageLoader:
    def __init__(self, pil_data):
        self.pil_data = pil_data
        self.cache = {}

    def __getitem__(self, index):
        if index not in self.cache:
            arr, mode = self.pil_data[index]
            img = Image.fromarray(arr)
            if img.mode != mode:
                img = img.convert(mode)
            self.cache[index] = ImageTk.PhotoImage(img)
        return self.cache[index]

    def __len__(self):
        return len(self.pil_data)

def set_preview_temp(o_name1,qt1):
    with open("Files/Temp Files/Inventory temp.csv", 'w', newline='') as new_csv_open:
        rec=[o_name1, qt1, "Preview"]
        writer=csv.writer(new_csv_open)
        writer.writerow(rec)
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
            theme_data=ujson.load(themefile)
            theme=theme_data["Theme"]
    subprocess.Popen(['python', f'{theme} Version/Item Data/gui.py'])

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

def xp_formula(n):
    if 1 <= n <= 20:
        return 20 * n + 10
    elif 21 <= n <= 100:
        return 410 + 0.3444 * (n - 20) ** 3
    elif 101 <= n <= 200:  # n > 100
        return xp_formula(100) + 0.28 * (n - 80) ** 3
    else:  # n > 100
        return xp_formula(200) + 0.15 * (n - 180) ** 3

def get_fin_xp():
    # Load the status file
    with open("Files/Player Data/Status.json", 'r') as fson:
        data = ujson.load(fson)
        lvl = int(data["status"][0]['level'])  # Current level
        old_lvl = lvl
        xp = float(data["status"][0]['XP'])  # Current XP value
        last_lvl = int(data["status"][0]['last_level'])  # Last processed level

    leveled_up = False
    new_lvl = lvl

    # Dynamic level checking (no level cap)
    while xp >= xp_formula(new_lvl + 1):
        new_lvl += 1
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

    # XP needed for next level
    next_level_xp = xp_formula(new_lvl + 1)
    fin_xp = next_level_xp - xp

    return [leveled_up, fin_xp]

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

def rank_up_skill(name_of_skill, old_level):
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data = ujson.load(themefile)
        theme = theme_data["Theme"]

    with open("Files/Temp Files/Skill file.csv", "w", newline="") as f:
        writer=csv.writer(f)
        writer.writerow([f"{name_of_skill}", f"{old_level}"])
    subprocess.Popen(['python', f'{theme} Version/Skill Level up/gui.py'])

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

def images_to_npy_with_mode(folder_path, output_path, resize=None, sort=True):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if sort:
        files.sort()

    data_to_save = []

    for filename in files:
        path = os.path.join(folder_path, filename)
        if not os.path.exists(path):
            continue

        img = Image.open(path)
        mode = img.mode
        img = img.convert("RGBA")

        if resize:
            img = img.resize(resize)

        data_to_save.append((np.array(img), mode))

    np.save(output_path, np.array(data_to_save, dtype=object), allow_pickle=True)
    print(f"[Cached] {len(data_to_save)} frames → {output_path}")

def load_or_cache_images(folder_path, resize, job, type_, profile=False):
    width, height = resize
    job = job.upper()
    type_ = type_.lower()

    if profile: start_total = time.perf_counter()

    # Step 1: Build cache filename
    if job == "NONE":
        cache_name = f"{type_}_frame_stack {width} {height}.npy"
    else:
        cache_name = f"alt_{type_}_frame_stack {width} {height}.npy"

    cache_path = os.path.join(folder_path, cache_name)

    # Step 2: Check for cache
    if profile: start_check = time.perf_counter()
    if not os.path.exists(cache_path):
        print(f"[CACHE MISS] Generating cache: {cache_path}")
        images_to_npy_with_mode(folder_path, cache_path, resize=resize)
    if profile: end_check = time.perf_counter()

    # Step 3: Load raw data
    if profile: start_load = time.perf_counter()
    cached_data = np.load(cache_path, allow_pickle=True)
    if isinstance(cached_data, np.ndarray):
        cached_data = cached_data.tolist()
    if profile: end_load = time.perf_counter()

    # Step 4: Wrap in lazy loader
    if profile: start_wrap = time.perf_counter()
    loader = LazyImageLoader(cached_data)
    if profile: end_wrap = time.perf_counter()

    end_total = time.perf_counter()

    if profile:
        # Profile report
        print(f"\n--- Load Profile for '{type_}' ({job}) ---")
        print(f"Cache check/build  : {(end_check - start_check):.4f}s")
        print(f"Cache load (NumPy) : {(end_load - start_load):.4f}s")
        print(f"LazyLoader wrapping: {(end_wrap - start_wrap):.4f}s")
        print(f"TOTAL LOAD TIME    : {(end_total - start_total):.4f}s")
        print("----------------------------------------\n")

    return loader

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

def skill_message(skill_name):
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data = ujson.load(themefile)
        theme = theme_data["Theme"]

    with open("Files/Temp Files/Skill Use.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([skill_name])
    
    subprocess.Popen(['python', f'{theme} Version/Skill Use/gui.py'])

def skill_use(skill_name,cooldown, mana=0, skill_open=True):
    with open("Files/Player Data/Status.json", 'r') as f:
        status_data = ujson.load(f)
        mp = status_data["status"][0]["mp"]
        if mp < mana:
            return False
    with open("Files/Player Data/Skill tracker.json", "r") as f:
        skill_track_data = ujson.load(f)
    
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("Files/Player Data/Skill.json", 'r') as f:
        skill_data = ujson.load(f)
    
    if skill_name not in skill_data.keys():
        return False

    try:
        skill_track_data[skill_name]["last_used"]
        dt1 = datetime.strptime(skill_track_data[skill_name]["last_used"], "%Y-%m-%d %H:%M:%S")
        dt2 = datetime.strptime(formatted, "%Y-%m-%d %H:%M:%S")

        # Calculate time difference
        diff_seconds = abs((dt2 - dt1).total_seconds())
        if diff_seconds >= cooldown:
            skill_track_data[skill_name]["last_used"] = formatted
            with open("Files/Player Data/Skill tracker.json", "w") as f:
                ujson.dump(skill_track_data, f, indent=6)

                if skill_open: skill_message(skill_name)

            return True
        else:
            return False
    except:
        skill_track_data[skill_name]={"last_used":formatted, "cooldown":cooldown}
        skill_track_data[skill_name]["last_used"] = formatted
        with open("Files/Player Data/Skill tracker.json", "w") as f:
            ujson.dump(skill_track_data, f, indent=6)

        if skill_open: skill_message(skill_name)

        return True

def skill_tracking_and_fatigue():
    fatigue_open=False
    while True:
        with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
            theme_data=ujson.load(themefile)
            theme=theme_data["Theme"]
        
        if not os.path.exists("Files/Player Data/Skill tracker.json"):
            with open("Files/Player Data/Skill tracker.json", "w") as f:
                ujson.dump({}, f, indent=6)

        #Status File
        with open("Files/Player Data/Status.json", 'r') as f:
            status_data = ujson.load(f)
        
        #Skill File
        with open("Files/Player Data/Skill.json", 'r') as f:
            skill_data = ujson.load(f)

        fat_percent=(status_data["status"][0]["fatigue"]/status_data["status"][0]["fatigue_max"])*100


        if fat_percent>=50:
            if skill_use("Nimble Endurance", (24*60*60)) == True and ("Nimble Endurance"in skill_data) and fat_percent>=100:
                with open("Files/Player Data/Status.json", 'r') as f:
                    status_data = ujson.load(f)

                status = status_data["status"][0]

                fat_percent = (status["fatigue"] / status["fatigue_max"]) * 100
                lvl=skill_data["Nimble Endurance"][0]["lvl"]
                if type(lvl)==str: lvl=10
                reduce_fatigue_value = (2*lvl / 100) * status["fatigue_max"]
                status["fatigue"] -= reduce_fatigue_value

                # Step 4: Update fatigue in Status.json
                with open("Files/Player Data/Status.json", 'w') as f:
                    ujson.dump(status_data, f, indent=6)
            
            elif skill_use("Rush", (24*60*60)) == True and ("Rush"in skill_data):

                status = status_data["status"][0]

                fat_percent = (status["fatigue"] / status["fatigue_max"]) * 100
                lvl=skill_data["Rush"][0]["lvl"]
                if type(lvl)==str: lvl=10
                reduce_fatigue_value = (2*lvl / 100) * status["fatigue_max"]
                status["fatigue"] -= reduce_fatigue_value

                # Step 4: Update fatigue in Status.json
                with open("Files/Player Data/Status.json", 'w') as f:
                    ujson.dump(status_data, f, indent=6)

            if fatigue_open==False:
                subprocess.Popen(['python', f"{theme} Version/Fatigue/gui.py"])
                fatigue_open=True

        if fat_percent<50:
            fatigue_open=False


        time.sleep(3)
        
def equipment_value_plus(val):
    with open("Files/Player Data/Skill.json", 'r') as f:
        skill_data = ujson.load(f)

    addition = 0
    if skill_use("Mind Over Matter", (0)) and ("Mind Over Matter" in skill_data):
        lvl = skill_data["Mind Over Matter"][0]["lvl"]
        if isinstance(lvl, str):
            lvl = 10

        equipment_percent = 0.05 * lvl
        addition = abs(val) * equipment_percent

    if val == 0:
        return 0

    if val > 0:
        final_value = int(val + addition)
    else:
        final_value = int(val - addition)

    return final_value

def fix_7x():
    if os.path.exists("thesystem/temp 7x1.txt"):
        with open("Files/Player Data/Settings.json", "w") as fson:
            data={
                    "Settings": {
                        "Calorie_Penalty": "True",
                        "Main_Penalty": "True",
                        "Performernce (ANIME):": "False",
                        "Transparency": 0.75,
                        "SFX Delay": 0,
                        "Microphone": "False"
                    }
                }
            ujson.dump(data, fson, indent=3)

        with open("Files/Data/Skill_List.json", "w") as skill_file:
            skill_data={
                "Rush": [
                    {
                    "lvl": 1,
                    "type": "Passive",
                    "desc": "Lowers fatigue by 2% for every level upgrade. (Mana Cost: 100)",
                    "base": "STR",
                    "rewards": {
                        "STRav": 5,
                        "Gatekeepers Necklace": 1
                    },
                    "cooldown": "24h",
                    "mana": 100
                    },
                    {
                    "Condition": ["VIT"]
                    }
                ],
                "Dash": [
                    {
                    "lvl": 1,
                    "type": "Active",
                    "desc": "Decreases Time based activities by 5% for each level. (Mana Cost: 250)",
                    "base": "STR",
                    "rewards": {
                        "STRav": 5,
                        "Gauntlet of Lightning": 1
                    },
                    "cooldown": "1h",
                    "mana": 250
                    },
                    {
                    "Condition": ["AGI"]
                    }
                ],
                "Negotiation": [
                    {
                    "lvl": 1,
                    "type": "Passive",
                    "desc": "Get a 1.5% per level coin cashback on trades and buys. Also applies to selling items. Cannot be stopped. (Mana Cost: 50)",
                    "base": "INT",
                    "rewards": {
                        "INTav": 5,
                        "Demon Monarch's Ring": 1
                    },
                    "cooldown": "None",
                    "mana": 50
                    },
                    {
                    "Condition": ["MAN"]
                    }
                ],
                "Tacital": [
                    {
                    "lvl": 1,
                    "type": "Passive",
                    "desc": "X% chance to be chosen as raid leader if party members are at similar or lower levels. Cannot be stopped.",
                    "base": "INT",
                    "rewards": {
                        "INTav": 5,
                        "Aetherial Circlet": 1
                    },
                    "cooldown": "None",
                    "mana": ""
                    },
                    {
                    "Condition": ["INT"]
                    }
                ],
                "Mind Over Matter": [
                    {
                    "lvl": 1,
                    "type": "Passive",
                    "desc": "Increases stat values on equipped armor by 5%; scalable with level upgrades.  Applies to Debuffs as well (Mana Cost: 75)",
                    "base": "INT",
                    "rewards": {
                        "INTav": 5,
                        "Ring of Arcane Mastery": 1
                    },
                    "cooldown": "None",
                    "mana": 75
                    },
                    {
                    "Condition": ["INT", "MAN"]
                    }
                ],
                "Iron Warrior": [
                    {
                    "lvl": 1,
                    "type": "Passive",
                    "desc": "Increases HP by 2.5% when below 50% of max HP, for every level upgrade. (Mana Cost: 100)",
                    "base": "STR",
                    "rewards": {
                        "STRav": 5,
                        "Titanium Plate Armor": 1
                    },
                    "cooldown": "24h",
                    "mana": 100
                    },
                    {
                    "Condition": ["STR", "VIT"]
                    }
                ],
                "Charismatic Aura": [
                    {
                    "lvl": 1,
                    "type": "Passive",
                    "desc": "Slightly increases stat and level on leaderboards. **Does not affect dungeon workouts.**",
                    "base": "MAN",
                    "rewards": {
                        "INTav": 5,
                        "High-Minister's Amulet": 1
                    },
                    "cooldown": "24h",
                    "mana": ""
                    },
                    {
                    "Condition": ["MAN", "PER"]
                    }
                ],
                "Nimble Endurance": [
                    {
                    "lvl": 1,
                    "type": "Passive",
                    "desc": "Reduces the Fatigue by 5% per Level when Fatigue was over 100% (Mana Cost: 250)",
                    "base": "AGI",
                    "rewards": {
                        "STRav": 5,
                        "Dragonscale Boots": 1
                    },
                    "cooldown": "24h",
                    "mana": 250
                    },
                    {
                    "Condition": ["AGI", "VIT"]
                    }
                ],
                "Iron Fist": [
                    {
                    "lvl": 1,
                    "type": "Active",
                    "desc": "Same as Fatal Strike, but reduces 2% of HP as you level up. (Mana Cost: 100)",
                    "base": "STR",
                    "rewards": {
                        "STRav": 5,
                        "Gauntlet of the Eternal Guardian": 1
                    },
                    "cooldown": "1h",
                    "mana": 100
                    },
                    {
                    "Condition": ["STR", "VIT"]
                    }
                ],
                "Fatal Strike": [
                    {
                    "lvl": 1,
                    "type": "Active",
                    "desc": "Reduces workout values by 2% for self per level upgrade. (Mana Cost: 200)",
                    "base": "STR",
                    "rewards": {
                        "STRav": 5,
                        "Blade of Precision": 1
                    },
                    "cooldown": "1h",
                    "mana": 200
                    },
                    {
                    "Condition": ["STR", "AGI"]
                    }
                ],
                "Resourceful Adaptation": [
                    {
                    "lvl": 1,
                    "type": "Active",
                    "desc": "Allows changing workouts in dungeons randomly. (Mana Cost: 150)",
                    "base": "INT",
                    "rewards": {
                        "INTav": 5,
                        "Chameleon Cloak": 1
                    },
                    "cooldown": "1h",
                    "mana": 150
                    },
                    {
                    "Condition": ["INT", "PER"]
                    }
                ],
                "Brute Force Mastery": [
                    {
                    "lvl": 1,
                    "type": "Active",
                    "desc": "Reduces the difficulty of STR-based tasks by 7% per level, but increases the difficulty of AGI-based tasks by 5% per level. Lasts for 30 minutes. (Mana Cost: 150)",
                    "base": "STR",
                    "rewards": {
                        "First Glove of Colossus": 1,
                        "Second Glove of Colossus": 1
                    },
                    "cooldown": "1h",
                    "mana": 150
                    },
                    {
                    "Condition": ["STR"]
                    }
                ]
                }

            ujson.dump(skill_data, skill_file, indent=6)

        with open("Files/Data/Dungeon_Boss_List.json") as data_dungeon_boss:
            dunegon_boss_data={
                    "Red Ants":{
                        "rank":"A",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":40
                    },
                    "White Ants":{
                        "rank":"S",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":50
                    },
                    "Small Goblin":{
                        "rank":"E",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":10
                    },
                    "Wolfmen":{
                        "rank":"D",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":20
                    },
                    "Desert Centipiede":{
                        "rank":"B",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":40
                    },
                    "Steel Fanged Lycan":{
                        "rank":"E",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":10
                    },
                    "Razor Claw Briga":{
                        "rank":"E",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":10
                    },
                    "Black Shadow Razor":{
                        "rank":"E",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":10
                    },
                    "Blue Venom-Fanged Kaska":{
                        "rank":"D",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":20
                    },
                    "Defense Golem":{
                        "rank":"D",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":20
                    },
                    "Carnivorous Ants":{
                        "rank":"C",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":30
                    },
                    "Acid Breathing Spider":{
                        "rank":"C",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":30
                    },
                    "Hell's Gatekeeper Cerberus":{
                        "rank":"A",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":50
                    },
                    "Huge Goblins":{
                        "rank":"D",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":20
                    },
                    "Trained Goblins":{
                        "rank":"C",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":30
                    },
                    "General Goblins":{
                        "rank":"C",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":30
                    },
                    "Goblins Leader":{
                        "rank":"B",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":40
                    },
                    "Serpent of Blood Eyes":{
                        "rank":"B",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":40
                    },
                    "Scorpion King":{
                        "rank":"B",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":40
                    },
                    "Small Scorpion":{
                        "rank":"C",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":30
                    },
                    "High Wolfmen":{
                        "rank":"C",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":30
                    },
                    "Wolf-Lord":{
                        "rank":"B",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":40
                    },
                    "Ice Wraiths":{
                        "rank":"A",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":50
                    },
                    "Ice Bears":{
                        "rank":"A",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":50
                    },
                    "Sleuth Ice Bears":{
                        "rank":"A",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":50
                    },
                    "Yetis":{
                        "rank":"A",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":50
                    },
                    "Baruka - Ice Elf King":{
                        "rank":"S",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":60
                    },
                    "Stone Golems":{
                        "rank":"C",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":30
                    },
                    "Vulcan Guards":{
                        "rank":"A",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":50
                    },
                    "Vulcan":{
                        "rank":"S",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":60
                    },
                    "Skeletal Men":{
                        "rank":"B",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":40
                    },
                    "Trained Skeletal Men":{
                        "rank":"A",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":50
                    },
                    "Metus - Soul Reaper":{
                        "rank":"S",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":60
                    },
                    "Stone Titans":{
                        "rank":"A",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":50
                    },
                    "Dungeon Jackals":{
                        "rank":"C",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":30
                    },
                    "High Orcs":{
                        "rank":"S",
                        "type":"Normal",
                        "swarm":"Yes",
                        "XP":60
                    },
                    "Trained High Orcs":{
                        "rank":"S",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":60
                    },
                    "Leader of the High Orcs":{
                        "rank":"SS",
                        "type":"Boss",
                        "swarm":"No",
                        "XP":100
                    },
                    "Demon Knights":{
                        "rank":"A",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":50
                    },
                    "Demon Noble":{
                        "rank":"A",
                        "type":"Normal",
                        "swarm":"No",
                        "XP":50
                    },
                    "Flame Djinn": {
                        "rank": "S",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 70
                    },
                    "Necrotic Reapers": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 50
                    },
                    "Darkwood Dryad": {
                        "rank": "B",
                        "type": "Normal",
                        "swarm": "No",
                        "XP": 40
                    },
                    "Elder Manticore": {
                        "rank": "A",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 50
                    },
                    "Spectral Assassins": {
                        "rank": "C",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 30
                    },
                    "Ancient Basilisk": {
                        "rank": "S",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 60
                    },
                    "Forest Serpent": {
                        "rank": "C",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 30
                    },
                    "Void Phantoms": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 50
                    },
                    "Crystal Elemental": {
                        "rank": "B",
                        "type": "Normal",
                        "swarm": "No",
                        "XP": 40
                    },
                    "Blight-Infused Treant": {
                        "rank": "S",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 60
                    },
                    "Mire Hags": {
                        "rank": "C",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 30
                    },
                    "Thunder Roc": {
                        "rank": "B",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 40
                    },
                    "Cave Drakes": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 50
                    },
                    "Lich King": {
                        "rank": "SS",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 100
                    },
                    "Frostbound Revenants": {
                        "rank": "D",
                        "type": "Normal",
                        "swarm": "No",
                        "XP": 20
                    },
                    "Shadow Prowlers": {
                        "rank": "C",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 30
                    },
                    "Magma Leviathan": {
                        "rank": "SS",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 100
                    },
                    "Cursed Centurions": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 50
                    },
                    "Storm Elemental": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "No",
                        "XP": 50
                    },
                    "Bone Dragon": {
                        "rank": "S",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 70
                    },
                    "Lunar Shade Wolves": {
                        "rank": "B",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 40
                    },
                    "Sand Revenant": {
                        "rank": "C",
                        "type": "Normal",
                        "swarm": "No",
                        "XP": 30
                    },
                    "Ember Fiends": {
                        "rank": "B",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 40
                    },
                    "Undead Legionnaires": {
                        "rank": "D",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 20
                    },
                    "Ashen Phantoms": {
                        "rank": "C",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 30
                    },
                    "Arcane Minotaur": {
                        "rank": "B",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 40
                    },
                    "Petrifying Gorgons": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "No",
                        "XP": 50
                    },
                    "Bloodthirsty Wraiths": {
                        "rank": "C",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 30
                    },
                    "Savage Orc Berserkers": {
                        "rank": "B",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 40
                    },
                    "Dire Fang Bears": {
                        "rank": "D",
                        "type": "Normal",
                        "swarm": "No",
                        "XP": 20
                    },
                    "Ghastly Revenants": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 50
                    },
                    "Giant Ice Serpent": {
                        "rank": "S",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 60
                    },
                    "Voidborne Behemoth": {
                        "rank": "SS",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 120
                    },
                    "Crimson Slimes": {
                        "rank": "D",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 20
                    },
                    "Spectral Archers": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 50
                    },
                    "Twilight Shapeshifters": {
                        "rank": "B",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 40
                    },
                    "Nightmare Riders": {
                        "rank": "S",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 60
                    },
                    "Venomous Dire Bats": {
                        "rank": "C",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 30
                    },
                    "Stone Elemental": {
                        "rank": "C",
                        "type": "Normal",
                        "swarm": "No",
                        "XP": 30
                    },
                    "Enchanted Willow Wisps": {
                        "rank": "D",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 20
                    },
                    "Death Whisper Harpy": {
                        "rank": "B",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 40
                    },
                    "Cursed Souls": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 50
                    },
                    "Golem Constrictor": {
                        "rank": "A",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 50
                    },
                    "Obsidian Dragon": {
                        "rank": "SS",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 120
                    },
                    "Lava Serpent": {
                        "rank": "B",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 40
                    },
                    "Thunder Wyverns": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 50
                    },
                    "Fire Wraiths": {
                        "rank": "A",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 50
                    },
                    "Poisonous Widow Spider": {
                        "rank": "B",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 40
                    },
                    "Phantom Knights": {
                        "rank": "S",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 60
                    },
                    "Forest Troll": {
                        "rank": "C",
                        "type": "Normal",
                        "swarm": "No",
                        "XP": 30
                    },
                    "Swarm of Shadows": {
                        "rank": "S",
                        "type": "Normal",
                        "swarm": "Yes",
                        "XP": 60
                    },
                    "Crystal Golem": {
                        "rank": "S",
                        "type": "Boss",
                        "swarm": "No",
                        "XP": 60
                    }
                }

            ujson.dump(dunegon_boss_data, data_dungeon_boss, indent=5)

        with open("Files/Player Data/Skill.json", "r") as pl_skill_file:
            file_a=ujson.load(pl_skill_file)

        with open("Files/Data/Skill_List.json", "r") as sys_skill_file:
            file_b=ujson.load(sys_skill_file)

        for skill, entries_a in file_a.items():
            if skill in file_b and isinstance(entries_a, list) and isinstance(file_b[skill], list):
                try:
                    # Update description from file_b to file_a
                    desc_b = file_b[skill][0].get("desc")
                    if desc_b:
                        entries_a[0]["desc"] = desc_b
                except (IndexError, KeyError, TypeError):
                    continue  # Skip malformed entries

        with open("Files/Player Data/Skill.json", "w") as pl_skill_file_write:
            ujson.dump(pl_skill_file_write, file_a, indent=6)

        os.remove("thesystem/temp 7x1.txt")

