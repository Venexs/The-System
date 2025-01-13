import ujson
import csv
import thesystem.system as system
import subprocess
from datetime import datetime, timedelta
import random
import threading


with open('Files/Data/Theme_Check.json', 'r') as themefile:
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
    with open("Files/Tabs.json",'r') as tab_son:
        tab_son_data=ujson.load(tab_son)

    with open("Files/Tabs.json",'w') as fin_tab_son:
        tab_son_data["Dungeons"]='Close'
        ujson.dump(tab_son_data,fin_tab_son,indent=4)
    threading.Thread(target=system.fade_out, args=(win, 0.8)).start()
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    system.animate_window_close(win, initial_height, window_width, step=20, delay=1)

def check_fatigue(rank):
    with open("Files/Status.json", 'r') as data_fson:
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
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

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
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_d_dunfile(eve):
    rank='D'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

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
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_c_dunfile(eve):
    rank='C'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

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
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_b_dunfile(eve):
    rank='B'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

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
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_a_dunfile(eve):
    rank='A'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

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
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

def open_s_dunfile(eve):
    rank='S'
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

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
            ujson.dump(dun_full_data, final_dun_full, indent=6)

        subprocess.Popen(['python', f'{theme} Version/Dungeon Runs/gui.py'])
        ex_close(eve)

rank_order = {'E': 1, 'D': 2, 'C': 3, 'B': 4, 'A': 5, 'S': 6}

def instance_dungeon(eve):
    # Load the ujson data from the file
    with open('Files/inventory.json', 'r') as file:
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
    with open('Files/Inventory.json', 'r') as file:
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
    with open('Files/Inventory.json', 'w') as file:
        ujson.dump(data, file, indent=4)

    rank=item["rank"]
    with open("Files\Data\Todays_Dungeon.json", 'r') as dun_full:
        dun_full_data=ujson.load(dun_full)

    with open("Files\Data\Dungeon_Rank.csv", 'w', newline='') as rank_file:
        fw=csv.writer(rank_file)
        fw.writerow([rank,"Instance"])

    with open("Files\Data\Todays_Dungeon.json", 'w') as final_dun_full:
        ujson.dump(dun_full_data, final_dun_full, indent=6)

    subprocess.Popen(['python', 'Manwha Version/Dungeon Runs/gui.py'])
    window.quit()

def dun_check():
    global e_rank, d_rank, c_rank, b_rank, a_rank, s_rank, red_gate

    # Path to the ujson file
    file_path = "Files\\Data\\Todays_Dungeon.json"
    
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

def dungeon_rank_get(rank,amt1,amt1_check):
    with open("Files/status.json", 'r') as fson:
        data=ujson.load(fson)
        agi=data["status"][0]['agi']
        stre=data["status"][0]['str']
    minus=reduction(amt1, stre, agi, amt1_check)
    if rank=='D':
        if amt1_check=="amt":
            if amt1==50:
                amt1+=10
            elif amt1==15:
                amt1+=5
            elif amt1==2:
                amt1+=1
            elif amt1==30:
                amt1+=15
            elif amt1==1:
                amt1+=1
        elif amt1_check=="time":
            if amt1==45:
                amt1+=15
            elif amt1==60:
                amt1+=60
            elif amt1==1:
                amt1+=1
    elif rank=='C':
        if amt1_check=="amt":
            if amt1==50:
                amt1+=20
            elif amt1==15:
                amt1+=15
            elif amt1==2:
                amt1+=2
            elif amt1==30:
                amt1+=30
            elif amt1==1:
                amt1+=2
        elif amt1_check=="time":
            if amt1==45:
                amt1+=30
            elif amt1==60:
                amt1+=120
            elif amt1==1:
                amt1+=2
    elif rank=='B':
        if amt1_check=="amt":
            if amt1==50:
                amt1+=30
            elif amt1==15:
                amt1+=35
            elif amt1==2:
                amt1+=3
            elif amt1==30:
                amt1+=60
            elif amt1==1:
                amt1+=3
        elif amt1_check=="time":
            if amt1==45:
                amt1+=45
            elif amt1==60:
                amt1+=240
            elif amt1==1:
                amt1+=4
    elif rank=='A':
        if amt1_check=="amt":
            if amt1==50:
                amt1+=100
            elif amt1==15:
                amt1+=50
            elif amt1==2:
                amt1+=5
            elif amt1==30:
                amt1+=70
            elif amt1==1:
                amt1+=4
        elif amt1_check=="time":
            if amt1==45:
                amt1+=65
            elif amt1==60:
                amt1+=360
            elif amt1==1:
                amt1+=6
    elif rank=='S':
        if amt1_check=="amt":
            if amt1==50:
                amt1+=150
            elif amt1==15:
                amt1+=85
            elif amt1==2:
                amt1+=8
            elif amt1==30:
                amt1+=90
            elif amt1==1:
                amt1+=5
        elif amt1_check=="time":
            if amt1==45:
                amt1+=75
            elif amt1==60:
                amt1+=540
            elif amt1==1:
                amt1+=9

    amt1=amt1-minus
    return amt1

def reduction(val, stre, agi, types):
    if types=="amt":
        if val==50:
            if stre>=20 and stre<=30:
                return -10
            elif stre>=31 and stre<=40:
                return -20
            elif stre>=41 and stre<=50:
                return -30
            elif stre>=51 and stre<=60:
                return -40
            elif stre>=61 and stre<=70:
                return -100
            else:
                return 0
        
        elif val==15:
            if stre>=20 and stre<=30:
                return -5
            elif stre>=31 and stre<=40:
                return -5
            elif stre>=41 and stre<=50:
                return -10
            elif stre>=51 and stre<=60:
                return -25
            elif stre>=61 and stre<=70:
                return -35
            else:
                return 0
            
        elif val==30:
            if stre>=20 and stre<=30:
                return -10
            elif stre>=31 and stre<=40:
                return -10
            elif stre>=41 and stre<=50:
                return -20
            elif stre>=51 and stre<=60:
                return -25
            elif stre>=61 and stre<=70:
                return -35
        
        else:
            return 0
        
    elif types=="time":
        if val==45:
            if agi>=20 and agi<=30:
                return -10
            elif agi>=31 and agi<=40:
                return -20
            elif agi>=41 and agi<=50:
                return -30
            elif agi>=51 and agi<=60:
                return -30
            elif agi>=61 and agi<=70:
                return -40
            else:
                return 0
        
        elif val==60:
            if agi>=20 and agi<=30:
                return -20
            elif agi>=31 and agi<=40:
                return -30
            elif agi>=41 and agi<=50:
                return -100
            elif agi>=51 and agi<=60:
                return -100
            elif agi>=61 and agi<=70:
                return -200
            else:
                return 0
        
        else:
            return 0




