from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage
from datetime import datetime
import time
import subprocess
import json
import os
import threading
import ctypes
import sys

# Hosts modification-related imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)
import thesystem.system  # Assuming you have the system module


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

target_height = 259
window_width = 524
initial_height = 0

window.geometry(f"{window_width}x{initial_height}")
thesystem.system.animate_window_open(window, target_height, window_width, step=30, delay=1)

window.configure(bg="#FFFFFF")
window.wm_attributes("-topmost", True)
window.overrideredirect(True)
window.attributes('-alpha', 0.7)


# Hosts file path and website list
hosts_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"  # For Windows
redirect_ip = "127.0.0.1"
blocked_websites = ["www.pornhub.com", "pornhub.com", "www.hanime.tv", "hanime.tv"]

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

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """Re-launch the script as an administrator if it's not already running with admin privileges."""
    if not is_admin():
        # Try to relaunch the script with administrator privileges
        try:
            # ShellExecuteW will re-run the script with elevated privileges
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit()  # Exit the original process
        except Exception as e:
            print(f"Failed to run as admin: {str(e)}")
            sys.exit()

# Check and request admin rights
# run_as_admin()

def block_websites():
    """Block the specified websites by modifying the hosts file."""
    with open(hosts_path, 'r+') as hosts_file:
        content = hosts_file.read()
        for website in blocked_websites:
            if website not in content:
                hosts_file.write(f"{redirect_ip} {website}\n")


def unblock_websites():
    """Unblock the specified websites by removing them from the hosts file."""
    with open(hosts_path, 'r+') as hosts_file:
        content = hosts_file.readlines()
        hosts_file.seek(0)
        for line in content:
            if not any(website in line for website in blocked_websites):
                hosts_file.write(line)
        hosts_file.truncate()
    # When the countdown is complete, close the window and unblock websites
    countdown_completed()


# Function to run when countdown reaches 00:00:00
def countdown_completed():
    window.quit()
    subprocess.Popen(['python', 'Manwha Version/Penalty Quest Rewards/gui.py'])

subprocess.Popen(['python', 'Files\Mod\default\sfx.py'])

with open("Files/Data/Penalty_Info.json", "r") as pen_info_file:
    pen_info_data = json.load(pen_info_file)
    info = pen_info_data["Penalty Info"]
    pr_name1 = info[0]
    pr_name2 = info[1]

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 259,
    width = 524,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    758.0,
    402.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Manwha"]["Video"]
player = thesystem.system.VideoPlayer(canvas, video_path, 300.0, 190.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    260.0,
    129.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    133.0,
    52.0,
    image=image_image_3
)

countdown_label = canvas.create_text(
    116.0,
    146.0,
    anchor="nw",
    text="00:00:00",
    fill="#FFFFFF",
    font=("Exo Bold", 64 * -1)
)

canvas.create_text(
    72.0,
    122.0,
    anchor="nw",
    text="Cannot use the Inputted distraction programs",
    fill="#FFFFFF",
    font=("Exo Regular", 18 * -1)
)

canvas.create_text(
    32.0,
    76.0,
    anchor="nw",
    text="[PENALTY QUEST: BLOCKED]",
    fill="#FF0000",
    font=("Exo Bold", 20 * -1)
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
    block_websites()  # Block the websites immediately
    print(f"Blocking websites for {duration_in_seconds / 3600} hours...")

    time.sleep(duration_in_seconds)  # Wait for the specified duration (e.g., 4 hours)

    unblock_websites()  # Unblock the websites after 4 hours
    print("Websites have been unblocked after the specified duration.")


# Set blocking duration (4 hours = 14400 seconds)
blocking_duration = 4 * 60 * 60  # 4 hours

# Start a thread to handle the blocking/unblocking while countdown runs in the main thread
blocking_thread = threading.Thread(target=run_blocking_for_duration, args=(blocking_duration,))
blocking_thread.start()

# Run the penalty countdown for 4 hours in parallel with blocking
thesystem.system.update_penalty_countdown(duration_seconds=blocking_duration, countdown_label=countdown_label, canvas=canvas, window=window)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    266.0,
    10.0,
    image=image_image_4
)

canvas.tag_bind(image_4, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_4, "<B1-Motion>", move_window)

window.resizable(False, False)
window.mainloop()
