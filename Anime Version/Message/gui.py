
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
import subprocess
import threading
import ujson
import csv
import sys
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system
import thesystem.misc

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    get_stuff_path_str=pres_file_data["Anime"]["Message Box"]

def get_stuff_path(key):
    full_path=get_stuff_path_str+'/'+key
    return full_path


window = Tk()

initial_height = 0
target_height = 144
window_width = 715

stop_event=threading.Event()

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

thesystem.system.make_window_transparent(window,transp_clr)

with open("Files/Player Data/Settings.json", 'r') as settings_open:
    setting_data=ujson.load(settings_open)

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width,  step=20, delay=1)
thesystem.system.center_window(window,window_width,target_height)

window.configure(bg = "#FFFFFF")
set_data=thesystem.misc.return_settings()
transp_value=set_data["Settings"]["Transparency"]

window.attributes('-alpha',transp_value)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

# Preload top and bottom images
top_images = f"thesystem/{all_prev}top_bar"
bottom_images = f"thesystem/{all_prev}bottom_bar"

top_preloaded_images = thesystem.system.load_or_cache_images(top_images, (715, 41), job, type_="top")
bottom_preloaded_images = thesystem.system.load_or_cache_images(bottom_images, (715, 41), job, type_="bottom")

subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])             

def start_move(event):
    window.lastx, window.lasty = event.widget.winfo_pointerxy()

def move_window(event):
    x_root, y_root = event.widget.winfo_pointerxy()
    deltax, deltay = x_root - window.lastx, y_root - window.lasty

    if deltax != 0 or deltay != 0:  # Update only if there is actual movement
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")
        window.lastx, window.lasty = x_root, y_root


def ex_close(win):
    if setting_data["Settings"]["Performernce (ANIME):"] != "True":
        stop_event.set()
        update_thread.join()
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, 0, window_width, step=30, delay=1)

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
    file=get_stuff_path("back.png"))
image_1 = canvas.create_image(
    448.0,
    277.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Anime"][video]
    prealoaded_frames=np.load(video_path)
player = thesystem.system.FastVideoPlayer(canvas, prealoaded_frames, 430.0, 263.0)

image_image_2 = PhotoImage(
    file=get_stuff_path("frame.png"))
image_2 = canvas.create_image(
    369.0,
    78.0,
    image=image_image_2
)

with open("Files/Checks/Message.csv", 'r') as check_file:
    check_fr=csv.reader(check_file)
    for k in check_fr:
        message=k[0]

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    file_path=pres_file_data["Message"][message][0]

canvas_center_x = window_width // 2
canvas_center_y = target_height // 2

original_image = Image.open(file_path)
new_width = int(original_image.width * 0.95)
new_height = int(original_image.height * 0.95)
resized_image = original_image.resize((new_width, new_height))

# Convert to a PhotoImage for Tkinter
image_image_3 = ImageTk.PhotoImage(resized_image)

# Place the resized image on the canvas
image_3 = canvas.create_image(
    canvas_center_x,
    canvas_center_y,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=get_stuff_path("close.png"))
image_4 = canvas.create_image(
    610.0,
    53.0,
    image=image_image_4
)

canvas.tag_bind(image_4, "<ButtonPress-1>", ex_close)

side = PhotoImage(file=get_stuff_path("blue.png"))
if job.upper()!="NONE":
    side = PhotoImage(file=get_stuff_path("purple.png"))
canvas.create_image(677.0, 71.0, image=side)
canvas.create_image(47.0, 72.0, image=side)

canvas.create_rectangle(
    0.0,
    0.0,
    760.0,
    30.0,
    fill=transp_clr,    
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    162.0,
    16.0,
    fill=transp_clr,    
    outline="")

canvas.create_rectangle(
    0.0,
    123.0,
    715.0,
    144.0,
    fill=transp_clr,    
    outline="")

image_40 = thesystem.system.side_bar("left_bar.png", (30, 100))
canvas.create_image(82.0, 76.0, image=image_40)

image_50 = thesystem.system.side_bar("right_bar.png", (30, 114))
canvas.create_image(640.0, 75.0, image=image_50)

image_index = 0
bot_image_index = 0

top_image = canvas.create_image(
    357.0,
    20.0,
    image=top_preloaded_images[image_index]
)

canvas.tag_bind(top_image, "<ButtonPress-1>", start_move)
canvas.tag_bind(top_image, "<B1-Motion>", move_window)

bottom_image = canvas.create_image(
    370.0,
    128.0,
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

# Start the animation
if setting_data["Settings"]["Performernce (ANIME):"] != "True":
    update_thread = threading.Thread(target=update_images)
    update_thread.start()

window.resizable(False, False)
window.mainloop()
