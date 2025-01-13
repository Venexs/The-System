<<<<<<< Updated upstream

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json
import queue
import csv
import subprocess
from PIL import Image, ImageTk
from datetime import datetime, timedelta, date
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import sys
import random
import cv2
import os

last_run = 0 

def fin_pen():
    today = datetime.now().date()

    yesterday = today - timedelta(days=1)
    with open('Files/Checks/Daily_time_check.csv', 'r', newline='') as fout:
        fr=csv.reader(fout)
        for k in fr:
            status=k[1]
            dates=k[0]

    p_date=datetime.strptime(dates, "%Y-%m-%d").date()
    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=json.load(themefile)
        theme=theme_data["Theme"]
    with open("Files/Settings.json", 'r') as settings_open:
        setting_data=json.load(settings_open)
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
    with open("Files\Data\Calorie_Count.json", 'r') as calorie_add_file:
        calorie_add_data=json.load(calorie_add_file)
        calorie_add_key=list(calorie_add_data.keys())[0]
        cal_tdy_val=calorie_add_data[calorie_add_data]
    
    # Get today's date
    current_date = date.today()
    current_date_t = date.now()

    # Format the date as a string
    formatted_date = current_date.strftime("%Y-%m-%d")
    day_of_week = (current_date_t.strftime("%A"))
    try:
        with open("Files\Workout\Cal_Count.json", 'r') as calorie_val_search_file:
            calorie_val_search_data=json.load(calorie_val_search_file)
            cal_val=calorie_val_search_data[day_of_week]
            
        with open("Files/status.json", 'r') as stat_first_fson:
            stat_first_fson_data=json.load(stat_first_fson)
            result=stat_first_fson_data["cal_data"][0]["result"]
    
    except:
        result='MILD WEIGHT LOSS'
        cal_tdy_val=0

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

    #! ===================================================================

def penalty_check(win):
    with open("Files/Data/Penalty_Info.json", "r") as pen_info_file:
        data0=json.load(pen_info_file)
        target_time_str=data0["Penalty Time"]

    now=datetime.now()
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
        with open("Files/Data/First_open.csv", 'r') as first_open_check_file:
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
        with open("Files/Data/Prove_file.csv", 'r') as second_open_check_file:
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
    
        subprocess.Popen(['python', 'First/Start/gui.py'])

        sys.exit()
    
    elif first_run_file_check==True and second_run_file_check==False:
        stp_eve.set()

        # Wait for the thread to finish
        thrd.join()

        subprocess.Popen(['python', 'First/Check/gui.py'])

        sys.exit()

def random_skill_check():
    # Load the primary status file
    with open("Files/status.json", 'r') as fson:
        data = json.load(fson)

    # Extract player stats and metadata
    name = data["status"][0]['name'].upper()
    hp = data["status"][0]['hp']
    mp = data["status"][0]['mp']
    lvl = data["status"][0]['level']
    old_lvl = f"{lvl:02d}"

    stre = data["status"][0]['str']
    intel = data["status"][0]['int']
    agi = data["status"][0]['agi']
    vit = data["status"][0]['vit']
    per = data["status"][0]['per']
    man = data["status"][0]['man']

    tit = data["status"][1]['title'].upper()
    job = data["status"][1]['job'].upper()
    xp_str = data["status"][0]['XP']
    coins = data["status"][0]['coins']

    # Check level-up and skill eligibility
    if lvl % 5 == 0:
        with open("Files/Skills/Skill_old_check.json", 'r') as check_file:
            old_lvl_data = json.load(check_file)

        if lvl != old_lvl_data["old_stat"][0]["lvl"]:
            # Calculate stat differences
            comp_rec = {
                "STR": int(stre) - int(old_lvl_data["old_stat"][0]["str"]),
                "INT": int(intel) - int(old_lvl_data["old_stat"][0]["int"]),
                "AGI": int(agi) - int(old_lvl_data["old_stat"][0]["agi"]),
                "VIT": int(vit) - int(old_lvl_data["old_stat"][0]["vit"]),
                "PER": int(per) - int(old_lvl_data["old_stat"][0]["per"]),
                "MAN": int(man) - int(old_lvl_data["old_stat"][0]["man"])
            }

            # Identify the max stat(s)
            max_value = max(comp_rec.values())
            max_keys = [key for key, value in comp_rec.items() if value == max_value]

            # Handle ties for multiple max stats, limit to 2 alphabetically
            max_keys = sorted(max_keys)[:2]

            # Load skill list data
            with open("Files/Skills/Skill_List.json", 'r') as skill_list:
                skill_list_data = json.load(skill_list)

            # Match skills with conditions
            name_of_skill = [
                skill for skill, details in skill_list_data.items()
                if set(details[1]["Condition"]).issubset(max_keys)
            ]

            # Choose a skill
            choosen_skill = random.choice(name_of_skill) if name_of_skill else "Dash"

            # Load current skills
            with open("Files/Skills/Skill.json", 'r') as main_skills:
                main_skill_data = json.load(main_skills)

            # Check for duplication and process accordingly
            if choosen_skill in main_skill_data:
                if main_skill_data[choosen_skill][0]["lvl"] != "MAX":
                    main_skill_data[choosen_skill][0]["lvl"] += 1
                    with open("Files/Skills/Skill.json", 'w') as update_main_skills:
                        json.dump(main_skill_data, update_main_skills, indent=6)

                    with open("Files/Temp Files/Skill Up Temp.csv", 'w', newline='') as skill_temp_csv_open:
                        fw = csv.writer(skill_temp_csv_open)
                        fw.writerow([choosen_skill])

                    with open('Files/Data/New_Updates.json', 'w') as updatefile:
                        fin_data = {"Skills": "False", "Quests": "False", "Upgrade": "True", "Lines": "False"}
                        json.dump(fin_data, updatefile, indent=4)
            else:
                main_skill_data[choosen_skill] = [(skill_list_data[choosen_skill].pop(0))]
                main_skill_data[choosen_skill][0]["pl_point"] = 0

                with open("Files/Skills/Skill.json", 'w') as update_main_skills:
                    json.dump(main_skill_data, update_main_skills, indent=6)

                with open('Files/Data/New_Updates.json', 'w') as updatefile:
                    fin_data = {"Skills": "True", "Quests": "False", "Upgrade": "False", "Lines": "False"}
                    json.dump(fin_data, updatefile, indent=4)

            # Update old stats
            old_lvl_data["old_stat"][0].update({
                "lvl": lvl,
                "str": stre,
                "int": intel,
                "agi": agi,
                "vit": vit,
                "per": per,
                "man": man,
            })

            with open("Files/Skills/Skill_old_check.json", 'w') as final_check_file:
                json.dump(old_lvl_data, final_check_file, indent=4)

def check_midnight(window,stop_event):
    while not stop_event.is_set():
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            penalty_check(window)
        time.sleep(1)

def random_quest():
    # ! The Random Quests thing
    with open('Files/Data/Random_Quest_Day.json', 'r') as random_quest:
        random_quest_data=json.load(random_quest)
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
                with open("Files/Quests/Active_Quests.json", 'r') as active_quests_file:
                    activ_quests=json.load(active_quests_file)
                    name_of_activ_quests=list(activ_quests.keys())
                    activ_quests_vals=0
                    for k in name_of_activ_quests:
                        activ_quests_vals+=1
            except:
                name_of_activ_quests=[]

            if activ_quests_vals<13 and activ_quests_vals!=13:
                # ? Quest Name
                with open("Files\Quests\Quest_Names.json", 'r') as quest_name_file:
                    quest_names=json.load(quest_name_file)
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
                with open("Files\Quests\Quest_Desc.json", 'r') as quest_desc_file:
                    quest_desc=json.load(quest_desc_file)
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
                with open("Files\Data\Inventory_List.json", 'r') as rewards_name_file:
                    reward_names=json.load(rewards_name_file)
                    reward_names_list=list(reward_names.keys())

                    final_rewards_list=[]
                    for k in reward_names_list:
                        if rank==reward_names[k][0]["rank"]:
                            final_rewards_list.append(k)
                    
                    rew2=random.choice(final_rewards_list)

                # ? Quest Info
                file_name=f"Files\Workout\{random_ab}_based.json"
                with open(file_name, 'r') as quest_file_name:
                    quest_main_names=json.load(quest_file_name)
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

                with open("Files/Quests/Active_Quests.json", 'w') as fin_active_quest_file:
                    json.dump(activ_quests, fin_active_quest_file, indent=6)

                random_quest_data["Day"]=random.randint(0,6)

    if comp_check==True:
        with open('Files/Data/Random_Quest_Day.json', 'w') as finalrandom_quest:
            json.dump(random_quest_data, finalrandom_quest, indent=4)

        with open('Files/Data/New_Updates.json', 'w') as updatefile:
            fin_data={
                        "Skills":"False",
                        "Quests":"True",
                        "Upgrade":"False",
                        "Lines":"False"
                    }
            json.dump(fin_data, updatefile, indent=4)

def make_window_transparent(window,color="#0C679B"):
    window.wm_attributes('-transparentcolor', color)

