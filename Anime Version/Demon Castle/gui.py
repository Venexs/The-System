
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import csv
import json
import cv2
from PIL import Image, ImageTk
import random
import threading
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

with open("Files/Tabs.json",'r') as tab_son:
    tab_son_data=json.load(tab_son)

with open("Files/Tabs.json",'w') as fin_tab_son:
    tab_son_data["Castle"]='Open'
    json.dump(tab_son_data,fin_tab_son,indent=4)

run_once_val=False

def get_priority_key_and_value(contents):
    """
    Returns the key and value of the first "Doing" item in the dictionary.
    If no "Doing" is found, returns the key and value of the first "Undone".
    If neither is found, returns (None, None).
    """
    for key, value in contents.items():
        if value == "Doing":
            return key, value
    for key, value in contents.items():
        if value == "Undone":
            return key, value
    return None, None

def all_completed(data):
    """
    Checks if all items in the 'hidden_images' section are marked as Completed = True.
    Returns True if all are completed, False otherwise.
    """
    try:
        if "hidden_images" not in data:
            return False  # Return False if 'hidden_images' is not present

        for key, value in data["hidden_images"].items():
            if not value.get("Completed", False):  # Check if 'Completed' is False or missing
                return False
            
        return True
    except:
        return False

def load_image_visibility(file_path, total_images=50, hidden_percentage=0.35):
    global run_once_val
    global floor
    """
    Reads a JSON file to determine hidden state of images. If the file doesn't exist or can't be read,
    generates visibility states dynamically and saves them to the JSON file.
    """
    val=False
    reboot=False
    try:
        # Attempt to read the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        complete_data=all_completed(data)
        print(complete_data)
        if complete_data:
            try:
                with open("Files/Demons Castle/Demon_Floor.json", 'r') as floor_file:
                    floor_data = json.load(floor_file)
            except:
                floor_data = {str(i): "Doing" if i == 1 else "Undone" for i in range(1, 101)}
                with open("Files/Demons Castle/Demon_Floor.json", 'w') as floor_file:
                    json.dump(floor_data,floor_file, indent=4)
                
                with open("Files/Demons Castle/Demon_Floor.json", 'r') as floor_file:
                    floor_data = json.load(floor_file)

            with open("Files/Demons Castle/Demon_Floor.json", 'w') as floor_file:
                floor_num=get_priority_key_and_value(floor_data)
                next_floor=str(int(floor_num[0])+1)
                floor_data[floor_num[0]]='Done'
                floor_data[next_floor]='Doing'
                json.dump(floor_data,floor_file,indent=4)

            data={}
            for k in range(len(hidden_images)):
                data[str(hidden_images[k])] = {}
                if next_floor==50 or next_floor==25 or next_floor==75:
                    data[str(53)]['Completed'] = False
                else:
                    try:
                        del data[str(53)]
                    except:
                        print()
                data[str(hidden_images[k])]['Completed'] = False

            with open(file_path, 'w') as f:
                json.dump({"hidden_images":data}, f, indent=4)
                
        try:
            with open("Files/Demons Castle/Demon_Floor.json", 'r') as floor_file:
                floor_data = json.load(floor_file)
        except:
            floor_data = {str(i): "Doing" if i == 1 else "Undone" for i in range(1, 101)}
            with open("Files/Demons Castle/Demon_Floor.json", 'w') as floor_file:
                json.dump(floor_data,floor_file, indent=4)
            
            with open("Files/Demons Castle/Demon_Floor.json", 'r') as floor_file:
                floor_data = json.load(floor_file)

        result = get_priority_key_and_value(floor_data)
        reboot=False
        floor=result[0]
        if result[1]=='Doing':
            reboot=True
        if 'hidden_images' in data:
            val=True
            #print(f"Loaded hidden images from file: {data['hidden_images']}")  # Debug
            #print(list(data['hidden_images']))
            return list(data['hidden_images'])
    
    except:
        print("JSON file not found or invalid. Generating new hidden images.")  # Debug
    
    if reboot or val==False:
        # Generate hidden images if file doesn't exist or is invalid
        hidden_count = int(total_images * (1-hidden_percentage))
        hidden_images = random.sample(range(4, 54), hidden_count)  # Randomly pick images to hide

        # Save the generated hidden images to the JSON file
        try:
            data={}
            for k in range(len(hidden_images)):
                data[str(hidden_images[k])] = {}
                if next_floor==50 or next_floor==25 or next_floor==75:
                    data[str(53)]['Completed'] = False
                else:
                    try:
                        del data[str(53)]
                    except:
                        print()
                data[str(hidden_images[k])]['Completed'] = False

            with open(file_path, 'w') as f:
                json.dump({"hidden_images":data}, f, indent=4)
            #print(f"Saved hidden images to file: {hidden_images}")  # Debug
        except IOError as e:
            print(f"Error saving hidden images to file: {e}")
        
        if run_once_val==False:
            run_once_val=True
            load_image_visibility(file_path)
        return hidden_images

