
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ujson
import csv
import subprocess
import random
import cv2
from PIL import Image, ImageTk
import sys
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

initial_height = 0
target_height = 274
window_width = 741

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=20, delay=1)

window.configure(bg = "#FFFFFF")
set_data=thesystem.misc.return_settings()
transp_value=set_data["Settings"]["Transparency"]

window.attributes('-alpha',transp_value)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

def complete():
    with open("Files/Player Data/Ability_Check.json", 'r') as ability_check_file:
        ability_check_file_data=ujson.load(ability_check_file)
    
    with open("Files/Player Data/Ability_Check.json", 'w') as fin_ability_check_file:
        ability_check_file_data["Check"][abi]=0
        ujson.dump(ability_check_file_data, fin_ability_check_file, indent=4)

    with open("Files/Player Data/Job_info.json", 'r') as stat_fson:
        stat_data=ujson.load(stat_fson)

    stat_data["status"][1][abi]+=1
    with open("Files/Player Data/Job_info.json", 'w') as final_stat_fson:
        ujson.dump(stat_data, final_stat_fson, indent=4)
    
    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
        abi_l=abi.lower()

        if abi_l in ["str",'vit','agi']:
            abi_2="str_based"
        elif abi_l in ["int",'per','man']:
            abi_2="int_based"
        data["status"][0][abi_l]+=1
        data["avail_eq"][0][abi_2]-=1

    with open("Files/Player Data/Status.json", 'w') as fin_fson:
        ujson.dump(data, fin_fson, indent=4)
    ex_close(window)

def start_move(event):
    window.lastx, window.lasty = event.widget.winfo_pointerxy()

def move_window(event):
    x_root, y_root = event.widget.winfo_pointerxy()
    deltax, deltay = x_root - window.lastx, y_root - window.lasty

    if deltax != 0 or deltay != 0:  # Update only if there is actual movement
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")
        window.lastx, window.lasty = x_root, y_root


def ex_close(win):
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    subprocess.Popen(['python', 'Manwha Version/Status Tab/gui.py'])
    thesystem.system.animate_window_close(window, target_height, window_width, step=20, delay=1)

with open("Files/Temp Files/Urgent Temp.csv", 'r') as urgent_file:
    fr=csv.reader(urgent_file)
    for k in fr:
        abi=k[0]

desc1=desc2=desc3=''
segments = []
segment_length = 77

file_name=f"Files\Workout\{abi}_based.json"
with open(file_name, 'r') as workout_file:
    workout_file_data=ujson.load(workout_file)
    workout_file_list=list(workout_file_data.keys())

    name=random.choice(workout_file_list)

    desc_full=workout_file_data[name][0]["desc"]

    for i in range(0, len(desc_full), segment_length):
        segments.append(desc_full[i:i+segment_length])

    if len(segments) >= 1:
        desc1 = segments[0]
    if len(segments) >= 2:
        desc2 = segments[1]
    if len(segments) >= 3:
        desc3 = segments[2]
    
    both_check=False
    one_check=False
    time_check=False

    amt1=amt2=''
    amt1_val=amt2_val=''

    if "amt" in workout_file_data[name][0]:
        one_check=True
        amt1=workout_file_data[name][0]["amt"]
        amt1_val=workout_file_data[name][0]["amtval"]
        if "time" in workout_file_data[name][0]:
            both_check=True
            time_check=True
            amt2=workout_file_data[name][0]["time"]
            amt2_val=workout_file_data[name][0]["timeval"]

    if "time" in workout_file_data[name][0]:
        time_check=True
        amt2=workout_file_data[name][0]["time"]
        amt2_val=workout_file_data[name][0]["timeval"]
        if "amt" in workout_file_data[name][0]:
            one_check=True
            both_check=True
            amt1=workout_file_data[name][0]["amt"]
            amt1_val=workout_file_data[name][0]["amtval"]

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 274,
    width = 741,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    685.0,
    504.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
    preloaded_frames=np.load(video_path)
player = thesystem.system.FastVideoPlayer(canvas, preloaded_frames, 360.0, 180.0, resize_factor=0.8)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    370.2817077636719,
    137.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    371.0,
    61.0,
    image=image_image_3
)

canvas.create_text(
    45.0,
    90.0,
    anchor="nw",
    text="Do the below mentioned exercise for as much as it is mentioned within the time-limit ",
    fill="#FFD337",
    font=("Exo Regular", 15 * -1)
)

canvas.create_text(
    45.0,
    109.0,
    anchor="nw",
    text=f"to increase the {abi} ability",
    fill="#FFD337",
    font=("Exo Regular", 15 * -1)
)

canvas.create_text(
    45.0,
    129.0,
    anchor="nw",
    text=f"[{name}]",
    fill="#FFD337",
    font=("Exo Bold", 20 * -1)
)

if one_check==True and both_check==False:
    canvas.create_text(
        45.0,
        158.0,
        anchor="nw",
        text=f"For, {amt1} {amt1_val}",
        fill="#FFD337",
        font=("Exo Regular", 13 * -1)
    )

elif time_check==True and both_check==False:
    canvas.create_text(
        45.0,
        158.0,
        anchor="nw",
        text=f"For, {amt2} {amt2_val}",
        fill="#FFD337",
        font=("Exo Regular", 13 * -1)
    )

elif both_check==True:
    canvas.create_text(
        45.0,
        158.0,
        anchor="nw",
        text=f"For, {amt1} {amt1_val}",
        fill="#FFD337",
        font=("Exo Regular", 13 * -1)
    )

    canvas.create_text(
        45.0+180,
        158.0,
        anchor="nw",
        text=f"For, {amt2} {amt2_val}",
        fill="#FFD337",
        font=("Exo Regular", 13 * -1)
    )

canvas.create_text(
    45.0,
    179.0,
    anchor="nw",
    text=desc1,
    fill="#FFD337",
    font=("Exo Regular", 10 * -1)
)

canvas.create_text(
    45.0,
    193.0,
    anchor="nw",
    text=desc2,
    fill="#FFD337",
    font=("Exo Regular", 10 * -1)
)

canvas.create_text(
    45.0,
    207.0,
    anchor="nw",
    text=desc3,
    fill="#FFD337",
    font=("Exo Regular", 10 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: complete(),
    relief="flat"
)
button_1.place(
    x=584.0,
    y=231.0,
    width=137.0,
    height=19.0
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    370.0,
    2.0,
    image=image_image_4
)

canvas.tag_bind(image_4, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_4, "<B1-Motion>", move_window)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(window),
    relief="flat"
)
button_2.place(
    x=700.0,
    y=19.0,
    width=24.0,
    height=24.0
)
window.resizable(False, False)
window.mainloop()