def animate_window_open(window, target_height, width, step=2, delay=5, doners=False):
    current_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{width}x{current_height}+{screen_width//2 - width//2}+{screen_height//2 - current_height//2}")

    if current_height < target_height:
        new_height = min(current_height + step, target_height)
    else:
        new_height = current_height
    
    new_y = screen_height // 2 - new_height // 2
    window.geometry(f"{width}x{new_height}+{screen_width//2 - width//2}+{new_y}")

    done_val=False

    if round((new_height/target_height), 1)==0.2:
        if doners==False:
            #subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])
            done_val=True

    if new_height < target_height:
        window.after(delay, animate_window_open, window, target_height, width, step, delay, done_val)

def animate_window_open_middle(window, target_height, target_width, step=2, delay=5, doners=False):
    # Get the current dimensions of the window
    current_height = window.winfo_height()
    current_width = window.winfo_width()

    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the new height and width for the animation step
    new_height = min(current_height + step, target_height) if current_height < target_height else current_height
    new_width = min(current_width + step, target_width) if current_width < target_width else current_width

    # Center the window as it resizes
    new_x = screen_width // 2 - new_width // 2
    new_y = screen_height // 2 - new_height // 2

    # Update the window geometry
    window.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")

    # Trigger the sound effect logic
    done_val = False
    if round((new_height / target_height), 1) == 0.2 and not doners:
        # subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])  # Uncomment for actual sound trigger
        done_val = True

    # Continue animation if the target size is not reached
    if new_height < target_height or new_width < target_width:
        window.after(delay, animate_window_open, window, target_height, target_width, step, delay, done_val)

def animate_window_close(window, target_height, width, step=2, delay=5):
    current_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{width}x{current_height}+{screen_width//2 - width//2}+{screen_height//2 - current_height//2}")

    if current_height > target_height:
        new_height = max(current_height - step, target_height)
    else:
        new_height = current_height
    
    new_y = screen_height // 2 - new_height // 2
    window.geometry(f"{width}x{new_height}+{screen_width//2 - width//2}+{new_y}")

    if new_height > target_height:
        window.after(delay, animate_window_close, window, target_height, width, step, delay)
    else:
        window.quit()

def animate_window_close_middle(window, target_height, target_width, step=2, delay=5):
    # Get the current dimensions of the window
    current_height = window.winfo_height()
    current_width = window.winfo_width()

    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the new height and width for the animation step
    new_height = max(current_height - step, target_height) if current_height > target_height else current_height
    new_width = max(current_width - step, target_width) if current_width > target_width else current_width

    # Center the window as it resizes
    new_x = screen_width // 2 - new_width // 2
    new_y = screen_height // 2 - new_height // 2

    # Update the window geometry
    window.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")

    # Continue animation if the target size is not reached
    if new_height > target_height or new_width > target_width:
        window.after(delay, animate_window_close, window, target_height, target_width, step, delay)
    else:
        # Close the window when the target size is reached
        window.quit()

class VideoPlayer:
    def __init__(self, canvas, video_path, x=0, y=0, frame_skip=5, resize_factor=0.7):
        self.canvas = canvas
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.x = x  # Accept but ignore
        self.y = y  # Accept but ignore
        self.frame_skip = frame_skip
        self.resize_factor = resize_factor
        self.image_id = self.canvas.create_image(0, 0, anchor='nw')  # Initial anchor
        self.frame_count = 0

        # Ensure canvas dimensions are updated before starting
        self.canvas.update_idletasks()
        self.update_frame()

    def update_frame(self):
        # Read the frame only if it's necessary (skip others)
        if self.frame_count % self.frame_skip == 0:
            ret, frame = self.cap.read()

            if not ret:
                # Restart video when reaching the end
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()

            if ret:
                # Perform resizing and color conversion
                frame = cv2.resize(frame, (0, 0), fx=self.resize_factor, fy=self.resize_factor)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert to ImageTk format
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)

                # Calculate the centered position
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                video_width, video_height = img.size
                x_center = (canvas_width - video_width) // 2
                y_center = (canvas_height - video_height) // 2

                # Update the canvas image and position
                self.canvas.coords(self.image_id, x_center, y_center)
                self.canvas.itemconfig(self.image_id, image=imgtk)
                self.canvas.imgtk = imgtk

        # Increment frame count and schedule next frame update
        self.frame_count += 1
        self.canvas.after(15, self.update_frame)  # Slightly slower update to ease load

    def __del__(self):
        self.cap.release()

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
            with open('Files/Data/Theme_Check.json', 'r') as themefile:
                theme_data = json.load(themefile)
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
    with open("Files/Data/Job_info.json", 'r') as stat_fson:
        data=json.load(stat_fson)

    canvas.itemconfig("Jobs", state="hidden")
    data["status"][1]["job_confirm"]='True'

    with open("Files/Data/Job_info.json", 'w') as fson:
        json.dump(data, fson, indent=4)

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
    with open("Files/Status.json", 'r') as fson:
        data = json.load(fson)
        lvl = int(data["status"][0]['level'])  # Current level
        xp = float(data["status"][0]['XP'])  # Current XP value
        last_lvl = int(data["status"][0]['last_level'])  # Last processed level

    # Load level-up values
    with open("Files/Data/Level_Up_Values.json", 'r') as fron2:
        level_up_values = json.load(fron2)["XP Check"]

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

        # Save updated status to file
        with open("Files/Status.json", 'w') as up_fson:
            json.dump(data, up_fson, indent=4)

        # Trigger level-up GUI
        with open('Files/Data/Theme_Check.json', 'r') as themefile:
            theme_data = json.load(themefile)
            theme = theme_data["Theme"]
            subprocess.Popen(['python', f'{theme} Version/Leveled up/gui.py'])

            if data["status"][0]['level']>=100:
                message_open("Courage of the Weak")

    else:
        print()
    fin_xp = None
    if str(lvl + 1) in level_up_values:
        next_level_xp = float(level_up_values[str(lvl + 1)])
        fin_xp = next_level_xp - xp  # Difference between next level XP and current XP

    return [leveled_up,fin_xp]

def get_fin_xp_no_win():
    with open("Files/status.json", 'r') as fson:
        data=json.load(fson)
        lvl=data["status"][0]['level']
        xp_str=data["status"][0]['XP']
    if lvl!=0:
        fin_chk=False
        with open("Files/Data/Level_Up_Values.json", 'r') as fron2:
            data_2=json.load(fron2)
            xp_chl=data_2["XP Check"][str(lvl+1)]
            if xp_str>=xp_chl:
                fin_chk=True

        if fin_chk==True:
            data["status"][0]['level']+=1
            with open("Files/status.json", 'w') as up_fson:
                json.dump(data, up_fson, indent=4)
            with open('Files/Data/Theme_Check.json', 'r') as themefile:
                theme_data=json.load(themefile)
                theme=theme_data["Theme"]
            subprocess.Popen(['python', f'{theme} Version/Leveled up/gui.py'])
            return [xp_str,fin_chk]

def daily_preview(window):
    with open("Files\Temp Files\Daily Rewards.csv", 'w', newline='') as rew_csv_open:
            rew_fw=csv.writer(rew_csv_open)
            rew_fw.writerow(["Preview"])
    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=json.load(themefile)
        theme=theme_data["Theme"]
    subprocess.Popen(['python', f'{theme} Version/Daily Quest Rewards/gui.py'])

def check_daily_comp(today_date_str, window):
    with open("Files/Data/Daily_Quest.json", 'r') as daily_quest_file:
        daily_quest_data = json.load(daily_quest_file)
        
        # Player's daily progress
        pl_push = daily_quest_data["Player"]["Push"]
        pl_sit = daily_quest_data["Player"]["Sit"]
        pl_sqat = daily_quest_data["Player"]["Squat"]
        pl_run = daily_quest_data["Player"]["Run"]
        pl_int = daily_quest_data["Player"]["Int_type"]
        pl_slp = daily_quest_data["Player"]["Sleep"]

        # Final quest goals
        fl_push = daily_quest_data["Final"]["Push"]
        fl_sit = daily_quest_data["Final"]["Sit"]
        fl_sqat = daily_quest_data["Final"]["Squat"]
        fl_run = daily_quest_data["Final"]["Run"]
        fl_int = daily_quest_data["Final"]["Int_type"]
        fl_slp = daily_quest_data["Final"]["Sleep"]

    with open('Files/Checks/Secret_Quest_Check.json', 'r') as secrer_quest:
        secrer_quest_data = json.load(secrer_quest)
        day_num = secrer_quest_data["Day"]
        tdy_week_num = datetime.today().weekday()

    # First check if today is the correct day to check completion
    if day_num == tdy_week_num:
        if (pl_push / 2) >= fl_push and (pl_run / 2) >= fl_run and (pl_sqat / 2) >= fl_sqat and (pl_sit / 2) >= fl_sit and (pl_int / 2) >= fl_int:
            if fl_push != 100 and fl_sit != 100 and fl_sqat != 100:
                # Update final quest data with rewards
                daily_quest_data["Final"]["Push"] += 5
                daily_quest_data["Final"]["Sit"] += 5
                daily_quest_data["Final"]["Squat"] += 5
                daily_quest_data["Final"]["Run"] += 0.5
                daily_quest_data["Streak"]["Value"] += 1

                # Reset player data
                daily_quest_data["Player"]["Push"] = 0
                daily_quest_data["Player"]["Sit"] = 0
                daily_quest_data["Player"]["Squat"] = 0
                daily_quest_data["Player"]["Run"] = 0
                daily_quest_data["Player"]["Int_type"] = 0
                daily_quest_data["Player"]["Sleep"] = 0

                # Increment intellect if not already at max
                if round(fl_int, 1) != 10:
                    daily_quest_data["Final"]["Int_type"] += 0.5

                daily_quest_data["Streak"]["Value"]+=1
                daily_quest_data["Streak"]["Greater_value"]+=1

                # Save the updated quest data
                with open("Files/Data/Daily_Quest.json", 'w') as final_daily_quest_file:
                    json.dump(daily_quest_data, final_daily_quest_file, indent=4)

                # Record the completion time check
                with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as fin_daily_date_check_file:
                    fw1 = csv.writer(fin_daily_date_check_file)
                    fw1.writerow([today_date_str, "False", "Complete"])

                # Log reward info
                with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                    rew_fw = csv.writer(rew_csv_open)
                    rew_fw.writerow(["Secret"])

                # Execute the reward GUI based on the theme
                with open('Files/Data/Theme_Check.json', 'r') as themefile:
                    theme_data = json.load(themefile)
                    theme = theme_data["Theme"]
                subprocess.Popen(['python', f'{theme} Version/Daily Quest Rewards/gui.py'])

                # Close the daily quest tab
                with open("Files/Tabs.json", 'r') as tab_son:
                    tab_son_data = json.load(tab_son)

                with open("Files/Tabs.json", 'w') as fin_tab_son:
                    tab_son_data["Daily"] = 'Close'
                    json.dump(tab_son_data, fin_tab_son, indent=4)

                window.quit()

        # Handle the condition where day_num != tdy_week_num
        if (pl_push) >= fl_push and (pl_run) >= fl_run and (pl_sqat) >= fl_sqat and (pl_sit) >= fl_sit and (pl_int) >= fl_int and (pl_slp) >= fl_slp:
            if fl_push != 100 and fl_sit != 100 and fl_sqat != 100:
                # Update final quest data with rewards
                daily_quest_data["Final"]["Push"] += 5
                daily_quest_data["Final"]["Sit"] += 5
                daily_quest_data["Final"]["Squat"] += 5
                daily_quest_data["Final"]["Run"] += 0.5
                daily_quest_data["Streak"]["Value"] += 1

                # Reset player data
                daily_quest_data["Player"]["Push"] = 0
                daily_quest_data["Player"]["Sit"] = 0
                daily_quest_data["Player"]["Squat"] = 0
                daily_quest_data["Player"]["Run"] = 0
                daily_quest_data["Player"]["Int_type"] = 0
                daily_quest_data["Player"]["Sleep"] = 0

                # Increment intellect if not already at max
                if round(fl_int, 1) != 10:
                    daily_quest_data["Final"]["Int_type"] += 0.5

                # Log reward info
                if (pl_push) >= fl_push*3 and (pl_run) >= fl_run*3 and (pl_sqat) >= fl_sqat*3 and (pl_sit) >= fl_sit*3 and (pl_int) >= fl_int*3:
                    with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                        rew_fw = csv.writer(rew_csv_open)
                        rew_fw.writerow(["Great Reward"])
                        daily_quest_data["Streak"]["Greater_value"] += 1
                else:
                    with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                        rew_fw = csv.writer(rew_csv_open)
                        rew_fw.writerow(["Reward"])
                        daily_quest_data["Streak"]["Greater_value"]=0
                        daily_quest_data["Streak"]["Value"] += 1

                # Save the updated quest data
                with open("Files/Data/Daily_Quest.json", 'w') as final_daily_quest_file:
                    json.dump(daily_quest_data, final_daily_quest_file, indent=4)

                # Record the completion time check
                with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as fin_daily_date_check_file:
                    fw1 = csv.writer(fin_daily_date_check_file)
                    fw1.writerow([today_date_str, "True", "Complete"])

                # Execute the reward GUI based on the theme
                with open('Files/Data/Theme_Check.json', 'r') as themefile:
                    theme_data = json.load(themefile)
                    theme = theme_data["Theme"]
                subprocess.Popen(['python', f'{theme} Version/Daily Quest Rewards/gui.py'])

                # Close the daily quest tab
                with open("Files/Tabs.json", 'r') as tab_son:
                    tab_son_data = json.load(tab_son)

                with open("Files/Tabs.json", 'w') as fin_tab_son:
                    tab_son_data["Daily"] = 'Close'
                    json.dump(tab_son_data, fin_tab_son, indent=4)

                window.quit()

    else:
        # Handle the condition where day_num != tdy_week_num
        if (pl_push) >= fl_push and (pl_run) >= fl_run and (pl_sqat) >= fl_sqat and (pl_sit) >= fl_sit and (pl_int) >= fl_int and (pl_slp) >= fl_slp:
            if fl_push != 100 and fl_sit != 100 and fl_sqat != 100:
                # Update final quest data with rewards
                daily_quest_data["Final"]["Push"] += 5
                daily_quest_data["Final"]["Sit"] += 5
                daily_quest_data["Final"]["Squat"] += 5
                daily_quest_data["Final"]["Run"] += 0.5
                daily_quest_data["Streak"]["Value"] += 1

                # Reset player data
                daily_quest_data["Player"]["Push"] = 0
                daily_quest_data["Player"]["Sit"] = 0
                daily_quest_data["Player"]["Squat"] = 0
                daily_quest_data["Player"]["Run"] = 0
                daily_quest_data["Player"]["Int_type"] = 0
                daily_quest_data["Player"]["Sleep"] = 0

                # Increment intellect if not already at max
                if round(fl_int, 1) != 10:
                    daily_quest_data["Final"]["Int_type"] += 0.5

                # Log reward info
                if (pl_push) >= fl_push*3 and (pl_run) >= fl_run*3 and (pl_sqat) >= fl_sqat*3 and (pl_sit) >= fl_sit*3 and (pl_int) >= fl_int*3:
                    with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                        rew_fw = csv.writer(rew_csv_open)
                        rew_fw.writerow(["Great Reward"])
                        daily_quest_data["Streak"]["Greater_value"] += 1
                else:
                    with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                        rew_fw = csv.writer(rew_csv_open)
                        rew_fw.writerow(["Reward"])
                        daily_quest_data["Streak"]["Greater_value"]=0
                        daily_quest_data["Streak"]["Value"] += 1

                # Save the updated quest data
                with open("Files/Data/Daily_Quest.json", 'w') as final_daily_quest_file:
                    json.dump(daily_quest_data, final_daily_quest_file, indent=4)

                # Record the completion time check
                with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as fin_daily_date_check_file:
                    fw1 = csv.writer(fin_daily_date_check_file)
                    fw1.writerow([today_date_str, "True", "Complete"])

                # Execute the reward GUI based on the theme
                with open('Files/Data/Theme_Check.json', 'r') as themefile:
                    theme_data = json.load(themefile)
                    theme = theme_data["Theme"]
                subprocess.Popen(['python', f'{theme} Version/Daily Quest Rewards/gui.py'])

                # Close the daily quest tab
                with open("Files/Tabs.json", 'r') as tab_son:
                    tab_son_data = json.load(tab_son)

                with open("Files/Tabs.json", 'w') as fin_tab_son:
                    tab_son_data["Daily"] = 'Close'
                    json.dump(tab_son_data, fin_tab_son, indent=4)

                window.quit()

def dun_check():
    global e_rank, d_rank, c_rank, b_rank, a_rank, s_rank, red_gate

    # Path to the JSON file
    file_path = "Files\\Data\\Todays_Dungeon.json"
    
    # Load the existing data from the file
    try:
        with open(file_path, 'r') as dun_check:
            dun_check_data = json.load(dun_check)
    except FileNotFoundError:
        dun_check_data = {}

    # Get today's date as a string
    current_date = datetime.now().date()
    current_date_string = current_date.strftime("%Y-%m-%d")

    # Check if data already exists for today's date
    if current_date_string not in dun_check_data:
        # E Rank Distro
        e_rank_vals = sum(1 for _ in range(5) if random.randint(1, 2) == 1)

        # D Rank Distro
        d_rank_vals = sum(1 for _ in range(7) if random.randint(1, 3) == 1)

        # C Rank Distro
        c_rank_vals = sum(1 for _ in range(10) if random.randint(1, 3) == 1)

        # B Rank Distro
        b_rank_vals = sum(1 for _ in range(10) if random.randint(1, 5) == 1)

        # A Rank Distro
        a_rank_vals = sum(1 for _ in range(10) if random.randint(1, 10) == 1)

        # S Rank Distro
        s_rank_vals = sum(1 for _ in range(1) if random.randint(1, 10) == 1)

        # Red Gate Rank Distro
        red_rank_vals = sum(1 for _ in range(10) if random.randint(1, 20) == 1)

        # Store today's values in the dictionary
        dun_check_data[current_date_string] = {
            "E": e_rank_vals,
            "D": d_rank_vals,
            "C": c_rank_vals,
            "B": b_rank_vals,
            "A": a_rank_vals,
            "S": s_rank_vals,
            "Red Gate": red_rank_vals
        }

        # Write the updated data back to the file
        with open(file_path, 'w') as wrt_dun_check:
            json.dump(dun_check_data, wrt_dun_check, indent=6)
    
    # Retrieve today's values from the data
    e_rank = dun_check_data[current_date_string]["E"]
    d_rank = dun_check_data[current_date_string]["D"]
    c_rank = dun_check_data[current_date_string]["C"]
    b_rank = dun_check_data[current_date_string]["B"]
    a_rank = dun_check_data[current_date_string]["A"]
    s_rank = dun_check_data[current_date_string]["S"]
    red_gate = dun_check_data[current_date_string]["Red Gate"]

    return e_rank, d_rank, c_rank, b_rank, a_rank, s_rank

def dungeon_rank_get(rank,amt1,amt1_check):
    with open("Files/status.json", 'r') as fson:
        data=json.load(fson)
        agi=data["status"][0]['agi']
        stre=data["status"][0]['str']
    minus=reduction(amt1, stre, agi, amt1_check)
    if rank=='D':
        if amt1_check=="amt":
            if amt1==50:
                amt1+=10
            elif amt1==15:
                amt1+=5
            elif amt1==2:
                amt1+=1
            elif amt1==30:
                amt1+=15
            elif amt1==1:
                amt1+=1
        elif amt1_check=="time":
            if amt1==45:
                amt1+=15
            elif amt1==60:
                amt1+=60
            elif amt1==1:
                amt1+=1
    elif rank=='C':
        if amt1_check=="amt":
            if amt1==50:
                amt1+=20
            elif amt1==15:
                amt1+=15
            elif amt1==2:
                amt1+=2
            elif amt1==30:
                amt1+=30
            elif amt1==1:
                amt1+=2
        elif amt1_check=="time":
            if amt1==45:
                amt1+=30
            elif amt1==60:
                amt1+=120
            elif amt1==1:
                amt1+=2
    elif rank=='B':
        if amt1_check=="amt":
            if amt1==50:
                amt1+=30
            elif amt1==15:
                amt1+=35
            elif amt1==2:
                amt1+=3
            elif amt1==30:
                amt1+=60
            elif amt1==1:
                amt1+=3
        elif amt1_check=="time":
            if amt1==45:
                amt1+=45
            elif amt1==60:
                amt1+=240
            elif amt1==1:
                amt1+=4
    elif rank=='A':
        if amt1_check=="amt":
            if amt1==50:
                amt1+=100
            elif amt1==15:
                amt1+=50
            elif amt1==2:
                amt1+=5
            elif amt1==30:
                amt1+=70
            elif amt1==1:
                amt1+=4
        elif amt1_check=="time":
            if amt1==45:
                amt1+=65
            elif amt1==60:
                amt1+=360
            elif amt1==1:
                amt1+=6
    elif rank=='S':
        if amt1_check=="amt":
            if amt1==50:
                amt1+=150
            elif amt1==15:
                amt1+=85
            elif amt1==2:
                amt1+=8
            elif amt1==30:
                amt1+=90
            elif amt1==1:
                amt1+=5
        elif amt1_check=="time":
            if amt1==45:
                amt1+=75
            elif amt1==60:
                amt1+=540
            elif amt1==1:
                amt1+=9

    amt1=amt1-minus
    return amt1

def get_item_button_image(name, max_width, max_height):
    try:
        # Construct the absolute path to the Images folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to the project root directory
        if name.split()[0]=='Coin' and name.split()[1]=='Bag':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Coin Pouch" + ' Big.png')
        elif name.split()[-1]=='Key':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Instance Keys" + ' Big.png')
        else:
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, name + ' Big.png')
        if not os.path.exists(files):
            raise FileNotFoundError
    except:
        file_loc = os.path.join(script_dir, "Images")
        files = os.path.join(file_loc, "Unknown.png")

    # Open the image
    image = Image.open(files)
    
    # Calculate the resize ratio
    width_ratio = max_width / image.width
    height_ratio = max_height / image.height
    resize_ratio = min(width_ratio, height_ratio)
    
    # Resize the image
    new_width = int(image.width * resize_ratio)
    new_height = int(image.height * resize_ratio)
    resized_image = image.resize((new_width, new_height))
    
    # Convert the image to PhotoImage
    photo_image = ImageTk.PhotoImage(resized_image)
    
    return photo_image

