
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
ASSETS_PATH2 = OUTPUT_PATH / Path(r"assets\frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH2 / Path(path)


window = Tk()

initial_height = 0
target_height = 251
window_width = 548

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=40, delay=1)

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
    subprocess.Popen(['python', 'Manwha Version/Skills Tab/gui.py'])
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, target_height, window_width, step=40, delay=1)
    window.quit()

name1=name2=name3=name4='-'
lvl1=lvl2=lvl3=lvl4='??'

with open("Files/Player Data/Skill.json", 'r') as fson:
    c=0
    try:
        data=ujson.load(fson)
        data_key=list(data.keys())
        for k in data_key:
            if data[k][0]["type"]=='Job':
                if c==0:
                    name1=k
                    lvl1=data[k][0]["lvl"]
                    c+=1
                elif c==1:
                    name2=k
                    lvl2=data[k][0]["lvl"]
                    c+=1
                elif c==2:
                    name3=k
                    lvl3=data[k][0]["lvl"]
                    c+=1
                elif c==3:
                    name4=k
                    lvl4=data[k][0]["lvl"]
                    c+=1
    except:
        print()

def open_prog(name):
    if name!='-':
        with open("Files/Temp Files/Skill Temp.csv", 'w', newline='') as csv_open:
            fw=csv.writer(csv_open)
            rec=[name]
            fw.writerow(rec)

        subprocess.Popen(['python', 'Manwha Version/Skill Info/gui.py'])

        ex_close(window)

canvas = Canvas(
    window,
    bg = "#FFD337",
    height = 251,
    width = 548,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    599.0,
    947.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
    preloaded_frames=np.load(video_path)
player = thesystem.system.FastVideoPlayer(canvas, preloaded_frames, 250.0, 150.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    283.0,
    121.5,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    236.0,
    64.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    281.0,
    215.0,
    image=image_image_4
)

canvas.create_text(
    69.0,
    204.0,
    anchor="nw",
    text=name4,
    fill="#FFD337",
    font=("Exo Regular", 18 * -1)
)

canvas.create_text(
    407.0,
    204.0,
    anchor="nw",
    text=f"Lvl.{lvl4}",
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_prog(name4),
    relief="flat"
)
button_1.place(
    x=481.0,
    y=203.0,
    width=24.0,
    height=24.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    281.0,
    183.0,
    image=image_image_5
)

canvas.create_text(
    69.0,
    172.0,
    anchor="nw",
    text=name3,
    fill="#FFD337",
    font=("Exo Regular", 18 * -1)
)

canvas.create_text(
    407.0,
    172.0,
    anchor="nw",
    text=f"Lvl.{lvl3}",
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_prog(name3),
    relief="flat"
)
button_2.place(
    x=481.0,
    y=171.0,
    width=24.0,
    height=24.0
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    281.0,
    151.0,
    image=image_image_6
)

canvas.create_text(
    69.0,
    140.0,
    anchor="nw",
    text=name2,
    fill="#FFD337",
    font=("Exo Regular", 18 * -1)
)

canvas.create_text(
    407.0,
    140.0,
    anchor="nw",
    text=f"Lvl.{lvl2}",
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_prog(name2),
    relief="flat"
)
button_3.place(
    x=481.0,
    y=139.0,
    width=24.0,
    height=24.0
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    281.0,
    119.0,
    image=image_image_7
)

canvas.create_text(
    69.0,
    108.0,
    anchor="nw",
    text=name1,
    fill="#FFD337",
    font=("Exo Regular", 18 * -1)
)

canvas.create_text(
    407.0,
    108.0,
    anchor="nw",
    text=f"Lvl.{lvl1}",
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_prog(name1),
    relief="flat"
)
button_4.place(
    x=481.0,
    y=107.0,
    width=24.0,
    height=24.0
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    284.0,
    10.0,
    image=image_image_8
)

canvas.tag_bind(image_8, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_8, "<B1-Motion>", move_window)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(window),
    relief="flat"
)
button_5.place(
    x=502.0,
    y=20.0,
    width=23.0,
    height=23.0
)
window.resizable(False, False)
window.mainloop()
