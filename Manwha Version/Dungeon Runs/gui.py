
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
from datetime import datetime, timedelta
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.dungeon
import thesystem.system

subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

initial_height = 0
target_height = 369
window_width = 697

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.make_window_transparent(window)
thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)

window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)


waves={}
XP_val=0
mob=1
rew_rank='X'

def start_move(event):
    window.lastx, window.lasty = event.widget.winfo_pointerxy()

def move_window(event):
    x_root, y_root = event.widget.winfo_pointerxy()
    deltax, deltay = x_root - window.lastx, y_root - window.lasty

    if deltax != 0 or deltay != 0:  # Update only if there is actual movement
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")
        window.lastx, window.lasty = x_root, y_root


def ex_close(win):
    win.quit()

def get_act():
    global activity1
    global activity2
    global activity3
    global activity4
    
    amt1=amt2=amt3=amt4=''
    full_act4_name=full_act3_name=full_act2_name=full_act1_name=''

    # Activities
    str_file_name=f"Files\Workout\STR_based.json"
    with open(str_file_name, 'r') as str_quest_file_name:
        str_quest_main_names=ujson.load(str_quest_file_name)

    str_quest_main_names_list=list(str_quest_main_names.keys())

    act1=random.choice(str_quest_main_names_list)
    act2=random.choice(str_quest_main_names_list)

    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
        lvl=data["status"][0]['level']

    try:
        amt1=str_quest_main_names[act1][0]["amt"]
        amtval1=str_quest_main_names[act1][0]["amtval"]
        amt1_check="amt"
    except:
        amt1=str_quest_main_names[act1][0]["time"]
        amtval1=str_quest_main_names[act1][0]["timeval"]
        amt1_check="time"
    
    try:
        amt2=str_quest_main_names[act2][0]["amt"]
        amtval2=str_quest_main_names[act2][0]["amtval"]
        amt2_check="amt"
    except:
        amt2=str_quest_main_names[act2][0]["time"]
        amtval2=str_quest_main_names[act2][0]["timeval"]
        amt2_check="time"
    
    amt1=thesystem.dungeon.dungeon_rank_get(rank, amt1, amt1_check, act1)
    amt2=thesystem.dungeon.dungeon_rank_get(rank, amt2, amt2_check, act2)

    full_act1_name='- '+act1+' '+str(amt1)+' '+amtval1
    full_act2_name='- '+act2+' '+str(amt2)+' '+amtval2

    agi_file_name=f"Files\Workout\AGI_based.json"
    with open(agi_file_name, 'r') as agi_quest_file_name:
        agi_quest_main_names=ujson.load(agi_quest_file_name)

    agi_quest_main_names_list=list(agi_quest_main_names.keys())

    act3=random.choice(agi_quest_main_names_list)
    act4=random.choice(agi_quest_main_names_list)

    if thesystem.system.give_ranking(lvl)!="E" and thesystem.system.give_ranking(lvl)!="D":
        try:
            amt3=agi_quest_main_names[act3][0]["amt"]
            amtval3=agi_quest_main_names[act3][0]["amtval"]
            amt3_check="amt"
        except:
            amt3=agi_quest_main_names[act3][0]["time"]
            amtval3=agi_quest_main_names[act3][0]["timeval"]
            amt3_check="time"
        amt3=thesystem.dungeon.dungeon_rank_get(rank, amt3, amt3_check, act3)
        full_act3_name='- '+act3+' '+str(amt3)+' '+amtval3

    if thesystem.system.give_ranking(lvl)!="E" and thesystem.system.give_ranking(lvl)!="D" and thesystem.system.give_ranking(lvl)!="C" and thesystem.system.give_ranking(lvl)!="B": 
        try:
            amt4=agi_quest_main_names[act4][0]["amt"]
            amtval4=agi_quest_main_names[act4][0]["amtval"]
            amt4_check="amt"
        except:
            amt4=agi_quest_main_names[act4][0]["time"]
            amtval4=agi_quest_main_names[act4][0]["timeval"]
            amt4_check="time"

        amt4=thesystem.dungeon.dungeon_rank_get(rank, amt4, amt4_check, act4)
        full_act4_name='- '+act4+' '+str(amt4)+' '+amtval4

    canvas.itemconfig(activity1, text=full_act1_name)
    canvas.itemconfig(activity2, text=full_act2_name)
    canvas.itemconfig(activity3, text=full_act3_name)
    canvas.itemconfig(activity4, text=full_act4_name)

