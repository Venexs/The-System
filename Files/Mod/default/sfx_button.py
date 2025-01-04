import winsound
import json

with open("Files\Mod\presets.json", 'r') as pres_file:
    pres_file_data=json.load(pres_file)

with open('Files/Data/Theme_Check.json', 'r') as themefile:
    theme_data=json.load(themefile)
    theme=theme_data["Theme"]
closes=pres_file_data[theme]["Button SFX"]
winsound.PlaySound(closes, winsound.SND_FILENAME)