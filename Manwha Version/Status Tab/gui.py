
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import threading
import ujson
import json
import csv
import subprocess
import time
import cv2
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import pandas as pd
import sys
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

with open("Files/Player Data/Tabs.json",'r') as tab_son:
    tab_son_data=ujson.load(tab_son)

with open("Files/Player Data/Tabs.json",'w') as fin_tab_son:
    tab_son_data["Status"]='Open'
    ujson.dump(tab_son_data,fin_tab_son,indent=4)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

initial_height = 0
target_height = 520
window_width = 355

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=40, delay=1)

subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])
window.configure(bg = "#FFFFFF")
set_data=thesystem.misc.return_settings()
transp_value=set_data["Settings"]["Transparency"]

window.attributes('-alpha',transp_value)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

def start_move(event):
    window.lastx, window.lasty = event.widget.winfo_pointerxy()

def move_window(event):
    x_root, y_root = event.widget.winfo_pointerxy()
    deltax, deltay = x_root - window.lastx, y_root - window.lasty

    if deltax != 0 or deltay != 0:  # Update only if there is actual movement
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")
        window.lastx, window.lasty = x_root, y_root


def ex_close(eve):
    with open("Files/Player Data/Tabs.json",'r') as tab_son:
        tab_son_data=ujson.load(tab_son)
    with open("Files/Player Data/Tabs.json",'w') as fin_tab_son:
        tab_son_data["Status"]='Close'
        ujson.dump(tab_son_data,fin_tab_son,indent=4)

    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    stop_update_thread_func()
    thesystem.system.animate_window_close(window, initial_height, window_width, step=20, delay=1)

def title_chng(event):
    subprocess.Popen(['python', 'Manwha Version/Equip Title/gui.py'])

    ex_close(0)

def title_color(name):
    if name=="False Ranker":
        color="#FF2F2F"
    elif name=="One Above All":
        color="#FFCF26"
    else:
        color="#FFFFFF"

    return color

def load_fatigue_value():
    with open('Files/Player Data/Status.json', 'r') as file:
        data = json.load(file)
        fatigue = data["status"][0].get("fatigue", 0)
        fatigue_max = data["status"][0].get("fatigue_max", 1)  # Avoid division by zero
        # Calculate fatigue percentage
        fatigue_percent = int((fatigue / fatigue_max) * 100)
        return fatigue_percent

update_thread = None
stop_update_thread = False

# Function to update fatigue text in a separate thread
def update_fatigue_text(canvas, fatigue_val):
    global stop_update_thread
    previous_fatigue_percent = None

    while not stop_update_thread:
        current_fatigue_percent = load_fatigue_value()
        if current_fatigue_percent != previous_fatigue_percent:
            canvas.itemconfig(fatigue_val, text=f"{current_fatigue_percent}%")
            previous_fatigue_percent = current_fatigue_percent

        # Break sleep into smaller intervals to check stop signal
        for _ in range(180):  # 180 seconds = 3 minutes
            if stop_update_thread:
                return
            time.sleep(1)

# Function to start the update thread
def start_update_thread(canvas, fatigue_val):
    global update_thread, stop_update_thread
    if update_thread and update_thread.is_alive():
        return
    stop_update_thread = False
    update_thread = threading.Thread(target=update_fatigue_text, args=(canvas, fatigue_val), daemon=True)
    update_thread.start()

# Function to stop the update thread
def stop_update_thread_func():
    global stop_update_thread
    stop_update_thread = True
    if update_thread and update_thread.is_alive():
        update_thread.join()  # Wait for thread to finish

