
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import sys
from PIL import Image, ImageTk
from datetime import datetime
import pandas as pd
import json
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


window = Tk()

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

initial_height = 0
target_height = 549
window_width = 753

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.make_window_transparent(window)
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
    subprocess.Popen(['python', 'First/Check/gui.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=30, delay=1)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 549,
    width = 753,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    718.0,
    928.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Anime"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 430.0, 263.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    385.0,
    281.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    376.0,
    103.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    382.0,
    282.0,
    image=image_image_4
)

canvas.create_rectangle(
    0.0,
    0.0,
    207.0,
    44.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    0.0,
    512.0,
    756.0,
    554.0,
    fill="#0C679B",
    outline="")

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    31.0,
    278.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    724.4500732421875,
    288.0,
    image=image_image_6
)

canvas.create_rectangle(
    194.0,
    0.0,
    756.0,
    56.0,
    fill="#0C679B",
    outline="")

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    375.0,
    42.0,
    image=image_image_7
)

canvas.tag_bind(image_7, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_7, "<B1-Motion>", move_window)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    378.0,
    523.0,
    image=image_image_8
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close("None"),
    relief="flat"
)
button_1.place(
    x=522.0,
    y=458.0,
    width=161.0,
    height=25.649993896484375
)
window.resizable(False, False)
window.mainloop()