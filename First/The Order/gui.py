
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Projects\System_SL-main\First\The Order\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("371x510")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 510,
    width = 371,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    383.0,
    413.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    234.0,
    344.272216796875,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    120.0,
    88.22274780273438,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    189.0,
    298.0,
    image=image_image_4
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=161.0,
    y=440.0,
    width=156.0,
    height=34.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    87.0,
    344.4087829589844,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    391.0,
    342.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    318.0,
    58.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    300.0,
    514.0,
    image=image_image_8
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=411.0,
    y=63.3824462890625,
    width=20.0,
    height=20.0
)

canvas.create_text(
    64.0,
    124.0,
    anchor="nw",
    text="Ensure that all points add up the below points or the Program will not Allow you to Change Points",
    fill="#FFFFFF",
    font=("Montserrat Medium", 13 * -1)
)

canvas.create_text(
    64.0,
    193.0,
    anchor="nw",
    text="Points Available: XXXXX",
    fill="#FFFFFF",
    font=("Montserrat Bold", 13 * -1)
)

canvas.create_text(
    64.0,
    234.0,
    anchor="nw",
    text="STR:",
    fill="#FFFFFF",
    font=("Montserrat Bold", 13 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    132.5,
    244.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=105.0,
    y=235.0,
    width=55.0,
    height=16.0
)

canvas.create_text(
    64.0,
    259.0,
    anchor="nw",
    text="INT:",
    fill="#FFFFFF",
    font=("Montserrat Bold", 13 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    132.5,
    269.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=105.0,
    y=260.0,
    width=55.0,
    height=16.0
)

canvas.create_text(
    64.0,
    283.0,
    anchor="nw",
    text="AGI:",
    fill="#FFFFFF",
    font=("Montserrat Bold", 13 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    132.5,
    293.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=105.0,
    y=284.0,
    width=55.0,
    height=16.0
)

canvas.create_text(
    64.0,
    308.0,
    anchor="nw",
    text="VIT:",
    fill="#FFFFFF",
    font=("Montserrat Bold", 13 * -1)
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    132.5,
    318.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=105.0,
    y=309.0,
    width=55.0,
    height=16.0
)

canvas.create_text(
    64.0,
    332.0,
    anchor="nw",
    text="PER:",
    fill="#FFFFFF",
    font=("Montserrat Bold", 13 * -1)
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    132.5,
    343.0,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=105.0,
    y=334.0,
    width=55.0,
    height=16.0
)

canvas.create_text(
    64.0,
    356.0,
    anchor="nw",
    text="MAN:",
    fill="#FFFFFF",
    font=("Montserrat Bold", 13 * -1)
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    132.5,
    367.0,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_6.place(
    x=105.0,
    y=358.0,
    width=55.0,
    height=16.0
)
window.resizable(False, False)
window.mainloop()