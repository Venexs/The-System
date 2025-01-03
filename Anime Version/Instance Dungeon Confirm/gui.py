
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json
import csv
from datetime import datetime, timedelta
import subprocess
import threading
import pandas as pd
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

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

window = Tk()

initial_height = 0
target_height = 144
window_width = 715

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.make_window_transparent(window)
thesystem.system.animate_window_open(window, target_height, window_width, step=35, delay=1)

window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

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
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=35, delay=1)
    win.quit()

def get_item_name_from_csv():
    # Read the item name from the CSV file
    with open('Files/Data/lowest_rank_item.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            return row['Name']

item_name = get_item_name_from_csv()
with open('Files/Inventory.json', 'r') as file:
    data = json.load(file)

# Find the item and update or remove it
if item_name in data:
    for item in data[item_name]:
        rank=item["rank"]

def update_inventory():
    # Get the item name from the CSV file
    item_name = get_item_name_from_csv()

    # Load the JSON data from the file
    with open('Files/Inventory.json', 'r') as file:
        data = json.load(file)
    
    # Find the item and update or remove it
    if item_name in data:
        for item in data[item_name]:
            if item['qty'] == 1:
                # Remove the item if quantity is 1
                data[item_name].remove(item)
            elif item['qty'] > 1:
                # Decrease quantity by 1 if greater than 1
                item['qty'] -= 1

        # If all instances are removed, delete the item from inventory
        if not data[item_name]:
            del data[item_name]

    # Write the updated data back to inventory.json
    with open('Files/Inventory.json', 'w') as file:
        json.dump(data, file, indent=4)

    rank=item["rank"]
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=json.load(dun_full)

    with open("Files\Data\Dungeon_Rank.csv", 'w', newline='') as rank_file:
        fw=csv.writer(rank_file)
        fw.writerow([rank,"Instance"])

    with open("Files\Data\Todays_Dungeon.json", 'w') as final_dun_full:
        json.dump(dun_full_data, final_dun_full, indent=6)

    subprocess.Popen(['python', 'Anime Version/Dungeon Runs/gui.py'])
    window.quit()

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 144,
    width = 715,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    448.0,
    277.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    normal_font_col=pres_file_data["Anime"]["Normal Font Color"]
    video_path=pres_file_data["Anime"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 478.0, 330.0, resize_factor=0.8)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    357.0,
    78.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    363.0,
    56.0,
    image=image_image_3
)

canvas.create_text(
    264.0,
    71.0,
    anchor="nw",
    text=f"{rank}-Rank Instance Dungeon",
    fill="#45EF2A",
    font=("Montserrat Regular", 15 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: update_inventory(),
    relief="flat"
)
button_1.place(
    x=212.0,
    y=95.0,
    width=68.0,
    height=17.0
)

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
    x=445.0,
    y=95.0,
    width=68.0,
    height=17.0
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    47.0,
    72.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    677.0,
    71.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    366.0,
    13.0,
    image=image_image_6
)

canvas.tag_bind(image_6, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_6, "<B1-Motion>", move_window)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    355.0,
    130.0,
    image=image_image_7
)
window.resizable(False, False)
window.mainloop()
