
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json
import csv
import subprocess
import cv2
from PIL import Image, ImageTk
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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

def ex_close(win):
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    subprocess.Popen(['python', 'Manwha Version\Equipment\gui.py'])
    thesystem.system.animate_window_close(window, target_height, window_width, step=30, delay=1)

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

window = Tk()

initial_height = 0
target_height = 288
window_width = 555

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)

window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 288,
    width = 555,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

# ! ======================================================================
# ! FILE RETRIEVAL
# ! ======================================================================


name1=name2=name3=name4=name5='-'
rank1=rank2=rank3=rank4=rank5='X'
dat1=dat2=dat3=dat4=dat5={}

with open('Files/Temp Files/Equipment Temp.csv', 'r') as fop:
    fr=csv.reader(fop)
    for k in fr:
        cat=k[0]
        try:
            typ=k[1]
        except:
            print()
    
with open('Files/Inventory.json', 'r') as fout:
    data=json.load(fout)
    rol=list(data.keys())
c = 0
for k in rol:
    if data[k][0]["cat"] == cat:  # Check if the category matches
        if c == 0:
            name1, rank1 = k, data[k][0]["rank"]
            dat1 = {k: data[k]}  # Store only the current item with its name as the key
        elif c == 1:
            name2, rank2 = k, data[k][0]["rank"]
            dat2 = {k: data[k]}
        elif c == 2:
            name3, rank3 = k, data[k][0]["rank"]
            dat3 = {k: data[k]}
        elif c == 3:
            name4, rank4 = k, data[k][0]["rank"]
            dat4 = {k: data[k]}
        elif c == 4:
            name5, rank5 = k, data[k][0]["rank"]
            dat5 = {k: data[k]}
        c += 1


# ! ======================================================================
# ! FILE INJECTION
# ! ======================================================================

def opens(val, name):
    def load_json(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def save_json(file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=6)

    def resolve_buff_name(buff_key):
        buff_map = {
            "AGIbuff": "AGI",
            "STRbuff": "STR",
            "VITbuff": "VIT",
            "INTbuff": "INT",
            "PERbuff": "PER",
            "MANbuff": "MAN",
            "AGIdebuff": "AGI",
            "STRdebuff": "STR",
            "VITdebuff": "VIT",
            "INTdebuff": "INT",
            "PERdebuff": "PER",
            "MANdebuff": "MAN",
        }
        return buff_map.get(buff_key, None)

    def process_item_buffs(item_data, status_data, sign=1):
        buffs = (item_data).get("buff", {})
        debuffs = (item_data).get("debuff", {})
        try:
            for key, value in buffs.items():
                buff_name = resolve_buff_name(key)
                if buff_name:
                    status_data["equipment"][0][buff_name] += sign * value
        except:
                print()
        try:
            for key, value in debuffs.items():
                debuff_name = resolve_buff_name(key)
                if debuff_name:
                    status_data["equipment"][0][debuff_name] -= sign * value
        except:
            print()

    # Load equipment and status files
    equipment_data = load_json('Files/Equipment.json')
    status_data = load_json('Files/status.json')

    # Process the currently equipped item if it exists
    if equipment_data.get(cat):
        current_item_name = list(equipment_data[cat].keys())[0]
        current_item_data = equipment_data[cat][current_item_name]
        process_item_buffs(current_item_data[0], status_data, sign=-1)  # Remove current item buffs

    # Save updated status data after removing old buffs
    save_json('Files/status.json', status_data)

    # Update equipment data with the new item
    if name != '-':
        new_item_data_map = {1: dat1, 2: dat2, 3: dat3, 4: dat4, 5: dat5}
        equipment_data[cat] = (new_item_data_map[val])
        save_json('Files/Equipment.json', equipment_data)


        # Process the new item's buffs
        new_item_name = list(equipment_data[cat].keys())[0]
        new_item_data = equipment_data[cat][new_item_name][0]
        process_item_buffs(new_item_data, status_data, sign=1)  # Add new item buffs

        # Save updated status data after applying new buffs
        save_json('Files/status.json', status_data)

    # Launch the GUI and close the current window
    subprocess.Popen(['python', 'Manwha Version/Equipment/gui.py'])
    window.quit()

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 300.0, 190.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    277.0,
    144.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    119.0,
    70.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    280.0,
    123.0,
    image=image_image_4
)

canvas.create_text(
    68.0,
    112.0,
    anchor="nw",
    text=name1,
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

canvas.create_text(
    391.0,
    112.0,
    anchor="nw",
    text=f"{rank1}-Rank",
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: opens(1, name1),
    relief="flat"
)
button_1.place(
    x=481.0,
    y=111.0,
    width=24.0,
    height=24.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    280.0,
    251.0,
    image=image_image_5
)

canvas.create_text(
    68.0,
    240.0,
    anchor="nw",
    text=name5,
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

canvas.create_text(
    391.0,
    240.0,
    anchor="nw",
    text=f"{rank5}-Rank",
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: opens(5, name5),
    relief="flat"
)
button_2.place(
    x=481.0,
    y=239.0,
    width=24.0,
    height=24.0
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    280.0,
    219.0,
    image=image_image_6
)

canvas.create_text(
    68.0,
    208.0,
    anchor="nw",
    text=name4,
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

canvas.create_text(
    391.0,
    208.0,
    anchor="nw",
    text=f"{rank4}-Rank",
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: opens(4, name4),
    relief="flat"
)
button_3.place(
    x=481.0,
    y=207.0,
    width=24.0,
    height=24.0
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    280.0,
    187.0,
    image=image_image_7
)

canvas.create_text(
    68.0,
    176.0,
    anchor="nw",
    text=name3,
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

canvas.create_text(
    391.0,
    176.0,
    anchor="nw",
    text=f"{rank3}-Rank",
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: opens(3, name3),
    relief="flat"
)
button_4.place(
    x=481.0,
    y=175.0,
    width=24.0,
    height=24.0
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    280.0,
    155.0,
    image=image_image_8
)

canvas.create_text(
    68.0,
    144.0,
    anchor="nw",
    text=name2,
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

canvas.create_text(
    391.0,
    144.0,
    anchor="nw",
    text=f"{rank2}-Rank",
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: opens(2, name2),
    relief="flat"
)
button_5.place(
    x=481.0,
    y=143.0,
    width=24.0,
    height=24.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(window),
    relief="flat"
)
button_6.place(
    x=505.0,
    y=30.0,
    width=21.407020568847656,
    height=20.974361419677734
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    280.0,
    10.0,
    image=image_image_9
)

canvas.tag_bind(image_9, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_9, "<B1-Motion>", move_window)

window.resizable(False, False)
window.mainloop()
