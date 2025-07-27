import winsound
import ujson
import time

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)

with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
    theme_data=ujson.load(themefile)
    theme=theme_data["Theme"]

glitch=pres_file_data[theme]["Glitch SFX"]
winsound.PlaySound(glitch, winsound.SND_FILENAME)