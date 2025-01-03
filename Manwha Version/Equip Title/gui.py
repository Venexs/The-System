
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import cv2
from PIL import Image, ImageTk
import subprocess
import json
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
    win.quit()

def color(name):
    if name=="False Ranker":
        color="#FF2F2F"
    elif name=="One Above All":
        color="#FFCF26"
    else:
        color="#FFFFFF"

    return color

name1=name2=name3=name4=name5=name6=name7=name8=name9=name10=name11=name12=name13=''
rank1=rank2=rank3=rank4=rank5=rank6=rank7=rank8=rank9=rank10=rank11=rank12=rank13='X'
c=0

def final(name0):
    if name0!='':
        with open("Files\Status.json", 'r') as fina_read_fson:
            fina_read_data=json.load(fina_read_fson)

        if fina_read_data["status"][1]["title_bool"]!="True":
            stat_val_add=data[name0]["Statbuff"]

            fina_read_data["status"][0]['str']=fina_read_data["status"][0]['str']+stat_val_add
            fina_read_data["status"][0]['agi']=fina_read_data["status"][0]['agi']+stat_val_add
            fina_read_data["status"][0]['vit']=fina_read_data["status"][0]['vit']+stat_val_add
            fina_read_data["status"][0]['int']=fina_read_data["status"][0]['int']+stat_val_add
            fina_read_data["status"][0]['per']=fina_read_data["status"][0]['per']+stat_val_add
            fina_read_data["status"][0]['man']=fina_read_data["status"][0]['man']+stat_val_add

            fina_read_data["status"][1]['title_bool']="True"
            fina_read_data["status"][1]['title']=name0

            with open("Files/status.json", 'w') as fina_write_fson:
                json.dump(fina_read_data, fina_write_fson, indent=4)

            subprocess.Popen(['python', 'Manwha Version/Status Tab/gui.py'])

            window.quit()

        elif fina_read_data["status"][1]["title_bool"]=="True":
            old_name=fina_read_data["status"][1]['title']
            old_str_val_sub=data[old_name]["Statbuff"]

            stat_val_add=data[name0]["Statbuff"]

            fina_read_data["status"][0]['str']=fina_read_data["status"][0]['str']+stat_val_add-old_str_val_sub
            fina_read_data["status"][0]['agi']=fina_read_data["status"][0]['agi']+stat_val_add-old_str_val_sub
            fina_read_data["status"][0]['vit']=fina_read_data["status"][0]['vit']+stat_val_add-old_str_val_sub
            fina_read_data["status"][0]['int']=fina_read_data["status"][0]['int']+stat_val_add-old_str_val_sub
            fina_read_data["status"][0]['per']=fina_read_data["status"][0]['per']+stat_val_add-old_str_val_sub
            fina_read_data["status"][0]['man']=fina_read_data["status"][0]['man']+stat_val_add-old_str_val_sub

            fina_read_data["status"][1]['title_bool']="True"
            fina_read_data["status"][1]['title']=name0

            with open("Files/status.json", 'w') as fina_write_fson:
                json.dump(fina_read_data, fina_write_fson, indent=4)

            subprocess.Popen(['python', 'Manwha Version/Status Tab/gui.py'])

            subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
            window.quit()

with open("Files\Titles\Titles.json", 'r') as fson:
    data=json.load(fson)
    data_key=list(data.keys())
    try:
        for k in data_key:
            if c==0:
                name1=k
                rank1=data[k]["Rank"]
                c+=1
            elif c==1:
                name2=k
                rank2=data[k]["Rank"]
                c+=1
            elif c==2:
                name3=k
                rank3=data[k]["Rank"]
                c+=1
            elif c==3:
                name4=k
                rank4=data[k]["Rank"]
                c+=1
            elif c==4:
                name5=k
                rank5=data[k]["Rank"]
                c+=1
            elif c==5:
                name6=k
                rank6=data[k]["Rank"]
                c+=1
            elif c==6:
                name7=k
                rank7=data[k]["Rank"]
                c+=1
            elif c==7:
                name8=k
                rank8=data[k]["Rank"]
                c+=1
            elif c==8:
                name9=k
                rank9=data[k]["Rank"]
                c+=1
            elif c==9:
                name10=k
                rank10=data[k]["Rank"]
                c+=1
            elif c==10:
                name11=k
                rank11=data[k]["Rank"]
                c+=1
            elif c==11:
                name12=k
                rank12=data[k]["Rank"]
                c+=1
            elif c==12:
                name13=k
                rank13=data[k]["Rank"]
                c+=1

    except:
        print("", end='')

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

window = Tk()

initial_height = 0
target_height = 288
window_width = 555

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.make_window_transparent(window)
thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)

window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 288,
    width = 555,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    794.0,
    448.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 200.0, 150.0, resize_factor=1)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    277.0,
    144.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    119.0,
    70.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    280.0,
    123.0,
    image=image_image_4
)

canvas.create_text(
    68.0,
    112.0,
    anchor="nw",
    text=name1.upper(),
    fill=color(name1),
    font=("Exo Medium", 18 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: final(name1),
    relief="flat"
)
button_1.place(
    x=481.0,
    y=111.0,
    width=24.0,
    height=24.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    280.0,
    251.0,
    image=image_image_5
)

canvas.create_text(
    68.0,
    240.0,
    anchor="nw",
    text=name5.upper(),
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: final(name5),
    relief="flat"
)
button_2.place(
    x=481.0,
    y=239.0,
    width=24.0,
    height=24.0
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    280.0,
    219.0,
    image=image_image_6
)

canvas.create_text(
    68.0,
    208.0,
    anchor="nw",
    text=name4.upper(),
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: final(name4),
    relief="flat"
)
button_3.place(
    x=481.0,
    y=207.0,
    width=24.0,
    height=24.0
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    280.0,
    187.0,
    image=image_image_7
)

canvas.create_text(
    68.0,
    176.0,
    anchor="nw",
    text=name3.upper(),
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: final(name3),
    relief="flat"
)
button_4.place(
    x=481.0,
    y=175.0,
    width=24.0,
    height=24.0
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    280.0,
    155.0,
    image=image_image_8
)

canvas.create_text(
    68.0,
    144.0,
    anchor="nw",
    text=name2.upper(),
    fill="#FFD337",
    font=("Exo Medium", 18 * -1)
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: final(name2),
    relief="flat"
)
button_5.place(
    x=481.0,
    y=143.0,
    width=24.0,
    height=24.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(window),
    relief="flat"
)
button_6.place(
    x=505.0,
    y=30.0,
    width=21.407020568847656,
    height=20.974361419677734
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    280.0,
    28.0,
    image=image_image_9
)

canvas.tag_bind(image_9, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_9, "<B1-Motion>", move_window)

window.resizable(False, False)
window.mainloop()