def start_job(event):
    with open("Files/Player Data/Job_info.json", 'r') as stat_fson:
        data=ujson.load(stat_fson)

    canvas.itemconfig("Job", state="hidden")
    data["status"][0]["job_active"]='True'

    data["status"][1]["plSTR"]=int(stre)
    data["status"][1]["plINT"]=int(intel)
    data["status"][1]["plAGI"]=int(agi)
    data["status"][1]["plVIT"]=int(vit)
    data["status"][1]["plPER"]=int(per)
    data["status"][1]["plMAN"]=int(man)

    with open("Files/Temp Files/Job_Change Date.csv", 'w', newline='') as time_open_csv_file:
        fw=csv.writer(time_open_csv_file)
        current_date = datetime.now()
        # Add 10 days to the current date
        future_date = current_date + timedelta(days=2)
        # Define the desired format for the date string
        date_format = "%Y-%m-%d"
        # Convert the future date to a string
        future_date_string = future_date.strftime(date_format)
        fw.writerow([future_date_string])

    with open("Files/Player Data/Job_info.json", 'w') as fson:
        ujson.dump(data, fson, indent=4)

def fatigue_window():
    subprocess.Popen(['python', 'Files/Mod/default/sfx_button.py'])
    subprocess.Popen(['python', 'Manwha Version/Fatigue/gui.py'])

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 520,
    width = 355,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    478.0,
    413.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
    preloaded_frames=np.load(video_path)
player = thesystem.system.FastVideoPlayer(canvas, preloaded_frames, 200.0, 180.0, resize_factor=1.2)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    176.5,
    260.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    61.0,
    34.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    176.0,
    303.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    176.0,
    178.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    748.0,
    80.0,
    image=image_image_6
)

# ? =====================================================================
# ? =====================================================================

with open("Files/Player Data/Status.json", 'r') as fson:
    data=ujson.load(fson)
    name=data["status"][0]['name'].upper()
    # ? =================================================
    hp=data["status"][0]['hp']
    mp=data["status"][0]['mp']
    lvl=data["status"][0]['level']
    old_lvl=f"{lvl:02d}"
    # ? =================================================
    stre=data["status"][0]['str']
    stre=thesystem.system.three_val(stre)

    intel=data["status"][0]['int']
    intel=thesystem.system.three_val(intel)

    agi=data["status"][0]['agi']
    agi=thesystem.system.three_val(agi)

    vit=data["status"][0]['vit']
    vit=thesystem.system.three_val(vit)

    per=data["status"][0]['per']
    per=thesystem.system.three_val(per)

    man=data["status"][0]['man']
    man=thesystem.system.three_val(man)
    # ? =================================================
    tit=data["status"][1]['title']
    job=data["status"][1]['job'].upper()
    # ? =================================================
    xp_str=data["status"][0]['XP']
    coins=data["status"][0]['coins']

    fatigue_max=data["status"][0]['fatigue_max']
    fatigue=data["status"][0]['fatigue']

    fat_val=(fatigue/fatigue_max)*100
    # ? =================================================
    av_str_based=data["avail_eq"][0]['str_based']
    av_str_based=thesystem.system.three_val(av_str_based)
    av_int_based=data["avail_eq"][0]['int_based']
    av_int_based=thesystem.system.three_val(av_int_based)
    # ? =================================================
    str_buff=data["equipment"][0]["STR"]
    str_buff=thesystem.system.sign(str_buff)+thesystem.system.pos_fix(thesystem.system.equipment_value_plus(str_buff))

    agi_buff=data["equipment"][0]["AGI"]
    agi_buff=thesystem.system.sign(agi_buff)+thesystem.system.pos_fix(thesystem.system.equipment_value_plus(agi_buff))

    vit_buff=data["equipment"][0]["VIT"]
    vit_buff=thesystem.system.sign(vit_buff)+thesystem.system.pos_fix(thesystem.system.equipment_value_plus(vit_buff))

    int_buff=data["equipment"][0]["INT"]
    int_buff=thesystem.system.sign(int_buff)+thesystem.system.pos_fix(thesystem.system.equipment_value_plus(int_buff))

    per_buff=data["equipment"][0]["PER"]
    per_buff=thesystem.system.sign(per_buff)+thesystem.system.pos_fix(thesystem.system.equipment_value_plus(per_buff))

    man_buff=data["equipment"][0]["MAN"]
    man_buff=thesystem.system.sign(man_buff)+thesystem.system.pos_fix(thesystem.system.equipment_value_plus(man_buff))
    # ? =================================================

# ? =====================================================================
fin_list = thesystem.system.get_fin_xp()