def get():
    global waves
    global XP_val
    global rank
    global rew_rank
    global mob
    global type_of_dun

    with open("Files\Data\Dungeon_Rank.csv", 'r') as rank_file:
        rank_file_reader=csv.reader(rank_file)
        for k in rank_file_reader:
            rank=k[0]
            type_of_dun=k[1]
            rew_rank=rank

    if rank!="Red":

        if mob==3:
            if rank=='E':rank='D'
            elif rank=='D':rank='C'
            elif rank=='C':rank='B'
            elif rank=='B':rank='A'
            elif rank=='A':rank='S'
        
        # Waves
        with open("Files\Data\Dungeon_Boss_List.json", 'r') as monster_file:
            monster_file_data=ujson.load(monster_file)
            monster_names=list(monster_file_data.keys())

            waves={}
            monsters={}
            bosses={}
            for k in monster_names:
                if monster_file_data[k]["rank"]==rank and monster_file_data[k]["type"]=='Normal':
                    monsters[k]=monster_file_data[k]

            mob1=random.choice(list(monsters.keys()))
            mob2=random.choice(list(monsters.keys()))

            waves['1']={mob1:monster_file_data[mob1]}
            waves['2']={mob1:monster_file_data[mob2]}

            XP_val+=monster_file_data[mob1]['XP']
            XP_val+=monster_file_data[mob2]['XP']

            if rank=='E': boss_rank='D'
            elif rank=='D': boss_rank='C'
            elif rank=='C': boss_rank='B'
            elif rank=='B': boss_rank='A'
            elif rank=='A': boss_rank='S'
            elif rank=='S': boss_rank='S'

            for k in monster_names:
                if monster_file_data[k]["rank"]==boss_rank and monster_file_data[k]["type"]=='Boss':
                    bosses[k]=monster_file_data[k]

            boss=random.choice(list(bosses.keys()))

            waves['Final']={boss:monster_file_data[boss]}
            XP_val+=monster_file_data[boss]['XP']

            get_act()
            mob_fun()

def mob_fun():
    global mob

    mob_num=str(mob)
    if rank!='Red' and mob_num=='3':
        name=list(waves["Final"])[0]
        mob_num_fin="Final"
    else:
        name=list(waves[mob_num])[0]
        mob_num_fin=mob_num

    if waves[mob_num_fin][name]['swarm']=='Yes':
        group="Group"
    else:
        group="Swarm"
    wave_text=f"[Wave - {mob_num_fin}]"
    group_txt=f"A {group} of {name} has appeared in front of you. "
    canvas.itemconfig(waves_txt, text=wave_text)
    canvas.itemconfig(enemy, text=group_txt)
    get_act()

