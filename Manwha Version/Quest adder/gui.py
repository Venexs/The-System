
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import json
import csv
import cv2
from PIL import Image, ImageTk
import random
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

initial_height = 0
target_height = 388
window_width = 481

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.make_window_transparent(window)
thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)

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
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    win.quit()

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 388,
    width = 481,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    857.0,
    469.5,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 277.0, 190.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    240.5,
    193.5,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    139.0,
    56.0,
    image=image_image_3
)

entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=30.0,
    y=110.0,
    width=369.0,
    height=20.0
)

canvas.create_text(
    30.0,
    92.0,
    anchor="nw",
    text="Enter Quest Name:",
    fill="#FFD337",
    font=("Exo Medium", 13 * -1)
)

entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=30.0,
    y=160.0,
    width=71.0,
    height=20.0
)

canvas.create_text(
    30.0,
    142.0,
    anchor="nw",
    text="Enter Quest Type (STR or INT): ",
    fill="#FFD337",
    font=("Exo Medium", 13 * -1)
)

entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=30.0,
    y=210.0,
    width=189.0,
    height=20.0
)

canvas.create_text(
    30.0,
    192.0,
    anchor="nw",
    text="Quest Objective:",
    fill="#FFD337",
    font=("Exo Medium", 13 * -1)
)

entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=30.0,
    y=260.0,
    width=71.0,
    height=20.0
)

canvas.create_text(
    30.0,
    242.0,
    anchor="nw",
    text="Quest Amount:",
    fill="#FFD337",
    font=("Exo Medium", 13 * -1)
)

entry_5 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=182.0,
    y=260.0,
    width=71.0,
    height=20.0
)

canvas.create_text(
    182.0,
    242.0,
    anchor="nw",
    text="Quest Amount Type:",
    fill="#FFD337",
    font=("Exo Medium", 13 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    197.0,
    307.0,
    image=image_image_4
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    63.5,
    353.0,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_6.place(
    x=28.0,
    y=342.0,
    width=71.0,
    height=20.0
)

canvas.create_text(
    28.0,
    324.0,
    anchor="nw",
    text="Quest Rank (E,D,C,B,A Or S) : ",
    fill="#FFD337",
    font=("Exo Medium", 13 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: thesystem.system.quest_adding_func(entry_1,entry_2,entry_3,entry_4,entry_5,entry_6,window),
    relief="flat"
)
button_1.place(
    x=350.0,
    y=346.0,
    width=109.0,
    height=22.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    241.0,
    10.0,
    image=image_image_5
)

canvas.tag_bind(image_5, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_5, "<B1-Motion>", move_window)

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
    x=447.0,
    y=13.0,
    width=23.0,
    height=23.0
)
window.resizable(False, False)
window.mainloop()