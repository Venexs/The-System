
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import random
import cv2
from PIL import Image, ImageTk
import time

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def make_window_transparent(window):
    window.wm_attributes('-transparentcolor', "#0C679B")

def center_window(root, width, height):
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate position x, y to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set the dimensions of the window and the position
    root.geometry(f'{width}x{height}+{x}+{y}')

def animate_window_open(window, target_height, width, step=2, delay=5):
    current_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{width}x{current_height}+{screen_width//2 - width//2}+{screen_height//2 - current_height//2}")

    if current_height < target_height:
        new_height = min(current_height + step, target_height)
    else:
        new_height = current_height
    
    new_y = screen_height // 2 - new_height // 2
    window.geometry(f"{width}x{new_height}+{screen_width//2 - width//2}+{new_y}")

    if new_height < target_height:
        window.after(delay, animate_window_open, window, target_height, width, step, delay)

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

class VideoPlayer:
    def __init__(self, canvas, video_path, x, y, frame_skip=2, resize_factor=0.8):
        self.canvas = canvas
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.x = x
        self.y = y
        self.frame_skip = frame_skip  # Number of frames to skip
        self.resize_factor = resize_factor  # Factor to resize frames
        self.image_id = self.canvas.create_image(self.x, self.y)
        self.frame_count = 0
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        
        if not ret:
            # If the video has ended, reset the capture object
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

        if ret:
            self.frame_count += 1
            if self.frame_count % self.frame_skip == 0:  # Skip frames for performance
                frame = cv2.resize(frame, (0, 0), fx=self.resize_factor, fy=self.resize_factor)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.itemconfig(self.image_id, image=imgtk)
                self.canvas.imgtk = imgtk

        self.canvas.after(10, self.update_frame)

    def __del__(self):
        self.cap.release()

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

def ex_close(eve):
    subprocess.Popen(['python', 'sfx_close.py'])
    animate_window_close(window, initial_height, window_width, step=30, delay=1)

def name(eve):
    subprocess.Popen(['python', 'Anime Version/Penalty Check/gui.py'])
    window.quit()

window = Tk()

initial_height = 0
target_height = 592
window_width = 934

window.geometry(f"{window_width}x{initial_height}")
animate_window_open(window, target_height, window_width, step=25, delay=1)

#center_window(window,window_width,target_height)
subprocess.Popen(['python', 'sfx.py'])
window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
make_window_transparent(window)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 592,
    width = 934,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    731.0,
    384.0,
    image=image_image_1
)

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)
    video_path=pres_file_data["Anime"]["Video"]
player = VideoPlayer(canvas, video_path, 430.0, 263.0)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    471.0,
    308.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    236.0,
    113.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    248.0,
    310.0,
    image=image_image_4
)

canvas.tag_bind(image_4, "<ButtonPress-1>", name)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    394.0,
    318.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    540.0,
    319.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    686.0,
    318.0,
    image=image_image_7
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
    x=759.0,
    y=73.0,
    width=25.0,
    height=25.0
)

canvas.create_rectangle(
    33.0,
    7.0,
    906.0,
    45.0,
    fill="#333333",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    336.0,
    50.0,
    fill="#0C679B",
    outline="")

canvas.create_rectangle(
    0.0,
    541.0,
    934.0,
    592.0,
    fill="#0C679B",
    outline="")

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    70.0,
    313.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    865.0,
    325.0,
    image=image_image_9
)

canvas.create_rectangle(
    235.0,
    0.0,
    934.0,
    69.0,
    fill="#0C679B",
    outline="")

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    452.0,
    47.0,
    image=image_image_10
)

canvas.tag_bind(image_10, "<ButtonPress-1>", start_move)
canvas.tag_bind(image_10, "<B1-Motion>", move_window)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    458.0,
    556.0,
    image=image_image_11
)
window.resizable(False, False)
window.mainloop()
