
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import csv
import json
import cv2
from PIL import Image, ImageTk
import csv
import random
import threading
import sys
import os
import random

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

initial_height = 0
target_height = 321
window_width = 652

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
    global lastx, lasty
    lastx = event.x_root
    lasty = event.y_root

def move_window(event):
    global lastx, lasty
    deltax = event.x_root - lastx
    deltay = event.y_root - lasty
    x = window.winfo_x() + deltax
    y = window.winfo_y() + deltay
    window.geometry("+%s+%s" % (x, y))
    lastx = event.x_root
    lasty = event.y_root

with open("Files/Demons Castle/Demon_info.csv", "r") as file_opem:
    reader = csv.reader(file_opem)
    for row in reader:
        floor = int(row[0])
        num = int(row[1])

def choose_demon_by_rank(rank_of):
    with open("Files/Demons Castle/Demon_Data.json", "r") as demon_file:
        demons = json.load(demon_file)
    # Filter demons by the given rank
    filtered_demons = [name for name, details in demons.items() if details["rank"] == rank_of]
    if not filtered_demons:
        return f"No demons found for rank {rank_of}."
    # Choose a random demon from the filtered list
    return random.choice(filtered_demons)

# Example usage
floor_rank = thesystem.system.give_ranking(floor)
name = choose_demon_by_rank(floor_rank)
final_boss=False

if floor==25 and num==53:
    name="Cerberus - 25th Floor Boss"
    floor_rank="S"
    soul_count=5

elif floor==50 and num==53:
    name="Vulcan - 50th Floor Boss"
    floor_rank="S"
    soul_count=5

elif floor==75 and num==53:
    name="Metus - 75th Floor Boss"
    floor_rank="S"
    soul_count=5

elif floor==100 and num==55:
    name="Demon Monarch Baaran - 100th Floor Boss"
    floor_rank="S"
    soul_count=5
    final_boss=True

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
        str_quest_main_names=json.load(str_quest_file_name)

    str_quest_main_names_list=list(str_quest_main_names.keys())

    act1=random.choice(str_quest_main_names_list)
    act2=random.choice(str_quest_main_names_list)

    with open("Files/status.json", 'r') as fson:
        data=json.load(fson)
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
    
    amt1=thesystem.system.dungeon_rank_get(floor_rank, amt1, amt1_check)
    amt2=thesystem.system.dungeon_rank_get(floor_rank, amt2, amt2_check)

    full_act1_name='- '+act1+' '+str(amt1)+' '+amtval1
    full_act2_name='- '+act2+' '+str(amt2)+' '+amtval2

    agi_file_name=f"Files\Workout\AGI_based.json"
    with open(agi_file_name, 'r') as agi_quest_file_name:
        agi_quest_main_names=json.load(agi_quest_file_name)

    agi_quest_main_names_list=list(agi_quest_main_names.keys())

    act3=random.choice(agi_quest_main_names_list)
    act4=random.choice(agi_quest_main_names_list)

    if floor_rank!="E" and floor_rank!="D":
        try:
            amt3=agi_quest_main_names[act3][0]["amt"]
            amtval3=agi_quest_main_names[act3][0]["amtval"]
            amt3_check="amt"
        except:
            amt3=agi_quest_main_names[act3][0]["time"]
            amtval3=agi_quest_main_names[act3][0]["timeval"]
            amt3_check="time"
        amt3=thesystem.system.dungeon_rank_get(floor_rank, amt3, amt3_check)
        full_act3_name='- '+act3+' '+str(amt3)+' '+amtval3

    if floor_rank!="E" and floor_rank!="D" and floor_rank!="C" and floor_rank!="B": 
        try:
            amt4=agi_quest_main_names[act4][0]["amt"]
            amtval4=agi_quest_main_names[act4][0]["amtval"]
            amt4_check="amt"
        except:
            amt4=agi_quest_main_names[act4][0]["time"]
            amtval4=agi_quest_main_names[act4][0]["timeval"]
            amt4_check="time"

        amt4=thesystem.system.dungeon_rank_get(floor_rank, amt4, amt4_check)
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
            monster_file_data=json.load(monster_file)
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
    get_act()