def get_armor_image(name, max_width=376, max_height=376):
    try:
        # Construct the absolute path to the Images folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_loc = os.path.join(script_dir, "Equipment Display")
        files = os.path.join(file_loc, name + '.png')
        if not os.path.exists(files):
            raise FileNotFoundError
    except:
        file_loc = os.path.join(script_dir, "Equipment Display")
        files = os.path.join(file_loc, "unknown.png")

    # Open the image
    image = Image.open(files)
    
    # Calculate the resize ratio
    width_ratio = max_width / image.width
    height_ratio = max_height / image.height
    resize_ratio = min(width_ratio, height_ratio)
    
    # Resize the image
    new_width = int(image.width * resize_ratio)
    new_height = int(image.height * resize_ratio)
    resized_image = image.resize((new_width, new_height))
    
    # Convert the image to PhotoImage
    photo_image = ImageTk.PhotoImage(resized_image)

    return photo_image

def inventory_name_cut(name):
    if len(name)>15:
        s=''
        for k in range(15):
            s+=name[k]
        s+='...'
        return s
    else:
        return name

def inventory_item_data(name,rank,category,t,r,s,window):
    try:
        if name!='-' and rank!='-' and category!='-':
            fout=open('Files/Temp Files/Inventory temp.csv', 'w', newline='')
            fw=csv.writer(fout)
            rec=[name]
            fw.writerow(rec)
            fout.close()

            with open('Files/Data/Theme_Check.json', 'r') as themefile:
                theme_data=json.load(themefile)
                theme=theme_data["Theme"]
            subprocess.Popen(['python', f'{theme} Version/Item Data/gui.py'])
    
    except:
        print()

