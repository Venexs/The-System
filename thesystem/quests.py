from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ujson
import csv
import random
import subprocess
import os
import thesystem.system
from PIL import Image, ImageTk

def quest_adding_func(entry_1,entry_2,entry_3,entry_4,entry_5,entry_6,window):
    try:
        with open("Files/Player Data/Active_Quests.json", 'r') as active_quests_file:
            activ_quests=ujson.load(active_quests_file)
            name_of_activ_quests=list(activ_quests.keys())
            activ_quests_vals=0
            for k in name_of_activ_quests:
                activ_quests_vals+=1
    except:
        name_of_activ_quests=[]
    
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]

    if activ_quests_vals<13 and activ_quests_vals!=13:
        quest_name='-'+entry_1.get()
        quest_type=(entry_2.get()).upper()
        quest_obj=entry_3.get()
        quest_amt=entry_4.get()
        quest_amt_type=entry_5.get()
        rank=(entry_6.get()).upper()

        if rank not in ["E", "D", "C", "B", "A", "S"]:
            rank='E'

        if quest_type not in ["STR", "INT"]:
            quest_type="STR"

        if quest_type=='STR':
            rew3="STRav"
        elif quest_type=='INT':
            rew3="INTav"

        id_val=random.randrange(1,999999)

        with open("Files/Data/Quest_Desc.json", 'r') as quest_desc_file:
            quest_desc=ujson.load(quest_desc_file)
            if rank in ["E", "D"]:
                desc_list=quest_desc["Easy"]
                findesc=random.choice(desc_list)
            elif rank in ["C", "B"]:
                desc_list=quest_desc["Intermediate"]
                findesc=random.choice(desc_list)
            elif rank in ["A", "S"]:
                desc_list=quest_desc["Hard"]
                findesc=random.choice(desc_list)

        # ? Rewards
        amt={
            "S":250000, 
            "A":130000,
            "B":80000,
            "C":5000,
            "D":500,
            "E":300
            }
        
        coinval=amt[rank]
        rew1=f"Coin Bag {coinval}"
        with open("Files/Data/Inventory_List.json", 'r') as rewards_name_file:
            reward_names=ujson.load(rewards_name_file)
            reward_names_list=list(reward_names.keys())

            final_rewards_list=[]
            for k in reward_names_list:
                if rank==reward_names[k][0]["rank"]:
                    final_rewards_list.append(k)
            
            rew2=random.choice(final_rewards_list)

        rew_dict={rew1:1, rew2:1}
        if rank in ["S"]:
            rew_dict["LVLADD"]=8
            rew_dict[rew3]=10
        elif rank in ["A"]:
            rew_dict["LVLADD"]=5
            rew_dict[rew3]=8
        elif rank in ["B"]:
            rew_dict["LVLADD"]=2
            rew_dict[rew3]=6


        detail=[{
            "desc":findesc,
            "amt":quest_amt,
            "amtval":quest_amt_type,
            "type":"Learn",
            "obj_desc":"Quest given by Player. No description Available",
            "rank":rank,
            "ID": id_val,
            "Rewards":rew_dict,
            "skill":quest_obj
        }]

        activ_quests[quest_name]=detail

        with open("Files/Player Data/Active_Quests.json", 'w') as fin_active_quest_file:
            ujson.dump(activ_quests, fin_active_quest_file, indent=6)

    else:
        thesystem.systen.message_open("Quest Slot Filled")

    window.quit()

    subprocess.Popen(['python', f'{theme} Version/Quests/gui.py'])

