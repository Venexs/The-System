import winsound
import json

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)

theme=pres_file_data["Active Theme"][0]
opens=pres_file_data[theme]["Open SFX"]
winsound.PlaySound(opens, winsound.SND_FILENAME)