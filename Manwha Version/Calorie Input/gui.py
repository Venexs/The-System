
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from datetime import datetime, timedelta, date
import subprocess
import sys
from PIL import Image, ImageTk
from datetime import datetime
import pandas as pd
import sys
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

initial_height = 0
target_height = 109
window_width = 507

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)
thesystem.system.center_window(window,window_width,target_height)

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

def ex_close(eve):
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=12, delay=1)

def add_cal(eve=0):
    with open("Files\Data\Calorie_Count.json", 'r') as calorie_add_file:
        calorie_add_data=json.load(calorie_add_file)
        calorie_add_key=list(calorie_add_data.keys())[0]

    # Get today's date
    current_date = date.today()

    # Format the date as a string
    formatted_date = current_date.strftime("%Y-%m-%d")

    if calorie_add_key==formatted_date:
        cal_c=float(entry_1.get())
        calorie_add_data[formatted_date][0]+=cal_c
        with open("Files\Data\Calorie_Count.json", 'w') as calorie_add_file_write:
            json.dump(calorie_add_data, calorie_add_file_write, indent=4)

    else:
        new_data={formatted_date:[0]}
        with open("Files\Data\Calorie_Count.json", 'w') as calorie_add_file_write:
            json.dump(new_data, calorie_add_file_write, indent=4)
        add_cal(None)

    ex_close()

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 109,
    width = 507,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    663.0,
    691.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 200.0, 163.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    253.50003051757812,
    54.5,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    253.0,
    35.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    481.0,
    24.0,
    image=image_image_4
)

canvas.tag_bind(image_4, "<ButtonPress-1>", ex_close)

entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Montserrat Bold", 25 * -1),
    justify="center"
)
entry_1.place(
    x=108.0,
    y=51.708038330078125,
    width=282.0,
    height=38.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_cal(None),
    relief="flat"
)
button_1.place(
    x=403.0,
    y=60.708038330078125,
    width=23.0,
    height=23.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    253.0,
    10.0,
    image=image_image_5
)
canvas.tag_bind(image_5, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_5, "<B1-Motion>", move_window)

window.resizable(False, False)
window.mainloop()