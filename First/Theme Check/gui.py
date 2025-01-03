
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label
import subprocess
import threading
import random
import cv2
import json
from PIL import Image, ImageTk
import time
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

def make_window_transparent(window):
    window.wm_attributes('-transparentcolor', "#0C679B")

def center_window(root, width, height):
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate position x, y to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set the dimensions of the window and the position
    root.geometry(f'{width}x{height}+{x}+{y}')

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
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=20, delay=1)


def name(eve,name):
    with open("Files\Data\Theme_Check.json", 'r') as file:
        data = json.load(file)
    
    # Modify the theme from "Anime" to "Manwha"
    data["Theme"] = name
    
    # Write the updated data back to the file
    with open("Files\Data\Theme_Check.json", 'w') as file:
        json.dump(data, file, indent=4)

    with open("Files/Checks/theme_open.csv", 'r') as info_open:
        info_fr=csv.reader(info_open)
        for k in info_fr:
            istrue=k[0]

    with open('Files/Data/Theme_Check.json', 'r') as themefile:
            theme_data=json.load(themefile)
            theme=theme_data["Theme"]

    if istrue=='True':
        subprocess.Popen(['Python', f'{theme} Version/Settings/gui.py'])
        with open("Files/Checks/theme_open.csv", 'w', newline='') as info_open:
            fw=csv.writer(info_open)
            fw.writerow(["False"])
        ex_close(window)
    
    else:
        subprocess.Popen(['python', f'{theme} Version/Penalty Check/gui.py'])
        ex_close(window)

window = Tk()

initial_height = 0
target_height = 592
window_width = 934

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=60, delay=1)

#center_window(window,window_width,target_height)
subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])
window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
make_window_transparent(window)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 592,
    width = 934,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    731.0,
    384.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Anime"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 430.0, 263.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    471.0,
    308.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    236.0,
    113.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    248.0,
    318.0,
    image=image_image_4
)

canvas.tag_bind(image_4, "<ButtonPress-1>", lambda event: name(event, "Anime"))

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    394.0,
    318.0,
    image=image_image_5
)

canvas.tag_bind(image_5, "<ButtonPress-1>", lambda event: name(event, "Manwha"))

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    540.0,
    318.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    686.0,
    318.0,
    image=image_image_7
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
    x=759.0,
    y=73.0,
    width=25.0,
    height=25.0
)

canvas.create_rectangle(
    33.0,
    7.0,
    906.0,
    45.0,
    fill="#333333",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    336.0,
    50.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    0.0,
    541.0,
    934.0,
    592.0,
    fill="#0C679B",
    outline="")

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    70.0,
    313.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    865.0,
    325.0,
    image=image_image_9
)

canvas.create_rectangle(
    235.0,
    0.0,
    934.0,
    69.0,
    fill="#0C679B",
    outline="")

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    452.0,
    47.0,
    image=image_image_10
)

canvas.tag_bind(image_10, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_10, "<B1-Motion>", move_window)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    458.0,
    556.0,
    image=image_image_11
)
window.resizable(False, False)
window.mainloop()
