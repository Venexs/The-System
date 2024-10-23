from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json
import csv
import subprocess
from PIL import Image, ImageTk
from datetime import datetime, timedelta, date
import threading
import time
import sys
import random
import cv2
import os

def fin_pen():
    today = datetime.now().date()

    yesterday = today - timedelta(days=1)
    with open('Files/Checks/Today_Quest.csv', 'r', newline='') as fout:
        fr=csv.reader(fout)
        for k in fr:
            status=k[1]
            dates=k[0]

    p_date=datetime.strptime(dates, "%Y-%m-%d").date()
    if yesterday==p_date and status=="UNDONE":
        subprocess.Popen(['python', 'Anime Version/Penalty Quest/gui.py'])
    elif yesterday!=p_date or status=="UNDONE":
        subprocess.Popen(['python', 'Anime Version/Penalty Quest/gui.py'])

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

    cal_pen=False

    if result=='MILD WEIGHT LOSS':
        cal_30=cal_val+(cal_val*0.25)
        if cal_tdy_val>cal_30 or cal_tdy_val==0:
            cal_pen=True

    elif result=='MILD WEIGHT GAIN':
        cal_30=cal_val-(cal_val*0.25)
        if cal_tdy_val<cal_30 or cal_tdy_val==0:
            cal_pen=True

    if cal_pen==True:
        subprocess.Popen(['python', 'First/Calorie Penalty/gui.py'])

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
        with open("Files/Data/First_open.csv", 'r') as second_open_check_file:
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
    with open("Files/status.json", 'r') as fson:
        data=json.load(fson)
        name=data["status"][0]['name'].upper()
        # ? =================================================
        hp=data["status"][0]['hp']
        mp=data["status"][0]['mp']
        lvl=data["status"][0]['level']
        old_lvl=f"{lvl:02d}"
        # ? =================================================
        stre=data["status"][0]['str']
        intel=data["status"][0]['int']
        agi=data["status"][0]['agi']
        vit=data["status"][0]['vit']
        per=data["status"][0]['per']
        man=data["status"][0]['man']
        # ? =================================================
        tit=data["status"][1]['title'].upper()
        job=data["status"][1]['job'].upper()
        # ? =================================================
        xp_str=data["status"][0]['XP']
        coins=data["status"][0]['coins']
        # ? =================================================
        av_str_based=data["avail_eq"][0]['str_based']
        av_int_based=data["avail_eq"][0]['int_based']
        # ? =================================================
    if lvl%5==0:
        with open("Files/Skills/Skill_old_check.json", 'r') as check_file:
            old_lvl_data=json.load(check_file)
            old_lvl_key=list(old_lvl_data.keys())

        if lvl!=old_lvl_data["old_stat"][0]["lvl"]:
            comp_str= int(stre) - int(old_lvl_data["old_stat"][0]["str"])
            comp_int= int(intel) - int(old_lvl_data["old_stat"][0]["int"])
            comp_agi= int(agi) - int(old_lvl_data["old_stat"][0]["agi"])
            comp_vit= int(vit) - int(old_lvl_data["old_stat"][0]["vit"])
            comp_per= int(per) - int(old_lvl_data["old_stat"][0]["lvl"])
            comp_man= int(man) - int(old_lvl_data["old_stat"][0]["man"])

            comp_rec={"STR":comp_str, "INT":comp_int, "AGI":comp_agi, "VIT":comp_vit, "PER":comp_per, "MAN":comp_man}
            max_value = max(comp_rec.values())

            max_keys = [key for key, value in comp_rec.items() if value == max_value]

            if len(max_keys) > 1:
                second_max_value = max(v for k, v in comp_rec.items() if k not in max_keys)
                second_max_keys = [key for key, value in comp_rec.items() if value == second_max_value]
                max_keys.extend(second_max_keys)

            if len(max_keys)>2:
                new_keys=[]
                new_keys.append(max_keys[0])
                new_keys.append(max_keys[1])
                max_keys=sorted(new_keys)

            with open("Files/Skills/Skill_List.json", 'r') as skill_list:
                skill_list_data=json.load(skill_list)
                skill_list_keys=list(skill_list_data.keys())
        
            name_of_skill=[]
            skill_value=0
            
            for k in skill_list_keys:
                if sorted(skill_list_data[k][1]["Condition"]) in max_keys:
                    name_of_skill.append(k)
                    skill_value+=1

            print(skill_value)
            try:
                if skill_value!=0:
                    choosen_skill=name_of_skill[random.randint(0, skill_value)]
                else:
                    choosen_skill=name_of_skill[0]
            except:
                choosen_skill="Dash"

            with open("Files/Skills/Skill.json", 'r') as main_skills:
                main_skill_data=json.load(main_skills)
                try:
                    main_skill_keys=list(main_skill_data.keys())
                except:
                    main_skill_keys=[]

            dupli=False

            if main_skill_keys!=[]:
                for k in main_skill_keys:
                    if k==choosen_skill:
                        dupli=True
            
            print(choosen_skill)

            if dupli==True:
                if main_skill_data[choosen_skill][0]["lvl"]!="MAX":
                    main_skill_data[choosen_skill][0]["lvl"]+=1

                    with open("Files/Skills/Skill.json", 'w') as update_main_skills:
                        json.dump(main_skill_data, update_main_skills, indent=6)
                    with open("Files/Temp Files/Skill Up Temp.csv", 'w', newline='') as skill_temp_csv_open:
                        fw=csv.writer(skill_temp_csv_open)
                        fw.writerow([choosen_skill])
                    with open('Files/Data/New_Updates.json', 'w') as updatefile:
                        fin_data={
                                    "Skills":"False",
                                    "Quests":"False",
                                    "Upgrade":"True",
                                    "Lines":"False"
                                }
                        json.dump(fin_data, updatefile, indent=4)
            
            elif dupli==False:
                main_skill_data[choosen_skill]=[(skill_list_data[choosen_skill].pop(0))]
                main_skill_data[choosen_skill][0]["pl_point"]=0
                with open("Files/Skills/Skill.json", 'w') as update_main_skills:
                    json.dump(main_skill_data, update_main_skills, indent=6)
                with open('Files/Data/New_Updates.json', 'w') as updatefile:
                    fin_data={
                                "Skills":"True",
                                "Quests":"False",
                                "Upgrade":"False",
                                "Lines":"False"
                            }
                    json.dump(fin_data, updatefile, indent=4)
                
            old_lvl_data["old_stat"][0]["lvl"]=lvl
            old_lvl_data["old_stat"][0]["str"]=stre
            old_lvl_data["old_stat"][0]["int"]=intel
            old_lvl_data["old_stat"][0]["agi"]=agi
            old_lvl_data["old_stat"][0]["vit"]=vit
            old_lvl_data["old_stat"][0]["per"]=per
            old_lvl_data["old_stat"][0]["man"]=man

            with open("Files/Skills/Skill_old_check.json", 'w') as final_check_file:
                json.dump(old_lvl_data, final_check_file, indent=4)

