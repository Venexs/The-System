from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage
import subprocess
from datetime import datetime, timedelta, date
import cv2
from PIL import Image, ImageTk
import time
import json
import sys
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Initialize the main window
window = Tk()

# Configure the window
window.geometry("1272x718")
subprocess.Popen(['python', 'sfx_glitch.py'])

window.configure(bg="#000000")
window.wm_attributes("-topmost", True)
window.attributes('-fullscreen', True)

# Load the JSON file
with open("Files\Checks\Cal_penalty.json", 'r') as file:
    data=json.load(file)
    y=data["Final"]

# Get current week number (ISO week number: 1-53)
current_week = datetime.now().isocalendar()[1]

# Check if the week number in the JSON file is different from the current week number
if data.get("Week") != current_week:
    # If the week is different, reset the value and update the week number
    data["Value"] = 0
    data["Week"] = current_week

# Add the new value to the current value
data["Value"] += 1

x=data["Value"]

today_str = datetime.now().strftime("%d-%m-%Y")

with open("Files\Data\Calorie_Count.json", 'r') as cal_file:
    cal_file_data = json.load(cal_file)

if today_str in cal_file_data:
    cal_val=cal_file_data[today_str] 

# Write the updated data back to the JSON file
with open("Files\Checks\Cal_penalty.json", 'w') as file:
    json.dump(data, file, indent=4)

z=y-x
if z<0:
    z=0

if x==y or x>y:
    subprocess.Popen(['python', 'Anime Version/Final Penalty/gui.py'])
    window.quit()

# Create the canvas
canvas = Canvas(
    window,
    bg="#000000",
    height=718,
    width=1272,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.pack(fill="both", expand=True)

def ex_close(eve):
    subprocess.Popen(['python', 'sfx_close.py'])
    window.quit()

# Load images
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))

# Function to dynamically center the contents based on the window size
def on_resize(event):
    window_width = event.width
    window_height = event.height

    # Center X and Y positions
    center_x = window_width / 2
    center_y = window_height / 2

    # Reposition images and texts relative to the center
    canvas.coords(image_1_obj, center_x, center_y - 200)  # Center image 1
    canvas.coords(image_2_obj, center_x, center_y + 150)  # Center image 2
    canvas.coords(image_3_obj, center_x + 448, center_y + 310)  # Right-aligned image 3

    # Adjust the text relative to the center
    canvas.coords(text_1, center_x - 303, center_y - 140)  # Text 1
    canvas.coords(text_2, center_x - 63, center_y - 93)   # Text 2
    canvas.coords(text_3, center_x - 254, center_y + 10)   # Text 3
    canvas.coords(text_4, center_x - 333, center_y + 53)   # Text 4

# Add images to the canvas, placeholder positions (adjusted in `on_resize`)
image_1_obj = canvas.create_image(0, 0, image=image_image_1)
image_2_obj = canvas.create_image(0, 0, image=image_image_2)
image_3_obj = canvas.create_image(0, 0, image=image_image_3)

# Add text to the canvas
text_1 = canvas.create_text(
    0, 0,  # Initial position, adjusted in on_resize
    anchor="nw",
    text="Your Calorie count of the day was, ",
    fill="#FFFFFF",
    font=("Montserrat Regular", 36 * -1)
)

text_2 = canvas.create_text(
    0, 0,
    anchor="nw",
    text=f"{cal_val}....",
    fill="#FFFFFF",
    font=("Montserrat Regular", 36 * -1)
)

text_3 = canvas.create_text(
    0, 0,
    anchor="nw",
    text=f"This is your {x}/{y} offence of the week",
    fill="#FF0000",
    font=("Montserrat SemiBold", 28 * -1)
)

text_4 = canvas.create_text(
    0, 0,
    anchor="nw",
    text=f"You have {z} offences left before Penalty begins",
    fill="#FF0000",
    font=("Montserrat SemiBold", 28 * -1)
)

# Bind the window resize event to reposition elements
window.bind('<Configure>', on_resize)

# Ensure that the window does not resize its elements
window.resizable(False, False)

# Start the main loop
window.mainloop()
