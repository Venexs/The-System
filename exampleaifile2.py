from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, WORD, Label, END # AI ADDED LABEL
import ujson
import csv
import subprocess
import cv2
import math
from PIL import Image, ImageTk
import threading
import sys
import os
from google import genai
import os
from supabase import create_client
import random
import time


current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../'))

sys.path.insert(0, project_root)

import thesystem.system
import thesystem.inventory

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")

YOUR_API_KEY = "AIzaSyBcV8U32iIXkd8Kyd9EZE2bbIbsahgOFI8"

with open("Files/Tabs.json",'r') as tab_son:
    tab_son_data=ujson.load(tab_son)

with open("Files/Tabs.json",'w') as fin_tab_son:
    tab_son_data["Inventory"]='Open'
    ujson.dump(tab_son_data,fin_tab_son,indent=4)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

initial_height = 0
target_height = 592
window_width = 855

window.geometry(f"{window_width}x{initial_height}")
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

top_images = [f"thesystem/{all_prev}top_bar/{top_val}{str(i).zfill(4)}.png" for i in range(1, 501)]
bottom_images = [f"thesystem/{all_prev}bottom_bar/{str(i).zfill(4)}.png" for i in range(1, 501)]

thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)

window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

# Preload top and bottom images
top_preloaded_images = thesystem.system.preload_images(top_images, (970, 40))
bottom_preloaded_images = thesystem.system.preload_images(bottom_images, (970, 40))

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

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

URL = "https://smewvswweqnpwzngdtco.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNtZXd2c3d3ZXFucHd6bmdkdGNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyMDY2NjcsImV4cCI6MjA0OTc4MjY2N30.0SSN0bbwzFMCGC47XUuwqyKfF__Zikm_rJHqXWf78PU"

supabase = create_client(URL, KEY)

# dungeon_id

def ex_close(win):
    with open("Files/Tabs.json",'r') as tab_son:
        tab_son_data=ujson.load(tab_son)

    with open("Files/Tabs.json",'w') as fin_tab_son:
        tab_son_data["Inventory"]='Close'
        ujson.dump(tab_son_data,fin_tab_son,indent=4)
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=50, delay=1)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 592,
    width = 855,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    479.0,
    364.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Anime"][video]
player = thesystem.system.VideoPlayer(canvas, video_path, 479.0, 364.0)


side = PhotoImage(file=relative_to_assets("blue.png"))
if job.upper()!="NONE":
    side = PhotoImage(file=relative_to_assets("purple.png"))
canvas.create_image(-10.0, 283.0, image=side)
canvas.create_image(851.0, 308.0, image=side)

canvas.create_rectangle(
    0.0,
    0.0,
    101.0,
    21.0,
    fill=transp_clr,
    outline="")

canvas.create_rectangle(
    0.0,
    520.0,
    1000.0,
    716.0,
    fill=transp_clr,
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    1000.0,
    34.0,
    fill=transp_clr,
    outline="")

image_40 = thesystem.system.side_bar("left_bar.png", (101, 520))
canvas.create_image(-13.0, 280.0, image=image_40)

image_50 = thesystem.system.side_bar("right_bar.png", (80, 500))
canvas.create_image(851.0, 280.0, image=image_50)

image_index = 0
bot_image_index = 0

top_image = canvas.create_image(
    472.0,
    20.0,
    image=top_preloaded_images[image_index]
)

canvas.tag_bind(top_image, "<ButtonPress-1>", start_move)
canvas.tag_bind(top_image, "<B1-Motion>", move_window)

bottom_image = canvas.create_image(
    427.0,
    530.0,
    image=bottom_preloaded_images[bot_image_index]
)

step,delay=1,1

def update_images():
    global image_index, bot_image_index

    # Update top image
    image_index = (image_index + 1) % len(top_preloaded_images)
    canvas.itemconfig(top_image, image=top_preloaded_images[image_index])

    # Update bottom image
    bot_image_index = (bot_image_index + 1) % len(bottom_preloaded_images)
    canvas.itemconfig(bottom_image, image=bottom_preloaded_images[bot_image_index])

    # Schedule next update (24 FPS)
    window.after(1000 // 24, update_images)

# Start the animation
update_images()

# =========================================================================================================


button_image_26 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_26 = Button(
    image=button_image_26,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(window),
    relief="flat"
)
button_26.place(
    x=806.0,
    y=64.0,
    width=20.0,
    height=20.0
)


# System Alerts Implementation

# Create a label with red alert text
alert_text = Text(window, height=10, width=50, font=("Montserrat", 14), fg="red", bg="black", wrap='word')
alert_text.pack()

alert_text.place(x=125, y=100)  # Adjust x and y values as needed

# Configure the Gemini API with your API key
client = genai.Client(api_key='AIzaSyBcV8U32iIXkd8Kyd9EZE2bbIbsahgOFI8')

# Generate alert text
response = client.models.generate_content(
    contents="Generate a short alert message for a solo leveling style danger notification. It should introduce a task relevant to self improvement, make sure you are not vague and are specific with the task.",
    model="gemini-1.5-flash"
)

# Extract the generated text
generated_text = response.text

alert_text.delete("1.0", END)  # Clear existing text
alert_text.insert(END, generated_text)  # Insert new text



window.resizable(False, False)
window.mainloop()