import ujson

def settings_ope(checkbox_var1,checkbox_var0):
    val1=checkbox_var1.get()
    val0=checkbox_var0.get()

    with open("Files/Settings.json", 'r') as settings_open:
        setting_data=ujson.load(settings_open)
    
    if val1==0:
        setting_data["Settings"]["Calorie_Penalty"]="False"
    else:
        setting_data["Settings"]["Calorie_Penalty"]="True"

    if val0==0:
        setting_data["Settings"]["Main_Penalty"]="False"
    else:
        setting_data["Settings"]["Main_Penalty"]="True"
    
    with open("Files/Settings.json", 'w') as settings_open_final:
        ujson.dump(setting_data, settings_open_final, indent=4)
