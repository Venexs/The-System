from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json
import csv
import subprocess
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import threading
import time
import sys
import random

def fin_pen():
    today = datetime.now().date()

    yesterday = today - timedelta(days=1)
    with open('Files/Checks/Today_Quest.csv', 'r', newline='') as fout:
        fr=csv.reader(fout)
        for k in fr:
            status=k[1]
            date=k[0]

    p_date=datetime.strptime(date, "%Y-%m-%d").date()
    if yesterday!=p_date and status=="UNDONE":
        subprocess.Popen(['python', 'Anime Version/Penalty Quest/build/gui.py'])
    elif yesterday!=p_date or status=="UNDONE":
        subprocess.Popen(['python', 'Anime Version/Penalty Quest/build/gui.py'])

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

    if first_run_file_check==True:
        stp_eve.set()

        # Wait for the thread to finish
        thrd.join()

        subprocess.Popen(['python', 'First/Check/build/gui.py'])

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