def next():
    global mob
    global XP_val
    global rank
    global rew_rank
    global soul_count

    mob+=1

    if mob==2:
        with open("Files/Status.json", 'r') as status_read_file:
            status_read_data=json.load(status_read_file)

        if (floor==25 or floor==50 or floor==75 or floor==100) and (num==53 or num==55):
            XP_val=1000
        else:
            with open("Files/Demons Castle/Demon_Data.json", "r") as demon_file:
                demons = json.load(demon_file)
                XP_val=demons[name]["XP"]
                soul_count=demons[name]["soul"]

        if final_boss==False:
            with open("Files/Demons Castle/image_visibility.json", 'r') as f:
                data = json.load(f)
                data['hidden_images'][str(num)]["Completed"]=True
            with open("Files/Demons Castle/image_visibility.json", 'w') as f:
                json.dump(data, f, indent=4)

        status_read_data["status"][0]['XP']+=XP_val
        with open("Files/Demons Castle/Demon_Castle.json", 'r') as fson_fin:
            findata = json.load(fson_fin)
            findata['XP']+=XP_val
            findata['Souls']+=soul_count
            if final_boss==True:
                findata['Final']=True
        
        with open("Files/Demons Castle/Demon_Castle.json", 'w') as fson_fin:
            json.dump(findata, fson_fin, indent=6)

        with open("Files/status.json", 'w') as fson:
            json.dump(status_read_data, fson, indent=4)

        thesystem.system.get_fin_xp()
        subprocess.Popen(['python', 'Manwha Version/Demon Castle/gui.py'])
        window.quit()

    else:
        subprocess.Popen(['python', 'Files\Mod\default\sfx_glitch.py'])
        mob_fun()


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 321,
    width = 652,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)


with open("Files/Status.json", 'r') as fson:
    data=json.load(fson)
    lvl=data["status"][0]['level']

if lvl<=(int(floor)-10):
    color="#FF2F2F"
elif lvl>=(int(floor)+10):
    color="#ffee2f"
elif lvl>=(int(floor)+20):
    color="#ffffff"
else:
    color="#FFFFFF"


canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    825.0,
    513.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 478.0, 277.0, resize_factor=1.3)


image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    326.0,
    160.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    154.0,
    56.0,
    image=image_image_3
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: next(),
    relief="flat"
)
button_1.place(
    x=483.0,
    y=279.0,
    width=150.0,
    height=22.0
)

canvas.create_text(
    51.0,
    92.0,
    anchor="nw",
    text=f"FLOOR: {floor}",
    fill="#FFD337",
    font=("Exo Bold", 16 * -1)
)

canvas.create_text(
    51.0,
    132.0,
    anchor="nw",
    text="ENEMY NAME:",
    fill="#FFD337",
    font=("Exo Bold", 16 * -1)
)

canvas.create_text(
    176.0,
    132.0,
    anchor="nw",
    text=name,
    fill=color,
    font=("Exo Medium", 16 * -1)
)

canvas.create_text(
    51.0,
    112.0,
    anchor="nw",
    text="[]",
    fill="#FFD337",
    font=("Exo Medium", 14 * -1)
)

activity1=canvas.create_text(
    93.99966430664062,
    171.0,
    anchor="nw",
    text="-Activity 0",
    fill="#FFD337",
    font=("Exo Regular", 14 * -1)
)

activity2=canvas.create_text(
    93.99966430664062,
    191.0,
    anchor="nw",
    text="-Activity 1",
    fill="#FFD337",
    font=("Exo Regular", 14 * -1)
)

activity3=canvas.create_text(
    93.99966430664062,
    211.0,
    anchor="nw",
    text="-Activity 2",
    fill="#FFD337",
    font=("Exo Regular", 14 * -1)
)

activity4=canvas.create_text(
    93.99966430664062,
    231.0,
    anchor="nw",
    text="-Activity 3",
    fill="#FFD337",
    font=("Exo Regular", 14 * -1)
)

canvas.create_text(
    393.0,
    37.0,
    anchor="nw",
    text="Do not stress yourself",
    fill="#FFD337",
    font=("Exo Regular", 12 * -1)
)

canvas.create_text(
    393.0,
    49.0,
    anchor="nw",
    text="and take your time to do this",
    fill="#FFD337",
    font=("Exo Regular", 12 * -1)
)

canvas.create_text(
    393.0,
    37.0,
    anchor="nw",
    text="Time Left:",
    fill="#FFD337",
    font=("Exo Regular", 12 * -1),
    state="hidden"
)

canvas.create_text(
    393.0,
    49.0,
    anchor="nw",
    text="00:00:00",
    fill="#FFD337",
    font=("Exo Bold", 32 * -1),
    state="hidden"
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    326.0,
    10.0,
    image=image_image_4
)

canvas.tag_bind(image_4, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_4, "<B1-Motion>", move_window)

get()

window.resizable(False, False)
window.mainloop()