import ujson
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from datetime import datetime, date
import subprocess
import thesystem.system
import threading

def add_cal(entry_1, window, initial_height, window_width):
    with open("Files/Data/Calorie_Count.json", 'r') as calorie_add_file:
        calorie_add_data=ujson.load(calorie_add_file)
        calorie_add_key=list(calorie_add_data.keys())[0]

    # Get today's date
    current_date = date.today()

    # Format the date as a string
    formatted_date = current_date.strftime("%Y-%m-%d")

    if calorie_add_key==formatted_date:
        cal_c=float(entry_1.get())
        calorie_add_data[formatted_date][0]+=cal_c
        with open("Files/Data/Calorie_Count.json", 'w') as calorie_add_file_write:
            ujson.dump(calorie_add_data, calorie_add_file_write, indent=4)

    else:
        new_data={formatted_date:[0]}
        with open("Files/Data/Calorie_Count.json", 'w') as calorie_add_file_write:
            ujson.dump(new_data, calorie_add_file_write, indent=4)
        add_cal(entry_1, window, initial_height, window_width)

    ex_close(window, initial_height, window_width)

def ex_close(window, initial_height, window_width):
    threading.Thread(target=thesystem.system.fade_out, args=(window, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, initial_height, window_width, step=12, delay=1)
