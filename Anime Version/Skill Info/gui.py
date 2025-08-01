
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


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

check=False

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    get_stuff_path_str=pres_file_data["Anime"]["Mid Size Screen"]

def get_stuff_path(key):
    full_path=get_stuff_path_str+'/'+key
    return full_path

window = Tk()

initial_height = 0
target_height = 555
window_width = 898

window.geometry(f"{window_width}x{initial_height}")

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

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=50, delay=1)
thesystem.system.make_window_transparent(window, transp_clr)

window.configure(bg = "#FFFFFF")
set_data=thesystem.misc.return_settings()
transp_value=set_data["Settings"]["Transparency"]

window.attributes('-alpha',transp_value)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

with open("Files/Player Data/Settings.json", 'r') as settings_open:
    setting_data=ujson.load(settings_open)

# Preload top and bottom images
top_images = f"thesystem/{all_prev}top_bar"
bottom_images = f"thesystem/{all_prev}bottom_bar"

top_preloaded_images = thesystem.system.load_or_cache_images(top_images, (957, 43), job, type_="top")
bottom_preloaded_images = thesystem.system.load_or_cache_images(bottom_images, (1026, 47), job, type_="bottom")

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
    thesystem.system.animate_window_open(window, target_height, window_width, step=25, delay=1)

with open("Files/Temp Files/Skill Temp.csv", 'r') as csv_open:
    fr=csv.reader(csv_open)
    for k in fr:
        name=k[0]

desc1=desc2=desc3=desc4=''
segments = []
segment_length = 60

with open("Files/Player Data/Skill.json", 'r') as fson:
    data=ujson.load(fson)
    data_key=list(data.keys())
    for k in data_key:
        if k==name:
            lvl=data[k][0]["lvl"]
            typ=data[k][0]["type"]

            base=data[k][0]["base"]

            desc=data[k][0]["desc"]
            rewards=data[k][0]["rewards"]

            pl_points=data[k][0]["pl_point"]

            for i in range(0, len(desc), segment_length):
                segments.append(desc[i:i+segment_length])

            if len(segments) >= 1:
                desc1 = segments[0]
            if len(segments) >= 2:
                desc2 = segments[1]
            if len(segments) >= 3:
                desc3 = segments[2]
            if len(segments) >= 4:
                desc4 = segments[3]

main_lvl=lvl

# ? ===============================================================================

name1=name2=name3=name4='-'
o_name1=o_name2=o_name3=o_name4='-'
qt1=qt2=qt3=qt4=0
dicts={}

try:
    c=0
    reward_key=list(rewards.keys())
    for k in reward_key:
        if c==0:
            if k=="LVLADD":
                name1="Level Increase"
                o_name1=k
                qt1=data[name][0]["rewards"]["LVLADD"]
                c+=1
            elif k=="STRav":
                name1="Addition of STR, AGI, VIT, Available Points"
                o_name1=k
                qt1=data[name][0]["rewards"]["STRav"]
                c+=1
            elif k=="INTav":
                name1="Addition of INT, PER, MAN, Available Points"
                o_name1=k
                qt1=data[name][0]["rewards"]["INTav"]
                c+=1
            else:
                name1=k
                o_name1=k
                qt1=data[name][0]["rewards"][k]
            
            dicts[o_name1]=qt1

        elif c==1:
            if k=="LVLADD":
                name2="Level Increase"
                o_name2=k
                qt2=rewards=data[name][0]["rewards"]["LVLADD"]
                c+=1
            elif k=="STRav":
                name2="Addition of STR, AGI, VIT, Available Points"
                o_name2=k
                qt2=rewards=data[name][0]["rewards"]["STRav"]
                c+=1
            elif k=="INTav":
                name2="Addition of INT, PER, MAN, Available Points"
                o_name2=k
                qt2=rewards=data[name][0]["rewards"]["INTav"]
                c+=1
            else:
                name2=k
                o_name2=k
                qt2=data[name][0]["rewards"][k]

            dicts[o_name2]=qt2

        elif c==2:
            if k=="LVLADD":
                name3="Level Increase"
                o_name3=k
                qt3=rewards=data[name][0]["rewards"]["LVLADD"]
                c+=1
            elif k=="STRav":
                name3="Addition of STR, AGI, VIT, Available Points"
                o_name3=k
                qt3=rewards=data[name][0]["rewards"]["STRav"]
                c+=1
            elif k=="INTav":
                name3="Addition of INT, PER, MAN, Available Points"
                o_name3=k
                qt3=rewards=data[name][0]["rewards"]["INTav"]
                c+=1
            else:
                name3=k
                o_name3=k
                qt3=data[name][0]["rewards"][k]

            dicts[o_name3]=qt3

        elif c==3:
            if k=="LVLADD":
                name4="Level Increase"
                o_name4=k
                qt4=rewards=data[name][0]["rewards"]["LVLADD"]
                c+=1
            elif k=="STRav":
                name4="Addition of STR, AGI, VIT, Available Points"
                o_name4=k
                qt4=rewards=data[name][0]["rewards"]["STRav"]
                c+=1
            elif k=="INTav":
                name4="Addition of INT, PER, MAN, Available Points"
                o_name4=k
                qt4=rewards=data[name][0]["rewards"]["INTav"]
                c+=1
            else:
                name4=k
                o_name4=k
                qt4=data[name][0]["rewards"][k]

            dicts[o_name4]=qt4

