import time
import ujson
import os
import subprocess
from datetime import datetime, timedelta, date
import thesystem.system

def skill_use(skill_name,cooldown):
    with open("Files/Player Data/Skill tracker.json", "r") as f:
        skill_track_data = ujson.load(f)
    
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
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

                thesystem.system.skill_message(skill_name)

            return True
        else:
            return False
    except:
        skill_track_data[skill_name]={"last_used":formatted, "cooldown":cooldown}
        skill_track_data[skill_name]["last_used"] = formatted
        with open("Files/Player Data/Skill tracker.json", "w") as f:
            ujson.dump(skill_track_data, f, indent=6)

        thesystem.system.skill_message(skill_name)

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
            if skill_use("Rush", (24*60*60)) == True and ("Rush"in skill_data):
                with open("Files/Player Data/Status.json", 'r') as f:
                    status_data = ujson.load(f)

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

