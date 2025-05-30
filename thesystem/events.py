from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ujson
import csv
import random
import subprocess
import os
import thesystem.system
from PIL import Image, ImageTk
from datetime import datetime, timedelta, date
import time

def event_tracker():
    while True:
        today_day = datetime.today().strftime('%A')
        current_time = datetime.now().strftime("%H:%M")
        
        with open("Files/Player Data/Player Events.json", "r") as f:
            data = ujson.load(f)
        data_keys=data.keys()
        for key in data_keys:
            if today_day in data[key]["days"]:
                if data[key]["time"]==current_time:
                    with open("Files/Temp Files/Event.csv", "w", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([key])
                    data[key]["begun"]=True
                    with open("Files/Player Data/Player Events.json", "w") as f:
                        ujson.dump(data, f, indent=6)
                    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
                        theme_data=ujson.load(themefile)
                        theme=theme_data["Theme"]
                    subprocess.Popen(['python', f"{theme} Version/Urgent Quest PVE/gui.py"])
                elif current_time > data[key]["time"]:
                    if data[key]["begun"]==False:
                        print()
        time.sleep(3)