except:
    print()

def delete():
    with open("Files/Player Data/Skill.json", 'r') as fols:
        skills=ujson.load(fols)

    del skills[name]

    with open("Files/Player Data/Skill.json", 'w') as fols:
        ujson.dump(skills, fols, indent=6)

    subprocess.Popen(['python', 'Anime Version/Skills Tab/gui.py'])

    window.quit()

def update():
    if lvl!="MAX":
        subprocess.Popen(['python', 'Anime Version/Skill Info/gui1.py'])

        window.quit()

def reward():
    rol=list(dicts.keys())
    for k in rol:
        if k=="LVLADD":
            for k in range(dicts[k]):
                with open("Files/Player Data/Status.json", 'r') as fson:
                    data_status=ujson.load(fson)
                    
                    data_status["status"][0]['level']+=1
                    data_status["status"][0]['str']+=1
                    data_status["status"][0]['agi']+=1
                    data_status["status"][0]['vit']+=1
                    data_status["status"][0]['int']+=1
                    data_status["status"][0]['per']+=1
                    data_status["status"][0]['hp']+=10
                    data_status["status"][0]['mp']+=10
                    data_status["status"][0]['fatigue_max']+=40
                
                with open("Files/Player Data/Status.json", 'w') as fson:
                    ujson.dump(data_status, fson, indent=4)

        elif k=="STRav":
            for k in range(dicts[k]):
                with open("Files/Player Data/Status.json", 'r') as fson:
                    data_status_2=ujson.load(fson)
                    
                    data_status_2["avail_eq"][0]['str_based']+=1

                with open("Files/Player Data/Status.json", 'w') as fson:
                    ujson.dump(data_status_2, fson, indent=4)

        elif k=="INTav":
            for k in range(dicts[k]):
                with open("Files/Player Data/Status.json", 'r') as fson:
                    data_status_3=ujson.load(fson)
                    
                    data_status_3["avail_eq"][0]['int_based']+=1

                with open("Files/Player Data/Status.json", 'w') as fson:
                    ujson.dump(data_status_3, fson, indent=4)

        else:
            check=False
            with open("Files/Data/Inventory_list.json", 'r') as fson:
                data_inv=ujson.load(fson)
                item=data_inv[k]
                name_of_item=k
            
            with open("Files/Player Data/Inventory.json", 'r') as fson:
                data_fininv=ujson.load(fson)
                key_data=list(data_fininv.keys())

                for k in key_data:
                    if name_of_item==k:
                        check=True
            
            if check==True:
                data_fininv[name_of_item][0]["qty"]+=1

            elif check==False:
                data_fininv[name_of_item]=item

            with open("Files/Player Data/Inventory.json", 'w') as finaladdon:
                ujson.dump(data_fininv, finaladdon, indent=6)

if main_lvl==10:
    new_lvl="MAX"
    data[name][0]["lvl"]=new_lvl

    main_lvl=new_lvl
    with open("Files/Player Data/Skill.json", 'w') as fin_skill:
        ujson.dump(data, fin_skill, indent=6)

    with open("Files/Player Data/Status.json", 'r') as status:
        status_data=ujson.load(status)

    if base=='STR':
        status_data["avail_eq"][0]['str_based']=status_data["avail_eq"][0]['str_based']+pl_points

    elif base=='INT':
        status_data["avail_eq"][0]['int_based']=status_data["avail_eq"][0]['int_based']+pl_points

    with open("Files/Player Data/Status.json", 'w') as fin_status:
        ujson.dump(status_data, fin_status, indent=4)

    reward()

def get_skill_img(name):
    path = f"Files\\Mod\\default\\Skills\\{name}.png"
    image = Image.open(path)
    image = image.resize((105, 105), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 555,
    width = 898,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=get_stuff_path("image_1.png"))
