import subprocess
import ujson
import time

import thesystem.system

def return_status():
    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
        return data
    
def load_ujson(filename):
    with open(filename, 'r') as file:
        return ujson.load(file)

def dump_ujson(filename, data, indents=6):
    with open(filename, 'w') as file:
        ujson.dump(data, file, indent=indents)
        return True
    
def check_theme():
    theme_data=load_ujson("Files/Player Data/Theme_Check.json")
    theme=theme_data["Theme"]

    return theme

def update_screen(screen, state='Open'):
    tab_son_data=load_ujson("Files/Player Data/Tabs.json")
    new_state="Open"
    if state == 'Open':
        new_state="Close"

    if tab_son_data[screen]==new_state:
        tab_son_data[screen]=state
        dump_ujson("Files/Player Data/Tabs.json", tab_son_data, 4)
        return True
    return False

def return_settings():
    with open("Files/Player Data/Settings.json", 'r') as fson:
        data=ujson.load(fson)
        return data
    
def voice_activate():
    first_run=False
    while True:
        with open("Files/Player Data/Settings.json", 'r') as fson:
            data=ujson.load(fson)
            
        if data["Settings"]["Microphone"]=="True" and first_run==False:
            subprocess.Popen(['python', 'voice.py'])
            thesystem.system.info_open("Voice")
            first_run=True
        
        time.sleep(2)