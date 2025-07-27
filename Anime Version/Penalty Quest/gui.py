from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage
from datetime import datetime
import time
import subprocess
import ujson
import os
import threading
import ctypes
import sys
import psutil
import numpy as np

# Hosts modification-related imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

import thesystem.system 
import thesystem.penalty

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

target_height = 289
window_width = 524
initial_height = 0

window.geometry(f"{window_width}x{target_height}")

window.geometry("524x289")
window.configure(bg="#FFFFFF")
window.wm_attributes("-topmost", True)
window.overrideredirect(True)
window.attributes('-alpha', 0.8)

with open("Files/Player Data/Penalty_Info.json", "r") as pen_info_file:
    pen_info_data = ujson.load(pen_info_file)
    info = pen_info_data["Penalty Info"]
    pr_name1 = info[0]
    pr_name2 = info[1]


def close_programs_if_open(program_name1, program_name2):
    """
    Closes all instances of two programs if they are running and not equal to '-'.

    :param program_name1: First program name (e.g., 'chrome.exe' or '-')
    :param program_name2: Second program name (e.g., 'notepad.exe' or '-')
    """
    to_close = set()

    # Filter out invalid names
    if program_name1 != "-":
        to_close.add(program_name1.lower())
    if program_name2 != "-":
        to_close.add(program_name2.lower())

    for proc in psutil.process_iter(['name']):
        try:
            pname = proc.info['name']
            if pname and pname.lower() in to_close:
                print(f"Closing {pname} (PID: {proc.pid})")
                proc.terminate()
                proc.wait(timeout=3)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def ex_close(eve):
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=5, delay=1)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=289,
    width=524,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    277.0,
    351.0,
    image=image_image_1
)

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)
    video_path=pres_file_data["Anime"]["Video"]
    preloaded_frames=np.load(video_path)
player = thesystem.system.FastVideoPlayer(canvas, preloaded_frames, 300.0, 190.0)


image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    270.0,
    150.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    267.0,
    61.0,
    image=image_image_3
)

countdown_label = canvas.create_text(
    120.0,
    163.0,
    anchor="nw",
    text="00:00:00",
    fill="#FFFFFF",
    font=("Montserrat Bold", 64 * -1)
)

canvas.create_text(
    60.0,
    129.0,
    anchor="nw",
    text="Cannot use the Inputted distraction programs",
    fill="#FFFFFF",
    font=("Montserrat Regular", 18 * -1)
)

canvas.create_text(
    116.0,
    99.0,
    anchor="nw",
    text="[PENALTY QUEST: BLOCKED]",
    fill="#FF0000",
    font=("Montserrat Bold", 20 * -1)
)


# Function to update the countdown on the label
def update_countdown(duration_in_seconds):
    """Updates the countdown on the Tkinter canvas every second."""
    while duration_in_seconds > 0:
        mins, secs = divmod(duration_in_seconds, 60)
        hours, mins = divmod(mins, 60)
        countdown_text = f"{hours:02d}:{mins:02d}:{secs:02d}"
        canvas.itemconfig(countdown_label, text=countdown_text)
        window.update()
        time.sleep(1)
        duration_in_seconds -= 1

# Blocking function to run for 4 hours
def run_blocking_for_duration(duration_in_seconds):
    """Block websites for a specific duration, then unblock them."""
    close_programs_if_open(program_name1=pr_name1, program_name2=pr_name2)()  # Block the websites immediately
    print(f"Blocking websites for {duration_in_seconds / 3600} hours...")

    time.sleep(duration_in_seconds)  # Wait for the specified duration (e.g., 4 hours)
    ex_close(window)

# Set blocking duration (4 hours = 14400 seconds)
blocking_duration = 4 * 60 * 60  # 4 hours

# Start a thread to handle the blocking/unblocking while countdown runs in the main thread
blocking_thread = threading.Thread(target=run_blocking_for_duration, args=(blocking_duration,))
blocking_thread.start()

# Run the penalty countdown for 4 hours in parallel with blocking
thesystem.system.update_penalty_countdown(duration_seconds=blocking_duration, countdown_label=countdown_label, canvas=canvas, window=window)

window.resizable(False, False)
window.mainloop()