def check_midnight(window,stop_event):
    while stop_event.is_set():
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
            #subprocess.Popen(['python', 'sfx.py'])
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
    with open("Files\Mod\presets.json", 'r') as pres_file:
        pres_file_data=json.load(pres_file)
        final_video_path=pres_file_data["Anime"]["Video"]

    def __init__(self, canvas, video_path, x, y, frame_skip=5, resize_factor=0.7):
        self.canvas = canvas
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.x = x
        self.y = y
        self.frame_skip = frame_skip  # Increase skip to reduce load
        self.resize_factor = resize_factor
        self.image_id = self.canvas.create_image(self.x, self.y)
        self.frame_count = 0
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
                # Perform resizing and color conversion only if needed
                frame = cv2.resize(frame, (0, 0), fx=self.resize_factor, fy=self.resize_factor)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert to ImageTk format
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)

                # Update the canvas image
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

def update_penalty_countdown(duration_seconds,countdown_label,canvas,window):
    end_time = datetime.now() + timedelta(seconds=duration_seconds)
    update_penalty_countdown(end_time)
    remaining_time = end_time - datetime.now()

    if remaining_time.days < 0:
        subprocess.Popen(['python', 'Anime Version/Penalty Quest Rewards/gui.py'])
        window.quit()

    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    timer_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    canvas.itemconfig(countdown_label, text=timer_text)

    window.after(1000, update_penalty_countdown, end_time)

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

def get_fin_xp(window):
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
            subprocess.Popen(['python', 'Anime Version/Leveled up/gui.py'])
            subprocess.Popen(['python', 'Anime Version/Status Tab/gui.py'])
            window.quit()

    with open("Files/Data/Level_Up_Values.json", 'r') as fron:
        data_1=json.load(fron)
        xp_end=data_1["XP Check"][str(lvl)]

        fin_xp=xp_end-xp_str
        re_open_check=False
        if fin_xp<0:
            data["status"][0]['level']+=1
            with open("Files/status.json", 'w') as final_lvl_fson:
                json.dump(data, final_lvl_fson, indent=4)
            re_open_check=True
            subprocess.Popen(['python', 'Anime Version/Status Tab/gui.py'])  
        return [fin_xp,re_open_check]