def next():
    global mob
    global XP_val
    global rank
    global rew_rank

    mob+=1

    if mob==4:
        with open("Files/Player Data/Status.json", 'r') as status_read_file:
            status_read_data=ujson.load(status_read_file)

        if rew_rank=='E':
            coin=100
            avp=1
        elif rew_rank=='D':
            coin=500
            avp=2
        elif rew_rank=='C':
            coin=1000
            avp=3
        elif rew_rank=='B':
            coin=5000
            avp=4
        elif rew_rank=='A':
            coin=10000
            avp=5
        elif rew_rank=='S':
            coin=20000
            avp=6

        if type_of_dun=='Normal':
            status_read_data["avail_eq"][0]['str_based']+=avp
            status_read_data["avail_eq"][0]['int_based']+=avp
            status_read_data["status"][0]['XP']+=XP_val
            status_read_data["status"][0]['coins']+=coin
            with open("Files/Player Data/Status.json", 'w') as fson:
                ujson.dump(status_read_data, fson, indent=4)

            with open("Files/Checks/Message.csv", 'w', newline='') as check_file:
                check_fw = csv.writer(check_file)
                check_fw.writerow(["Quest Completed"])

        elif type_of_dun=='Instance':
            status_read_data["status"][0]['XP']+=(XP_val*2)
            status_read_data["status"][0]['coins']+=(coin*2)
            status_read_data["avail_eq"][0]['str_based']+=(avp*2)
            status_read_data["avail_eq"][0]['int_based']+=(avp*2)
            with open("Files/Player Data/Status.json", 'w') as fson:
                ujson.dump(status_read_data, fson, indent=4)

            with open("Files/Checks/Message.csv", 'w', newline='') as check_file:
                check_fw = csv.writer(check_file)
                check_fw.writerow(["Instance Reward"])

        thesystem.system.get_fin_xp()
        subprocess.Popen(['python', 'Manwha Version/Message/gui.py'])
        window.quit()

    else:
        subprocess.Popen(['python', 'Files\Mod\default\sfx_glitch.py'])
        mob_fun()

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 369,
    width = 697,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    574.0,
    539.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 300.0, 240.0, resize_factor=1)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    348.1684875488281,
    184.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    177.0,
    54.0,
    image=image_image_3
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(window),
    relief="flat"
)
button_1.place(
    x=534.0,
    y=308.0,
    width=127.0,
    height=22.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: next(),
    relief="flat"
)
button_2.place(
    x=511.0,
    y=277.0,
    width=150.0,
    height=22.0
)

with open("Files\Data\Dungeon_Rank.csv", 'r') as rank_file:
    rank_file_reader=csv.reader(rank_file)
    for k in rank_file_reader:
        rank=k[0]
        type_of_dun=k[1]

canvas.create_text(
    40.0,
    74.0,
    anchor="nw",
    text=f"{rank}-Rank │ {type_of_dun} Dungeon",
    fill="#FFD337",
    font=("Exo Bold", 15 * -1)
)

waves_txt=canvas.create_text(
    40.0,
    110.0,
    anchor="nw",
    text="[Wave - XX]",
    fill="#FFD337",
    font=("Exo Medium", 15 * -1)
)

enemy=canvas.create_text(
    82.0,
    145.0,
    anchor="nw",
    text="A [group] of [Normal Enemy-1] has appeared in front of you. ",
    fill="#FFD337",
    font=("Exo Medium", 15 * -1)
)

canvas.create_text(
    82.0,
    165.0,
    anchor="nw",
    text="Do the activities below to generate enough [STR/AGI] to defeat them",
    fill="#FFD337",
    font=("Exo Medium", 15 * -1)
)

activity1=canvas.create_text(
    102.0,
    197.0,
    anchor="nw",
    text="-Activity 0",
    fill="#FFD337",
    font=("Exo Regular", 15 * -1)
)

activity2=canvas.create_text(
    102.0,
    217.0,
    anchor="nw",
    text="-Activity 1",
    fill="#FFD337",
    font=("Exo Regular", 15 * -1)
)

activity3=canvas.create_text(
    102.0,
    237.0,
    anchor="nw",
    text="-Activity 2",
    fill="#FFD337",
    font=("Exo Regular", 15 * -1)
)

activity4=canvas.create_text(
    102.0,
    257.0,
    anchor="nw",
    text="-Activity 3",
    fill="#FFD337",
    font=("Exo Regular", 15 * -1)
)

canvas.create_text(
    521.0,
    49.0,
    anchor="nw",
    text="Time Left:",
    fill="#FFD337",
    font=("Exo Regular", 12 * -1),
    tags="red time",
    state="hidden"
)

canvas.create_text(
    521.0,
    61.0,
    anchor="nw",
    text="00:00:00",
    fill="#FFD337",
    font=("Exo Bold", 32 * -1),
    tags="red time",
    state="hidden"
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    347.0,
    10.0,
    image=image_image_4
)

canvas.tag_bind(image_4, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_4, "<B1-Motion>", move_window)

get()

window.resizable(False, False)
window.mainloop()
