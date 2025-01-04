import json
import csv
import thesystem.system as system
import subprocess
from datetime import datetime, timedelta
import threading

with open('Files/Data/Theme_Check.json', 'r') as themefile:
    theme_data = json.load(themefile)
    theme = theme_data["Theme"]

if theme=='Anime':
    initial_height = 0
    target_height = 666
    window_width = 475
elif theme=='Manwha':
    initial_height = 0
    target_height = 622
    window_width = 393

def ex_close(win):
    with open("Files/Tabs.json",'r') as tab_son:
        tab_son_data=json.load(tab_son)

    with open("Files/Tabs.json",'w') as fin_tab_son:
        tab_son_data["Dungeons"]='Close'
        json.dump(tab_son_data,fin_tab_son,indent=4)
    threading.Thread(target=system.fade_out, args=(win, 0.8)).start()
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    system.animate_window_close(win, initial_height, window_width, step=20, delay=1)

def check_fatigue(rank):
    with open("Files/Status.json", 'r') as data_fson:
        data_status=json.load(data_fson)
        finaL_fatigue=data_status["status"][0]["fatigue_max"]
        pl_fatigue=data_status["status"][0]["fatigue"]

        fatigue=system.give_fatigue_from_rank(rank)
 
        fatigue_true=False
        if (pl_fatigue+fatigue)>=finaL_fatigue:
            fatigue_true=True
    
    if fatigue_true==True:
        system.message_open("High Rank")
    return fatigue_true

def open_e_dunfile(eve):
    rank='E'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=json.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files\Data\Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files\Data\Todays_Dungeon.json", 'w') as final_dun_full:
            json.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_d_dunfile(eve):
    rank='D'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=json.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files\Data\Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files\Data\Todays_Dungeon.json", 'w') as final_dun_full:
            json.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_c_dunfile(eve):
    rank='C'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=json.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files\Data\Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files\Data\Todays_Dungeon.json", 'w') as final_dun_full:
            json.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_b_dunfile(eve):
    rank='B'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=json.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files\Data\Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files\Data\Todays_Dungeon.json", 'w') as final_dun_full:
            json.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_a_dunfile(eve):
    rank='A'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=json.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files\Data\Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files\Data\Todays_Dungeon.json", 'w') as final_dun_full:
            json.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_s_dunfile(eve):
    rank='S'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=json.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files\Data\Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files\Data\Todays_Dungeon.json", 'w') as final_dun_full:
            json.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

rank_order = {'E': 1, 'D': 2, 'C': 3, 'B': 4, 'A': 5, 'S': 6}

def instance_dungeon(eve):
    # Load the JSON data from the file
    with open('Files/inventory.json', 'r') as file:
        data = json.load(file)

    # Filter items with 'Instance Keys' category and store with names
    instance_keys_items = [
        (key, item)
        for key, items in data.items()
        for item in items
        if item.get("cat") == "Instance Keys"
    ]

    # Sort items by rank (using rank_order)
    sorted_items = sorted(instance_keys_items, key=lambda x: rank_order.get(x[1].get("rank", "Z"), float('inf')))
    
    # If there's an item with the lowest rank, write it to CSV and return it
    if sorted_items:
        item_name, item_data = sorted_items[0]
        
        # Write the item with the lowest rank to a CSV file
        with open('Files/Data/lowest_rank_item.csv', 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Description', 'Quantity', 'Category', 'Rank', 'Buff', 'Debuff', 'Value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write item data
            writer.writerow({
                'Name': item_name,
                'Description': item_data.get('desc', ''),
                'Quantity': item_data.get('qty', 0),
                'Category': item_data.get('cat', ''),
                'Rank': item_data.get('rank', ''),
                'Buff': item_data.get('buff', ''),
                'Debuff': item_data.get('debuff', ''),
                'Value': item_data.get('Value', 0)
            })

            rank=item_data.get('rank', '')
        fat_check=check_fatigue(rank)
        if fat_check==False:
            subprocess.Popen(['python', f'{theme} Version/Instance Dungeon Confirm/gui.py'])
            ex_close(eve)
    else:
        with open("Files/Checks/Message.csv", 'w', newline='') as check_file:
            check_fw = csv.writer(check_file)
            check_fw.writerow(["No Instance Keys"])
        subprocess.Popen(['python', f'{theme} Version/Message/gui.py'])
