import ujson
import random
import subprocess
import tkinter
import csv
import thesystem.system
import threading

def get_priority_key_and_value(contents):
    """
    Returns the key and value of the first "Doing" item in the dictionary.
    If no "Doing" is found, returns the key and value of the first "Undone".
    If neither is found, returns (None, None).
    """
    for key, value in contents.items():
        if value == "Doing":
            return key, value
    for key, value in contents.items():
        if value == "Undone":
            return key, value
    return None, None

def all_completed(data):
    """
    Checks if all items in the 'hidden_images' section are marked as Completed = True.
    Returns True if all are completed, False otherwise.
    """
    try:
        if "hidden_images" not in data:
            return False  # Return False if 'hidden_images' is not present

        for key, value in data["hidden_images"].items():
            if not value.get("Completed", False):  # Check if 'Completed' is False or missing
                return False
            
        return True
    except:
        return False
    
def load_image_visibility(file_path, run_once_val, total_images=50, hidden_percentage=0.35):
    global floor
    """
    Reads a ujson file to determine hidden state of images. If the file doesn't exist or can't be read,
    generates visibility states dynamically and saves them to the ujson file.
    """
    val=False
    reboot=False
    try:
        # Attempt to read the ujson file
        with open(file_path, 'r') as f:
            data = ujson.load(f)
        
        complete_data=all_completed(data)
        print(complete_data)
        if complete_data:
            try:
                with open("Files/Player Data/Demon_Floor.json", 'r') as floor_file:
                    floor_data = ujson.load(floor_file)
            except:
                floor_data = {str(i): "Doing" if i == 1 else "Undone" for i in range(1, 101)}
                with open("Files/Player Data/Demon_Floor.json", 'w') as floor_file:
                    ujson.dump(floor_data,floor_file, indent=4)
                
                with open("Files/Player Data/Demon_Floor.json", 'r') as floor_file:
                    floor_data = ujson.load(floor_file)

            with open("Files/Player Data/Demon_Floor.json", 'w') as floor_file:
                floor_num=get_priority_key_and_value(floor_data)
                next_floor=str(int(floor_num[0])+1)
                floor_data[floor_num[0]]='Done'
                floor_data[next_floor]='Doing'
                ujson.dump(floor_data,floor_file,indent=4)

            data={}
            for k in range(len(hidden_images)):
                data[str(hidden_images[k])] = {}
                if next_floor in [25, 50, 75]:
                    if str(53) not in data:
                        data[str(53)] = {}
                    data[str(53)]['Completed'] = False
                else:
                    data.pop(str(53), None)  # delete safely if it exists

                data[str(hidden_images[k])]['Completed'] = False

            with open(file_path, 'w') as f:
                ujson.dump({"hidden_images":data}, f, indent=4)
                
        try:
            with open("Files/Player Data/Demon_Floor.json", 'r') as floor_file:
                floor_data = ujson.load(floor_file)
        except:
            floor_data = {str(i): "Doing" if i == 1 else "Undone" for i in range(1, 101)}
            with open("Files/Player Data/Demon_Floor.json", 'w') as floor_file:
                ujson.dump(floor_data,floor_file, indent=4)
            
            with open("Files/Player Data/Demon_Floor.json", 'r') as floor_file:
                floor_data = ujson.load(floor_file)

        result = get_priority_key_and_value(floor_data)
        reboot=False
        floor=result[0]
        if result[1]=='Doing':
            reboot=True
        if 'hidden_images' in data:
            val=True
            #print(f"Loaded hidden images from file: {data['hidden_images']}")  # Debug
            #print(list(data['hidden_images']))
            return [list(data['hidden_images']), floor]
    
    except:
        print("ujson file not found or invalid. Generating new hidden images.")  # Debug
    
    if reboot or val==False:
        # Generate hidden images if file doesn't exist or is invalid
        hidden_count = int(total_images * (1-hidden_percentage))
        hidden_images = random.sample(range(4, 54), hidden_count)  # Randomly pick images to hide

        # Save the generated hidden images to the ujson file
        try:
            data={}
            for k in range(len(hidden_images)):
                data[str(hidden_images[k])] = {}
                try:
                    if next_floor in [25, 50, 75]:
                        if str(53) not in data:
                            data[str(53)] = {}
                        data[str(53)]['Completed'] = False
                    else:
                        data.pop(str(53), None)
                except:
                    pass
                
                data[str(hidden_images[k])]['Completed'] = False

            with open(file_path, 'w') as f:
                ujson.dump({"hidden_images":data}, f, indent=4)
            #print(f"Saved hidden images to file: {hidden_images}")  # Debug
        except IOError as e:
            print(f"Error saving hidden images to file: {e}")
        
        if run_once_val==False:
            run_once_val=True
            load_image_visibility(file_path, run_once_val)
        return [hidden_images,floor]

