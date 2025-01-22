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

