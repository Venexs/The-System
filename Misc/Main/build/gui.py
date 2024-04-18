from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess
import sched
import time
from datetime import datetime, timedelta
import csv
import winsound
import json


subprocess.Popen(['python', 'sfx.py'])
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1264x73")
window.configure(bg = "#FFFFFF")
window.attributes('-alpha',0.8)

def penalty_check():
    # Get today's date
    today = datetime.now().date()

    # Calculate yesterday's date
    yesterday = today - timedelta(days=1)
    with open('Files/Checks/Today_Quest', 'r', newline='') as fout:
        fr=csv.reader(fout)
        for k in fr:
            status=k[0]
            date=k[1]

    p_date=datetime.strptime(date, "%Y-%m-%d").date()
    if yesterday!=p_date:
        subprocess.Popen(['python', 'Daily Quest/build/gui.py'])


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 73,
    width = 1264,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    650.0000022053719,
    279.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    673.9999968409538,
    280.0,
    image=image_image_2
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: subprocess.Popen(['python', 'Inventory/build/gui.py']),
    relief="flat"
)
button_1.place(
    x=20.00010430812199,
    y=8.0,
    width=198.0000034570685,
    height=50.000000834464856
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: subprocess.Popen(['python', 'Daily Quest/build/gui.py']),
    relief="flat"
)
button_2.place(
    x=227.00009667872746,
    y=8.0,
    width=198.0000034570685,
    height=50.000000834464856
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: subprocess.Popen(['python', 'Quests/build/gui.py']),
    relief="flat"
)
button_3.place(
    x=434.0001348257001,
    y=8.0,
    width=198.0000034570685,
    height=50.000000834464856
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: subprocess.Popen(['python', 'Skills Tab/build/gui.py']),
    relief="flat"
)
button_4.place(
    x=641.0000432729657,
    y=8.0,
    width=198.0000034570685,
    height=50.000000834464856
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: subprocess.Popen(['python', 'Status Tab/build/gui.py']),
    relief="flat"
)
button_5.place(
    x=848.0000432729657,
    y=8.0,
    width=198.0000034570685,
    height=50.000000834464856
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: subprocess.Popen(['python', 'Equipment/build/gui.py']),
    relief="flat"
)
button_6.place(
    x=1055.0000432729657,
    y=8.0,
    width=198.0000034570685,
    height=50.000000834464856
)

subprocess.Popen(['python', 'Run Once/First Order Info/build/gui.py'])
subprocess.Popen(['python', 'Run Once/Main Check/build/gui.py'])

window.resizable(False, False)
window.mainloop()