def get_inventory_button_image(name):
    try:
        # Construct the absolute path to the Images folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to the project root directory
        if name.split()[0]=='Coin' and name.split()[1]=='Bag':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Coin Pouch" + ' Small.png')
        elif name.split()[-1]=='Key':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Instance Keys" + ' Small.png')
        else:
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, name + ' Small.png')
        if not os.path.exists(files):
            print(FileNotFoundError)
    except:
        file_loc = os.path.join(script_dir, "Images")
        files = os.path.join(file_loc, "Unknown.png")
    
    return PhotoImage(file=files)

def equip_item(cat,item_full_data, window):

    if cat!="ORDER":
        with open('Files/Inventory.json', 'r') as fout:
            data=json.load(fout)
            rol=list(data.keys())
        with open('Files/Equipment.json', 'r') as first_equipment_file:
            first_equipment_file_data=json.load(first_equipment_file)
            if first_equipment_file_data[cat]!={}:
                item_old_name=list(first_equipment_file_data[cat].keys())[0]
                old_item_buff_main=list(first_equipment_file_data[cat][item_old_name][0]["buff"].keys())
                try:
                    # ? HELM BUFF 1 
                    old_item_boost_1_name=old_item_buff_main[0]
                    if old_item_boost_1_name=="AGIbuff":
                        oldbuff_1_name="AGI"
                    elif old_item_boost_1_name=="STRbuff":
                        oldbuff_1_name="STR"
                    elif old_item_boost_1_name=="VITbuff":
                        oldbuff_1_name="VIT"
                    elif old_item_boost_1_name=="INTbuff":
                        oldbuff_1_name="INT"
                    elif old_item_boost_1_name=="PERbuff":
                        oldbuff_1_name="PER"
                    elif old_item_boost_1_name=="MANbuff":
                        oldbuff_1_name="MAN"

                    oldbuff1_value=data[cat][item_old_name][0]["buff"][old_item_boost_1_name]

                    # ? HELM BUFF 2
                    old_item_boost_2_name=old_item_buff_main[1]
                    if old_item_boost_2_name=="AGIbuff":
                        oldbuff_2_name="AGI"
                    elif old_item_boost_2_name=="STRbuff":
                        oldbuff_2_name="STR"
                    elif old_item_boost_2_name=="VITbuff":
                        oldbuff_2_name="VIT"
                    elif old_item_boost_2_name=="INTbuff":
                        oldbuff_2_name="INT"
                    elif old_item_boost_2_name=="PERbuff":
                        oldbuff_2_name="PER"
                    elif old_item_boost_2_name=="MANbuff":
                        oldbuff_2_name="MAN"

                    oldbuff2_value=data[cat][item_old_name][0]["buff"][old_item_boost_2_name]
                except:
                    print("",end='')

                try:
                    old_item_debuff_main=list(first_equipment_file_data[cat][item_old_name][0]["debuff"].keys())
                    # ? HELM BUFF 1 
                    old_item_deboost_1_name=old_item_debuff_main[0]
                    if old_item_deboost_1_name=="AGIbuff":
                        olddebuff_1_name="AGI"
                    elif old_item_deboost_1_name=="STRdebuff":
                        olddebuff_1_name="STR"
                    elif old_item_deboost_1_name=="VITdebuff":
                        olddebuff_1_name="VIT"
                    elif old_item_deboost_1_name=="INTdebuff":
                        olddebuff_1_name="INT"
                    elif old_item_deboost_1_name=="PERdebuff":
                        olddebuff_1_name="PER"
                    elif old_item_deboost_1_name=="MANdebuff":
                        olddebuff_1_name="MAN"

                    olddebuff1_value=data[cat][item_old_name][0]["debuff"][old_item_deboost_1_name]

                    # ? HELM BUFF 2
                    old_item_deboost_2_name=old_item_debuff_main[1]
                    if old_item_deboost_2_name=="AGIdebuff":
                        olddebuff_2_name="AGI"
                    elif old_item_deboost_2_name=="STRdebuff":
                        olddebuff_2_name="STR"
                    elif old_item_deboost_2_name=="VITdebuff":
                        olddebuff_2_name="VIT"
                    elif old_item_deboost_2_name=="INTdebuff":
                        olddebuff_2_name="INT"
                    elif old_item_deboost_2_name=="PERdebuff":
                        olddebuff_2_name="PER"
                    elif old_item_deboost_2_name=="MANdebuff":
                        olddebuff_2_name="MAN"

                    olddebuff2_value=data[cat][item_old_name][0]["debuff"][old_item_deboost_2_name]
                except:
                    print("",end='')

                with open("Files/status.json", 'r') as status_file_eq:
                    status_file_eq_data=json.load(status_file_eq)
                    try:
                        status_file_eq_data["equipment"][0][oldbuff_1_name]=-oldbuff1_value
                        status_file_eq_data["equipment"][0][oldbuff_2_name]=-oldbuff2_value
                    except:
                        print()

                    try:
                        status_file_eq_data["equipment"][0][olddebuff_1_name]=+olddebuff1_value
                        status_file_eq_data["equipment"][0][olddebuff_2_name]=+olddebuff2_value
                    except:
                        print()

                first_equipment_file_data[cat]={}

                with open('Files/Equipment.json', 'w') as second_write_equipment_file:
                    json.dump(first_equipment_file_data, second_write_equipment_file, indent=6)

                with open('Files/status.json', 'w') as second_write_status_file:
                    json.dump(status_file_eq_data, second_write_status_file, indent=4)

        if cat in ["HELM", "CHESTPLATE", "FIRST GAUNTLET", "SECOND GAUNTLET", "BOOTS", "COLLAR", "RING"]:
            with open('Files/Equipment.json', 'r') as finale_equip:
                finale_equip_data=json.load(finale_equip)
                finale_equip_data[cat]=item_full_data

            with open('Files/Equipment.json', 'w') as inject:
                json.dump(finale_equip_data, inject, indent=6)

            with open('Files/Equipment.json', 'r') as second_equipment_file:
                second_equipment_file_data=json.load(second_equipment_file)
                item_new_name=list(second_equipment_file_data[cat].keys())[0]
                new_item_buff_main=list(second_equipment_file_data[cat][item_new_name][0]["buff"].keys())

                # ? HELM BUFF 1 
                new_item_boost_1_name=new_item_buff_main[0]
                if new_item_boost_1_name=="AGIbuff":
                    newbuff_1_name="AGI"
                elif new_item_boost_1_name=="STRbuff":
                    newbuff_1_name="STR"
                elif new_item_boost_1_name=="VITbuff":
                    newbuff_1_name="VIT"
                elif new_item_boost_1_name=="INTbuff":
                    newbuff_1_name="INT"
                elif new_item_boost_1_name=="PERbuff":
                    newbuff_1_name="PER"
                elif new_item_boost_1_name=="MANbuff":
                    newbuff_1_name="MAN"

                newbuff1_value=second_equipment_file_data[cat][item_new_name][0]["buff"][new_item_boost_1_name]

                try:
                    # ? HELM BUFF 2
                    new_item_boost_2_name=new_item_buff_main[1]
                    if new_item_boost_2_name=="AGIbuff":
                        newbuff_2_name="AGI"
                    elif new_item_boost_2_name=="STRbuff":
                        newbuff_2_name="STR"
                    elif new_item_boost_2_name=="VITbuff":
                        newbuff_2_name="VIT"
                    elif new_item_boost_2_name=="INTbuff":
                        newbuff_2_name="INT"
                    elif new_item_boost_2_name=="PERbuff":
                        newbuff_2_name="PER"
                    elif new_item_boost_2_name=="MANbuff":
                        newbuff_2_name="MAN"

                    newbuff2_value=second_equipment_file_data[cat][item_new_name][0]["buff"][new_item_boost_2_name]
                except:
                    print("",end='')

                try:
                    new_item_debuff_main=list(second_equipment_file_data[cat][item_new_name][0]["debuff"].keys())
                    # ? HELM BUFF 1 
                    new_item_deboost_1_name=new_item_debuff_main[0]
                    if new_item_deboost_1_name=="AGIdebuff":
                        newbuff_1_name="AGI"
                    elif new_item_deboost_1_name=="STRdebuff":
                        newbuff_1_name="STR"
                    elif new_item_deboost_1_name=="VITdebuff":
                        newbuff_1_name="VIT"
                    elif new_item_deboost_1_name=="INTdebuff":
                        newbuff_1_name="INT"
                    elif new_item_deboost_1_name=="PERdebuff":
                        newbuff_1_name="PER"
                    elif new_item_deboost_1_name=="MANdebuff":
                        newbuff_1_name="MAN"

                    newdebuff1_value=data[cat][item_new_name][0]["debuff"][new_item_deboost_1_name]

                    # ? HELM BUFF 2
                    new_item_deboost_2_name=new_item_buff_main[1]
                    if new_item_deboost_2_name=="AGIdebuff":
                        newdebuff_2_name="AGI"
                    elif new_item_deboost_2_name=="STRdebuff":
                        newdebuff_2_name="STR"
                    elif new_item_deboost_2_name=="VITdebuff":
                        newdebuff_2_name="VIT"
                    elif new_item_deboost_2_name=="INTdebuff":
                        newdebuff_2_name="INT"
                    elif new_item_deboost_2_name=="PERdebuff":
                        newdebuff_2_name="PER"
                    elif new_item_deboost_2_name=="MANdebuff":
                        newdebuff_2_name="MAN"

                    newdebuff2_value=data[cat][item_new_name][0]["debuff"][new_item_deboost_2_name]
                except:
                    print("",end='')

                with open("Files/status.json", 'r') as status2_file_eq:
                    status2_file_eq_data=json.load(status2_file_eq)
                    try:
                        status2_file_eq_data["equipment"][0][newbuff_1_name]=status2_file_eq_data["equipment"][0][newbuff_1_name]+newbuff1_value
                        status2_file_eq_data["equipment"][0][newbuff_2_name]=status2_file_eq_data["equipment"][0][newbuff_2_name]+newbuff2_value
                    except:
                        print()

                    try:
                        status2_file_eq_data["equipment"][0][olddebuff_1_name]=-newdebuff1_value
                        status2_file_eq_data["equipment"][0][olddebuff_2_name]=-newdebuff2_value
                    except:
                        print()

                with open('Files/Equipment.json', 'w') as second_final_write_equipment_file:
                    json.dump(second_equipment_file_data, second_final_write_equipment_file, indent=6)

                with open('Files/status.json', 'w') as second_final_write_status_file:
                    json.dump(status2_file_eq_data, second_final_write_status_file, indent=4)

            with open('Files/Data/Theme_Check.json', 'r') as themefile:
                theme_data=json.load(themefile)
                theme=theme_data["Theme"]
            with open("Files/Tabs.json",'r') as tab_son:
                tab_son_data=json.load(tab_son)

            if tab_son_data["Inventory"]=='Close':
                subprocess.Popen(['python', f'{theme} Version/Equipment/gui.py'])
            window.quit()

    else:
        with open("Files/Inventory.json", 'r') as fson:
            data_fininv=json.load(fson)
        del data_fininv["The Orb of Order"]

        subprocess.Popen(['python', "First\The Order\gui.py"])
        window.quit()

