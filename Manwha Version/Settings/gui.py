
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, IntVar, Checkbutton
import json
import csv
import subprocess
import threading
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import pandas as pd
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system
import thesystem.settings as settings

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

with open("Files/Tabs.json",'r') as tab_son:
    tab_son_data=json.load(tab_son)

with open("Files/Tabs.json",'w') as fin_tab_son:
    tab_son_data["Settings"]='Open'
    json.dump(tab_son_data,fin_tab_son,indent=4)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

window = Tk()

initial_height = 0
target_height = 622
window_width = 393

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=35, delay=1)

window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

checkbox_var1 = IntVar(value=0)
checkbox_var0 = IntVar(value=0)

with open("Files\Settings.json", 'r') as settings_open:
    setting_data=json.load(settings_open)

if setting_data["Settings"]["Calorie_Penalty"]=="True":
    checkbox_var1 = IntVar(value=1)

if setting_data["Settings"]["Main_Penalty"]=="True":
    checkbox_var0 = IntVar(value=1)

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

def theme_open():
    with open("Files/Checks/theme_open.csv", 'w', newline='') as info_open:
        fw=csv.writer(info_open)
        fw.writerow(["True"])
        
    subprocess.Popen(['python', 'First\Theme Check\gui.py'])
    ex_close(window)

def info_open():
    with open("Files/Checks/info_open.csv", 'w', newline='') as info_open:
        fw=csv.writer(info_open)
        fw.writerow(["True"])

    subprocess.Popen(['python', 'First\Info\gui.py'])
    ex_close(window)


def ex_close(win):
    with open("Files/Tabs.json",'r') as tab_son:
        tab_son_data=json.load(tab_son)

    with open("Files/Tabs.json",'w') as fin_tab_son:
        tab_son_data["Settings"]='Close'
        json.dump(tab_son_data,fin_tab_son,indent=4)
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=20, delay=1)

unchecked_image = PhotoImage(file="assets/frame0/Off.png")
checked_image  = PhotoImage(file="assets/frame0/On.png")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 622,
    width = 393,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    525.0,
    424.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 200.0, 300.0, resize_factor=1.2)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    196.5,
    310.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    104.0,
    56.0,
    image=image_image_3
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
    x=348.0,
    y=35.0,
    width=20.0,
    height=20.0
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    196.0,
    10.0,
    image=image_image_4
)

canvas.tag_bind(image_4, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_4, "<B1-Motion>", move_window)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    196.0,
    338.0,
    image=image_image_5
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: theme_open(),
    relief="flat"
)
button_2.place(
    x=29.0,
    y=121.0,
    width=156.0,
    height=34.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: info_open(),
    relief="flat"
)
button_3.place(
    x=29.0,
    y=167.0,
    width=156.0,
    height=34.0
)

canvas.create_text(
    30.0,
    223.0,
    anchor="nw",
    text="Have Penalty for Daily Quests:",
    fill="#FFFFFF",
    font=("Exo SemiBold", 11 * -1)
)

checkbox = Checkbutton(
    window,
    variable=checkbox_var1,
    command= lambda: settings.settings_ope(checkbox_var1, checkbox_var0),
    image=unchecked_image,
    selectimage=checked_image,
    compound="center",       # Place the image to the left of the text
    indicatoron=False,       # Hide the default checkbox indicator
    bd=0,
    highlightthickness=0,    # Remove the focus highlight around the widget
    padx=0,                  # Remove internal horizontal padding
    pady=0
)

# Position the checkbox using place
checkbox.place(x=265, y=229, width=14, height=14)

canvas.create_text(
    30.0,
    261.0,
    anchor="nw",
    text="Have Penalty for Calorie Coutnt:",
    fill="#FFFFFF",
    font=("Exo SemiBold", 11 * -1)
)

checkbox1 = Checkbutton(
    window,
    variable=checkbox_var0,
    command= lambda: settings.settings_ope(checkbox_var1, checkbox_var0),
    image=unchecked_image,
    selectimage=checked_image,
    compound="center",       # Place the image to the left of the text
    indicatoron=False,       # Hide the default checkbox indicator
    bd=0,
    highlightthickness=0,    # Remove the focus highlight around the widget
    padx=0,                  # Remove internal horizontal padding
    pady=0
)

# Position the checkbox using place
checkbox1.place(x=265, y=267, width=14, height=14)

window.resizable(False, False)
window.mainloop()