image_1 = canvas.create_image(
    450.0,
    277.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Anime"][video]  # Replace with your video path
    preloaded_frames=np.load(video_path)
player = thesystem.system.FastVideoPlayer(canvas, preloaded_frames, 450.0, 277.0, pause_duration=0.4)

image_image_2 = PhotoImage(
    file=get_stuff_path("frame.png"))
image_2 = canvas.create_image(
    449.0,
    283.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=get_stuff_path("skills_title.png"))
image_3 = canvas.create_image(
    449.023681640625,
    116.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=get_stuff_path("name_box.png"))
image_4 = canvas.create_image(
    513.6856384277344,
    225.34335327148438,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=get_stuff_path("image_box.png"))
image_5 = canvas.create_image(
    236.40396118164062,
    251.2617950439453,
    image=image_image_5
)

image_image_6 =get_skill_img(name)
image_6 = canvas.create_image(
    236.023681640625,
    251.0,
    image=image_image_6
)

canvas.create_text(
    326.023681640625,
    217.0,
    anchor="nw",
    text=name,
    fill="#FFFFFF",
    font=("Montserrat Regular", 16 * -1)
)

canvas.create_text(
    330.0,
    262.0,
    anchor="nw",
    text=f"Lvl.{lvl}",
    fill="#FFFFFF",
    font=("Montserrat Regular", 14 * -1)
)

image_image_7 = PhotoImage(
    file=get_stuff_path("box.png"))
image_7 = canvas.create_image(
    448.023681640625,
    308.0,
    image=image_image_7
)

canvas.create_text(
    330.023681640625,
    245.0,
    anchor="nw",
    text="Skill Level:",
    fill="#FFFFFF",
    font=("Montserrat SemiBold", 12 * -1)
)

canvas.create_text(
    481.023681640625,
    245.0,
    anchor="nw",
    text="Skill Type:",
    fill="#FFFFFF",
    font=("Montserrat SemiBold", 12 * -1)
)

canvas.create_text(
    481.0,
    262.0,
    anchor="nw",
    text=f"[{typ} Skill]",
    fill="#FFFFFF",
    font=("Montserrat Regular", 14 * -1)
)

canvas.create_text(
    326.0,
    304.0,
    anchor="nw",
    text=desc1,
    fill="#FFFFFF",
    font=("Montserrat Regular", 12 * -1)
)

canvas.create_text(
    326.0,
    321.0,
    anchor="nw",
    text=desc2,
    fill="#FFFFFF",
    font=("Montserrat Regular", 12 * -1)
)

canvas.create_text(
    326.0,
    321.0+17,
    anchor="nw",
    text=desc3,
    fill="#FFFFFF",
    font=("Montserrat Regular", 12 * -1)
)

canvas.create_text(
    326.0,
    321.0+34,
    anchor="nw",
    text=desc4,
    fill="#FFFFFF",
    font=("Montserrat Regular", 12 * -1)
)

button_image_1 = PhotoImage(
    file=get_stuff_path("return.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (subprocess.Popen(['python', 'Anime Version/Skills Tab/gui.py']),window.quit()),
    relief="flat"
)
button_1.place(
    x=786.023681640625,
    y=61.0,
    width=40.0,
    height=40.0
)

button_image_2 = PhotoImage(
    file=get_stuff_path("delete.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: delete(),
    relief="flat"
)
button_2.place(
    x=633.0,
    y=407.0,
    width=96.023681640625,
    height=16.0
)

button_image_3 = PhotoImage(
    file=get_stuff_path("upgrade.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:update(),
    relief="flat"
)
button_3.place(
    x=628.0,
    y=386.0,
    width=101.0,
    height=16.0
)

canvas.create_text(
    181.0,
    371.0,
    anchor="nw",
    text="REWARDS ON MAX:",
    fill="#10DF4A",
    font=("Montserrat SemiBold", 14 * -1)
)

button_image_4 = PhotoImage(
    file=get_stuff_path("gift.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: thesystem.system.set_preview_temp(o_name1, qt1),
    relief="flat"
)
button_4.place(
    x=181.0,
    y=390.0,
    width=13.0,
    height=13.0
)

canvas.create_text(
    194.0,
    388.0,
    anchor="nw",
    text=f"-{name1}",
    fill="#FFFFFF",
    font=("Montserrat Light", 12 * -1)
)

button_image_5 = PhotoImage(
    file=get_stuff_path("gift.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: thesystem.system.set_preview_temp(o_name2, qt2),
    relief="flat"
)
button_5.place(
    x=181.0,
    y=405.0,
    width=13.0,
    height=13.0
)

canvas.create_text(
    194.0,
    403.0,
    anchor="nw",
    text=f"-{name2}",
    fill="#FFFFFF",
    font=("Montserrat Light", 12 * -1)
)

side = PhotoImage(file=get_stuff_path("blue.png"))
if job.upper()!="NONE":
    side = PhotoImage(file=get_stuff_path("purple.png"))
canvas.create_image(35.0, 270.0, image=side)
canvas.create_image(890.0, 294.0, image=side)

canvas.create_rectangle(
    0.0,
    0.0,
    240.0,
    24.0,
    fill=transp_clr,
    outline="")

canvas.create_rectangle(
    0.0,
    513.0,
    925.0,
    555.0,
    fill=transp_clr,
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    957.0,
    36.0,
    fill=transp_clr,
    outline="")

image_40 = thesystem.system.side_bar("left_bar.png", (60, 490))
canvas.create_image(50.0, 270.0, image=image_40)

image_50 = thesystem.system.side_bar("right_bar.png", (60, 490))
canvas.create_image(870.0, 275.0, image=image_50)

image_index = 0
bot_image_index = 0

top_image = canvas.create_image(
    478.0,
    21.0,
    image=top_preloaded_images[image_index]
)

canvas.tag_bind(top_image, "<ButtonPress-1>", start_move)
canvas.tag_bind(top_image, "<B1-Motion>", move_window)

bottom_image = canvas.create_image(
    480.0,
    530.0,
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

# ! ============================================================
window.resizable(False, False)
window.mainloop()
