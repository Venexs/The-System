
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
from PIL import Image, ImageDraw, ImageTk
import ujson
import threading
import sys
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    get_stuff_path_str=pres_file_data["Anime"]["Message Box"]

def get_stuff_path(key):
    full_path=get_stuff_path_str+'/'+key
    return full_path

window = Tk()

stop_event=threading.Event()

initial_height = 0
target_height = 144
window_width = 715

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

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 144,
    width = 715,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

def move_rectangle_up(rectangle_id, final_y, step_y, delay):
    current_coords = canvas.coords(rectangle_id)
    current_y1 = current_coords[1]
    current_y2 = current_coords[3]

    if current_y1 > final_y:
        new_y1 = current_y1 - step_y
        new_y2 = current_y2 - step_y
        canvas.coords(rectangle_id, 0.0, new_y1, 715.0, new_y2)
        window.after(delay, move_rectangle_up, rectangle_id, final_y, step_y, delay)

def move_rectangle_down(rectangle_id, final_y, step_y, delay):
    current_coords = canvas.coords(rectangle_id)
    current_y1 = current_coords[1]
    current_y2 = current_coords[3]

    if current_y1 < final_y:
        new_y1 = current_y1 + step_y
        new_y2 = current_y2 + step_y
        canvas.coords(rectangle_id, 0.0, new_y1, 715.0, new_y2)
        window.after(delay, move_rectangle_down, rectangle_id, final_y, step_y, delay)

def move_image_up(image_id, canvas, step=1, delay=10, val=24):
    coords = canvas.coords(image_id)
    new_y = coords[1] - step

    if new_y >= val:
        canvas.coords(image_id, coords[0], new_y)
        canvas.after(delay, move_image_up, image_id, canvas, step, delay)

def move_image_down(image_id, canvas, step=1, delay=10, val=130):
    coords = canvas.coords(image_id)
    new_y = coords[1] + step

    if new_y <= val:
        canvas.coords(image_id, coords[0], new_y)
        canvas.after(delay, move_image_down, image_id, canvas, step, delay)

def start_move(event):
    window.lastx, window.lasty = event.widget.winfo_pointerxy()

def move_window(event):
    x_root, y_root = event.widget.winfo_pointerxy()
    deltax, deltay = x_root - window.lastx, y_root - window.lasty

    if deltax != 0 or deltay != 0:  # Update only if there is actual movement
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")
        window.lastx, window.lasty = x_root, y_root


def ex_close(eve):
    if setting_data["Settings"]["Performernce (ANIME):"] != "True":
        stop_event.set()
        update_thread.join()
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=5, delay=1)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=get_stuff_path("back.png"))
image_1 = canvas.create_image(
    430.0,
    163.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Anime"][video]
    preloaded_frames=np.load(video_path)
player = thesystem.system.FastVideoPlayer(canvas, preloaded_frames, 430.0, 263.0)

image_image_2 = PhotoImage(
    file=get_stuff_path("level_up.png"))
image_2 = canvas.create_image(
    363.0,
    77.0,
    image=image_image_2
)

glow_color = "#FFFFFF"
glow_width = 5
text_color="#FFFFFF",
font=("Montserrat", 40 * -1)

image_image_3 = PhotoImage(
    file=get_stuff_path("close.png"))
image_3 = canvas.create_image(
    596.0,
    53.0,
    image=image_image_3
)

canvas.tag_bind(image_3, "<ButtonPress-1>", ex_close)


side = PhotoImage(file=get_stuff_path("blue.png"))
if job.upper()!="NONE":
    side = PhotoImage(file=get_stuff_path("purple.png"))
canvas.create_image(677.0, 71.0, image=side)
canvas.create_image(47.0, 72.0, image=side)

canvas.create_rectangle(
    158.0,
    0.0,
    732.0,
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

rectangle1_id=canvas.create_rectangle(
    0.0,
    73.0,
    715.0,
    144.0,
    fill=transp_clr,
    outline="")

rectangle2_id=canvas.create_rectangle(
    0.0,
    0.0,
    715.0,
    73.0,
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

def start_animations():
    threading.Thread(target=move_image_up, args=(top_image, canvas, step, 1)).start()
    threading.Thread(target=move_image_down, args=(bottom_image, canvas, step, 1)).start()
    threading.Thread(target=move_rectangle_down, args=(rectangle1_id, 300, 2, delay)).start()
    threading.Thread(target=move_rectangle_up, args=(rectangle2_id, -177, 2, delay)).start()

window.after(1, start_animations)

window.resizable(False, False)
window.mainloop()
