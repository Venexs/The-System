
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import csv
import subprocess
import subprocess
subprocess.Popen(['python', 'sfx.py'])
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Projects\System\Equipment\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("957x555")
window.configure(bg = "#FFFFFF")

def open_select(cat):
    fout=open('Files/Temp Files/Equipment Temp.csv', 'w', newline='')
    fw=csv.writer(fout)
    rec=[cat]
    fw.writerow(rec)
    fout.close()

    subprocess.Popen(['python', 'Equip Item/build/gui.py'])

    window.quit()

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 555,
    width = 957,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    478.0,
    277.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    477.0,
    276.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    477.0,
    287.9999999999999,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    479.0,
    278.0,
    image=image_image_4
)

# ! ============================================================================
# ! Title
# ! ============================================================================

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    212.0,
    115.0,
    image=image_image_5
)

canvas.create_text(
    136.0,
    102.0,
    anchor="nw",
    text="EQUIPMENT",
    fill="#FFFFFF",
    font=("MontserratRoman SemiBold", 24 * -1)
)

with open('Files/Equipment.csv', 'r') as fout:
    fr=csv.reader(fout)
    for k in fr:
        helm=k[0]
        helm_buff=k[1]

        chest=k[2]
        chest_buff=k[3]

        f_gaun=k[4]
        f_gaun_buff=k[5]

        boot=k[6]
        boot_buff=k[7]

        collar=k[8]
        collar_buff=k[9]

        ring=k[10]
        ring_buff=k[11]

        s_gaun=k[12]
        s_gaun_buff=k[13]

# ? ====================================================================
# ? Helmet Part
# ? ====================================================================

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    164.0,
    190.0,
    image=image_image_6
)

canvas.create_text(
    212.0,
    190.0,
    anchor="nw",
    text=f"[{helm}]",
    fill="#FFFFFF",
    font=("MontserratRoman Regular", 11 * -1)
)

canvas.create_text(
    212.0,
    207.0,
    anchor="nw",
    text=helm_buff,
    fill="#69FF44",
    font=("MontserratRoman Regular", 12 * -1)
)
# ? Helmet Part Button
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select('HELM'),
    relief="flat"
)
button_1.place(
    x=208.0,
    y=167.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? Chestplate Part
# ? ====================================================================

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    262.0,
    285.0,
    image=image_image_7
)

canvas.create_text(
    96.0,
    267.0,
    anchor="nw",
    text=f"[{chest}]",
    fill="#FFFFFF",
    font=("MontserratRoman Regular", 11 * -1)
)

canvas.create_text(
    96.0,
    284.0,
    anchor="nw",
    text=chest_buff,
    fill="#69FF44",
    font=("MontserratRoman Regular", 12 * -1)
)
# ? Chestplate Part Button
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select('CHESTPLATE'),
    relief="flat"
)
button_2.place(
    x=305.0,
    y=252.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? First Gauntlet Part
# ? ====================================================================

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    164.0,
    381.0,
    image=image_image_8
)

canvas.create_text(
    212.0,
    378.0,
    anchor="nw",
    text=f"[{f_gaun}]",
    fill="#FFFFFF",
    font=("MontserratRoman Regular", 11 * -1)
)

canvas.create_text(
    212.0,
    395.0,
    anchor="nw",
    text=f_gaun_buff,
    fill="#69FF44",
    font=("MontserratRoman Regular", 12 * -1)
)
# ? First Gauntlet Part Button
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select('FIRST GAUNTLET'),
    relief="flat"
)
button_3.place(
    x=207.0,
    y=346.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? Boots Part
# ? ====================================================================

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    807.0,
    418.0,
    image=image_image_9
)

canvas.create_text(
    685.0,
    409.0,
    anchor="nw",
    text=f"[{boot}]",
    fill="#FFFFFF",
    font=("MontserratRoman Regular", 11 * -1)
)

canvas.create_text(
    678.0,
    425.0,
    anchor="nw",
    text=boot_buff,
    fill="#69FF44",
    font=("MontserratRoman Regular", 12 * -1)
)
# ? Boots Part Button
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:  open_select('BOOTS'),
    relief="flat"
)
button_4.place(
    x=753.0,
    y=394.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? Collar Part
# ? ====================================================================

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    806.0,
    126.0,
    image=image_image_10
)

canvas.create_text(
    684.0,
    117.0,
    anchor="nw",
    text=f"[{collar}]",
    fill="#FFFFFF",
    font=("MontserratRoman Regular", 11 * -1)
)

canvas.create_text(
    677.0,
    133.0,
    anchor="nw",
    text=collar_buff,
    fill="#69FF44",
    font=("MontserratRoman Regular", 12 * -1)
)
# ? Collar Part Button
button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select('COLLAR'),
    relief="flat"
)
button_5.place(
    x=752.0,
    y=98.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? Ring Part
# ? ====================================================================

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    684.0,
    318.0,
    image=image_image_11
)

canvas.create_text(
    730.0,
    308.0,
    anchor="nw",
    text=f"[{ring}]",
    fill="#FFFFFF",
    font=("MontserratRoman Regular", 11 * -1)
)

canvas.create_text(
    730.0,
    321.0,
    anchor="nw",
    text=ring_buff,
    fill="#69FF44",
    font=("MontserratRoman Regular", 12 * -1)
)
# ? Ring Part Button
button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select('RING'),
    relief="flat"
)
button_6.place(
    x=627.0,
    y=280.0,
    width=12.0,
    height=12.0
)

# ? ====================================================================
# ? Second Gauntlet Part
# ? ====================================================================

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    684.0,
    226.0,
    image=image_image_12
)

canvas.create_text(
    730.0,
    216.0,
    anchor="nw",
    text=f"[{s_gaun}]",
    fill="#FFFFFF",
    font=("MontserratRoman Regular", 11 * -1)
)

canvas.create_text(
    730.0,
    229.0,
    anchor="nw",
    text=s_gaun_buff,
    fill="#69FF44",
    font=("MontserratRoman Regular", 12 * -1)
)
# ? Second Gauntlet Part Button
button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_select('SECOND GAUNTLET'),
    relief="flat"
)
button_7.place(
    x=628.0,
    y=190.0,
    width=12.0,
    height=12.0
)

# ! ====================================================================
# ! ====================================================================
# ! ====================================================================

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    332.0,
    150.38160705566406,
    image=image_image_13
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    379.0,
    256.1320343017578,
    image=image_image_14
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    292.0,
    326.88160705566406,
    image=image_image_15
)

image_image_16 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(
    332.0,
    150.38160705566406,
    image=image_image_16
)

image_image_17 = PhotoImage(
    file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(
    630.0,
    125.0,
    image=image_image_17
)

image_image_18 = PhotoImage(
    file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(
    603.0160522460938,
    223.0,
    image=image_image_18
)

image_image_19 = PhotoImage(
    file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(
    605.908523776442,
    327.5000013367189,
    image=image_image_19
)

image_image_20 = PhotoImage(
    file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(
    639.9093198482187,
    375.92901396502793,
    image=image_image_20
)
window.resizable(False, False)
window.mainloop()