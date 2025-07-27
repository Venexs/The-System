import ujson
import csv
import thesystem.skills
import thesystem.system as system
import subprocess
from datetime import datetime, timedelta
import random
import threading
import thesystem.system

with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
    theme_data = ujson.load(themefile)
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
    with open("Files/Player Data/Tabs.json",'r') as tab_son:
        tab_son_data=ujson.load(tab_son)

    with open("Files/Player Data/Tabs.json",'w') as fin_tab_son:
        tab_son_data["Dungeons"]='Close'
        ujson.dump(tab_son_data,fin_tab_son,indent=4)
    threading.Thread(target=system.fade_out, args=(win, 0.8)).start()
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    system.animate_window_close(win, initial_height, window_width, step=20, delay=1)

def check_fatigue(rank):
    with open("Files/Player Data/Status.json", 'r') as data_fson:
        data_status=ujson.load(data_fson)
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
    with open("Files/Player Data/Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files/Data/Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files/Player Data/Todays_Dungeon.json", 'w') as final_dun_full:
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_d_dunfile(eve):
    rank='D'
    with open("Files/Player Data/Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files/Data/Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files/Player Data/Todays_Dungeon.json", 'w') as final_dun_full:
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_c_dunfile(eve):
    rank='C'
    with open("Files/Player Data/Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files/Data/Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files/Player Data/Todays_Dungeon.json", 'w') as final_dun_full:
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_b_dunfile(eve):
    rank='B'
    with open("Files/Player Data/Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files/Data/Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files/Player Data/Todays_Dungeon.json", 'w') as final_dun_full:
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_a_dunfile(eve):
    rank='A'
    with open("Files/Player Data/Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files/Data/Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files/Player Data/Todays_Dungeon.json", 'w') as final_dun_full:
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_s_dunfile(eve):
    rank='S'
    with open("Files/Player Data/Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

    date_format = "%Y-%m-%d"
    current_date = datetime.now().date()
    current_date_string = current_date.strftime(date_format)
    fat_check=check_fatigue(rank)
    if dun_full_data[current_date_string][rank]!=0 and fat_check==False:
        dun_full_data[current_date_string][rank]-=1
        with open("Files/Data/Dungeon_Rank.csv", 'w', newline='') as rank_file:
            fw=csv.writer(rank_file)
            fw.writerow([rank,"Normal"])

        with open("Files/Player Data/Todays_Dungeon.json", 'w') as final_dun_full:
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

rank_order = {'E': 1, 'D': 2, 'C': 3, 'B': 4, 'A': 5, 'S': 6}

def instance_dungeon(eve):
    # Load the ujson data from the file
    with open('Files/Player Data/Inventory.json', 'r') as file:
        data = ujson.load(file)

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

def get_item_name_from_csv():
    # Read the item name from the CSV file
    with open('Files/Data/lowest_rank_item.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            return row['Name']
        
def update_inventory(window):
    # Get the item name from the CSV file
    item_name = get_item_name_from_csv()

    # Load the ujson data from the file
    with open('Files/Player Data/Inventory.json', 'r') as file:
        data = ujson.load(file)
    
    # Find the item and update or remove it
    if item_name in data:
        for item in data[item_name]:
            if item['qty'] == 1:
                # Remove the item if quantity is 1
                data[item_name].remove(item)
            elif item['qty'] > 1:
                # Decrease quantity by 1 if greater than 1
                item['qty'] -= 1

        # If all instances are removed, delete the item from inventory
        if not data[item_name]:
            del data[item_name]

    # Write the updated data back to inventory.json
    with open('Files/Player Data/Inventory.json', 'w') as file:
        ujson.dump(data, file, indent=4)

    rank=item["rank"]
    with open("Files/Player Data/Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

    with open("Files/Data/Dungeon_Rank.csv", 'w', newline='') as rank_file:
        fw=csv.writer(rank_file)
        fw.writerow([rank,"Instance"])

    with open("Files/Player Data/Todays_Dungeon.json", 'w') as final_dun_full:
        ujson.dump(dun_full_data, final_dun_full, indent=6)

    subprocess.Popen(['python', 'Manwha Version/Dungeon Runs/gui.py'])
    window.quit()

def dun_check():
    global e_rank, d_rank, c_rank, b_rank, a_rank, s_rank, red_gate

    # Path to the ujson file
    file_path = "Files\\Player Data\\Todays_Dungeon.json"
    
    # Load the existing data from the file
    try:
        with open(file_path, 'r') as dun_check:
            dun_check_data = ujson.load(dun_check)
    except FileNotFoundError:
        dun_check_data = {}

    # Get today's date as a string
    current_date = datetime.now().date()
    current_date_string = current_date.strftime("%Y-%m-%d")

    # Check if data already exists for today's date
    if current_date_string not in dun_check_data:
        dun_check_data = {}
        # E Rank Distro
        e_rank_vals = sum(1 for _ in range(5) if random.randint(1, 2) == 1)

        # D Rank Distro
        d_rank_vals = sum(1 for _ in range(7) if random.randint(1, 3) == 1)

        # C Rank Distro
        c_rank_vals = sum(1 for _ in range(10) if random.randint(1, 3) == 1)

        # B Rank Distro
        b_rank_vals = sum(1 for _ in range(10) if random.randint(1, 5) == 1)

        # A Rank Distro
        a_rank_vals = sum(1 for _ in range(10) if random.randint(1, 10) == 1)

        # S Rank Distro
        s_rank_vals = sum(1 for _ in range(1) if random.randint(1, 10) == 1)

        # Red Gate Rank Distro
        red_rank_vals = sum(1 for _ in range(10) if random.randint(1, 20) == 1)

        # Store today's values in the dictionary
        dun_check_data[current_date_string] = {
            "E": e_rank_vals,
            "D": d_rank_vals,
            "C": c_rank_vals,
            "B": b_rank_vals,
            "A": a_rank_vals,
            "S": s_rank_vals,
            "Red Gate": red_rank_vals
        }

        # Write the updated data back to the file
        with open(file_path, 'w') as wrt_dun_check:
            ujson.dump(dun_check_data, wrt_dun_check, indent=6)
    
    # Retrieve today's values from the data
    e_rank = dun_check_data[current_date_string]["E"]
    d_rank = dun_check_data[current_date_string]["D"]
    c_rank = dun_check_data[current_date_string]["C"]
    b_rank = dun_check_data[current_date_string]["B"]
    a_rank = dun_check_data[current_date_string]["A"]
    s_rank = dun_check_data[current_date_string]["S"]
    red_gate = dun_check_data[current_date_string]["Red Gate"]

    return e_rank, d_rank, c_rank, b_rank, a_rank, s_rank

def dungeon_rank_get(rank, amt1, amt1_check, act1):
    with open("Files/Player Data/Status.json", 'r') as fson:
        data = ujson.load(fson)
        agi1 = data["status"][0]['agi']
        stre1 = data["status"][0]['str']
        str_eqip = data["equipment"][0]['STR']
        agi_eqip = data["equipment"][0]['AGI']

        with open("Files/Player Data/Skill.json", 'r') as f:
            skill_data = ujson.load(f)

        equipment_percent=0
        if thesystem.system.skill_use("Mind Over Matter", (0)) == True and ("Mind Over Matter"in skill_data):
            lvl=skill_data["Mind Over Matter"][0]["lvl"]
            if type(lvl)==str: lvl=10

            equipment_percent=0.05*lvl

        agi_eqip1=agi_eqip+(agi_eqip*equipment_percent)
        str_eqip1=str_eqip+(str_eqip*equipment_percent)

        agi=agi1+agi_eqip1
        stre=stre1+str_eqip1
    
    rank_modifiers = {
        'D': {"amt": {50: 10, 15: 5, 2: 1, 30: 15, 1: 1}, "time": {45: 15, 60: 60, 1: 1}},
        'C': {"amt": {50: 20, 15: 15, 2: 2, 30: 30, 1: 2}, "time": {45: 30, 60: 120, 1: 2}},
        'B': {"amt": {50: 30, 15: 35, 2: 3, 30: 60, 1: 3}, "time": {45: 45, 60: 240, 1: 4}},
        'A': {"amt": {50: 100, 15: 50, 2: 5, 30: 70, 1: 4}, "time": {45: 65, 60: 360, 1: 6}},
        'S': {"amt": {50: 150, 15: 85, 2: 8, 30: 90, 1: 5}, "time": {45: 75, 60: 540, 1: 9}}
    }
    
    if rank in rank_modifiers and amt1_check in rank_modifiers[rank]:
        amt1 += rank_modifiers[rank][amt1_check].get(amt1, 0)
    
    amt1 -= (reduction(amt1, stre, agi, amt1_check))
    amt1 = max(1, int(round(amt1 * 0.25)))
    return amt1

def reduction(val, stre, agi, types):
    thresholds = {
        "amt": {
            50: [(80, 120, -10), (121, 160, -20), (161, 200, -30), (201, 240, -40), (241, 280, -100)],
            15: [(80, 120, -5), (121, 160, -5), (161, 200, -10), (201, 240, -25), (241, 280, -35)],
            30: [(80, 120, -10), (121, 160, -10), (161, 200, -20), (201, 240, -25), (241, 280, -35)]
        },
        "time": {
            45: [(80, 120, -10), (121, 160, -20), (161, 200, -30), (201, 240, -30), (241, 280, -40)],
            60: [(80, 120, -20), (121, 160, -30), (161, 200, -100), (201, 240, -100), (241, 280, -200)]
        }
    }
    
    if types in thresholds and val in thresholds[types]:
        stat = stre if types == "amt" else agi
        for lower, upper, reduction in thresholds[types][val]:
            if lower <= stat <= upper:
                return reduction
    
    return 0

def calculate_hp_deduction(player_rank: str, quest_rank: str, enemies_ignored: int = 1) -> float:
    hp_add=0
    # Rank weights — linear scale
    player_rank_scores = {'National': 7, 'S': 6, 'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1}
    quest_rank_scores = {'E': 1, 'D': 2, 'C': 3, 'B': 4, 'A': 5, 'S': 6}

    # Clamp number of ignored enemies
    enemies_ignored = max(0, min(enemies_ignored, 4))

    # Convert ranks to numeric scale
    player_score = player_rank_scores.get(player_rank, 1)
    quest_score = quest_rank_scores.get(quest_rank, 1)

    # Deduction per enemy is:
    #   (quest_score / player_score) * (base per-enemy percent)
    # We'll use base = 0.1 (10%), and total is capped at 100%

    base_deduction_per_enemy = 0.1  # 10% base per enemy
    deduction = (quest_score / player_score) * base_deduction_per_enemy * enemies_ignored

    with open("Files/Player Data/Status.json", 'r') as data_fson:
        data_status=ujson.load(data_fson)
        current_hp=data_status["status"][0]["hp"]
        level=data_status["status"][0]["level"]
        max_hp=100+(100*level)

        deductable=max_hp*deduction

        if current_hp-deductable<=50:
            #Skill File
            with open("Files/Player Data/Skill.json", 'r') as f:
                skill_data = ujson.load(f)

            if thesystem.skills.skill_use("Iron Warrior", (24*60*60)) == True and ("Iron Warrior"in skill_data):
                lvl=skill_data["Iron Warrior"][0]["lvl"]
                if type(lvl)==str: lvl=10
                hp_add=max_hp*(0.025*lvl)

        if (current_hp+hp_add)-deductable<0:
            data_status["status"][0]["hp"]=0
            thesystem.system.message_open("Dead")
        
        else:
            data_status["status"][0]["hp"]-=deductable
            data_status["status"][0]["hp"]+=hp_add

        with open("Files/Player Data/Status.json", 'w') as data_fson:
            ujson.dump(data_status, data_fson)

        if data_status["status"][0]["hp"]-(deductable/enemies_ignored)<0:
            thesystem.system.message_open("Will die")

        
