import ujson
import subprocess
import thesystem.system
import thesystem.misc

try:
    file_path= "Files/Data/Vow_status.json"
    vow_status = thesystem.misc.load_ujson(file_path)
    vow=vow_status["Vow"]
except:
    vow=False

if vow==False:
    subprocess.Popen(["python", "gui.py"])

else:
    thesystem.system.message_open("System Deleted")