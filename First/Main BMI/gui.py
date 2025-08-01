
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import threading
import ujson
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

def start_move(event):
    window.lastx, window.lasty = event.widget.winfo_pointerxy()

def move_window(event):
    x_root, y_root = event.widget.winfo_pointerxy()
    deltax, deltay = x_root - window.lastx, y_root - window.lasty

    if deltax != 0 or deltay != 0:  # Update only if there is actual movement
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")
        window.lastx, window.lasty = x_root, y_root


def ex_close(eve):
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    subprocess.Popen(['python', 'First\Daily Quest Tweak\gui.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=30, delay=1)

window = Tk()

initial_height = 0
target_height = 549
window_width = 867

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)
subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])

window.configure(bg = "#FFFFFF")
set_data=thesystem.misc.return_settings()
transp_value=set_data["Settings"]["Transparency"]

window.attributes('-alpha',transp_value)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
thesystem.system.make_window_transparent(window)

with open("Files/Player Data/Status.json", 'r') as first_fson:
    data=ujson.load(first_fson)
    cc=data["cal_data"][0]["calorie calc"]
    r1=data["cal_data"][0]["final calorie calc"]
    bmi=data["cal_data"][0]["BMI"]

    mon=sun=cc
    tue=wed=thu=fri=sat=round(cc*0.85)

with open("Files\Workout\Cal_Count.json", 'w') as cal_fson:
    fin={"Monday":mon, "Tuesday":tue, "Wednesday":wed, "Thursday":thu, "Friday":fri, "Saturday":sat, "Sunday":sun}
    ujson.dump(fin, cal_fson, indent=4)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 549,
    width = 867,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    665.0,
    922.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Anime"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 430.0, 263.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    682.0,
    258.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    450.0,
    286.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    188.0,
    101.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    202.0,
    186.0,
    image=image_image_5
)

canvas.create_text(
    645.0,
    397.0,
    anchor="nw",
    text=f"BMI:",
    fill="#FFFFFF",
    font=("Montserrat ExtraBold", 20 * -1)
)

canvas.create_text(
    100.0,
    140.0,
    anchor="nw",
    text="-Maximum Calories you need to consume per day:",
    fill="#FFFFFF",
    font=("Montserrat Medium", 16 * -1)
)

canvas.create_text(
    100.0,
    214.0,
    anchor="nw",
    text="-Recommended/Exercised Calorie Count of a Week:",
    fill="#FFFFFF",
    font=("Montserrat Medium", 16 * -1)
)

canvas.create_text(
    147.0,
    165.0,
    anchor="nw",
    text=f"{cc}",
    fill="#FFFFFF",
    font=("Montserrat Bold", 32 * -1)
)

canvas.create_text(
    240.0,
    189.0,
    anchor="nw",
    text="cal",
    fill="#FFFFFF",
    font=("Montserrat Bold", 11 * -1)
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    258.0,
    345.0,
    image=image_image_6
)

canvas.create_text(
    251.0,
    264.0,
    anchor="nw",
    text=f"{mon} ",
    fill="#FFFFFF",
    font=("Montserrat Regular", 20 * -1)
)

canvas.create_text(
    251.0,
    290.0,
    anchor="nw",
    text=f"{tue} ",
    fill="#FFFFFF",
    font=("Montserrat Regular", 20 * -1)
)

canvas.create_text(
    251.0,
    314.0,
    anchor="nw",
    text=f"{wed} ",
    fill="#FFFFFF",
    font=("Montserrat Regular", 20 * -1)
)

canvas.create_text(
    251.0,
    339.0,
    anchor="nw",
    text=f"{thu} ",
    fill="#FFFFFF",
    font=("Montserrat Regular", 20 * -1)
)

canvas.create_text(
    251.0,
    364.0,
    anchor="nw",
    text=f"{fri} ",
    fill="#FFFFFF",
    font=("Montserrat Regular", 20 * -1)
)

canvas.create_text(
    251.0,
    389.0,
    anchor="nw",
    text=f"{sat} ",
    fill="#FFFFFF",
    font=("Montserrat Regular", 20 * -1)
)

canvas.create_text(
    251.0,
    416.0,
    anchor="nw",
    text=f"{sun} ",
    fill="#FFFFFF",
    font=("Montserrat Regular", 20 * -1)
)

canvas.create_text(
    694.0,
    397.0,
    anchor="nw",
    text=f"{bmi}",
    fill="#FFFFFF",
    font=("Montserrat Medium", 20 * -1)
)

#canvas.create_text(
#    643.0,
#    421.0,
#    anchor="nw",
#    text="Perfect!",
#    fill="#FFFFFF",
#    font=("Montserrat Medium", 20 * -1)
#)

canvas.create_rectangle(
    0.0,
    0.0,
    237.0,
    44.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    0.0,
    512.0,
    867.0,
    554.0,
    fill="#0C679B",
    outline="")

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    36.0,
    278.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    831.0,
    288.0,
    image=image_image_8
)

canvas.create_rectangle(
    222.0,
    0.0,
    867.0,
    56.0,
    fill="#0C679B",
    outline="")

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    429.0,
    42.0,
    image=image_image_9
)

canvas.tag_bind(image_9, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_9, "<B1-Motion>", move_window)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    433.0,
    523.0,
    image=image_image_10
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
    x=752.9273681640625,
    y=79.543701171875,
    width=26.41452407836914,
    height=29.49186897277832
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(eve=None),
    relief="flat"
)
button_2.place(
    x=644.0,
    y=462.0,
    width=112.0,
    height=20.0
)
window.resizable(False, False)
window.mainloop()
