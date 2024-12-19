from pathlib import Path
import json
import csv
import subprocess
import threading
import os
import sys
from datetime import datetime, timedelta
from tkinter import Tk, Canvas, PhotoImage

# Set up paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)
import thesystem.system

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

# Window Configuration
window = Tk()
window.geometry("488x0")  # Initial collapsed height
window.configure(bg="#FFFFFF")
window.attributes('-alpha', 0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
thesystem.system.make_window_transparent(window)

# Animate window open
window_width = 488
target_height = 716
thesystem.system.animate_window_open(window, target_height, window_width, step=40, delay=1)

# Load JSON data once to reduce file I/O
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

status_data = load_json("Files/status.json")
job_data = load_json("Files/Data/Job_info.json")
presets_data = load_json("Files/Mod/presets.json")

# Helper Functions
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def update_tabs_json(status='Open'):
    tabs_json_path = "Files/Tabs.json"
    with open(tabs_json_path, 'r+') as tab_json:
        tab_data = json.load(tab_json)
        tab_data["Status"] = status
        tab_json.seek(0)
        json.dump(tab_data, tab_json, indent=4)
        tab_json.truncate()

# Window Movement
def start_move(event):
    global lastx, lasty
    lastx, lasty = event.x_root, event.y_root

def move_window(event):
    global lastx, lasty
    x = window.winfo_x() + (event.x_root - lastx)
    y = window.winfo_y() + (event.y_root - lasty)
    window.geometry(f"+{x}+{y}")
    lastx, lasty = event.x_root, event.y_root

# Update and Close Functions
def ex_close(event=None):
    update_tabs_json('Close')
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, 0, window_width, step=20, delay=1)

def start_job(event):
    with open("Files/status.json", 'r') as fson:
        data=json.load(fson)
        name=data["status"][0]['name'].upper()
        # ? =================================================
        hp=data["status"][0]['hp']
        mp=data["status"][0]['mp']
        lvl=data["status"][0]['level']
        old_lvl=f"{lvl:02d}"
        # ? =================================================
        stre=data["status"][0]['str']
        stre=thesystem.system.three_val(stre)

        intel=data["status"][0]['int']
        intel=thesystem.system.three_val(intel)

        agi=data["status"][0]['agi']
        agi=thesystem.system.three_val(agi)

        vit=data["status"][0]['vit']
        vit=thesystem.system.three_val(vit)

        per=data["status"][0]['per']
        per=thesystem.system.three_val(per)

        man=data["status"][0]['man']
        man=thesystem.system.three_val(man)
        # ? =================================================
        tit=data["status"][1]['title']
        job=data["status"][1]['job'].upper()
        # ? =================================================
        xp_str=data["status"][0]['XP']
        coins=data["status"][0]['coins']

        fatigue_max=data["status"][0]['fatigue_max']
        fatigue=data["status"][0]['fatigue']

        fat_val=(fatigue/fatigue_max)*100
        # ? =================================================
        av_str_based=data["avail_eq"][0]['str_based']
        av_str_based=thesystem.system.three_val(av_str_based)
        av_int_based=data["avail_eq"][0]['int_based']
        av_int_based=thesystem.system.three_val(av_int_based)
        # ? =================================================
        str_buff=data["equipment"][0]["STR"]
        str_buff=thesystem.system.sign(str_buff)+thesystem.system.pos_fix(str_buff)

        agi_buff=data["equipment"][0]["AGI"]
        agi_buff=thesystem.system.sign(agi_buff)+thesystem.system.pos_fix(agi_buff)

        vit_buff=data["equipment"][0]["VIT"]
        vit_buff=thesystem.system.sign(vit_buff)+thesystem.system.pos_fix(vit_buff)

        int_buff=data["equipment"][0]["INT"]
        int_buff=thesystem.system.sign(int_buff)+thesystem.system.pos_fix(int_buff)

        per_buff=data["equipment"][0]["PER"]
        per_buff=thesystem.system.sign(per_buff)+thesystem.system.pos_fix(per_buff)

        man_buff=data["equipment"][0]["MAN"]
        man_buff=thesystem.system.sign(man_buff)+thesystem.system.pos_fix(man_buff)
        # ? =================================================

    with open("Files/Data/Job_info.json", 'r') as stat_fson:
        data=json.load(stat_fson)

    canvas.itemconfig("Job", state="hidden")
    data["status"][0]["job_active"]='True'

    data["status"][1]["plSTR"]=int(stre)
    data["status"][1]["plINT"]=int(intel)
    data["status"][1]["plAGI"]=int(agi)
    data["status"][1]["plVIT"]=int(vit)
    data["status"][1]["plPER"]=int(per)
    data["status"][1]["plMAN"]=int(man)

    with open("Files\Temp Files\Job_Change Date.csv", 'w', newline='') as time_open_csv_file:
        fw=csv.writer(time_open_csv_file)
        current_date = datetime.now()
        # Add 10 days to the current date
        future_date = current_date + timedelta(days=1)
        # Define the desired format for the date string
        date_format = "%Y-%m-%d"
        # Convert the future date to a string
        future_date_string = future_date.strftime(date_format)
        fw.writerow([future_date_string])

    with open("Files/Data/Job_info.json", 'w') as fson:
        json.dump(data, fson, indent=4)