re_check = fin_list[0]
fin_xp=round(fin_list[1], 2)

if re_check==True:
    try:
        subprocess.Popen(["python", "Manwha Version/Status Tab/gui.py"])
        
        ex_close(0)
    except:
        print()
# ? =====================================================================


def update_stat(stat_name): 
    with open("Files/Player Data/Ability_Check.json", 'r') as ability_check_file:
        ability_check_file_data=ujson.load(ability_check_file)
        val=ability_check_file_data["Check"][stat_name.upper()]
    available_points = data["avail_eq"][0]["str_based"] if stat_name in ["str", "agi", "vit"] else data["avail_eq"][0]["int_based"]
    if val<8 and available_points > 0:
            de_update_str() if stat_name in ["str", "agi", "vit"] else de_update_int()
            data["status"][0][stat_name] += 1
            val=data["status"][0][stat_name]
            canvas.itemconfig(stat_text_widgets[stat_name], text=f"{val:03d}")
            subprocess.Popen(['python', 'Files/Mod/default/sfx_point.py'])
            data["avail_eq"][0]["str_based" if stat_name in ["str", "agi", "vit"] else "int_based"] -= 1
            if stat_name=='vit':
                data["status"][0]["fatigue_max"]+=20
            elif stat_name=='int':
                data["status"][0]["mp"]+=5
            with open("Files/Player Data/Status.json", 'w') as fson:
                ujson.dump(data, fson, indent=6)
            with open("Files/Player Data/Ability_Check.json", 'w') as fin_ability_check_file:
                ability_check_file_data["Check"][stat_name.upper()]+=1
                ujson.dump(ability_check_file_data, fin_ability_check_file, indent=4)
            #if stat_name=='vit':
                #update_fatigue_text(canvas,fatigue_val)
    elif val>=8 and available_points > 0:
        with open("Files/Temp Files/Urgent Temp.csv", 'w', newline='') as urgent_file:
            fr=csv.writer(urgent_file)
            fr.writerow([stat_name.upper()])
        subprocess.Popen(['python', 'Manwha Version/Urgent Quest/gui.py'])
        ex_close(0)

# / =================================================
# / =================================================

def de_update_str():
    global av_str_based
    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
        check_value=data["avail_eq"][0]['str_based']
    if check_value>0:
        global av_str_based_txt
        current_number = int(check_value)
        new_number = current_number - 1
        new_text = f"{new_number:03d}"
        canvas.itemconfig(av_str_based_txt, text=new_text)
        av_str_based=new_number

def de_update_int():
    global av_int_based
    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
        check_value=data["avail_eq"][0]['int_based']
    if check_value>0:
        global av_int_based_txt
        current_number = int(check_value)
        new_number = current_number - 1
        new_text = f"{new_number:03d}"
        canvas.itemconfig(av_int_based_txt, text=new_text)
        av_int_based=new_number
# / =================================================
# / =================================================

str_txt=canvas.create_text(
    49.0,
    219.0,
    anchor="nw",
    text=stre,
    fill="#FFD337",
    font=("Exo SemiBold", 20 * -1)
)

canvas.create_text(
    92.0,
    222.0+2,
    anchor="nw",
    text=f"({str_buff})",
    fill="#FFE819",
    font=("Exo Regular", 13 * -1)
)

int_txt=canvas.create_text(
    47.0,
    273.0,
    anchor="nw",
    text=intel,
    fill="#FFD337",
    font=("Exo SemiBold", 20 * -1)
)

canvas.create_text(
    90.0,
    276.0+2,
    anchor="nw",
    text=f"({int_buff})",
    fill="#FFE819",
    font=("Exo Regular", 13 * -1)
)

agi_txt=canvas.create_text(
    47.0,
    325.0,
    anchor="nw",
    text=agi,
    fill="#FFD337",
    font=("Exo SemiBold", 20 * -1)
)

canvas.create_text(
    90.0,
    328.0+2,
    anchor="nw",
    text=f"({agi_buff})",
    fill="#FFE819",
    font=("Exo Regular", 13 * -1)
)

