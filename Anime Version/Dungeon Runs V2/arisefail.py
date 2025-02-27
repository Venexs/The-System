# [Your existing imports remain unchanged]
import sys
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
import subprocess
import threading
import ujson
import csv
import os
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

import thesystem.system
import thesystem.misc

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data = ujson.load(pres_file)
    get_stuff_path_str = pres_file_data["Anime"]["Message Box"]

def get_stuff_path(key):
    full_path = get_stuff_path_str + '/' + key
    return full_path

window = Tk()
initial_height = 0
target_height = 144
window_width = 715

job = thesystem.misc.return_status()["status"][1]["job"]

top_val = 'dailyquest.py'
all_prev = ''
video = 'Video'
transp_clr = '#0C679B'

if job != 'None':
    top_val = ''
    all_prev = 'alt_'
    video = 'Alt Video'
    transp_clr = '#652AA3'

thesystem.system.make_window_transparent(window, transp_clr)

top_images = [f"thesystem/{all_prev}top_bar/{top_val}{str(i).zfill(4)}.png" for i in range(1, 501)]
bottom_images = [f"thesystem/{all_prev}bottom_bar/{str(i).zfill(4)}.png" for i in range(1, 501)]

thesystem.system.center_window(window, window_width, target_height)
window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=20, delay=1)
thesystem.system.center_window(window, window_width, target_height)

window.configure(bg="#FFFFFF")
window.attributes('-alpha', 0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

# Preload top and bottom images
top_preloaded_images = thesystem.system.preload_images(top_images, (715, 41))
bottom_preloaded_images = thesystem.system.preload_images(bottom_images, (715, 41))

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

def ex_close(win):
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, 0, window_width, step=30, delay=1)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=144,
    width=715,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=get_stuff_path("back.png"))
image_1 = canvas.create_image(448.0, 277.0, image=image_image_1)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data = ujson.load(pres_file)
    video_path = pres_file_data["Anime"][video]
player = thesystem.system.VideoPlayer(canvas, video_path, 430.0, 263.0)

image_image_2 = PhotoImage(file=get_stuff_path("frame.png"))
image_2 = canvas.create_image(369.0, 78.0, image=image_image_2)

# Read message from CSV
with open("Files/Checks/Message.csv", 'r') as check_file:
    check_fr = csv.reader(check_file)
    for k in check_fr:
        message = k[0]

# Probability constants (adjustable for testing)
SUMMON_SUCCESS_CHANCE = 0.10  # 10% chance to successfully summon (overall 2.5% chance)

def summon_attempt():
    # Define boss_name with a default value
    boss_name = "Unknown Boss"

    # Update boss_name if an argument is provided
    if len(sys.argv) > 1:  # sys.argv[0] is the script name, sys.argv[1] is the first argument
        boss_name = sys.argv[1]

    if random.random() < SUMMON_SUCCESS_CHANCE:
        # Successful summon
        # TODO: Add boss to shadow soldiers (e.g., update JSON or database)
        subprocess.Popen(['python', 'Anime Version/Dungeon Runs V2/arisesuccess.py'])
        ex_close(window)
    else:
        # Step 1: Read the current attempt value
        with open("Files/Checks/attempt.csv", 'r', newline='') as check_file:
            csv_reader = csv.reader(check_file)
            row = next(csv_reader, [1])  # Default to 1 if file is empty
            current_value = int(row[0])  # Convert string to integer

        # Step 2: Increment the value
        new_value = current_value + 1

        # Step 3: Write the new value back to the file
        with open("Files/Checks/attempt.csv", 'w', newline='') as check_file:
            csv_writer = csv.writer(check_file)
            csv_writer.writerow([new_value])

        # Step 4: Check if attempts are >= 3
        if current_value >= 3:
            # Show a different window (e.g., maxattempts.py)
            if len(sys.argv) > 1:
                subprocess.Popen(['python', 'Anime Version/Dungeon Runs V2/maxattempts.py', boss_name])
            else:
                subprocess.Popen(['python', 'Anime Version/Dungeon Runs V2/maxattempts.py'])
        else:
            # Show the regular failure window
            if len(sys.argv) > 1:
                subprocess.Popen(['python', 'Anime Version/Dungeon Runs V2/arisefail.py', boss_name])
            else:
                subprocess.Popen(['python', 'Anime Version/Dungeon Runs V2/arisefail.py'])

        ex_close(window)


