
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
# Fork by Venexs


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from datetime import datetime, timedelta, date
import ujson
import json
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
import thesystem.misc as misc
import thesystem.dailyquest as dailyquest
import thesystem.quests as quests

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    get_stuff_path_str=pres_file_data["Anime"]["Default"]

def get_stuff_path(key):
    full_path=get_stuff_path_str+'/'+key
    return full_path

window = Tk()
stop_event=threading.Event()

initial_height = 0
target_height = 449
window_width = 696

window.geometry(f"{window_width}x{initial_height}")

window.configure(bg = "#FFFFFF")
set_data=thesystem.misc.return_settings()
transp_value=set_data["Settings"]["Transparency"]

window.attributes('-alpha',transp_value)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

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

thesystem.system.center_window(window,window_width,target_height)
thesystem.system.animate_window_open(window, target_height, window_width, step=50, delay=1)


with open("Files/Player Data/Settings.json", 'r') as settings_open:
        setting_data=ujson.load(settings_open)

top_images = f"thesystem/{all_prev}top_bar"
bottom_images = f"thesystem/{all_prev}bottom_bar"

top_preloaded_images = thesystem.system.load_or_cache_images(top_images, (695, 39), job, type_="top")
bottom_preloaded_images = thesystem.system.load_or_cache_images(bottom_images, (702, 36), job, type_="bottom")

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
    thesystem.system.animate_window_close(window, 0, window_width, step=20, delay=1)

with open("Files\Temp Files\Quest Rewards.json", "r") as file:
    data = ujson.load(file)
    quest_rewards = data["Type"]

rew1=rew2=rew3=rew4=''
rew1_name=rew2_name=rew3_name=rew4_name=''

c=0