vit_txt=canvas.create_text(
    227.0,
    219.0,
    anchor="nw",
    text=vit,
    fill="#FFD337",
    font=("Exo SemiBold", 20 * -1)
)

canvas.create_text(
    268.0,
    222.0+2,
    anchor="nw",
    text=f"({vit_buff})",
    fill="#FFE819",
    font=("Exo Regular", 13 * -1)
)

per_txt=canvas.create_text(
    234.0,
    271.0,
    anchor="nw",
    text=per,
    fill="#FFD337",
    font=("Exo SemiBold", 20 * -1)
)

canvas.create_text(
    275.0,
    274.0+2,
    anchor="nw",
    text=f"({per_buff})",
    fill="#FFE819",
    font=("Exo Regular", 13 * -1)
)

man_txt=canvas.create_text(
    240.0,
    327.0,
    anchor="nw",
    text=man,
    fill="#FFD337",
    font=("Exo SemiBold", 20 * -1)
)

canvas.create_text(
    282.0,
    329.0+2 ,
    anchor="nw",
    text=f"({man_buff})",
    fill="#FFE819",
    font=("Exo Regular", 13 * -1)
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    31.0,
    231.0+2,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    29.0,
    285.0+2,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    30.0,
    337.0+2,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    211.0,
    231.0+2,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    215.0,
    283.0+2,
    image=image_image_11
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    218.0,
    339.0+2,
    image=image_image_12
)

# // ====================================================================

image_image_33 = PhotoImage(
    file=relative_to_assets("button_1.png"))
image_33 = canvas.create_image(
    142.0,
    222.0+10,
    image=image_image_33
)

canvas.tag_bind(image_33, "<ButtonPress-1>", lambda e: update_stat("str"))

# // ====================================================================

image_image_44 = PhotoImage(
    file=relative_to_assets("button_1.png"))
image_44 = canvas.create_image(
    142.0,
    276.0+10,
    image=image_image_44
)

canvas.tag_bind(image_44, "<ButtonPress-1>", lambda e: update_stat("int"))

# // ====================================================================

image_image_55 = PhotoImage(
    file=relative_to_assets("button_1.png"))
image_55 = canvas.create_image(
    142.0,
    328.0+10,
    image=image_image_55
)

canvas.tag_bind(image_55, "<ButtonPress-1>", lambda e: update_stat("agi"))

# // ====================================================================

image_image_66 = PhotoImage(
    file=relative_to_assets("button_1.png"))
image_66 = canvas.create_image(
    325.0,
    219.0+15,
    image=image_image_66
)

canvas.tag_bind(image_66, "<ButtonPress-1>", lambda e: update_stat("vit"))

# // ====================================================================

image_image_77 = PhotoImage(
    file=relative_to_assets("button_1.png"))
image_77 = canvas.create_image(
    325.0,
    271.0+15,
    image=image_image_77
)

canvas.tag_bind(image_77, "<ButtonPress-1>", lambda e: update_stat("per"))

# // ====================================================================

image_image_88 = PhotoImage(
    file=relative_to_assets("button_1.png"))
image_88 = canvas.create_image(
    325.0,
    327.0+15,
    image=image_image_88
)

canvas.tag_bind(image_88, "<ButtonPress-1>", lambda e: update_stat("man"))


# // ====================================================================

gap = 20

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    41.0-gap,
    176.5,
    image=image_image_13
)

canvas.create_text(
    60.0-gap,
    163.0,
    anchor="nw",
    text=hp,
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    136.0-gap,
    176.5,
    image=image_image_14
)

canvas.create_text(
    154.0-gap,
    164.0,
    anchor="nw",
    text=mp,
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    256.0-gap,
    176.5,
    image=image_image_15
)

