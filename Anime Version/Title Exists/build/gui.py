
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import json
import csv

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

subprocess.Popen(['python', 'sfx.py'])

window = Tk()

window.geometry("881x81")
window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 88,
    width = 881,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    420.0,
    163.0,
    image=image_image_1
)

canvas.create_text(
    151.0,
    19.0,
    anchor="nw",
    text="Title Exists already in your list",
    fill="#FFFFFF",
    font=("Montserrat Regular", 40 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    444.0,
    42.2,
    image=image_image_2
)
window.resizable(False, False)
window.mainloop()