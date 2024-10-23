import winsound
import json

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)

theme=pres_file_data["Active Theme"]
glitch=pres_file_data[theme]["Glitch SFX"][0]
winsound.PlaySound(glitch, winsound.SND_FILENAME)