def return_back_to_tab(loc,window):
    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=json.load(themefile)
        theme=theme_data["Theme"]
        fin_loc=f'{theme} Version/{loc}/gui.py'
    subprocess.Popen(['python', fin_loc])
    window.quit()   

def selling_item(name,window,val):
    with open("Files/status.json", 'r') as read_status_file:
        read_status_file_data=json.load(read_status_file)

    with open("Files/Inventory.json", 'r') as fin_inv_fson:
        fin_inv_data=json.load(fin_inv_fson)

        fin_qt=fin_inv_data[name][0]["qty"]
        fin_inv_data[name][0]["qty"]=fin_qt-1
        closing=False
        if fin_inv_data[name][0]["qty"]==0:
            del fin_inv_data[name]
            closing=True

    with open("Files/Inventory.json", 'w') as finaladdon_inv:
        json.dump(fin_inv_data, finaladdon_inv, indent=6)

    with open("Files/status.json", 'w') as write_status_file:
        read_status_file_data["status"][0]['coins']+=int(val)
        json.dump(read_status_file_data, write_status_file, indent=4)

    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=json.load(themefile)
        theme=theme_data["Theme"]

    if closing==True:
        subprocess.Popen(['python', f'{theme} Version/Inventory/gui.py'])

        window.quit()

    else:
        subprocess.Popen(['python', f'{theme} Version/Item Data/gui.py'])

        window.quit()

def quest_adding_func(entry_1,entry_2,entry_3,entry_4,entry_5,entry_6,window):
    try:
        with open("Files/Quests/Active_Quests.json", 'r') as active_quests_file:
            activ_quests=json.load(active_quests_file)
            name_of_activ_quests=list(activ_quests.keys())
            activ_quests_vals=0
            for k in name_of_activ_quests:
                activ_quests_vals+=1
    except:
        name_of_activ_quests=[]
    
    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=json.load(themefile)
        theme=theme_data["Theme"]

    if activ_quests_vals<13 and activ_quests_vals!=13:
        quest_name='-'+entry_1.get()
        quest_type=(entry_2.get()).upper()
        quest_obj=entry_3.get()
        quest_amt=entry_4.get()
        quest_amt_type=entry_5.get()
        rank=(entry_6.get()).upper()

        if rank not in ["E", "D", "C", "B", "A", "S"]:
            rank='E'

        if quest_type not in ["STR", "INT"]:
            quest_type="STR"

        if quest_type=='STR':
            rew3="STRav"
        elif quest_type=='INT':
            rew3="INTav"

        id_val=random.randrange(1,999999)

        with open("Files\Quests\Quest_Desc.json", 'r') as quest_desc_file:
            quest_desc=json.load(quest_desc_file)
            if rank in ["E", "D"]:
                desc_list=quest_desc["Easy"]
                findesc=random.choice(desc_list)
            elif rank in ["C", "B"]:
                desc_list=quest_desc["Intermediate"]
                findesc=random.choice(desc_list)
            elif rank in ["A", "S"]:
                desc_list=quest_desc["Hard"]
                findesc=random.choice(desc_list)

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
        with open("Files\Data\Inventory_List.json", 'r') as rewards_name_file:
            reward_names=json.load(rewards_name_file)
            reward_names_list=list(reward_names.keys())

            final_rewards_list=[]
            for k in reward_names_list:
                if rank==reward_names[k][0]["rank"]:
                    final_rewards_list.append(k)
            
            rew2=random.choice(final_rewards_list)

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


        detail=[{
            "desc":findesc,
            "amt":quest_amt,
            "amtval":quest_amt_type,
            "type":"Learn",
            "obj_desc":"Quest given by Player. No description Available",
            "rank":rank,
            "ID": id_val,
            "Rewards":rew_dict,
            "skill":quest_obj
        }]

        activ_quests[quest_name]=detail

        with open("Files/Quests/Active_Quests.json", 'w') as fin_active_quest_file:
            json.dump(activ_quests, fin_active_quest_file, indent=6)

    else:
        message_open("Quest Slot Filled")

    window.quit()

    subprocess.Popen(['python', f'{theme} Version/Quests/gui.py'])

