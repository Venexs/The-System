
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import json
import threading
import csv
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

initial_height = 0
target_height = 144
window_width = 715

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.make_window_transparent(window)
thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)
subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])
thesystem.system.center_window(window,window_width,target_height)

def ex_close(window,):
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, 0, window_width, step=20, delay=1)


window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

def complete(eve=''):
    hr=entry_1.get()
    mn=entry_2.get()

    true_file1_name='NONE'
    true_file2_name='NONE'

    data0={}
    with open("Files/Data/Penalty_Info.json", "w") as pen_info_file:
        data0["Penalty Info"]=[true_file1_name,true_file2_name]
        data0["Penalty Time"]=f"{hr}:{mn}"
        json.dump(data0, pen_info_file, indent=4)

    with open("Files/Data/First_open.csv", 'w', newline='') as first_open_check_file:
        fw=csv.writer(first_open_check_file)
        fw.writerow(["True"])

    subprocess.Popen(['python', 'gui.py'])
    ex_close()

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

def ex_close(eve=''):
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=30, delay=1)

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
    video_path=pres_file_data["Anime"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 430.0, 263.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    369.0,
    78.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    366.0,
    47.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    348.0,
    67.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    384.0,
    67.0,
    image=image_image_5
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    677.0,
    71.0,
    image=image_image_8
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    47.0,
    72.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    677.0,
    71.0,
    image=image_image_8
)

canvas.create_rectangle(
    158.0,
    0.0,
    732.0,
    20.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    162.0,
    16.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    0.0,
    123.0,
    715.0,
    144.0,
    fill="#0C679B",
    outline="")

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    357.0,
    15.0,
    image=image_image_9
)

canvas.tag_bind(image_9, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_9, "<B1-Motion>", move_window)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    380.0,
    130.0,
    image=image_image_10
)

entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=333.0,
    y=79.0,
    width=30.0,
    height=31.0
)

entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=369.0,
    y=79.0,
    width=30.0,
    height=31.0
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    612.0,
    99.0,
    image=image_image_11
)

canvas.tag_bind(image_11, "<ButtonPress-1>", complete)

window.resizable(False, False)
window.mainloop()