import ujson

def settings_ope(checkbox_var1,checkbox_var0,checkbox_var2,checkbox_var3):
    val1=checkbox_var1.get()
    val0=checkbox_var0.get()
    val2=checkbox_var2.get()
    val3=checkbox_var3.get()

    with open("Files/Player Data/Settings.json", 'r') as settings_open:
        setting_data=ujson.load(settings_open)

    if val0==0:
        setting_data["Settings"]["Main_Penalty"]="False"
    else:
        setting_data["Settings"]["Main_Penalty"]="True"

    if val2==0:
        setting_data["Settings"]["Performernce (ANIME):"]="False"
    else:
        setting_data["Settings"]["Performernce (ANIME):"]="True"

    if val3==0:
        setting_data["Settings"]["Microphone"]="False"
    else:
        setting_data["Settings"]["Microphone"]="True"


    with open("Files/Player Data/Settings.json", 'w') as settings_open_final:
        ujson.dump(setting_data, settings_open_final, indent=4)