if data["Type"] == "Daily":
    reward, type_re = dailyquest.get_check_rew()
    rank = dailyquest.get_rank()
    streak=dailyquest.get_streak()
    title, list_of_titles_data = dailyquest.get_titles()

    with open("Files/Player Data/Status.json", 'r') as rank_check_file:
        rank_check_data=json.load(rank_check_file)

    if type_re=="Reward":
        with open("Files/Data/Rank_Rewards.json", 'r') as final_rank_check_file:
            final_rank_check_data=json.load(final_rank_check_file)
            rew_list=final_rank_check_data[rank]

            av_str=av_int=rew_list[0]
            xp_pl=rew_list[1]
            coins=rew_list[2]

    elif type_re=='Secret':
        with open("Files/Data/Rank_Rewards.json", 'r') as final_rank_check_file:
            final_rank_check_data=json.load(final_rank_check_file)
            rew_list=final_rank_check_data[rank]

            av_str=av_int=(rew_list[0]*2)
            xp_pl=(rew_list[1]*2)
            coins=(rew_list[2]*2)

    elif type_re=='Great Reward':
        with open("Files/Player Data/Daily_Quest.json", 'r') as daily_quest_file:
            daily_quest_data = json.load(daily_quest_file)
            gr_streak=daily_quest_data["Streak"]["Greater_value"]
        
        great_rank=False
        if gr_streak>=3:
            cr=3
        else:
            cr=2

        with open("Files/Data/Rank_Rewards.json", 'r') as final_rank_check_file:
            final_rank_check_data=json.load(final_rank_check_file)
            rew_list=final_rank_check_data[rank]

            av_str=av_int=(rew_list[0]*cr)
            xp_pl=(rew_list[1]*cr)
            coins=(rew_list[2]*cr)
        
        if cr==3:
            great_rank=True

    elif type_re=="Preview":
        with open("Files/Data/Rank_Rewards.json", 'r') as final_rank_check_file:
            final_rank_check_data=json.load(final_rank_check_file)
            rew_list=final_rank_check_data[rank]

            av_str=av_int=rew_list[0]
            xp_pl=rew_list[1]
            coins=rew_list[2]

    rew1_name="INT. Based Points"
    rew2_name="STR. Based Points"

    rew1=av_int
    rew2=av_str
    rew3_name=f"Experience Points: {xp_pl}"
    rew3=1
    rew4_name=f"Coins: {coins}"
    rew4=1

    c=4

    def get():
        today = date.today()
        today_date_str = today.strftime("%Y-%m-%d")

        with open("Files/Player Data/Status.json", 'w') as status_import:
            rank_check_data["status"][0]['coins']+=coins
            rank_check_data["status"][0]['XP']+=xp_pl
            rank_check_data["avail_eq"][0]['str_based']+=av_str
            rank_check_data["avail_eq"][0]['int_based']+=av_int
            rank_check_data["status"][0]["fatigue"]+=thesystem.system.give_fatigue_from_rank(rank)
            json.dump(rank_check_data, status_import, indent=4)

        with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as Daily_date_check_file:
            fw=csv.writer(Daily_date_check_file)
            fw.writerow([today_date_str, "True", "Complete"])

    def secret_get():
        today = date.today()
        today_date_str = today.strftime("%Y-%m-%d")

        with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as Daily_date_check_file:
            fw=csv.writer(Daily_date_check_file)
            fw.writerow([today_date_str, "True", "Complete"])

        dupli_title=False
        try:
            with open("Files/Player Data/Titles.json", 'r') as title_import:
                title_import_data=json.load(title_import)
                title_import_data_list=list(title_import_data.keys())
                for k in title_import_data_list:
                    if k==title:
                        dupli_title=True
        except:
            dupli_title=False

        if dupli_title==True:
            thesystem.system.message_open("Title Exists")

        else:
            try:
                with open("Files/Player Data/Titles.json", 'r') as title_import:
                    title_import_data=json.load(title_import)
            except:
                title_import_data={}
            
            title_import_data[title]=list_of_titles_data[title]
            
            with open("Files/Player Data/Titles.json", 'w') as final_title_import:
                json.dump(title_import_data, final_title_import, indent=4)

        with open("Files/Player Data/Status.json", 'w') as status_import:
            rank_check_data["status"][0]['coins']+=coins
            rank_check_data["avail_eq"][0]['str_based']+=av_str
            rank_check_data["avail_eq"][0]['int_based']+=av_int
            rank_check_data["status"][0]['XP']+=xp_pl
            rank_check_data["status"][0]["fatigue"]+=(thesystem.system.give_fatigue_from_rank(rank)*2)
            json.dump(rank_check_data, status_import, indent=4)

        with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as Daily_date_check_file:
            fw=csv.writer(Daily_date_check_file)
            fw.writerow([today_date_str, "True", "Complete"])

    def great_get():
        today = date.today()
        today_date_str = today.strftime("%Y-%m-%d")

        with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as Daily_date_check_file:
            fw=csv.writer(Daily_date_check_file)
            fw.writerow([today_date_str, "True", "Complete"])

        dupli_title=False
        try:
            with open("Files/Player Data/Titles.json", 'r') as title_import:
                title_import_data=json.load(title_import)
                title_import_data_list=list(title_import_data.keys())
                for k in title_import_data_list:
                    if k=="Blessed":
                        dupli_title=True
        except:
            dupli_title=False

        if dupli_title==True:
            thesystem.system.message_open("Title Exists")

        else:
            try:
                with open("Files/Player Data/Titles.json", 'r') as title_import:
                    title_import_data=json.load(title_import)
            except:
                title_import_data={}
            
            title_import_data["Blessed"]=list_of_titles_data["Blessed"]
            
            with open("Files/Player Data/Titles.json", 'w') as final_title_import:
                json.dump(title_import_data, final_title_import, indent=4)

        with open("Files/Player Data/Status.json", 'w') as status_import:
            rank_check_data["status"][0]['coins']+=coins
            rank_check_data["avail_eq"][0]['str_based']+=av_str
            rank_check_data["avail_eq"][0]['int_based']+=av_int
            rank_check_data["status"][0]['XP']+=xp_pl
            rank_check_data["status"][0]["fatigue"]+=(thesystem.system.give_fatigue_from_rank(rank)*2)
            json.dump(rank_check_data, status_import, indent=4)

        with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as Daily_date_check_file:
            fw=csv.writer(Daily_date_check_file)
            fw.writerow([today_date_str, "True", "Complete"])

    if type_re=='Secret':
        secret_get()
    elif type_re=='Great Reward':
        great_get()
    else:
        get()

