import json
import subprocess
import thesystem.system

try:
    file_path= "Files/Data/Vow_status.json"
    with open(file_path, 'r') as vow_file:
        vow_status = json.load(vow_file)
        vow=vow_status["Vow"]
except:
    vow=False

if vow==False:
    subprocess.Popen(["python", "gui.py"])

else:
    thesystem.system.message_open("System Deleted")