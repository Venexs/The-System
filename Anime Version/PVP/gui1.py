
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, Listbox, Scrollbar
import subprocess
import threading
import cv2
from PIL import Image, ImageTk
import json
import time
import sys
import os
from supabase import create_client, Client
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


URL = "https://smewvswweqnpwzngdtco.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNtZXd2c3d3ZXFucHd6bmdkdGNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyMDY2NjcsImV4cCI6MjA0OTc4MjY2N30.0SSN0bbwzFMCGC47XUuwqyKfF__Zikm_rJHqXWf78PU"
SESSION_FILE = "Files/Data/session.json"

supabase: Client = create_client(URL, KEY)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

initial_height = 0
initial_width = 0
target_height = 431
window_width = 712

thesystem.system.make_window_transparent(window)

window.geometry(f"{initial_width}x{initial_height}")
thesystem.system.animate_window_open_middle(window, target_height, window_width, step=20, delay=1)

thesystem.system.center_window(window,window_width,target_height)
window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.6)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)

def animate_window_close(window, target_height, width, step=2, delay=5):
    current_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{width}x{current_height}+{screen_width//2 - width//2}+{screen_height//2 - current_height//2}")

    if current_height > target_height:
        new_height = max(current_height - step, target_height)
    else:
        new_height = current_height
    
    new_y = screen_height // 2 - new_height // 2
    window.geometry(f"{width}x{new_height}+{screen_width//2 - width//2}+{new_y}")

    if new_height > target_height:
        window.after(delay, animate_window_close, window, target_height, width, step, delay)
    else:
        
        window.quit()

def ex_close(eve):
    subprocess.Popen(['python', os.path.join(project_root, 'Files/Mod/default/sfx_close.py')])
    animate_window_close(window, initial_height, window_width, step=45, delay=1)


canvas = Canvas(
    window,
    bg = "#0678FF",
    height = 432,
    width = 712,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    356.0,
    216.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    356.0,
    216.0,
    image=image_image_2
)

button_image_20 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_20 = Button(
    image=button_image_20,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: ex_close(window),
    relief="flat"
)
button_20.place(
    x=655.0,
    y=35.0,
    width=21.20473861694336,
    height=24.221660614013672
)


transparent_image = Image.new('RGBA', (1, 1), (0, 0, 0, 0))  # Create a 1x1 transparent image
transparent_photo = ImageTk.PhotoImage(transparent_image)

# Add this line below the existing canvas placements
opponent_name_text = canvas.create_text(
    350, 200,  # x, y coordinates
    anchor="n",
    text="REQUEST TO BATTLE SENT... CHECK DISCORD STATUS TO SEE IF THEY ARE ONLINE.",
    fill="White",  # Text color
    font=("Montserrat Bold", 10),
)

opponent_name_text1 = canvas.create_text(
    350, 250,  # x, y coordinates
    anchor="n",
    text="Please do not close this window. It will cancel your request.",
    fill="Red",  # Text color
    font=("Montserrat Bold", 10),
)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        selected_username = sys.argv[1]
        
        print(f"Received username: {selected_username}")
    else:
        print("No username received!")
        
        
window.resizable(False, False)
window.mainloop()
