
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
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
from dotenv import load_dotenv, set_key

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


URL = "https://smewvswweqnpwzngdtco.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNtZXd2c3d3ZXFucHd6bmdkdGNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyMDY2NjcsImV4cCI6MjA0OTc4MjY2N30.0SSN0bbwzFMCGC47XUuwqyKfF__Zikm_rJHqXWf78PU"

supabase: Client = create_client(URL, KEY)

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
window.attributes('-alpha',0.8)
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
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    animate_window_close(window, initial_height, window_width, step=25, delay=1)


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

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    356.0,
    241.0,
    image=image_image_3
)


image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    356.0,
    68.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    356.0,
    142.0,
    image=image_image_6
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    356.0,
    20.0,
    image=image_image_11
)

canvas.tag_bind(image_11, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_11, "<B1-Motion>", move_window)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    162.0,
    178.0,
    image=image_image_8
)

entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=133.0,
    y=194.0,
    width=427.0,
    height=23.0
)


image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    180.0,
    292.0,
    image=image_image_10
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    346.5,
    320.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=133.0,
    y=308.0,
    width=427.0,
    height=23.0
)


SESSION_FILE = "Files/Data/session.json"

# Save session to a JSON file
def save_session_to_file(session_data):
    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f)
    print(f"Session saved to {SESSION_FILE}")

# Load session from the JSON file
def load_session_from_file():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            session_data = json.load(f)
        print(f"Session loaded from {SESSION_FILE}")
        return session_data
    else:
        print(f"No session file found at {SESSION_FILE}")
    return None

# Sign-in function
def Signin():
    email = entry_1.get()
    password = entry_3.get()
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        if response and response.session:
            # Access the session data
            session_data = {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "expires_in": response.session.expires_in,
            }

            # Save session data to the file
            save_session_to_file(session_data)
            # Proceed with further actions
            ex_close(window)
            subprocess.Popen(['python', 'E:\\System\\Edited\\SystemUpdate3\\System_SL-main\\Logs\\background.py'])
            subprocess.Popen(['python', 'E:\\System\\Edited\\SystemUpdate3\\System_SL-main\\gui.py'])
        else:
            print("Sign-in failed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))

# Create the button
button = Button(
    image=image_image_7, 
    borderwidth=0, 
    highlightthickness=0,
    command=Signin
)

button.place(x=133.0, y=382.0) 


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
















window.resizable(False, False)
window.mainloop()