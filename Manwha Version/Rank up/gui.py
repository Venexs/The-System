
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
# Fork by Venexs


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ujson
import csv
import subprocess
import threading
import cv2
from PIL import Image, ImageTk
import sys
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
target_height=363
window_width=645

window.configure(bg = "#FFFFFF")
set_data=thesystem.misc.return_settings()
transp_value=set_data["Settings"]["Transparency"]

window.attributes('-alpha',transp_value)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])

thesystem.system.center_window(window,window_width,target_height)
thesystem.system.animate_window_open(window, target_height, window_width, step=40, delay=1)

def start_move(event):
    window.lastx, window.lasty = event.widget.winfo_pointerxy()

def move_window(event):
    x_root, y_root = event.widget.winfo_pointerxy()
    deltax, deltay = x_root - window.lastx, y_root - window.lasty

    if deltax != 0 or deltay != 0:  # Update only if there is actual movement
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")
        window.lastx, window.lasty = x_root, y_root


def ex_close(win):
    with open("Files/Player Data/Tabs.json",'r') as tab_son:
        tab_son_data=ujson.load(tab_son)

    with open("Files/Player Data/Tabs.json",'w') as fin_tab_son:
        tab_son_data["Intro"]='Close'
        ujson.dump(tab_son_data,fin_tab_son,indent=4)
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, target_height, window_width, step=20, delay=1)
    win.quit()


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 363,
    width = 645,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    824.0,
    680.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
    preloaded_frames=np.load(video_path)

player = thesystem.system.FastVideoPlayer(canvas, preloaded_frames, 200.0, 150.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    321.0,
    181.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    322.0,
    62.0,
    image=image_image_3
)

def center_text(canvas, text, y, font, fill):
    text_id = canvas.create_text(
        0,  # Temporary X position
        y,
        anchor="nw",
        text=text,
        fill=fill,
        font=font
    )

    # Ensure the text is drawn before getting its bounding box
    canvas.update_idletasks()

    # Get text width
    text_bbox = canvas.bbox(text_id)
    text_width = text_bbox[2] - text_bbox[0]

    # Get canvas width and calculate centered X position
    canvas_width = canvas.winfo_width()
    center_x = (canvas_width - text_width) / 2

    # Move text to the centered position
    canvas.coords(text_id, center_x, y)

status_data = thesystem.misc.load_ujson("Files/Player Data/Status.json")
name = status_data["status"][0]["name"]
level = status_data["status"][0]["level"]

with open("Files/Temp Files/Rank file.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        old_lvl = int(row[0])

old_rank=thesystem.system.give_ranking(old_lvl)
new_rank=thesystem.system.give_ranking(level)


# Centering each text
center_text(canvas, f"[{name}] has been promoted!", 97.0, ("Exo Regular", 15 * -1), "#FFFFFF")
center_text(canvas, f"[{old_rank} Rank]   Lv.{old_lvl}", 149.0, ("Exo Regular", 17 * -1), "#FFFFFF")
center_text(canvas, f"[{new_rank} Rank]   Lv.{level}", 241.0, ("Exo Bold", 17 * -1), "#00FF2A")


image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    323.41493225097656,
    160.14492797851562,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    323.0,
    206.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    323.0,
    252.11593627929688,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    322.0,
    11.0,
    image=image_image_7
)

canvas.tag_bind(image_7, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_7, "<B1-Motion>", move_window)

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
    x=594.0,
    y=19.0,
    width=29.97853660583496,
    height=30.20939064025879
)
window.resizable(False, False)
window.mainloop()