xtext = window_width / 2
ytext = target_height / 2 - 10
# Create the button
noticetext = canvas.create_text(
    xtext,
    ytext,
    anchor="center",
    text=f"Shadow Extraction Failed...",
    fill="red",
    tags="1",
    font=("Exo", 20 * -1)
)

noticetext1 = canvas.create_text(
    xtext,
    ytext,
    anchor="center",
    text=f"Retry Shadow Extraction...",
    fill="white",
    tags="2",
    state="hidden",
    font=("Exo", 20 * -1)
)

xbutton = window_width / 2
ybutton = target_height / 2 + 15

button_image_1 = PhotoImage(
    file=relative_to_assets("summon.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: summon_attempt(),
    relief="flat"
)
button_1.place(
    x=xbutton,
    y=ybutton,
    width=127.0,
    height=22.0
)

button_1.place_forget()    # Hide the button initially

xtext1 = window_width / 2
ytext1 = target_height / 2 + 10



with open("Files/Checks/attempt.csv", 'r') as attempt_check_file:
    fr = csv.reader(attempt_check_file)
    attempt_data = list(fr)  # Convert to list before accessing
    if attempt_data:
        attemptnumber = attempt_data[0][0]
    else:
        attemptnumber = "1"  # Default if file is empty


attempttext = canvas.create_text(
    xtext1,
    ytext1,
    anchor="center",
    text=f"{attemptnumber} /3 Attempts",
    fill="red",
    tags="1",
    font=("Exo", 16 * -1)
)

def updatetext():
    # Start animation for noticetext and attempttext
    thesystem.system.animate_text_out(canvas, noticetext, steps=30, delay=8, dx=-5)
    thesystem.system.animate_text_out(canvas, attempttext, steps=40, delay=15, dx=-5)
    canvas.after(200, lambda: subprocess.Popen(['python', 'Files\Mod\default\sfx_glitch.py']))
    canvas.after(300, lambda: canvas.itemconfig(noticetext1, state="normal"))
    button_1.place(x=xbutton, y=ybutton, width=127.0, height=22.0)  # Show it again
canvas.after(3000, lambda: updatetext())





image_image_4 = PhotoImage(file=get_stuff_path("close.png"))
image_4 = canvas.create_image(610.0, 53.0, image=image_image_4)
canvas.tag_bind(image_4, "<ButtonPress-1>", lambda e: ex_close(window))

side = PhotoImage(file=get_stuff_path("blue.png"))
if job.upper() != "NONE":
    side = PhotoImage(file=get_stuff_path("purple.png"))
canvas.create_image(677.0, 71.0, image=side)
canvas.create_image(47.0, 72.0, image=side)

canvas.create_rectangle(0.0, 0.0, 760.0, 30.0, fill=transp_clr, outline="")
canvas.create_rectangle(0.0, 0.0, 162.0, 16.0, fill=transp_clr, outline="")
canvas.create_rectangle(0.0, 123.0, 715.0, 144.0, fill=transp_clr, outline="")

image_40 = thesystem.system.side_bar("left_bar.png", (30, 100))
canvas.create_image(82.0, 76.0, image=image_40)

image_50 = thesystem.system.side_bar("right_bar.png", (30, 114))
canvas.create_image(640.0, 75.0, image=image_50)

image_index = 0
bot_image_index = 0

top_image = canvas.create_image(357.0, 20.0, image=top_preloaded_images[image_index])
canvas.tag_bind(top_image, "<ButtonPress-1>", start_move)
canvas.tag_bind(top_image, "<B1-Motion>", move_window)

bottom_image = canvas.create_image(370.0, 128.0, image=bottom_preloaded_images[bot_image_index])

def update_images():
    global image_index, bot_image_index
    image_index = (image_index + 1) % len(top_preloaded_images)
    canvas.itemconfig(top_image, image=top_preloaded_images[image_index])
    canvas.itemconfig(bottom_image, image=bottom_preloaded_images[bot_image_index])
    window.after(1000 // 24, update_images)

update_images()

window.resizable(False, False)
window.mainloop()