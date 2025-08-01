
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ujson
import csv
from datetime import datetime, timedelta
import subprocess
import threading
import pandas as pd
import sys
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system
import thesystem.dungeon

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])

window = Tk()

initial_height = 0
target_height = 125
window_width = 380

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.make_window_transparent(window)
thesystem.system.animate_window_open(window, target_height, window_width, step=35, delay=1)

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


def ex_close(win):
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=35, delay=1)


item_name = thesystem.dungeon.get_item_name_from_csv()
with open('Files/Player Data/Inventory.json', 'r') as file:
    data = ujson.load(file)

# Find the item and update or remove it
if item_name in data:
    for item in data[item_name]:
        rank=item["rank"]
        
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 125,
    width = 380,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    533.0,
    595.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
    preloaded_frames=np.load(video_path)
player = thesystem.system.FastVideoPlayer(canvas, preloaded_frames, 200.0, 163.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    190.0,
    62.5,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    190.0,
    49.0,
    image=image_image_3
)

canvas.create_text(
    97.0,
    66.0,
    anchor="nw",
    text=f"{rank}-Rank Instance Dungeon",
    fill="#45EF2A",
    font=("Exo Regular", 15 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: thesystem.dungeon.update_inventory(window),
    relief="flat"
)
button_1.place(
    x=34.0,
    y=90.0,
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
    x=267.0,
    y=90.0,
    width=68.0,
    height=17.0
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    190.0,
    10.0,
    image=image_image_4
)

canvas.tag_bind(image_4, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_4, "<B1-Motion>", move_window)

window.resizable(False, False)
window.mainloop()