# Path to the JSON file
json_file_path = "Files/Demons Castle/image_visibility.json"

# Load visibility data
hidden_images = load_image_visibility(json_file_path)

# Create images and set visibility
file_num=0

try:
    with open("Files/Demons Castle/Demon_Castle.json", 'r') as castle_file:
        castle_data = json.load(castle_file)
except:
    with open("Files/Demons Castle/Demon_Castle.json", 'w') as castle_file:
        castle_data={"Souls":0,"XP":0,"Rewards":False,"Final":False}
        json.dump(castle_data,castle_file, indent=4)

def relative_to_assets(path: str) -> Path:
    global file_num

    file_num+=1
    if file_num>=53 or file_num<4:
        return ASSETS_PATH / Path(path)
    
    with open(json_file_path, 'r') as fr:
        reading_data=json.load(fr)
        fin_data=reading_data["hidden_images"]
    
    int_list = list(map(int, fin_data))
    check=False
    if file_num in int_list:
        check=reading_data["hidden_images"][str(file_num)]["Completed"]

    if check==True:
        pat = ASSETS_PATH / Path("image_4.png")
        return pat
    else:
        pat = ASSETS_PATH / Path("image_5.png")
        return pat

def reward_castle():
    print("NO! THE DEMMON CASTLE ISN'T DONE YET!")
    #thesystem.system.message_open("Demon Castle Reward")

window = Tk()

initial_height = 0
target_height = 602
window_width = 1102

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.make_window_transparent(window)
thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)

window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

soul_count=castle_data["Souls"]
xp_count=castle_data["XP"]
rewards=castle_data["Rewards"]
final=castle_data["Final"]

if soul_count>=10000:
    with open("Files/Demons Castle/Demon_Castle.json", 'w') as castle_file:
        castle_data["Rewards"]=True
        json.dump(castle_data,castle_file, indent=4)
    
    reward_castle()

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
    with open("Files/Tabs.json",'r') as tab_son:
        tab_son_data=json.load(tab_son)

    with open("Files/Tabs.json",'w') as fin_tab_son:
        tab_son_data["Castle"]='Close'
        json.dump(tab_son_data,fin_tab_son,indent=4)
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=50, delay=1)

def demon_fight(event, canvas_name):
    numeber=canvas_name.split('_')[-1]
    with open("Files/Demons Castle/Demon_info.csv", "w", newline='') as file_opem:
        writer = csv.writer(file_opem)
        writer.writerow([floor, numeber])
    subprocess.Popen(['python', 'Anime Version\Demon Castle\gui1.py'])
    ex_close(window)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 602,
    width = 1102,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    961.0,
    329.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Anime"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 478.0, 277.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    554.0,
    319.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    740.0,
    313.0,
    image=image_image_3
)

# =================================================================

image_image_4 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_4 = canvas.create_image(
    622.0,
    465.0,
    image=image_image_4,
    state="hidden"
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    666.0,
    443.0,
    image=image_image_5,
    state="hidden"
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    666.0,
    490.0,
    image=image_image_6,
    state="hidden"
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    585.0,
    416.0,
    image=image_image_7,
    state="hidden"
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    641.0,
    404.0,
    image=image_image_8,
    state="hidden"
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    541.0,
    358.0,
    image=image_image_9,
    state="hidden"
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    643.0,
    347.0,
    image=image_image_10,
    state="hidden"
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    680.0,
    387.0,
    image=image_image_11,
    state="hidden"
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    662.0,
    312.0,
    image=image_image_12,
    state="hidden"
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    587.0,
    347.0,
    image=image_image_13,
    state="hidden"
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    543.0,
    299.0,
    image=image_image_14,
    state="hidden"
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    620.0,
    297.0,
    image=image_image_15,
    state="hidden"
)