def quest_reward(window,dicts,rank,name,special=False):
    rol=list(dicts.keys())
    for k in rol:
        if k=="LVLADD":
            with open("Files/Player Data/Status.json", 'r') as fson:
                    data_status=ujson.load(fson)
            
            old_level=data_status["status"][0]['level']
            for k in range(dicts[k]):
                data_status["status"][0]['level']+=1
                data_status["status"][0]['str']+=1
                data_status["status"][0]['agi']+=1
                data_status["status"][0]['vit']+=1
                data_status["status"][0]['int']+=1
                data_status["status"][0]['per']+=1
                data_status["status"][0]['hp']+=10
                data_status["status"][0]['mp']+=10
                data_status["status"][0]['fatigue_max']+=40
                if special!=True:
                    data_status["status"][0]['fatigue']+=thesystem.system.give_fatigue_from_rank(rank)
            
            new_level=data_status["status"][0]['level']
            thesystem.system.rank_up(old_level,new_level)
                
            if rank=="E":
                data_status["status"][0]['XP']+=10
            elif rank=="D":
                data_status["status"][0]['XP']+=20
            elif rank=="C":
                data_status["status"][0]['XP']+=40
            elif rank=="B":
                data_status["status"][0]['XP']+=80
            elif rank=="A":
                data_status["status"][0]['XP']+=150
            elif rank=="S":
                data_status["status"][0]['XP']+=200
            else:
                data_status["status"][0]['XP']+=1000

            with open("Files/Player Data/Status.json", 'w') as fson:
                ujson.dump(data_status, fson, indent=4)
            with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
                theme_data=ujson.load(themefile)
                theme=theme_data["Theme"]
            subprocess.Popen(['python', f'{theme} Version/Leveled up/gui.py'])

        elif k=="STRav":
            for k in range(dicts[k]):
                with open("Files/Player Data/Status.json", 'r') as fson:
                    data_status_2=ujson.load(fson)
                    
                    data_status_2["avail_eq"][0]['str_based']+=1

                with open("Files/Player Data/Status.json", 'w') as fson:
                    ujson.dump(data_status_2, fson, indent=4)

        elif k=="INTav":
            for k in range(dicts[k]):
                with open("Files/Player Data/Status.json", 'r') as fson:
                    data_status_3=ujson.load(fson)
                    
                    data_status_3["avail_eq"][0]['int_based']+=1

                with open("Files/Player Data/Status.json", 'w') as fson:
                    ujson.dump(data_status_3, fson, indent=4)

        else:
            check=False
            with open("Files/Data/Inventory_list.json", 'r') as fson:
                data_inv=ujson.load(fson)
                item=data_inv[k]
                name_of_item=k
            
            with open("Files/Player Data/Inventory.json", 'r') as fson:
                data_fininv=ujson.load(fson)
                key_data=list(data_fininv.keys())

                for k in key_data:
                    if name_of_item==k:
                        check=True
            
            if check==True:
                data_fininv[name_of_item][0]["qty"]+=1

            elif check==False:
                data_fininv[name_of_item]=item

            with open("Files/Player Data/Inventory.json", 'w') as finaladdon:
                ujson.dump(data_fininv, finaladdon, indent=6)

    with open("Files/Player Data/Active_Quests.json", 'r') as fols:
        quests=ujson.load(fols)

    del quests[name]

    with open("Files/Player Data/Active_Quests.json", 'w') as folas: 
        ujson.dump(quests, folas, indent=6)

    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    
    if special==False:
        if theme=="Anime":
            with open("Files\Temp Files\Quest Rewards.json", 'r') as fols:
                data_quest_rewards=ujson.load(fols)
                
            data_quest_rewards["Type"]="Quest"
            data_quest_rewards["Rewards"]=dicts

            with open("Files\Temp Files\Quest Rewards.json", 'w') as fols:
                ujson.dump(data_quest_rewards, fols, indent=6)
            
            subprocess.Popen(['python', f'{theme} Version/New Items/gui.py'])
        else:
            thesystem.system.message_open("Quest Completed")
            subprocess.Popen(['python', f'{theme} Version/Quests/gui.py'])
    else:
        thesystem.system.message_open("Revertion")
        subprocess.Popen(['python', 'First/Vows/gui.py'])

    window.quit()

def abandon_quest(name,window):
    with open("Files/Player Data/Active_Quests.json", 'r') as fols:
        quests=ujson.load(fols)

    del quests[name]

    with open("Files/Player Data/Active_Quests.json", 'w') as fols:
        ujson.dump(quests, fols, indent=6)

    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    subprocess.Popen(['python', f'{theme} Version/Quests/gui.py'])

    window.quit()

def get_quest_image(rank,typel):
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    if rank!='-' and typel!='-':
        if rank=='D' or rank=='E':
            if typel=="Common":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_5.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_6.png"))
            
        elif rank=='C' or rank=='B':
            if typel=="Common":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_8.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_9.png"))
            
        elif rank=='A':
            if typel=="Common":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_11.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_12.png"))
            
        elif rank=='S':
            if typel=="Common":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_14.png"))
            
            elif typel=="Learn":
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_15.png"))
        
        elif rank=='?':
            if typel=='Unknown':
                return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_16.png"))
    else:
        return PhotoImage(file=(f"{theme} Version/Quests/assets/frame0/image_17.png"))

def open_write_quest(name,id,type,window):
    if name!="-":
        with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
            theme_data=ujson.load(themefile)
            theme=theme_data["Theme"]
        with open("Files/Temp Files/Quest Temp.csv", 'w', newline='') as csv_open:
                fw=csv.writer(csv_open)
                rec=[name,id,type]
                fw.writerow(rec)

        subprocess.Popen(['python', f'{theme} Version/Quest Info/gui.py'])

        with open("Files/Player Data/Tabs.json",'r') as tab_son:
            tab_son_data=ujson.load(tab_son)

        with open("Files/Player Data/Tabs.json",'w') as fin_tab_son:
            tab_son_data["Quest"]='Close'
            ujson.dump(tab_son_data,fin_tab_son,indent=4)

        window.quit()

def get_item_image(name):
    try:
        # Construct the absolute path to the Images folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if name.split()[0] == 'Coin' and name.split()[1] == 'Bag':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Coin Pouch Big.png")

        elif name.split()[-1] == 'Key':
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Instance Keys Big.png")

        elif name=="INT. Based Points"or name=="INTav":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "AVINT" + '.png')

        elif name=="STR. Based Points" or name=="STRav":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "AVSTR" + '.png')

        elif name.split()[0]=="Coins:":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Coin" + '.png')

        elif name.split()[0]=="Experience":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "XP" + '.png')

        elif name=="LVLADD":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Level Add" + '.png')

        elif name=="":
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, "Unknown" + '.png')

        else:
            file_loc = os.path.join(script_dir, "Images")
            files = os.path.join(file_loc, name + ' Big.png')

        if not os.path.exists(files):
            files = os.path.join(file_loc, "Unknown.png")

        # Open and resize the image
        image = Image.open(files)

        # Crop to 680x680 (centered)
        width, height = image.size
        left = 0
        top = (height - 680) // 2  # Crop from center
        right = 680
        bottom = top + 680
        image = image.crop((left, top, right, bottom))

        image = image.resize((38, 38), Image.Resampling.LANCZOS)  # High-quality resize
        return ImageTk.PhotoImage(image)

    except:
        return None  # Handle errors properly




