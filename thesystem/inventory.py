from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
import ujson
import subprocess
import threading
import thesystem.system
import csv
import os

def create_inventory_item(canvas, window, item_data, x, y, button_images, item_images, image5):
    tr_n = item_data.get('name', '')
    name = item_data.get('tr_n', '')
    qt = item_data.get('qty', '')
    cat = item_data.get('cat', '')
    r = item_data.get('rank', '')
    d = item_data.get('desc', '')
    b = item_data.get('buff', '')
    db = item_data.get('debuff', '')

    # Load button image
    button_image = get_inventory_button_image(tr_n)
    button_images.append(button_image)  # Prevent garbage collection

    button = Button(
        image=button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (inventory_item_data(tr_n, r, cat, d, b, db, window),ex_close(window)),
        relief="flat"
    )
    button.place(x=x, y=y, width=68, height=82)

    # Load item image and add to canvas
    item_image = PhotoImage(file=image5)
    item_images.append(item_image)  # Prevent garbage collection
    canvas.create_image(x - 7, y + 42, image=item_image)

    # Background rectangle and text
    canvas.create_rectangle(x - 20, y + 84, x + 73, y + 98, fill="#3B3B3B", outline="")
    canvas.create_text(x - 20, y + 85, anchor="nw", text=name, fill="#FFFFFF", font=("Montserrat Medium", 10 * -1))
    canvas.create_text(x + 7, y + 68, anchor="nw", text=qt, fill="#FFFFFF", font=("Montserrat Medium", 10 * -1))

def ex_close(win):
    with open("Files/Player Data/Tabs.json",'r') as tab_son:
        tab_son_data=ujson.load(tab_son)

    with open("Files/Player Data/Tabs.json",'w') as fin_tab_son:
        tab_son_data["Inventory"]='Close'
        ujson.dump(tab_son_data,fin_tab_son,indent=4)
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(win, win.winfo_height(), win.winfo_width(), step=40, delay=1)

def inventory_name_cut(name):
    if len(name)>15:
        s=''
        for k in range(15):
            s+=name[k]
        s+='...'
        return s
    else:
        return name

def inventory_item_data(name,rank,category,t,r,s,window):
    try:
        if name!='-' and rank!='-' and category!='-':
            fout=open('Files/Temp Files/Inventory temp.csv', 'w', newline='')
            fw=csv.writer(fout)
            rec=[name]
            fw.writerow(rec)
            fout.close()

            with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
                theme_data=ujson.load(themefile)
                theme=theme_data["Theme"]
            subprocess.Popen(['python', f'{theme} Version/Item Data/gui.py'])
    
    except:
        print()

def get_inventory_button_image(name):
    try:
        # Construct the absolute path to the Images folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to the project root directory
        if name.split()[0]=='Coin' and name.split()[1]=='Bag':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Coin Pouch" + ' Small.png')
        elif name.split()[-1]=='Key':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Instance Keys" + ' Small.png')
        elif name.split()[0]=='Rune' and name.split()[1]=='Stone':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Rune Stone" + ' Small.png')
        else:
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, name + ' Small.png')
        if not os.path.exists(files):
            print(FileNotFoundError)
    except:
        file_loc = os.path.join(script_dir, "Images")
        files = os.path.join(file_loc, "Unknown.png")
    
    return PhotoImage(file=files)

def selling_item(name,window,val):
    with open("Files/Player Data/Status.json", 'r') as read_status_file:
        read_status_file_data=ujson.load(read_status_file)

    with open("Files/Player Data/Inventory.json", 'r') as fin_inv_fson:
        fin_inv_data=ujson.load(fin_inv_fson)

        fin_qt=fin_inv_data[name][0]["qty"]
        fin_inv_data[name][0]["qty"]=fin_qt-1
        closing=False   
        if fin_inv_data[name][0]["qty"]==0:
            del fin_inv_data[name]
            closing=True

    
    
    with open("Files/Player Data/Skill.json", 'r') as f:
        skill_data = ujson.load(f)

    addition = 0
    if thesystem.system.skill_use("Negotiation", (0), False) and ("Negotiation" in skill_data):
        lvl = skill_data["Negotiation"][0]["lvl"]
        if isinstance(lvl, str):
            lvl = 10

        percentile = 0.015 * lvl
        addition = abs(val) * percentile


    with open("Files/Player Data/Inventory.json", 'w') as finaladdon_inv:
        ujson.dump(fin_inv_data, finaladdon_inv, indent=6)

    with open("Files/Player Data/Status.json", 'w') as write_status_file:
        read_status_file_data["status"][0]['coins']+=int(val+addition)
        ujson.dump(read_status_file_data, write_status_file, indent=4)

    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]

    if closing==True:
        subprocess.Popen(['python', f'{theme} Version/Inventory/gui.py'])

        window.quit()

    else:
        subprocess.Popen(['python', f'{theme} Version/Item Data/gui.py'])

        window.quit()

def get_item_button_image(name, max_width, max_height):
    try:
        # Construct the absolute path to the Images folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to the project root directory
        if name.split()[0]=='Coin' and name.split()[1]=='Bag':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Coin Pouch" + ' Big.png')
        elif name.split()[-1]=='Key':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Instance Keys" + ' Big.png')
        elif name.split()[0]=='Rune' and name.split()[1]=='Stone':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Rune Stone" + ' Big.png')
        else:
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, name + ' Big.png')
        if not os.path.exists(files):
            raise FileNotFoundError
    except:
        file_loc = os.path.join(script_dir, "Images")
        files = os.path.join(file_loc, "Unknown.png")

    # Open the image
    image = Image.open(files)
    
    # Calculate the resize ratio
    width_ratio = max_width / image.width
    height_ratio = max_height / image.height
    resize_ratio = min(width_ratio, height_ratio)
    
    # Resize the image
    new_width = int(image.width * resize_ratio)
    new_height = int(image.height * resize_ratio)
    resized_image = image.resize((new_width, new_height))
    
    # Convert the image to PhotoImage
    photo_image = ImageTk.PhotoImage(resized_image)
    
    return photo_image



