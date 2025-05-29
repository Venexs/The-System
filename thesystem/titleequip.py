import subprocess
import ujson
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


def final(name0,window):
    with open("Files/Player Data/Titles.json", 'r') as fson:
        data=ujson.load(fson)
    if name0!='':
        with open("Files/Player Data/Status.json", 'r') as fina_read_fson:
            fina_read_data=ujson.load(fina_read_fson)

        if fina_read_data["status"][1]["title_bool"]!="True":
            stat_val_add=data[name0]["Statbuff"]

            fina_read_data["status"][0]['str']=fina_read_data["status"][0]['str']+stat_val_add
            fina_read_data["status"][0]['agi']=fina_read_data["status"][0]['agi']+stat_val_add
            fina_read_data["status"][0]['vit']=fina_read_data["status"][0]['vit']+stat_val_add
            fina_read_data["status"][0]['int']=fina_read_data["status"][0]['int']+stat_val_add
            fina_read_data["status"][0]['per']=fina_read_data["status"][0]['per']+stat_val_add
            fina_read_data["status"][0]['man']=fina_read_data["status"][0]['man']+stat_val_add

            fina_read_data["status"][1]['title_bool']="True"
            fina_read_data["status"][1]['title']=name0

            with open("Files/Player Data/Status.json", 'w') as fina_write_fson:
                ujson.dump(fina_read_data, fina_write_fson, indent=4)

            subprocess.Popen(['python', 'Anime Version/Status Tab/gui.py'])

            window.quit()

        elif fina_read_data["status"][1]["title_bool"]=="True":
            old_name=fina_read_data["status"][1]['title']
            old_str_val_sub=data[old_name]["Statbuff"]

            stat_val_add=data[name0]["Statbuff"]

            fina_read_data["status"][0]['str']=fina_read_data["status"][0]['str']+stat_val_add-old_str_val_sub
            fina_read_data["status"][0]['agi']=fina_read_data["status"][0]['agi']+stat_val_add-old_str_val_sub
            fina_read_data["status"][0]['vit']=fina_read_data["status"][0]['vit']+stat_val_add-old_str_val_sub
            fina_read_data["status"][0]['int']=fina_read_data["status"][0]['int']+stat_val_add-old_str_val_sub
            fina_read_data["status"][0]['per']=fina_read_data["status"][0]['per']+stat_val_add-old_str_val_sub
            fina_read_data["status"][0]['man']=fina_read_data["status"][0]['man']+stat_val_add-old_str_val_sub

            fina_read_data["status"][1]['title_bool']="True"
            fina_read_data["status"][1]['title']=name0

            with open("Files/Player Data/Status.json", 'w') as fina_write_fson:
                ujson.dump(fina_read_data, fina_write_fson, indent=4)

            subprocess.Popen(['python', 'Anime Version/Status Tab/gui.py'])

            window.quit()

def color(name):
    if name=="False Ranker":
        color="#FF2F2F"
    elif name=="One Above All":
        color="#FFCF26"
    else:    
        color="#FFFFFF"

    return color