def set_preview_temp(nameob,quantity):
    if nameob!='-' and quantity!=0:
        with open("Files/Temp Files/Inventory temp.csv", 'w', newline='') as new_csv_open:
            fw=csv.writer(new_csv_open)
            rec=[nameob, quantity, 'Preview']
            fw.writerow(rec)
        with open('Files/Data/Theme_Check.json', 'r') as themefile:
            theme_data=json.load(themefile)
            theme=theme_data["Theme"]
        subprocess.Popen(['python', f'{theme} Version/Item Data/gui.py'])

def quest_reward(window,dicts,rank,name,special=False):
    rol=list(dicts.keys())
    for k in rol:
        if k=="LVLADD":
            with open("Files/Status.json", 'r') as fson:
                    data_status=json.load(fson)
            
            for k in range(dicts[k]):                
                data_status["status"][0]['level']+=1
                data_status["status"][0]['str']+=1
                data_status["status"][0]['agi']+=1
                data_status["status"][0]['vit']+=1
                data_status["status"][0]['int']+=1
                data_status["status"][0]['per']+=1
                data_status["status"][0]['hp']+=10
                data_status["status"][0]['mp']+=10
                data_status["status"][0]['fatigue_max']+=40
                if special!=True:
                    data_status["status"][0]['fatigue']+=give_fatigue_from_rank(rank)
                
            if rank=="E":
                data_status["status"][0]['XP']+=10
            elif rank=="D":
                data_status["status"][0]['XP']+=20
            elif rank=="C":
                data_status["status"][0]['XP']+=40
            elif rank=="B":
                data_status["status"][0]['XP']+=80
            elif rank=="A":
                data_status["status"][0]['XP']+=150
            elif rank=="S":
                data_status["status"][0]['XP']+=200
            else:
                data_status["status"][0]['XP']+=1000

            with open("Files/status.json", 'w') as fson:
                json.dump(data_status, fson, indent=4)
            with open('Files/Data/Theme_Check.json', 'r') as themefile:
                theme_data=json.load(themefile)
                theme=theme_data["Theme"]
            subprocess.Popen(['python', f'{theme} Version/Leveled up/gui.py'])

        elif k=="STRav":
            for k in range(dicts[k]):
                with open("Files/Status.json", 'r') as fson:
                    data_status_2=json.load(fson)
                    
                    data_status_2["avail_eq"][0]['str_based']+=1

                with open("Files/status.json", 'w') as fson:
                    json.dump(data_status_2, fson, indent=4)

        elif k=="INTav":
            for k in range(dicts[k]):
                with open("Files/Status.json", 'r') as fson:
                    data_status_3=json.load(fson)
                    
                    data_status_3["avail_eq"][0]['int_based']+=1

                with open("Files/status.json", 'w') as fson:
                    json.dump(data_status_3, fson, indent=4)

        else:
            check=False
            with open("Files/Data/Inventory_list.json", 'r') as fson:
                data_inv=json.load(fson)
                item=data_inv[k]
                name_of_item=k
            
            with open("Files/Inventory.json", 'r') as fson:
                data_fininv=json.load(fson)
                key_data=list(data_fininv.keys())

                for k in key_data:
                    if name_of_item==k:
                        check=True
            
            if check==True:
                data_fininv[name_of_item][0]["qty"]+=1

            elif check==False:
                data_fininv[name_of_item]=item

            with open("Files/Inventory.json", 'w') as finaladdon:
                json.dump(data_fininv, finaladdon, indent=6)

    with open("Files/Quests/Active_Quests.json", 'r') as fols:
        quests=json.load(fols)

    del quests[name]

    with open("Files/Quests/Active_Quests.json", 'w') as folas: 
        json.dump(quests, folas, indent=6)

    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=json.load(themefile)
        theme=theme_data["Theme"]
    
    if special==False:
        message_open("Quest Completed")
        subprocess.Popen(['python', f'{theme} Version/Quests/gui.py'])
    else:
        message_open("Revertion")
        subprocess.Popen(['python', 'First/Vows/gui.py'])

    window.quit()

def abandon_quest(name,window):
    with open("Files/Quests/Active_Quests.json", 'r') as fols:
        quests=json.load(fols)

    del quests[name]

    with open("Files/Quests/Active_Quests.json", 'w') as fols:
        json.dump(quests, fols, indent=6)

    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=json.load(themefile)
        theme=theme_data["Theme"]
    subprocess.Popen(['python', f'{theme} Version/Quests/gui.py'])

    window.quit()

def get_quest_image(rank,typel):
    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=json.load(themefile)
        theme=theme_data["Theme"]
    if rank!='-' and typel!='-':
        if rank=='D' or rank=='E':
            if typel=="Common":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_5.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_6.png"))
            
        elif rank=='C' or rank=='B':
            if typel=="Common":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_8.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_9.png"))
            
        elif rank=='A':
            if typel=="Common":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_11.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_12.png"))
            
        elif rank=='S':
            if typel=="Common":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_14.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_15.png"))
        
        elif rank=='?':
            if typel=='Unknown':
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_16.png"))
    else:
        return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_17.png"))

def open_write_quest(name,id,type,window):
    if name!="-":
        with open('Files/Data/Theme_Check.json', 'r') as themefile:
            theme_data=json.load(themefile)
            theme=theme_data["Theme"]
        with open("Files/Temp Files/Quest Temp.csv", 'w', newline='') as csv_open:
                fw=csv.writer(csv_open)
                rec=[name,id,type]
                fw.writerow(rec)

        subprocess.Popen(['python', f'{theme} Version/Quest Info/gui.py'])

        with open("Files/Tabs.json",'r') as tab_son:
            tab_son_data=json.load(tab_son)

        with open("Files/Tabs.json",'w') as fin_tab_son:
            tab_son_data["Quest"]='Close'
            json.dump(tab_son_data,fin_tab_son,indent=4)

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
    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=json.load(themefile)
        theme=theme_data["Theme"]
    subprocess.Popen(['python', f"{theme} Version\Message\gui.py"])

def reduction(val, stre, agi, types):
    if types=="amt":
        if val==50:
            if stre>=20 and stre<=30:
                return -10
            elif stre>=31 and stre<=40:
                return -20
            elif stre>=41 and stre<=50:
                return -30
            elif stre>=51 and stre<=60:
                return -40
            elif stre>=61 and stre<=70:
                return -100
            else:
                return 0
        
        elif val==15:
            if stre>=20 and stre<=30:
                return -5
            elif stre>=31 and stre<=40:
                return -5
            elif stre>=41 and stre<=50:
                return -10
            elif stre>=51 and stre<=60:
                return -25
            elif stre>=61 and stre<=70:
                return -35
            else:
                return 0
            
        elif val==30:
            if stre>=20 and stre<=30:
                return -10
            elif stre>=31 and stre<=40:
                return -10
            elif stre>=41 and stre<=50:
                return -20
            elif stre>=51 and stre<=60:
                return -25
            elif stre>=61 and stre<=70:
                return -35
        
        else:
            return 0
        
    elif types=="time":
        if val==45:
            if agi>=20 and agi<=30:
                return -10
            elif agi>=31 and agi<=40:
                return -20
            elif agi>=41 and agi<=50:
                return -30
            elif agi>=51 and agi<=60:
                return -30
            elif agi>=61 and agi<=70:
                return -40
            else:
                return 0
        
        elif val==60:
            if agi>=20 and agi<=30:
                return -20
            elif agi>=31 and agi<=40:
                return -30
            elif agi>=41 and agi<=50:
                return -100
            elif agi>=51 and agi<=60:
                return -100
            elif agi>=61 and agi<=70:
                return -200
            else:
                return 0
        
        else:
            return 0

def xp_curve(x):
    if 1 <= x <= 15:
        return 30 + 20 * (x - 1)
    elif x > 15:
        return 30 + 20 * 14 + max(0, 121.3 * (x - 15)**1.3)  # Ensure XP gain is always positive
    elif x > 101:
        return 30 + 20 * 14 + max(0, 121.3 * (x - 15)**1.1)  # Ensure XP gain is always positive
    else:
        raise ValueError("x must be greater than or equal to 1")

