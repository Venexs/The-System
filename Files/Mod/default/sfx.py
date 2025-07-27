import winsound
import ujson
import time

with open("Files/Mod/presets.json", 'r') as pres_file:
    pres_file_data=ujson.load(pres_file)

with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
    theme_data=ujson.load(themefile)
    theme=theme_data["Theme"]

with open("Files/Player Data/Settings.json", 'r') as fson:
    data=ujson.load(fson)

sleep_time=data["Settings"]["SFX Delay"]

time.sleep(sleep_time)
opens=pres_file_data[theme]["Open SFX"]
winsound.PlaySound(opens, winsound.SND_FILENAME)