elif data["Type"]=="Quest":
    try:
        names=list(data["Rewards"])
        rew1_name=names[0]
        rew1=data["Rewards"][rew1_name]
        c+=1
        rew2_name=names[1]
        rew2=data["Rewards"][rew2_name]
        c+=1
        rew3_name=names[2]
        rew3=data["Rewards"][rew3_name]
        c+=1
        rew4_name=names[3]
        rew4=data["Rewards"][rew4_name]
        c+=1
    except:
        pass

if rew1_name=='': state1='hidden' 
else: state1='normal'
if rew2_name=='': state2='hidden'
else: state2='normal'
if rew3_name=='': state3='hidden'
else: state3='normal'
if rew4_name=='': state4='hidden'
else: state4='normal'

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
    file=get_stuff_path("backgroud.png"))
image_1 = canvas.create_image(
    609.0,
    301.0,
    image=image_image_1
)

pres_file_data=misc.load_ujson("Files/Mod/presets.json")
video_path=pres_file_data["Anime"][video]
preloaded_frames=np.load(video_path)
player = thesystem.system.FastVideoPlayer(canvas, preloaded_frames, 478.0, 313.0, pause_duration=1.0)

image_image_2 = PhotoImage(
    file=get_stuff_path("frame.png"))
image_2 = canvas.create_image(
    348.0,
    233.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=get_stuff_path("alert.png"))
image_3 = canvas.create_image(
    379.0,
    94.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=get_stuff_path("!.png"))
image_4 = canvas.create_image(
    186.0,
    94.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=get_stuff_path("new items.png"))
image_5 = canvas.create_image(
    348.0,
    162.0,
    image=image_image_5,
)

image_image_6 = quests.get_item_image(rew1_name)
image_6 = canvas.create_image(
    145.0-1,
    235.5-0.5,
    image=image_image_6,
    state=state1
)

canvas.create_text(
    170.0,
    232.0,
    anchor="nw",
    text=f"[{rew1_name}]",
    fill="#FFFFFF",
    font=("Montserrat Bold", 11 * -1),
    state=state1
)

canvas.create_text(
    170.0+3,
    210.0,
    anchor="nw",
    text=f"{rew1}",
    fill="#FFFFFF",
    font=("Montserrat Bold", 11 * -1),
    state=state1
)

if c>=1:
    canvas.create_text(
        295.0,
        245.0,
        anchor="nw",
        text="New!",
        fill="#FFFFFF",
        font=("Montserrat Medium", 11 * -1),
        state=state1
    )

image_image_7 = PhotoImage(
    file=get_stuff_path("new item frame.png"))
image_7 = canvas.create_image(
    223.0,
    235.0,
    image=image_image_7,
    state=state1
)

image_image_8 =quests.get_item_image(rew3_name)
image_8 = canvas.create_image(
    145.0-1,
    314.5-0.5,
    image=image_image_8,
    state=state3
)

canvas.create_text(
    170.0,
    311.0,
    anchor="nw",
    text=f"[{rew3_name}]",
    fill="#FFFFFF",
    font=("Montserrat Bold", 11 * -1),
    state=state3
)

canvas.create_text(
    170.0+3,
    210.0+79,
    anchor="nw",
    text=f"{rew3}",
    fill="#FFFFFF",
    font=("Montserrat Bold", 11 * -1),
    state=state3
)

