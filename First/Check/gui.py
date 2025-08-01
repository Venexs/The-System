
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import random
import ujson
import cv2
from PIL import Image, ImageTk
import time
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

window.after(2000)

initial_height = 0
target_height = 449
window_width = 696

job=thesystem.misc.return_status()["status"][1]["job"]

top_val='dailyquest.py'
all_prev=''
video='Video'
transp_clr='#0C679B'

if job!='None':
    top_val=''
    all_prev='alt_'
    video='Alt Video'
    transp_clr='#652AA3'

top_images = f"thesystem/{all_prev}top_bar"
bottom_images = f"thesystem/{all_prev}bottom_bar"

top_preloaded_images = thesystem.system.load_or_cache_images(top_images, (695, 39), job, type_="top")
bottom_preloaded_images = thesystem.system.load_or_cache_images(bottom_images, (702, 36), job, type_="bottom")

subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=20, delay=1)
thesystem.system.make_window_transparent(window, '#0C679B')
thesystem.system.center_window(window,window_width,target_height)
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


def ex_close(eve):
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=30, delay=1)

def prog():
    canvas.itemconfig("First", state="normal")
    window.after(3000, hide_first)

def hide_first():
    canvas.itemconfig("First", state="hidden")
    canvas.itemconfig("Second", state="normal")
    window.after(3000, show_third)

def show_third():
    canvas.itemconfig("Second", state="hidden")
    canvas.itemconfig("Third", state="normal")
    window.after(30000, end_prog)

def end_prog():
    canvas.itemconfig("Third", state="hidden")
    window.quit()  # Uncomment this line if you want to close the window after 20 seconds

def fin(a):
    subprocess.Popen(['python', 'First/Congrats/gui.py'])
    window.quit()

def no(a):
    window.quit()

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 449,
    width = 696,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    609.0,
    301.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Anime"]["Video"]
player = thesystem.system.FastVideoPlayer(canvas, np.load(video_path), 478.0, 313.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    348.0,
    233.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    379.0,
    110.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    186.0,
    110.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    347.0,
    276.0,
    image=image_image_5,
    tags="First",
    state="hidden"  
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    363.0,
    206.0,
    image=image_image_6,
    tags="Second",
    state="hidden"
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    349.0,
    202.0,
    image=image_image_7,
    tags="Third",
    state="hidden"
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    236.0,
    300.0,
    image=image_image_8,
    tags="Third",
    state="hidden"
)

canvas.tag_bind(image_8, "<ButtonPress-1>", fin)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    439.0,
    300.0,
    image=image_image_9,
    tags="Third",
    state="hidden"
)

canvas.tag_bind(image_9, "<ButtonPress-1>", no)

canvas.create_rectangle(
    0.0,
    0.0,
    696.0,
    29.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    0.0,
    6.0,
    190.0,
    42.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    0.0,
    414.0,
    696.0,
    449.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    696.0,
    29.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    0.0,
    5.0,
    60.0,
    455.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    647.0,
    0.0,
    696.0,
    458.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    119.0,
    0.0,
    381.0,
    38.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    56.0,
    421.0,
    923.0,
    460.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    50.0,
    19.0,
    643.0,
    44.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    137.0,
    -10.0,
    765.0,
    50.0,
    fill="#0C679B",
    outline="")

image_40 = thesystem.system.side_bar("left_bar.png", (47, 393))
canvas.create_image(33.0, 235.0, image=image_40)

image_50 = thesystem.system.side_bar("right_bar.png", (46, 385))
canvas.create_image(666.0, 235.0, image=image_50)

image_index = 0
bot_image_index = 0

top_image = canvas.create_image(
    348.0,
    29.0,
    image=top_preloaded_images[image_index]
)

canvas.tag_bind(top_image, "<ButtonPress-1>", start_move)
canvas.tag_bind(top_image, "<B1-Motion>", move_window)

bottom_image = canvas.create_image(
    357.0,
    437.0,
    image=bottom_preloaded_images[bot_image_index]
)

step,delay=1,1

def update_images():
    global image_index, bot_image_index

    image_index = (image_index + 1) % len(top_preloaded_images)
    top_img = top_preloaded_images[image_index]
    canvas.itemconfig(top_image, image=top_img)
    canvas.top_img = top_img

    bot_image_index = (bot_image_index + 1) % len(bottom_preloaded_images)
    bot_img = bottom_preloaded_images[bot_image_index]
    canvas.itemconfig(bottom_image, image=bot_img)
    canvas.bot_img = bot_img

    window.after(1000 // 24, update_images)

update_images()

button_image_20 = PhotoImage(
    file=relative_to_assets("close.png"))
button_20 = Button(
    image=button_image_20,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(window),
    relief="flat"
)
button_20.place(
    x=564.0,
    y=52.0,
    width=21.20473861694336,
    height=24.221660614013672
)

prog()

window.resizable(False, False)
window.mainloop()