def daily_preview(window):
    with open("Files\Temp Files\Daily Rewards.csv", 'w', newline='') as rew_csv_open:
            rew_fw=csv.writer(rew_csv_open)
            rew_fw.writerow(["Preview"])
    subprocess.Popen(['python', 'Anime Version/Daily Quest Rewards/gui.py'])

    window.quit()

def check_daily_comp(today_date_str, window):
    with open("Files/Data/Daily_Quest.json", 'r') as daily_quest_file:
        daily_quest_data=json.load(daily_quest_file)
        # ? =======================================================
        # ? Players
        pl_push=daily_quest_data["Player"]["Push"]
        pl_sit=daily_quest_data["Player"]["Sit"]
        pl_sqat=daily_quest_data["Player"]["Squat"]
        pl_run=daily_quest_data["Player"]["Run"]

        pl_int=daily_quest_data["Player"]["Int_type"]
        pl_slp=daily_quest_data["Player"]["Sleep"]
        # ? =======================================================
        # ? Final
        fl_push=daily_quest_data["Final"]["Push"]
        fl_sit=daily_quest_data["Final"]["Sit"]
        fl_sqat=daily_quest_data["Final"]["Squat"]
        fl_run=daily_quest_data["Final"]["Run"]

        fl_int=daily_quest_data["Final"]["Int_type"]
        fl_slp=daily_quest_data["Final"]["Sleep"]
        # ? =======================================================
    
    with open('Files\Checks\Secret_Quest_Check.json', 'r') as secrer_quest:
        secrer_quest_data=json.load(secrer_quest)
        day_num=secrer_quest_data["Day"]
        tdy_week_num=datetime.today().weekday()
    if day_num==tdy_week_num:
        if (pl_push/2)>=fl_push and (pl_run/2)>=fl_run and (pl_sqat/2)>=fl_sqat and (pl_sit/2)>=fl_sit and (pl_int/2)>=fl_int:
            if fl_push!=100 and fl_sit!=100 and fl_sqat!=100:
                daily_quest_data["Final"]["Push"]+=5
                daily_quest_data["Final"]["Sit"]+=5
                daily_quest_data["Final"]["Squat"]+=5
                daily_quest_data["Final"]["Run"]+=0.5

                daily_quest_data["Player"]["Push"]=0
                daily_quest_data["Player"]["Sit"]=0
                daily_quest_data["Player"]["Squat"]=0
                daily_quest_data["Player"]["Run"]=0
                daily_quest_data["Player"]["Int_type"]=0
                daily_quest_data["Player"]["Sleep"]=0

                if round(fl_int,1)!=10:
                    daily_quest_data["Final"]["Int_type"]+=0.5

                with open("Files/Data/Daily_Quest.json", 'w') as final_daily_quest_file:
                    json.dump(daily_quest_data, final_daily_quest_file, indent=4)

                with open("Files/Checks/Daily_time_check.csv", 'w',  newline='') as fin_daily_date_check_file:
                    fw1=csv.writer(fin_daily_date_check_file)
                    fw1.writerow([today_date_str,"UNDONE","Complete"])
            
                with open("Files\Temp Files\Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                    rew_fw=csv.writer(rew_csv_open)
                    rew_fw.writerow(["Secret"])
                
                subprocess.Popen(['python', 'Anime Version/Daily Quest Rewards/gui.py'])
                
                window.quit()
    else:
        if (pl_push)>=fl_push and (pl_run)>=fl_run and (pl_sqat)>=fl_sqat and (pl_sit)>=fl_sit and (pl_int)>=fl_int and (pl_slp)>=fl_slp:
            if fl_push!=100 and fl_sit!=100 and fl_sqat!=100:
                daily_quest_data["Final"]["Push"]+=5
                daily_quest_data["Final"]["Sit"]+=5
                daily_quest_data["Final"]["Squat"]+=5
                daily_quest_data["Final"]["Run"]+=0.5

                daily_quest_data["Player"]["Push"]=0
                daily_quest_data["Player"]["Sit"]=0
                daily_quest_data["Player"]["Squat"]=0
                daily_quest_data["Player"]["Run"]=0
                daily_quest_data["Player"]["Int_type"]=0
                daily_quest_data["Player"]["Sleep"]=0

                if round(fl_int,1)!=10:
                    daily_quest_data["Final"]["Int_type"]+=0.5
                else:
                    daily_quest_data["Final"]["Int_type"]+=0.5

                with open("Files/Data/Daily_Quest.json", 'w') as final_daily_quest_file:
                    json.dump(daily_quest_data, final_daily_quest_file, indent=4)

                with open("Files/Checks/Daily_time_check.csv", 'w',  newline='') as fin_daily_date_check_file:
                    fw1=csv.writer(fin_daily_date_check_file)
                    fw1.writerow([today_date_str,"DONE"])

                with open("Files\Temp Files\Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                    rew_fw=csv.writer(rew_csv_open)
                    rew_fw.writerow(["Reward"])
            
                subprocess.Popen(['python', 'Anime Version/Daily Quest Rewards/gui.py'])
                
                window.quit()

def dun_check():
    global e_rank
    global d_rank
    global c_rank
    global b_rank
    global a_rank
    global s_rank
    global red_gate

    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_check:
        dun_check_data=json.load(dun_check)

    dun_date=list(dun_check_data.keys())[0]
    date_format = "%Y-%m-%d"

    date_object = datetime.strptime(dun_date, date_format)
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)

    if date_object!=current_date:
        # E Rank Distro
        e_rank_vals=0
        for k in range(5):
            if random.randint(1, 2) == 1:
                e_rank_vals+=1

        # D Rank Distro
        d_rank_vals=0
        for k in range(7):
            if random.randint(1, 3) == 1:
                d_rank_vals+=1

        # C Rank Distro
        c_rank_vals=0
        for k in range(10):
            if random.randint(1, 3) == 1:
                c_rank_vals+=1

        # B Rank Distro
        b_rank_vals=0
        for k in range(10):
            if random.randint(1, 5) == 1:
                b_rank_vals+=1

        # A Rank Distro
        a_rank_vals=0
        for k in range(10):
            if random.randint(1, 10) == 1:
                a_rank_vals+=1

        # S Rank Distro
        s_rank_vals=0
        for k in range(1):
            if random.randint(1, 10) == 1:
                s_rank_vals+=1
        
        # Red Gate Rank Distro
        red_rank_vals=0
        for k in range(10):
            if random.randint(1, 20) == 1:
                red_rank_vals+=1

        dun={current_date_string:{"E":e_rank_vals,"D":d_rank_vals,"C":c_rank_vals,"B":b_rank_vals,"A":a_rank_vals,"S":s_rank_vals, "Red Gate":red_rank_vals}}
        with open("Files\Data\Todays_Dungeon.json", 'w') as wrt_dun_check:
            json.dump(dun, wrt_dun_check, indent=6)
            
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=json.load(dun_full)

        e_rank=dun_full_data[current_date_string]["E"]
        d_rank=dun_full_data[current_date_string]["D"]
        c_rank=dun_full_data[current_date_string]["C"]
        b_rank=dun_full_data[current_date_string]["B"]
        a_rank=dun_full_data[current_date_string]["A"]
        s_rank=dun_full_data[current_date_string]["S"]

        red_gate=dun_full_data[current_date_string]["Red Gate"]

    return [e_rank, d_rank, c_rank, b_rank, a_rank, s_rank]

def dungeon_rank_get(rank,amt1,amt1_check):
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

    return amt1

def get_item_button_image(name, max_width, max_height):
    try:
        # Construct the absolute path to the Images folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to the project root directory
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

            subprocess.Popen(['python', 'Anime Version/Item Data/gui.py'])

            window.quit()
    
    except:
        print()

def get_inventory_button_image(name):
    try:
        # Construct the absolute path to the Images folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to the project root directory
        file_loc = os.path.join(script_dir, "Images")
        files = os.path.join(file_loc, name + ' Small.png')
        if not os.path.exists(files):
            raise FileNotFoundError
    except:
        file_loc = os.path.join(script_dir, "Images")
        files = os.path.join(file_loc, "Unknown.png")
    
    return PhotoImage(file=files)

def equip_item(cat,item_full_data, window):
    if cat in ["HELM", "CHESTPLATE", "FIRST GAUNTLET", "SECOND GAUNTLET", "BOOTS", "COLLAR", "RING"]:
        with open('Files/Equipment.json', 'r') as finale_equip:
            finale_equip_data=json.load(finale_equip)
            finale_equip_data[cat]=item_full_data

        with open('Files/Equipment.json', 'w') as inject:
            json.dump(finale_equip_data, inject, indent=6)

        subprocess.Popen(['python', 'Anime Version/Equipment/gui.py'])
        window.quit()

def return_back_to_tab(loc,window):
    with open('Files/Data/Theme_Check.json', 'r') as themefile:
        theme_data=json.load(themefile)
        theme=theme_data["Theme"]
        fin_loc=f'{theme} Version/{loc}/gui.py'
    subprocess.Popen(['python', 'Anime Version/Inventory/gui.py'])
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

    if closing==True:
        subprocess.Popen(['python', 'Anime Version/Inventory/gui.py'])

        window.quit()

    else:
        subprocess.Popen(['python', 'Anime Version/Item Data/gui.py'])

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
        fout=open('Files/Temp Files/Inventory temp.csv', 'w', newline='')
        fw=csv.writer(fout)
        rec=["Quest Slot Filled"]
        fw.writerow(rec)
        fout.close()
        subprocess.Popen(['python', "Anime Version\Message\gui.py"])

    window.quit()

    subprocess.Popen(['python', 'Anime Version/Quests/gui.py'])

def set_preview_temp(nameob,quantity):
    if nameob!='-' and quantity!=0:
        with open("Files/Temp Files/Preview Item Temp.csv", 'w', newline='') as new_csv_open:
            fw=csv.writer(new_csv_open)
            rec=[nameob, quantity]
            fw.writerow(rec)
        subprocess.Popen(['python', 'Anime Version/Preview Item/gui.py'])

def quest_reward(window,dicts,rank,name):
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

            with open("Files/status.json", 'w') as fson:
                json.dump(data_status, fson, indent=4)
            subprocess.Popen(['python', 'Anime Version/Leveled up/gui.py'])

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

    fout=open('Files/Temp Files/Inventory temp.csv', 'w', newline='')
    fw=csv.writer(fout)
    rec=["Quest Completed"]
    fw.writerow(rec)
    fout.close()
    subprocess.Popen(['python', "Anime Version\Message\gui.py"])
    subprocess.Popen(['python', 'Anime Version/Quests/gui.py'])

    window.quit()

def abandon_quest(name,window):
    with open("Files/Quests/Active_Quests.json", 'r') as fols:
        quests=json.load(fols)

    del quests[name]

    with open("Files/Quests/Active_Quests.json", 'r') as fols:
        json.dump(quests, fols, indent=6)

    subprocess.Popen(['python', 'Anime Version/Quests/gui.py'])

    window.quit()

def get_quest_image(rank,typel):
    if rank!='-' and typel!='-':
        if rank=='D' or rank=='E':
            if typel=="Common":
                return PhotoImage(file=("Anime Version/Quests/assets/frame0/image_5.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=("Anime Version/Quests/assets/frame0/image_6.png"))
            
        elif rank=='C' or rank=='B':
            if typel=="Common":
                return PhotoImage(file=("Anime Version/Quests/assets/frame0/image_8.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=("Anime Version/Quests/assets/frame0/image_9.png"))
            
        elif rank=='A':
            if typel=="Common":
                return PhotoImage(file=("Anime Version/Quests/assets/frame0/image_11.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=("Anime Version/Quests/assets/frame0/image_12.png"))
            
        elif rank=='S':
            if typel=="Common":
                return PhotoImage(file=("Anime Version/Quests/assets/frame0/image_14.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=("Anime Version/Quests/assets/frame0/image_15.png"))
        
        elif rank=='?':
            if typel=='Unknown':
                return PhotoImage(file=("Anime Version/Quests/assets/frame0/image_16.png"))
    else:
        return PhotoImage(file=("Anime Version/Quests/assets/frame0/image_17.png"))

def open_write_quest(name,id,type,window):
    if name!="-":
        with open("Files/Temp Files/Quest Temp.csv", 'w', newline='') as csv_open:
                fw=csv.writer(csv_open)
                rec=[name,id]
                fw.writerow(rec)
        if type=='Learn':
            subprocess.Popen(['python', 'Anime Version/Quest Info/Learn Quest/gui.py'])
        
        elif type=='Common':
            subprocess.Popen(['python', 'Anime Version/Quest Info/Count Quest/gui.py'])

        elif type=='Unknown':
            subprocess.Popen(['python', 'Anime Version/Quest Info/Unknown Quest/gui.py'])

        window.quit()