image_image_16 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(
    583.0,
    265.0,
    image=image_image_16,
    state="hidden"
)

image_image_17 = PhotoImage(
    file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(
    553.0,
    234.0,
    image=image_image_17,
    state="hidden"
)

image_image_18 = PhotoImage(
    file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(
    618.0,
    236.0,
    image=image_image_18,
    state="hidden"
)

image_image_19 = PhotoImage(
    file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(
    589.0,
    196.0,
    image=image_image_19,
    state="hidden"
)

image_image_20 = PhotoImage(
    file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(
    614.0,
    156.0,
    image=image_image_20,
    state="hidden"
)

image_image_21 = PhotoImage(
    file=relative_to_assets("image_21.png"))
image_21 = canvas.create_image(
    643.0,
    196.0,
    image=image_image_21,
    state="hidden"
)

image_image_22 = PhotoImage(
    file=relative_to_assets("image_22.png"))
image_22 = canvas.create_image(
    664.0,
    120.0,
    image=image_image_22,
    state="hidden"
)

image_image_23 = PhotoImage(
    file=relative_to_assets("image_23.png"))
image_23 = canvas.create_image(
    689.0,
    183.0,
    image=image_image_23,
    state="hidden"
)

image_image_24 = PhotoImage(
    file=relative_to_assets("image_24.png"))
image_24 = canvas.create_image(
    707.0,
    147.0,
    image=image_image_24,
    state="hidden"
)

image_image_25 = PhotoImage(
    file=relative_to_assets("image_25.png"))
image_25 = canvas.create_image(
    735.0,
    207.0,
    image=image_image_25,
    state="hidden"
)

image_image_26 = PhotoImage(
    file=relative_to_assets("image_26.png"))
image_26 = canvas.create_image(
    743.0,
    109.0,
    image=image_image_26,
    state="hidden"
)

image_image_27 = PhotoImage(
    file=relative_to_assets("image_27.png"))
image_27 = canvas.create_image(
    786.0,
    156.0,
    image=image_image_27,
    state="hidden"
)

image_image_28 = PhotoImage(
    file=relative_to_assets("image_28.png"))
image_28 = canvas.create_image(
    849.0,
    149.0,
    image=image_image_28,
    state="hidden"
)

image_image_29 = PhotoImage(
    file=relative_to_assets("image_29.png"))
image_29 = canvas.create_image(
    822.0,
    193.0,
    image=image_image_29,
    state="hidden"
)

image_image_30 = PhotoImage(
    file=relative_to_assets("image_30.png"))
image_30 = canvas.create_image(
    797.0,
    240.0,
    image=image_image_30,
    state="hidden"
)

image_image_31 = PhotoImage(
    file=relative_to_assets("image_31.png"))
image_31 = canvas.create_image(
    841.0,
    234.0,
    image=image_image_31,
    state="hidden"
)

image_image_32 = PhotoImage(
    file=relative_to_assets("image_32.png"))
image_32 = canvas.create_image(
    888.0,
    207.0,
    image=image_image_32,
    state="hidden"
)

image_image_33 = PhotoImage(
    file=relative_to_assets("image_33.png"))
image_33 = canvas.create_image(
    928.0,
    249.0,
    image=image_image_33,
    state="hidden"
)

image_image_34 = PhotoImage(
    file=relative_to_assets("image_34.png"))
image_34 = canvas.create_image(
    874.0,
    263.0,
    image=image_image_34,
    state="hidden"
)

image_image_35 = PhotoImage(
    file=relative_to_assets("image_35.png"))
image_35 = canvas.create_image(
    837.0,
    295.0,
    image=image_image_35,
    state="hidden"
)

image_image_36 = PhotoImage(
    file=relative_to_assets("image_36.png"))
image_36 = canvas.create_image(
    885.0,
    317.0,
    image=image_image_36,
    state="hidden"
)

image_image_37 = PhotoImage(
    file=relative_to_assets("image_37.png"))
image_37 = canvas.create_image(
    926.0,
    293.0,
    image=image_image_37,
    state="hidden"
)

image_image_38 = PhotoImage(
    file=relative_to_assets("image_38.png"))
image_38 = canvas.create_image(
    926.0,
    344.0,
    image=image_image_38,
    state="hidden"
)

image_image_39 = PhotoImage(
    file=relative_to_assets("image_39.png"))
image_39 = canvas.create_image(
    803.0,
    372.0,
    image=image_image_39,
    state="hidden"
)

image_image_40 = PhotoImage(
    file=relative_to_assets("image_40.png"))
image_40 = canvas.create_image(
    718.0,
    395.0,
    image=image_image_40,
    state="hidden"
)

image_image_41 = PhotoImage(
    file=relative_to_assets("image_41.png"))
image_41 = canvas.create_image(
    670.0,
    249.0,
    image=image_image_41,
    state="hidden"
)

image_image_42 = PhotoImage(
    file=relative_to_assets("image_42.png"))
image_42 = canvas.create_image(
    720.0,
    427.0,
    image=image_image_42,
    state="hidden"
)

image_image_43 = PhotoImage(
    file=relative_to_assets("image_43.png"))
image_43 = canvas.create_image(
    726.0,
    488.0,
    image=image_image_43,
    state="hidden"
)

image_image_44 = PhotoImage(
    file=relative_to_assets("image_44.png"))
image_44 = canvas.create_image(
    768.0,
    451.0,
    image=image_image_44,
    state="hidden"
)

image_image_45 = PhotoImage(
    file=relative_to_assets("image_45.png"))
image_45 = canvas.create_image(
    770.0,
    414.0,
    image=image_image_45,
    state="hidden"
)

image_image_46 = PhotoImage(
    file=relative_to_assets("image_46.png"))
image_46 = canvas.create_image(
    809.0,
    457.0,
    image=image_image_46,
    state="hidden"
)

image_image_47 = PhotoImage(
    file=relative_to_assets("image_47.png"))
image_47 = canvas.create_image(
    910.0,
    400.0,
    image=image_image_47,
    state="hidden"
)

image_image_48 = PhotoImage(
    file=relative_to_assets("image_48.png"))
image_48 = canvas.create_image(
    883.0,
    453.0,
    image=image_image_48,
    state="hidden"
)

image_image_49 = PhotoImage(
    file=relative_to_assets("image_49.png"))
image_49 = canvas.create_image(
    814.0,
    498.0,
    image=image_image_49,
    state="hidden"
)

image_image_50 = PhotoImage(
    file=relative_to_assets("image_50.png"))
image_50 = canvas.create_image(
    759.0,
    509.0,
    image=image_image_50,
    state="hidden"
)

image_image_51 = PhotoImage(
    file=relative_to_assets("image_51.png"))
image_51 = canvas.create_image(
    830.0,
    416.0,
    image=image_image_51,
    state="hidden"
)

image_image_52 = PhotoImage(
    file=relative_to_assets("image_52.png"))
image_52 = canvas.create_image(
    876.0,
    370.0,
    image=image_image_52,
    state="hidden"
)

image_image_53 = PhotoImage(
    file=relative_to_assets("image_53.png"))
image_53 = canvas.create_image(
    739.0,
    366.0,
    image=image_image_53,
    state="hidden"
)

for i in range(4, 54):
    # Load and place image
    image_var_name = f"image_image_{i}"
    image_canvas_name = f"image_{i}"

    # Bind the click event
    with open(json_file_path, 'r') as fr:
        reading_data=json.load(fr)
        fin_data=reading_data["hidden_images"]
    
    int_list = list(map(int, fin_data))
    check=False
    if i in int_list:
        check=reading_data["hidden_images"][str(i)]["Completed"]
    
    if not check:
        canvas.tag_bind(globals()[image_canvas_name], "<ButtonPress-1>", lambda event, img=image_canvas_name: demon_fight(event, img))
    
    hi = list(map(int, hidden_images))

    # Set the visibility of the image
    if i not in hi:  # Hide images that are in the hidden list
        canvas.itemconfig(globals()[image_canvas_name], state='hidden')
    else:  # Show images that are not hidden
        canvas.itemconfig(globals()[image_canvas_name], state='normal')

image_image_54 = PhotoImage(
    file=relative_to_assets("image_54.png"))
image_54 = canvas.create_image(
    740.0,
    313.0,
    image=image_image_54,
    tags="baaran",
    state="hidden"
)

if final==True:
    image_image_55 = PhotoImage(
        file=relative_to_assets("image_55 - Copy.png"))
    image_55 = canvas.create_image(
        739.0,
        233.0,
        image=image_image_55,
        tags="baaran",
        state="hidden"
    )

else:
    image_image_55 = PhotoImage(
        file=relative_to_assets("image_55.png"))
    image_55 = canvas.create_image(
        739.0,
        233.0,
        image=image_image_55,
        tags="baaran",
        state="hidden"
    )

if int(floor)>=100:
    canvas.itemconfig("baaran", state="normal")

if not final:
    canvas.tag_bind(image_55, "<ButtonPress-1>", lambda event, img=image_55: demon_fight(event, "image_55"))

canvas.create_text(
    74.0,
    96.0,
    anchor="nw",
    text="THE DEMON CASTLE",
    fill="#FFFFFF",
    font=("Montserrat Bold", 36 * -1)
)

canvas.create_text(
    74.0,
    136.0,
    anchor="nw",
    text=f"FLOOR: {floor}",
    fill="#FFFFFF",
    font=("Montserrat Medium", 24 * -1)
)

canvas.create_text(
    74.0,
    180.0,
    anchor="nw",
    text=f"Demon Souls Collected: {soul_count}",
    fill="#FFFFFF",
    font=("Montserrat Medium", 22 * -1)
)

canvas.create_text(
    74.0,
    210.0,
    anchor="nw",
    text=f"XP Gained in Total: {xp_count}",
    fill="#FFFFFF",
    font=("Montserrat Medium", 22 * -1)
)

canvas.create_rectangle(
    57.998779296875,
    254.0,
    470.0011877711968,
    259.4242028644749,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    85.0,
    276.0,
    anchor="nw",
    text="Quest Info: ",
    fill="#FFFFFF",
    font=("Montserrat Bold", 20 * -1)
)

if rewards==False:
    canvas.create_text(
        104.0,
        308.0,
        anchor="nw",
        text="Gain 10000 Demon Souls",
        fill="#FFFFFF",
        font=("Montserrat Medium", 16 * -1)
    )

    canvas.create_text(
        104.0,
        336.0,
        anchor="nw",
        text="Something here I haven’t decided",
        fill="#FFFFFF",
        font=("Montserrat Medium", 16 * -1)
    )

    canvas.create_text(
        85.0,
        375.0,
        anchor="nw",
        text="Rewards:",
        fill="#FFFFFF",
        font=("Montserrat BoldItalic", 20 * -1)
    )

    canvas.create_text(
        104.0,
        407.0,
        anchor="nw",
        text="The Ord of Order",
        fill="#FFFFFF",
        font=("Montserrat Medium", 16 * -1)
    )

    canvas.create_text(
        104.0,
        431.0,
        anchor="nw",
        text="Any Object in The System",
        fill="#FFFFFF",
        font=("Montserrat Medium", 16 * -1)
    )

    canvas.create_text(
        104.0,
        455.0,
        anchor="nw",
        text="Level Up 10 times",
        fill="#FFFFFF",
        font=("Montserrat Medium", 16 * -1)
    )

else:
    canvas.create_text(
        104.0,
        308.0,
        anchor="nw",
        text="Kill Demon King Baaran",
        fill="#FFFFFF",
        font=("Montserrat Medium", 16 * -1)
    )

    canvas.create_text(
        85.0,
        375.0,
        anchor="nw",
        text="Rewards:",
        fill="#FFFFFF",
        font=("Montserrat BoldItalic", 20 * -1)
    )

    canvas.create_text(
        104.0,
        407.0,
        anchor="nw",
        text="Level Up 10 times",
        fill="#FFFFFF",
        font=("Montserrat Medium", 16 * -1)
    )


image_image_56 = PhotoImage(
    file=relative_to_assets("image_56.png"))
image_56 = canvas.create_image(
    0,
    300.678466796875,
    image=image_image_56
)

image_image_57 = PhotoImage(
    file=relative_to_assets("image_57.png"))
image_57 = canvas.create_image(
    1085.5823974609375,
    326.41552734375,
    image=image_image_57
)

image_image_58 = PhotoImage(
    file=relative_to_assets("image_58.png"))
image_58 = canvas.create_image(
    550.0,
    23.0,
    image=image_image_58
)

canvas.tag_bind(image_58, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_58, "<B1-Motion>", move_window)

image_image_59 = PhotoImage(
    file=relative_to_assets("image_59.png"))
image_59 = canvas.create_image(
    570.0,
    592.0,
    image=image_image_59
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
    x=1000.0,
    y=66.0,
    width=30.0,
    height=30.0
)
window.resizable(False, False)
window.mainloop()