# Title color assignment
def title_color(name):
    color_map = {"False Ranker": "#FF2F2F", "One Above All": "#FFCF26"}
    return color_map.get(name, "#FFFFFF")

# Initialize Canvas and Widgets
canvas = Canvas(window, bg="#FFFFFF", height=716, width=488, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

# Load images once to avoid redundant processing
images = {
    "background": PhotoImage(file=relative_to_assets("image_1.png")),
    "stats": [
        PhotoImage(file=relative_to_assets(f"image_{i}.png")) for i in range(2, 6)
    ]
}

# Background image and character attributes
canvas.create_image(430.0, 363.0, image=images["background"])
player = thesystem.system.VideoPlayer(canvas, presets_data["Anime"]["Video"], 430.0, 363.0)

# Display Character Status
name, hp, mp, lvl = status_data["status"][0]["name"].upper(), status_data["status"][0]["hp"], status_data["status"][0]["mp"], status_data["status"][0]["level"]
job, title = status_data["status"][1]["job"].upper(), status_data["status"][1]["title"]

canvas.create_text(322.0, 225.0, anchor="nw", text="LEVEL", fill="#FFFFFF", font=("Montserrat Regular", 24 * -1))
canvas.create_text(328.0, 164.0, anchor="nw", text=f"{lvl:02d}", fill="#FFFFFF", font=("Montserrat Bold", 60 * -1))
canvas.create_text(55.0, 199.0, anchor="nw", text="JOB:", fill="#FFFFFF", font=("Montserrat Bold", 20 * -1))
canvas.create_text(107.0, 200.0, anchor="nw", text=job, fill="#FFFFFF", font=("Montserrat Regular", 18 * -1))
canvas.create_text(122.0, 234.0, anchor="nw", text=title.upper(), fill=title_color(title), font=("Montserrat Regular", 18 * -1))

# Stat Display (STR, INT, etc.) with buffs
stat_attributes = ["str", "int", "agi", "vit", "per", "man"]
stat_text_widgets = {}

for i, stat in enumerate(stat_attributes):
    value = status_data["status"][0][stat]
    buff = status_data["equipment"][0].get(stat.upper(), 0)
    position = (104 if i < 3 else 282, 392 + (i % 3) * 55)

    stat_text_widgets[stat] = canvas.create_text(*position, anchor="nw", text=value, fill="#FFFFFF", font=("Montserrat SemiBold", 20 * -1))
    canvas.create_text(position[0] + 39, position[1] + 6, anchor="nw", text=f"({thesystem.system.sign(buff)+thesystem.system.pos_fix(buff)})", fill="#34FF48", font=("Montserrat Regular", 13 * -1))

# Assign stat updating functions
def update_stat(stat_name):
    available_points = job_data["avail_eq"][0]["str_based"] if stat_name in ["str", "agi", "vit"] else job_data["avail_eq"][0]["int_based"]
    if available_points > 0:
        status_data["status"][0][stat_name] += 1
        canvas.itemconfig(stat_text_widgets[stat_name], text=status_data["status"][0][stat_name])
        job_data["avail_eq"][0]["str_based" if stat_name in ["str", "agi", "vit"] else "int_based"] -= 1

stat_buttons = {
    stat: PhotoImage(file=relative_to_assets("button_1.png"))
    for stat in stat_attributes
}
for stat in stat_attributes:
    canvas.create_image(
        188.0 if stat in ["str", "int", "agi"] else 364.0, 
        408.0 + (stat_attributes.index(stat) % 3) * 54, 
        image=stat_buttons[stat], 
        tags=stat
    )
    canvas.tag_bind(stat, "<ButtonPress-1>", lambda e, s=stat: update_stat(s))

# Bind move and close functions
window.bind("<Button-1>", start_move)
window.bind("<B1-Motion>", move_window)
window.bind("<Escape>", ex_close)

# Update JSON for open tabs and start background processes
update_tabs_json()
subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])

window.mainloop()