def check_demons():
    if not os.path.exists("Files\Demons Castle\Demon_Data.json"):
        data={
    "Demon Imp": {
        "rank": "E",
        "type": "Normal",
        "swarm": "Yes",
        "soul":1,
        "XP": 10
    },
    "Demon Wisp": {
        "rank": "E",
        "type": "Normal",
        "swarm": "Yes",
        "soul":1,
        "XP": 12
    },
    "Demon Vermin": {
        "rank": "E",
        "type": "Normal",
        "swarm": "Yes",
        "soul":1,
        "XP": 15
    },
    "Demon Grunt": {
        "rank": "D",
        "type": "Normal",
        "swarm": "Yes",
        "soul":2,
        "XP": 20
    },
    "Demon Scout": {
        "rank": "D",
        "type": "Normal",
        "swarm": "No",
        "soul":2,
        "XP": 25
    },
    "Demon Hound": {
        "rank": "D",
        "type": "Normal",
        "swarm": "No",
        "soul":2,
        "XP": 30
    },
    "Demon Soldier": {
        "rank": "C",
        "type": "Normal",
        "swarm": "No",
        "soul":3,
        "XP": 40
    },
    "Demon Mage": {
        "rank": "C",
        "type": "Normal",
        "swarm": "No",
        "soul":3,
        "XP": 45
    },
    "Demon Beast": {
        "rank": "C",
        "type": "Normal",
        "swarm": "No",
        "soul":3,
        "XP": 50
    },
    "Demon Knight": {
        "rank": "B",
        "type": "Normal",
        "swarm": "No",
        "soul":4,
        "XP": 60
    },
    "Demon Berserker": {
        "rank": "B",
        "type": "Normal",
        "swarm": "No",
        "soul":4,
        "XP": 65
    },
    "Demon Guardian": {
        "rank": "B",
        "type": "Normal",
        "swarm": "No",
        "soul":4,
        "XP": 70
    },
    "Demon Captain": {
        "rank": "A",
        "type": "Normal",
        "swarm": "No",
        "soul":4,
        "XP": 80
    },
    "Demon Assassin": {
        "rank": "A",
        "type": "Normal",
        "swarm": "No",
        "soul":4,
        "XP": 85
    },
    "Demon Warlock": {
        "rank": "A",
        "type": "Normal",
        "swarm": "No",
        "soul":4,
        "XP": 90
    },
    "Demon Noble": {
        "rank": "S",
        "type": "Normal",
        "swarm": "No",
        "soul":4,
        "XP": 100
    },
    "Demon Warlord": {
        "rank": "S",
        "type": "Normal",
        "swarm": "No",
        "soul":4,
        "XP": 110
    },
    "Demon Sorcerer": {
        "rank": "S",
        "type": "Normal",
        "swarm": "No",
        "soul":4,
        "XP": 120
    },
    "Demon Lord": {
        "rank": "SS",
        "type": "Elite",
        "swarm": "No",
        "soul":4,
        "XP": 150
    },
    "Demon Archmage": {
        "rank": "SS",
        "type": "Elite",
        "swarm": "No",
        "soul":4,
        "XP": 160
    },
    "Demon Executioner": {
        "rank": "SS",
        "type": "Elite",
        "swarm": "No",
        "soul":4,
        "XP": 170
    },
    "Demon Overlord": {
        "rank": "SSS",
        "type": "Elite",
        "swarm": "No",
        "soul":4,
        "XP": 250
    },
    "Demon King": {
        "rank": "SSS",
        "type": "Elite",
        "swarm": "No",
        "soul":4,
        "XP": 300
    },
    "Demon Tyrant": {
        "rank": "SSS",
        "type": "Elite",
        "swarm": "No",
        "soul":4,
        "XP": 350
    }
}

        with open("Files\Demons Castle\Demon_Data.json", "w") as demon_file:
            json.dump(data, demon_file, indent=6)

        # Generate XP values for x between 1 and 100
        xp_values = {}
        prev_value = 0  # Track previous value to enforce monotonicity
        for x in range(1, 500):
            current_value = round(xp_curve(x), 1)
            if current_value <= prev_value:  # Ensure the current value is greater
                current_value = prev_value + 1
            xp_values[str(x)] = current_value
            prev_value = current_value  # Update previous value

        with open("Files/Data/Level_Up_Values.json", 'w') as fron3:
            json.dump({"XP Check": xp_values}, fron3, indent=4)

        with open("Files\Status.json", 'r') as status_file:
            status = json.load(status_file)
            lvl=status["status"][0]['level']
        
        xp_of=xp_values[str(lvl)]

        status["status"][0]['XP']=xp_of
        with open("Files\Status.json", 'w') as status_file:
            json.dump(status, status_file, indent=8)

def xp_input():
    # Generate XP values for x between 1 and 100
    xp_values = {}
    prev_value = 0  # Track previous value to enforce monotonicity
    for x in range(1, 500):
        current_value = round(xp_curve(x), 1)
        if current_value <= prev_value:  # Ensure the current value is greater
            current_value = prev_value + 1
        xp_values[str(x)] = current_value
        prev_value = current_value  # Update previous value

    with open("Files/Data/Level_Up_Values.json", 'w') as fron3:
        json.dump({"XP Check": xp_values}, fron3, indent=4)

def resize_image(image_path, size):
    """Resize an image and return the processed PIL Image."""
    if os.path.exists(image_path):
        return Image.open(image_path).resize(size)
    return None

def preload_images(image_paths, size):
    """Preload images by resizing them in parallel and converting them on the main thread."""
    resized_images = []

    # Resize images in parallel
    with ThreadPoolExecutor() as executor:
        resized_images = list(executor.map(lambda path: resize_image(path, size), image_paths))

    # Create PhotoImage objects on the main thread
    preloaded_images = [
        ImageTk.PhotoImage(img) for img in resized_images if img is not None
    ]
    return preloaded_images

def side_bar(image, size):
    # Construct the path to the image
    s = 'thesystem/side_bars/' + image
    # Check if the image exists
    if os.path.exists(s):
        # Open and resize the image
        s_m = Image.open(s).resize(size)
        # Convert the image to a format Tkinter can use
        return ImageTk.PhotoImage(s_m)
    else:
        print(f"Image {s} not found.")
        return None
=======

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ujson
import csv
import subprocess
from PIL import Image, ImageTk
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

last_run = 0 

def fin_pen():
    today = datetime.now().date()

    yesterday = today - timedelta(days=1)
    with open('Files/Checks/Daily_time_check.csv', 'r', newline='') as fout:
        fr=csv.reader(fout)
        for k in fr:
            status=k[1]
            dates=k[0]

    p_date=datetime.strptime(dates, "%Y-%m-%d").date()
    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    with open("Files/Settings.json", 'r') as settings_open:
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
    with open("Files\Data\Calorie_Count.json", 'r') as calorie_add_file:
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
        with open("Files\Workout\Cal_Count.json", 'r') as calorie_val_search_file:
            calorie_val_search_data=ujson.load(calorie_val_search_file)
            cal_val=calorie_val_search_data[day_of_week]
            
        with open("Files/status.json", 'r') as stat_first_fson:
            stat_first_fson_data=ujson.load(stat_first_fson)
            result=stat_first_fson_data["cal_data"][0]["result"]
    
    except:
        result='MILD WEIGHT LOSS'
        cal_tdy_val=0

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

    #! ===================================================================

def penalty_check(win):
    with open("Files/Data/Penalty_Info.json", "r") as pen_info_file:
        data0=ujson.load(pen_info_file)
        target_time_str=data0["Penalty Time"]

    now=datetime.now()
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
        with open("Files/Data/First_open.csv", 'r') as first_open_check_file:
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
        with open("Files/Data/Prove_file.csv", 'r') as second_open_check_file:
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
    
        subprocess.Popen(['python', 'First/Start/gui.py'])

        sys.exit()
    
    elif first_run_file_check==True and second_run_file_check==False:
        stp_eve.set()

        # Wait for the thread to finish
        thrd.join()

        subprocess.Popen(['python', 'First/Check/gui.py'])

        sys.exit()

def random_skill_check():
    # Load the primary status file
    with open("Files/status.json", 'r') as fson:
        data = ujson.load(fson)

    # Extract player stats and metadata
    name = data["status"][0]['name'].upper()
    hp = data["status"][0]['hp']
    mp = data["status"][0]['mp']
    lvl = data["status"][0]['level']
    old_lvl = f"{lvl:02d}"

    stre = data["status"][0]['str']
    intel = data["status"][0]['int']
    agi = data["status"][0]['agi']
    vit = data["status"][0]['vit']
    per = data["status"][0]['per']
    man = data["status"][0]['man']

    tit = data["status"][1]['title'].upper()
    job = data["status"][1]['job'].upper()
    xp_str = data["status"][0]['XP']
    coins = data["status"][0]['coins']

    # Check level-up and skill eligibility
    if lvl % 5 == 0:
        with open("Files/Skills/Skill_old_check.json", 'r') as check_file:
            old_lvl_data = ujson.load(check_file)

        if lvl != old_lvl_data["old_stat"][0]["lvl"]:
            # Calculate stat differences
            comp_rec = {
                "STR": int(stre) - int(old_lvl_data["old_stat"][0]["str"]),
                "INT": int(intel) - int(old_lvl_data["old_stat"][0]["int"]),
                "AGI": int(agi) - int(old_lvl_data["old_stat"][0]["agi"]),
                "VIT": int(vit) - int(old_lvl_data["old_stat"][0]["vit"]),
                "PER": int(per) - int(old_lvl_data["old_stat"][0]["per"]),
                "MAN": int(man) - int(old_lvl_data["old_stat"][0]["man"])
            }

            # Identify the max stat(s)
            max_value = max(comp_rec.values())
            max_keys = [key for key, value in comp_rec.items() if value == max_value]

            # Handle ties for multiple max stats, limit to 2 alphabetically
            max_keys = sorted(max_keys)[:2]

            # Load skill list data
            with open("Files/Skills/Skill_List.json", 'r') as skill_list:
                skill_list_data = ujson.load(skill_list)

            # Match skills with conditions
            name_of_skill = [
                skill for skill, details in skill_list_data.items()
                if set(details[1]["Condition"]).issubset(max_keys)
            ]

            # Choose a skill
            choosen_skill = random.choice(name_of_skill) if name_of_skill else "Dash"

            # Load current skills
            with open("Files/Skills/Skill.json", 'r') as main_skills:
                main_skill_data = ujson.load(main_skills)

            # Check for duplication and process accordingly
            if choosen_skill in main_skill_data:
                if main_skill_data[choosen_skill][0]["lvl"] != "MAX":
                    main_skill_data[choosen_skill][0]["lvl"] += 1
                    with open("Files/Skills/Skill.json", 'w') as update_main_skills:
                        ujson.dump(main_skill_data, update_main_skills, indent=6)

                    with open("Files/Temp Files/Skill Up Temp.csv", 'w', newline='') as skill_temp_csv_open:
                        fw = csv.writer(skill_temp_csv_open)
                        fw.writerow([choosen_skill])

                    with open('Files/Data/New_Updates.json', 'w') as updatefile:
                        fin_data = {"Skills": "False", "Quests": "False", "Upgrade": "True", "Lines": "False"}
                        ujson.dump(fin_data, updatefile, indent=4)
            else:
                main_skill_data[choosen_skill] = [(skill_list_data[choosen_skill].pop(0))]
                main_skill_data[choosen_skill][0]["pl_point"] = 0

                with open("Files/Skills/Skill.json", 'w') as update_main_skills:
                    ujson.dump(main_skill_data, update_main_skills, indent=6)

                with open('Files/Data/New_Updates.json', 'w') as updatefile:
                    fin_data = {"Skills": "True", "Quests": "False", "Upgrade": "False", "Lines": "False"}
                    ujson.dump(fin_data, updatefile, indent=4)

            # Update old stats
            old_lvl_data["old_stat"][0].update({
                "lvl": lvl,
                "str": stre,
                "int": intel,
                "agi": agi,
                "vit": vit,
                "per": per,
                "man": man,
            })

            with open("Files/Skills/Skill_old_check.json", 'w') as final_check_file:
                ujson.dump(old_lvl_data, final_check_file, indent=4)

