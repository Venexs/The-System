
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import csv
import ujson
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
import thesystem.equipmentbk
import thesystem.equipmentbk as equipment
import thesystem.inventory

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

with open("Files/Player Data/Tabs.json",'r') as tab_son:
    tab_son_data=ujson.load(tab_son)

with open("Files/Player Data/Tabs.json",'w') as fin_tab_son:
    tab_son_data["Equipment"]='Open'
    ujson.dump(tab_son_data,fin_tab_son,indent=4)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

subprocess.Popen(['python', 'Files/Mod/default/sfx.py'])

initial_height = 0
target_height = 479
window_width = 802

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.make_window_transparent(window)
thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)

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


def ex_close():
    with open("Files/Player Data/Tabs.json",'r') as tab_son:
        tab_son_data=ujson.load(tab_son)

    if tab_son_data["Equipment"]=='Open':

        with open("Files/Player Data/Tabs.json",'w') as fin_tab_son:
            tab_son_data["Equipment"]='Close'
            ujson.dump(tab_son_data,fin_tab_son,indent=4)

    #threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, target_height, window_width, step=20, delay=1)

def split_text(text, segment_length):
    # Check if the text length exceeds the segment length
    if len(text) > segment_length:
        # Find the last space within the segment length to avoid splitting a word
        split_point = text.rfind(" ", 0, segment_length)
        
        # If there's no space, we have to split at the exact segment length
        if split_point == -1:
            split_point = segment_length
        
        # Split text at the identified point
        part1 = text[:split_point]
        part2 = text[split_point:].lstrip()  # Remove leading spaces in part2
    else:
        # If text is within the segment length, assign it all to part1 and leave part2 empty
        part1 = text
        part2 = ""
    
    return part1, part2

def open_select(cat):
    fout=open('Files/Temp Files/Equipment Temp.csv', 'w', newline='')
    fw=csv.writer(fout)
    rec=[cat]
    fw.writerow(rec)
    fout.close()

    subprocess.Popen(['python', 'Manwha Version/Equip Item/gui.py'])

    ex_close()

def set_effect_open():
    subprocess.Popen(['python', 'Manwha Version/Set Effects/gui.py'])

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 479,
    width = 802,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    538.0,
    563.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
    preloaded_frames=np.load(video_path)
player = thesystem.system.FastVideoPlayer(canvas, preloaded_frames, 370.0, 200.0, resize_factor=1)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    400.0,
    239.0,
    image=image_image_2
)



# ! ============================================================================
# ! INFO ujson RETREVAL
# ! ============================================================================


helm = chest = f_gaun = s_gaun = boot = ring = collar = '-'
helmboost_1 = helmboost_2 = ''
chestboost_1 = chestboost_2 = ''
f_gaunboost_1 = f_gaunboost_2 = ''
s_gaunboost_1 = s_gaunboost_2 = ''
bootboost_1 = bootboost_2 = ''
ringboost_1 = ringboost_2 = ''
collarboost_1 = collarboost_2 = ''

max_width, max_height = 164/1.5, 126/1.5

def assign_equipment(equipment_list):
    global helm, chest, f_gaun, s_gaun, boot, ring, collar
    global helmboost_1, helmboost_2, chestboost_1, chestboost_2
    global f_gaunboost_1, f_gaunboost_2, s_gaunboost_1, s_gaunboost_2
    global bootboost_1, bootboost_2, ringboost_1, ringboost_2
    global collarboost_1, collarboost_2

    # Unpack equipment items and boosts from the list
    equipment_items, equipment_boosts = equipment_list

    # Assign values to the equipment variables
    helm, chest, f_gaun, s_gaun, boot, ring, collar = equipment_items
    helmboost_1, helmboost_2, chestboost_1, chestboost_2, f_gaunboost_1, f_gaunboost_2, s_gaunboost_1, s_gaunboost_2, bootboost_1, bootboost_2, ringboost_1, ringboost_2, collarboost_1, collarboost_2 = equipment_boosts

equipment_list=equipment.get_equipment()
assign_equipment(equipment_list)

image_image_3 = PhotoImage( 
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    401.0,
    234.0,
    image=image_image_3
)

boot_image = (thesystem.equipmentbk.get_armor_image(boot))
boot_im = canvas.create_image(
    401.0,
    234.0,
    image=boot_image
)

sgaun_image = (thesystem.equipmentbk.get_armor_image(s_gaun))
sgaun_im = canvas.create_image(
    401.0,
    234.0,
    image=sgaun_image
)