def demon_fight(canvas_name,window):
    numeber=canvas_name.split('_')[-1]
    with open("Files/Temp Files/Demon_info.csv", "w", newline='') as file_opem:
        writer = csv.writer(file_opem)
        writer.writerow([floor, numeber])
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    subprocess.Popen(['python', f'{theme} Version/Demon Castle/gui1.py'])
    ex_close(window)

def ex_close(win):
    with open("Files/Player Data/Tabs.json",'r') as tab_son:
        tab_son_data=ujson.load(tab_son)

    with open("Files/Player Data/Tabs.json",'w') as fin_tab_son:
        tab_son_data["Castle"]='Close'
        ujson.dump(tab_son_data,fin_tab_son,indent=4)
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(win, win.winfo_width(), win.winfo_height(), step=50, delay=1)

def reward_castle():
    #print("NO! THE DEMMON CASTLE ISN'T DONE YET!")
    thesystem.system.message_open("Demon Castle Reward")

    for k in range(10):
        with open("Files/Player Data/Status.json", 'r') as fson:
            data=ujson.load(fson)
            data["status"][0]['level']+=1
            # ? =================================================
            data["status"][0]['str']+=1
            data["status"][0]['int']+=1
            data["status"][0]['agi']+=1
            data["status"][0]['vit']+=1
            data["status"][0]['per']+=1
            data["status"][0]['man']+=1

    with open("Files/Player Data/Status.json", 'w') as fson:
        ujson.dump(data, fson, indent=6)
    
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    subprocess.Popen(['python', f"{theme} Version/Leveled up/gui.py"])

    with open("Files/Player Data/Inventory.json", 'r') as fson:
        data_fininv=ujson.load(fson)
    
    item=[
        {
            "desc":"An Orb that allows a player to realocate thier points to fit future needs. This does not affect Fatigue. Click on Equip to use",
            "qty":1,
            "cat":"ORDER",
            "rank":"?",
            "buff":"",
            "debuff":"",

            "Value":10000000
        }
    ]

    data_fininv["The Orb of Order"]=item

    with open("Files/Player Data/Inventory.json", 'w') as finaladdon:
        ujson.dump(data_fininv, finaladdon, indent=6)

    subprocess.Popen(['python', "Anime Version/Demon Castle/gui.py"])

def choose_demon_by_rank(rank_of):
    with open("Files/Player Data/Demon_Data.json", "r") as demon_file:
        demons = ujson.load(demon_file)
    # Filter demons by the given rank
    filtered_demons = [name for name, details in demons.items() if details["rank"] == rank_of]
    if not filtered_demons:
        return f"No demons found for rank {rank_of}."
    # Choose a random demon from the filtered list
    return random.choice(filtered_demons)

def color(lvl, floor):
    if lvl<=(int(floor)-10):
        color="#FF2F2F"
    elif lvl>=(int(floor)+10):
        color="#ffee2f"
    elif lvl>=(int(floor)+20):
        color="#ffffff"
    else:
        color="#FFFFFF"

    return color