def check_midnight(window,stop_event):
    while not stop_event.is_set():
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            penalty_check(window)
        time.sleep(1)

def random_quest():
    # ! The Random Quests thing
    with open('Files/Data/Random_Quest_Day.json', 'r') as random_quest:
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
                with open("Files/Quests/Active_Quests.json", 'r') as active_quests_file:
                    activ_quests=ujson.load(active_quests_file)
                    name_of_activ_quests=list(activ_quests.keys())
                    activ_quests_vals=0
                    for k in name_of_activ_quests:
                        activ_quests_vals+=1
            except:
                name_of_activ_quests=[]

            if activ_quests_vals<13 and activ_quests_vals!=13:
                # ? Quest Name
                with open("Files\Quests\Quest_Names.json", 'r') as quest_name_file:
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
                with open("Files\Quests\Quest_Desc.json", 'r') as quest_desc_file:
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
                with open("Files\Data\Inventory_List.json", 'r') as rewards_name_file:
                    reward_names=ujson.load(rewards_name_file)
                    reward_names_list=list(reward_names.keys())

                    final_rewards_list=[]
                    for k in reward_names_list:
                        if rank==reward_names[k][0]["rank"]:
                            final_rewards_list.append(k)
                    
                    rew2=random.choice(final_rewards_list)

                # ? Quest Info
                file_name=f"Files\Workout\{random_ab}_based.json"
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

                with open("Files/Quests/Active_Quests.json", 'w') as fin_active_quest_file:
                    ujson.dump(activ_quests, fin_active_quest_file, indent=6)

                random_quest_data["Day"]=random.randint(0,6)

    if comp_check==True:
        with open('Files/Data/Random_Quest_Day.json', 'w') as finalrandom_quest:
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

def animate_window_open(window, target_height, width, step=2, delay=5, doners=False):
    current_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{width}x{current_height}+{screen_width//2 - width//2}+{screen_height//2 - current_height//2}")

    if current_height < target_height:
        new_height = min(current_height + step, target_height)
    else:
        new_height = current_height
    
    new_y = screen_height // 2 - new_height // 2
    window.geometry(f"{width}x{new_height}+{screen_width//2 - width//2}+{new_y}")

    done_val=False

    if round((new_height/target_height), 1)==0.2:
        if doners==False:
            #subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])
            done_val=True

    if new_height < target_height:
        window.after(delay, animate_window_open, window, target_height, width, step, delay, done_val)

def animate_window_close(window, target_height, width, step=2, delay=5):
    current_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{width}x{current_height}+{screen_width//2 - width//2}+{screen_height//2 - current_height//2}")

    if current_height > target_height:
        new_height = max(current_height - step, target_height)
    else:
        new_height = current_height
    
    new_y = screen_height // 2 - new_height // 2
    window.geometry(f"{width}x{new_height}+{screen_width//2 - width//2}+{new_y}")

    if new_height > target_height:
        window.after(delay, animate_window_close, window, target_height, width, step, delay)
    else:
        window.quit()

class VideoPlayer:
    def __init__(self, canvas, video_path, del_x=0, del_y=0, resize_factor=0.7, buffer_size=10):
        self.canvas = canvas
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.image_id = self.canvas.create_image(0, 0, anchor='nw')  # Initial anchor
        self.frame_queue = queue.Queue(maxsize=buffer_size)
        self.stop_event = threading.Event()

        # Read the first frame to get video dimensions
        ret, frame = self.cap.read()
        if ret:
            self.original_width = frame.shape[1]
            self.original_height = frame.shape[0]
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video position
        else:
            raise ValueError("Unable to read video file.")

        # Start frame processing in a separate thread
        self.read_thread = threading.Thread(target=self._read_frames, daemon=True)
        self.read_thread.start()

        # Ensure canvas dimensions are updated before starting
        self.canvas.update_idletasks()
        self.update_frame()

    def _calculate_scaling_factor(self):
        """
        Calculate the scaling factor to ensure the video fills the canvas while maintaining aspect ratio.
        """
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate scaling factors for both axes
        scale_width = canvas_width / self.original_width
        scale_height = canvas_height / self.original_height

        # Use the larger scaling factor to ensure the video covers the canvas
        return max(scale_width, scale_height)

    def _read_frames(self):
        """
        Reads and processes video frames, adding them to a thread-safe queue.
        """
        while not self.stop_event.is_set():
            if not self.frame_queue.full():
                ret, frame = self.cap.read()

                if not ret:
                    # Restart video when reaching the end
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = self.cap.read()

                if ret:
                    # Resize frame to fill the canvas
                    scaling_factor = self._calculate_scaling_factor()
                    new_width = int(self.original_width * scaling_factor)
                    new_height = int(self.original_height * scaling_factor)

                    frame = cv2.resize(frame, (new_width, new_height))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Add processed frame to the queue
                    self.frame_queue.put(frame)
            else:
                time.sleep(0.005)  # Brief pause to prevent busy-waiting

    def update_frame(self):
        """
        Updates the canvas with the latest frame from the queue.
        """
        start_time = time.time()
        if not self.frame_queue.empty():
            # Get the next frame from the queue
            frame = self.frame_queue.get()

            # Convert frame to ImageTk format
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            # Calculate the position to center the frame on the canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            x_center = (canvas_width - frame.shape[1]) // 2
            y_center = (canvas_height - frame.shape[0]) // 2

            # Update the canvas image and position
            self.canvas.coords(self.image_id, x_center, y_center)
            self.canvas.itemconfig(self.image_id, image=imgtk)
            self.canvas.imgtk = imgtk

        # Calculate the delay to maintain 24 FPS
        elapsed_time = time.time() - start_time
        delay = max(0, int((1 / 24 - elapsed_time) * 1000))  # Convert to milliseconds
        self.canvas.after(delay, self.update_frame)

    def __del__(self):
        try:
            self.stop_event.set()  # Signal the reading thread to stop
            self.read_thread.join()  # Wait for the thread to finish
            if self.cap.isOpened():
                self.cap.release()
        except AttributeError:
            pass  # Ignore errors caused by partially destroyed objects

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
            with open('Files/Data/Theme_Check.json', 'r') as themefile:
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
    with open("Files/Data/Job_info.json", 'r') as stat_fson:
        data=ujson.load(stat_fson)

    canvas.itemconfig("Jobs", state="hidden")
    data["status"][1]["job_confirm"]='True'

    with open("Files/Data/Job_info.json", 'w') as fson:
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
    with open("Files/Status.json", 'r') as fson:
        data = ujson.load(fson)
        lvl = int(data["status"][0]['level'])  # Current level
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

        # Save updated status to file
        with open("Files/Status.json", 'w') as up_fson:
            ujson.dump(data, up_fson, indent=4)

        # Trigger level-up GUI
        with open('Files/Data/Theme_Check.json', 'r') as themefile:
            theme_data = ujson.load(themefile)
            theme = theme_data["Theme"]
            subprocess.Popen(['python', f'{theme} Version/Leveled up/gui.py'])

            if data["status"][0]['level']>=100:
                message_open("Courage of the Weak")

    else:
        print()
    fin_xp = None
    if str(lvl + 1) in level_up_values:
        next_level_xp = float(level_up_values[str(lvl + 1)])
        fin_xp = next_level_xp - xp  # Difference between next level XP and current XP

    return [leveled_up,fin_xp]

def return_back_to_tab(loc,window):
    with open('Files/Data/Theme_Check.json', 'r') as themefile:
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
    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    subprocess.Popen(['python', f"{theme} Version\Message\gui.py"])

def resize_image(image_path, size):
    """Resize an image using PIL."""
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            return img.resize(size, Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"Error opening/resizing image {image_path}: {e}")
            return None
    return None

def preload_images(image_paths, size):
    """Preload images by resizing them in parallel and converting to PhotoImage."""
    resized_images = []

    with ThreadPoolExecutor() as executor:
        resized_images = list(executor.map(lambda path: resize_image(path, size), image_paths))
    
    preloaded_images = []
    for img in resized_images:
        if img is not None:
            if isinstance(img, np.ndarray):  # Check if it's a NumPy array (OpenCV image)
                try:
                    preloaded_images.append(ImageTk.PhotoImage(image=Image.fromarray(img)))
                except Exception as e:
                    print(f"Error converting to PhotoImage: {e}")
                    print(f"Image shape: {img.shape}, dtype: {img.dtype}")
            elif isinstance(img, Image.Image):  # Check if it's a PIL Image
                preloaded_images.append(ImageTk.PhotoImage(image=img))
            else:
                print(f"Unknown image type: {type(img)}")
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

>>>>>>> Stashed changes