fgaun_image = (thesystem.equipmentbk.get_armor_image(f_gaun))
fgaun_im = canvas.create_image(
    401.0,
    234.0,
    image=fgaun_image
)

ring_image = (thesystem.equipmentbk.get_armor_image(ring))
ring_im = canvas.create_image(
    401.0,
    234.0,
    image=ring_image
)

helm_image = (thesystem.equipmentbk.get_armor_image(helm))
helm_im = canvas.create_image(
    401.0,
    234.0,
    image=helm_image
)

chest_image = (thesystem.equipmentbk.get_armor_image(chest))
chest_im = canvas.create_image(
    401.0,
    234.0,
    image=chest_image
)

collar_image = (thesystem.equipmentbk.get_armor_image(collar))
collar_im = canvas.create_image(
    401.0,
    234.0,
    image=collar_image
)


canvas.create_text(
    21.0,
    25.0,
    anchor="nw",
    text="EQUIPMENT",
    fill="#FFD337",
    font=("Exo Bold", 32 * -1)
)

# ? ====================================================================
# ? Helmet Part
# ? ====================================================================

image_image_4 = thesystem.inventory.get_item_button_image(helm, max_width, max_height)
image_4 = canvas.create_image(
    86.0,
    145.0,
    image=image_image_4
)

canvas.create_text(
    133.0,
    138.0,
    anchor="nw",
    text=f"[{helm}]",
    fill="#FFFFFF",
    font=("Exo Bold", 11 * -1)
)

