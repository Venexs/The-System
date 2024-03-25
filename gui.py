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

window.geometry("115x671")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 671,
    width = 115,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    277.0,
    478.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    103.0,
    378.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    285.0000000000001,
    377.9999999999999,
    image=image_image_3
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
    x=38.0,
    y=135.0,
    width=72.9000015258789,
    height=74.4423828125
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
    x=38.0,
    y=219.0,
    width=72.9000015258789,
    height=74.4423828125
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
    x=34.0,
    y=301.0,
    width=81.0,
    height=82.71375274658203
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
    x=38.0,
    y=392.0,
    width=72.9000015258789,
    height=74.4423828125
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
    x=38.0,
    y=482.0,
    width=72.9000015258789,
    height=74.4423828125
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
    x=38.0,
    y=572.0,
    width=72.9000015258789,
    height=74.4423828125
)

window.resizable(False, False)
window.mainloop()