fat_val = load_fatigue_value()
fatigue_val = canvas.create_text(
    297.0-gap,
    163.0,
    anchor="nw",
    text=f"{int(fat_val)}%",
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

image_image_16 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(
    118.0,
    381.0,
    image=image_image_16
)

canvas.create_text(
    219.0,
    371.0-3,
    anchor="nw",
    text=fin_xp,
    fill="#FFD337",
    font=("Exo Medium", 16 * -1)
)

canvas.create_text(
    279.0,
    69.0,
    anchor="nw",
    text=f"Lv.{old_lvl}",
    fill="#FFD337",
    font=("Exo Regular", 16 * -1)
)

canvas.create_text(
    27.0,
    92.0,
    anchor="nw",
    text="JOB:",
    fill="#FFD337",
    font=("Exo Regular", 15 * -1)
)

canvas.create_text(
    27.0,
    114.0,
    anchor="nw",
    text="TITLE:",
    fill="#FFD337",
    font=("Exo Regular", 15 * -1)
)

canvas.create_text(
    60.0,
    92.0,
    anchor="nw",
    text=job.upper(),
    fill="#FFD337",
    font=("Exo Bold", 15 * -1)
)

canvas.create_text(
    72.0,
    114.0,
    anchor="nw",
    text=tit.upper(),
    fill=title_color(tit),
    font=("Exo Bold", 15 * -1)
)

canvas.create_text(
    27.0,
    70.0,
    anchor="nw",
    text="NAME:",
    fill="#FFD337",
    font=("Exo Regular", 15 * -1)
)

canvas.create_text(
    76.0,
    70.0,
    anchor="nw",
    text=name,
    fill="#FFD337",
    font=("Exo Bold", 15 * -1)
)

av_int_based_txt=canvas.create_text(
    279.0,
    470.0,
    anchor="nw",
    text=av_int_based,
    fill="#FFD337",
    font=("Exo Bold", 24 * -1)
)

image_image_17 = PhotoImage(
    file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(
    210.0,
    485.0,
    image=image_image_17
)

av_str_based_txt=canvas.create_text(
    279.0,
    414.0,
    anchor="nw",
    text=av_str_based,
    fill="#FFD337",
    font=("Exo Bold", 24 * -1)
)

image_image_18 = PhotoImage(
    file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(
    210.0,
    435.0,
    image=image_image_18
)

stat_text_widgets={"str":str_txt, "int":int_txt, "agi":agi_txt, "vit":vit_txt, "per":per_txt, "man":man_txt}

image_image_19 = PhotoImage(
    file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(
    177.0,
    .0,
    image=image_image_19
)

canvas.tag_bind(image_19, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_19, "<B1-Motion>", move_window)

image_image_20 = PhotoImage(
    file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(
    338.0,
    19.0,
    image=image_image_20
)

canvas.tag_bind(image_20, "<ButtonPress-1>", ex_close)

image_image_21 = PhotoImage(
    file=relative_to_assets("image_21.png"))
image_21 = canvas.create_image(
    246.0,
    124.0,
    image=image_image_21
)

canvas.tag_bind(image_21, "<ButtonPress-1>", title_chng)

image_image_22 = PhotoImage(
    file=relative_to_assets("image_24_1.png"))
image_22 = canvas.create_image(
    246.0,
    102.0,
    image=image_image_22,
    tags='Job',
    state='normal'
)

canvas.tag_bind(image_22, "<ButtonPress-1>", start_job)

with open("Files/Player Data/Job_info.json", 'r') as stat_fson:
    stat_data=ujson.load(stat_fson)

if stat_data["status"][0]["job_active"]=='False' and lvl>=40:
    canvas.itemconfig("Job", state="normal")
else:
    canvas.itemconfig("Job", state="hidden")

image_image_23 = PhotoImage(
    file=relative_to_assets("image_23.png"))
image_23 = canvas.create_image(
    115.0,
    34.0,
    image=image_image_23
)

canvas.tag_bind(image_23, "<ButtonPress-1>", lambda event: thesystem.system.info_open("ABI Points"))

image_image_25 = PhotoImage(
    file=relative_to_assets("image_25.png"))
image_25 = canvas.create_image(
    337.0,
    174.0,
    image=image_image_25
)

canvas.tag_bind(image_25, "<ButtonPress-1>", lambda event: fatigue_window())

start_update_thread(canvas, fatigue_val)
window.resizable(False, False)
window.mainloop()