canvas.create_text(
    133.0,
    152.0,
    anchor="nw",
    text='-'+helmboost_1,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

canvas.create_text(
    133.0,
    168.0,
    anchor="nw",
    text='-'+helmboost_2,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select("HELM"),
    relief="flat"
)
button_1.place(
    x=130.0,
    y=123.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? Chestplate Part
# ? ====================================================================

image_image_5 = thesystem.inventory.get_item_button_image(chest, max_width, max_height)
image_5 = canvas.create_image(
    184.0,
    241.0,
    image=image_image_5
)

canvas.create_text(
    18.0,
    223.0,
    anchor="nw",
    text=f"[{chest}]",
    fill="#FFFFFF",
    font=("Exo Bold", 11 * -1)
)

canvas.create_text(
    18.0,
    240.0,
    anchor="nw",
    text='-'+chestboost_1,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

canvas.create_text(
    18.0,
    258.0,
    anchor="nw",
    text='-'+chestboost_2,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select("CHESTPLATE"),
    relief="flat"
)
button_2.place(
    x=227.0,
    y=208.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? First Gauntlet Part
# ? ====================================================================

image_image_6 = thesystem.inventory.get_item_button_image(f_gaun, max_width, max_height)
image_6 = canvas.create_image(
    86.0,
    337.0,
    image=image_image_6
)

canvas.create_text(
    130.0,
    319.0,
    anchor="nw",
    text=f"[{f_gaun}]",
    fill="#FFFFFF",
    font=("Exo Bold", 11 * -1)
)

canvas.create_text(
    130.0,
    336.0,
    anchor="nw",
    text='-'+f_gaunboost_1,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

canvas.create_text(
    130.0,
    351.0,
    anchor="nw",
    text='-'+f_gaunboost_2,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select("FIRST GAUNTLET"),
    relief="flat"
)
button_3.place(
    x=129.0,
    y=302.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? Boots Part
# ? ====================================================================

image_image_7 = thesystem.inventory.get_item_button_image(boot, max_width, max_height)
image_7 = canvas.create_image(
    729.0,
    374.0,
    image=image_image_7
)

canvas.create_text(
    564.0,
    361.0,
    anchor="nw",
    text=f"[{boot}]",
    fill="#FFFFFF",
    font=("Exo Bold", 11 * -1)
)

canvas.create_text(
    565.0,
    377.0,
    anchor="nw",
    text='-'+bootboost_1,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

canvas.create_text(
    565.0,
    392.0,
    anchor="nw",
    text='-'+bootboost_2,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select("BOOTS"),
    relief="flat"
)
button_4.place(
    x=675.0,
    y=350.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? Collar Part
# ? ====================================================================

image_image_8 = thesystem.inventory.get_item_button_image(collar, max_width, max_height)
image_8 = canvas.create_image(
    728.0,
    81.0,
    image=image_image_8
)

segment_length = 30
col_part1, col_part2 = split_text(collar, segment_length)

if len(collar)<30:
    canvas.create_text(
        576.0,
        66.0-3,
        anchor="nw",
        text=f"[{collar}]",
        fill="#FFFFFF",
        font=("Exo Bold", 11 * -1)
    )

else:
    canvas.create_text(
        576.0,
        66.0-3,
        anchor="nw",
        text=f"[{col_part1}",
        fill="#FFFFFF",
        font=("Exo Bold", 11 * -1)
    )

    canvas.create_text(
        576.0,
        66.0+7,
        anchor="nw",
        text=f"{col_part2}]",
        fill="#FFFFFF",
        font=("Exo Bold", 11 * -1)
    )

canvas.create_text(
    576.0,
    82.0+6,
    anchor="nw",
    text='-'+collarboost_1,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

canvas.create_text(
    576.0,
    97.0+6,
    anchor="nw",
    text='-'+collarboost_2,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select("COLLAR"),
    relief="flat"
)
button_5.place(
    x=674.0,
    y=54.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? Ring Part
# ? ====================================================================

image_image_9 = thesystem.inventory.get_item_button_image(ring, max_width, max_height)
image_9 = canvas.create_image(
    606.0,
    274.0,
    image=image_image_9
)

canvas.create_text(
    652.0,
    248.0,
    anchor="nw",
    text=f"[{ring}]",
    fill="#FFFFFF",
    font=("Exo Bold", 11 * -1)
)

canvas.create_text(
    652.0,
    264.0,
    anchor="nw",
    text='-'+ringboost_1,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

canvas.create_text(
    652.0,
    278.0,
    anchor="nw",
    text='-'+ringboost_2,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select("RING"),
    relief="flat"
)
button_6.place(
    x=549.0,
    y=236.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? Second Gauntlet Part
# ? ====================================================================
image_image_10 = thesystem.inventory.get_item_button_image(s_gaun, max_width, max_height)
image_10 = canvas.create_image(
    606.0,
    182.0,
    image=image_image_10
)

segment_length = 30
s_gpart1, s_gpart2 = split_text(s_gaun, segment_length)

if len(s_gaun)<31:
    canvas.create_text(
        652.0,
        155.0,
        anchor="nw",
        text=f"[{s_gaun}]",
        fill="#FFFFFF",
        font=("Exo Bold", 11 * -1)
    )
else:
    canvas.create_text(
        652.0,
        155.0-11,
        anchor="nw",
        text=f"[{s_gpart1}",
        fill="#FFFFFF",
        font=("Exo Bold", 11 * -1)
    )
    canvas.create_text(
        652.0,
        155.0,
        anchor="nw",
        text=f"{s_gpart2}]",
        fill="#FFFFFF",
        font=("Exo Bold", 11 * -1)
    )


canvas.create_text(
    652.0,
    171.0,
    anchor="nw",
    text='-'+s_gaunboost_1,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

canvas.create_text(
    652.0,
    186.0,
    anchor="nw",
    text='-'+s_gaunboost_2,
    fill="#69FF44",
    font=("Exo Regular", 12 * -1)
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select("SECOND GAUNTLET"),
    relief="flat"
)
button_7.place(
    x=550.0,
    y=146.0,
    width=12.0,
    height=12.0
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    254.0,
    106.0,
    image=image_image_11
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    298.0,
    212.0,
    image=image_image_12
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    214.0,
    283.0,
    image=image_image_13
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    254.0,
    106.0,
    image=image_image_14
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    552.0,
    81.0,
    image=image_image_15
)

image_image_16 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(
    525.0160522460938,
    179.0,
    image=image_image_16
)

image_image_17 = PhotoImage(
    file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(
    527.908523776442,
    283.7527784363283,
    image=image_image_17
)

image_image_18 = PhotoImage(
    file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(
    561.9093198482187,
    332.40972685565293,
    image=image_image_18
)

'''
button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=342.0,
    y=422.0,
    width=114.0,
    height=14.0
)
'''

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(),
    relief="flat"
)
button_9.place(
    x=765.0,
    y=10.0,
    width=25.0,
    height=25.0
)

image_image_19 = PhotoImage(
    file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(
    401.0,
    10.0,
    image=image_image_19
)

canvas.tag_bind(image_19, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_19, "<B1-Motion>", move_window)

image_image_20 = PhotoImage(
    file=relative_to_assets("image_25.png"))
image_20 = canvas.create_image(
    218.0,
    43.0,
    image=image_image_20
)

canvas.tag_bind(image_19, "<ButtonPress-1>", lambda event: thesystem.system.info_open("Equipment"))

window.resizable(False, False)
window.mainloop()