if c>=3:
    canvas.create_text(
        295.0,
        324.0,
        anchor="nw",
        text="New!",
        fill="#FFFFFF",
        font=("Montserrat Medium", 11 * -1),
        state=state3
    )

image_image_9 = PhotoImage(
    file=get_stuff_path("new item frame.png"))
image_9 = canvas.create_image(
    223.0,
    314.0,
    image=image_image_9,
    state=state3
)

image_image_10 = quests.get_item_image(rew2_name)
image_10 = canvas.create_image(
    393.0-1,
    235.5-0.5,
    image=image_image_10,
    state=state2
)

canvas.create_text(
    415.0,
    232.0,
    anchor="nw",
    text=f"[{rew2_name}]",
    fill="#FFFFFF",
    font=("Montserrat Bold", 11 * -1),
    state=state2
)

canvas.create_text(
    170.0+251,
    210.0,
    anchor="nw",
    text=f"{rew2}",
    fill="#FFFFFF",
    font=("Montserrat Bold", 11 * -1),
    state=state2
)

if c>=2:
    canvas.create_text(
        543.0,
        245.0,
        anchor="nw",
        text="New!",
        fill="#FFFFFF",
        font=("Montserrat Medium", 11 * -1),
        state=state2
    )

image_image_11 = PhotoImage(
    file=get_stuff_path("new item frame.png"))
image_11 = canvas.create_image(
    471.1288757324219,
    235.0,
    image=image_image_11,
    state=state2
)

image_image_12 =quests.get_item_image(rew4_name)
image_12 = canvas.create_image(
    393.0-1,
    314.5-0.5,
    image=image_image_12,
    state=state4
)

canvas.create_text(
    415.0,
    311.0,
    anchor="nw",
    text=f"[{rew4_name}]",
    fill="#FFFFFF",
    font=("Montserrat Bold", 11 * -1),
    state=state4
)

canvas.create_text(
    170.0+251,
    210.0+79,
    anchor="nw",
    text=f"{rew4}",
    fill="#FFFFFF",
    font=("Montserrat Bold", 11 * -1),
    state=state4
)

if c>=4:
    canvas.create_text(
        543.0,
        324.0,
        anchor="nw",
        text="New!",
        fill="#FFFFFF",
        font=("Montserrat Medium", 11 * -1),
        state=state4
    )

image_image_13 = PhotoImage(
    file=get_stuff_path("new item frame.png"))
image_13 = canvas.create_image(
    471.1288757324219,
    314.49151611328125,
    image=image_image_13,
    state=state4
)

canvas.create_rectangle(
    0.0,
    0.0,
    696.0,
    29.0,
    fill=transp_clr,
    outline="")

canvas.create_rectangle(
    0.0,
    5.0,
    60.0,
    455.0,
    fill=transp_clr,
    outline="")

canvas.create_rectangle(
    647.0,
    0.0,
    696.0,
    458.0,
    fill=transp_clr,
    outline="")

canvas.create_rectangle(
    119.0,
    0.0,
    381.0,
    38.0,
    fill=transp_clr,
    outline="")

canvas.create_rectangle(
    56.0,
    421.0,
    923.0,
    460.0,
    fill=transp_clr,
    outline="")

canvas.create_rectangle(
    50.0,
    19.0,
    643.0,
    44.0,
    fill=transp_clr,
    outline="")

canvas.create_rectangle(
    137.0,
    -10.0,
    765.0,
    50.0,
    fill=transp_clr,
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

update_thread = threading.Thread(target=update_images)
update_thread.start()

button_image_2 = PhotoImage(
    file=get_stuff_path("close.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(window),
    relief="flat"
)
button_2.place(
    x=564.0,
    y=52.0,
    width=23.0,
    height=23.0
)
window.resizable(False, False)
window.mainloop()
