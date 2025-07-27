from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ujson
import csv
import subprocess
import threading
import cv2
from PIL import Image, ImageTk
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../../'))

sys.path.insert(0, project_root)

import thesystem.system

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame0"
EQUIPMENT_TEMP_FILE = 'Files/Temp Files/Equipment Temp.csv'
INVENTORY_FILE = 'Files/Player Data/Inventory.json'
EQUIPMENT_FILE = 'Files/Player Data/Equipment.json'
STATUS_FILE = 'Files/Player Data/Status.json'
PRESETS_FILE = "Files/Mod/presets.json"

# Utility Functions
def relative_to_assets(path: str) -> Path:
    """Returns the relative path to assets."""
    return ASSETS_PATH / path

def load_ujson(file_path):
    """Loads ujson data from a file."""
    try:
        with open(file_path, 'r') as file:
            return ujson.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}

def save_ujson(file_path, data):
    """Saves ujson data to a file."""
    try:
        with open(file_path, 'w') as file:
            ujson.dump(data, file, indent=6)
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")

def resolve_buff_name(buff_key):
    """Maps buff/debuff keys to corresponding attribute names."""
    buff_map = {
        "AGIbuff": "AGI", "STRbuff": "STR", "VITbuff": "VIT",
        "INTbuff": "INT", "PERbuff": "PER", "MANbuff": "MAN",
        "AGIdebuff": "AGI", "STRdebuff": "STR", "VITdebuff": "VIT",
        "INTdebuff": "INT", "PERdebuff": "PER", "MANdebuff": "MAN",
    }
    return buff_map.get(buff_key)

def process_item_buffs(item_data, status_data, sign=1):
    """Applies or removes buffs/debuffs to/from the status data."""
    for buff_type in ("buff", "debuff"):
        items = item_data.get(buff_type, {})
        if not isinstance(items, dict):
            # Handle or log error: perhaps skip or try to parse the string into a dict
            continue
        for key, value in items.items():
            attribute = resolve_buff_name(key)
            if attribute:
                status_data["equipment"][0][attribute] += sign * value


# Command to open and handle equipment selection
def handle_selection(val, name, cat, window, dat1, dat2, dat3, dat4, dat5):
    equipment_data = load_ujson(EQUIPMENT_FILE)
    status_data = load_ujson(STATUS_FILE)

    if equipment_data.get(cat):
        current_item = list(equipment_data[cat].keys())[0]
        process_item_buffs(equipment_data[cat][current_item][0], status_data, sign=-1)

    if name != '-':
        new_item_data = {1: dat1, 2: dat2, 3: dat3, 4: dat4, 5: dat5}.get(val)
        if new_item_data is not None:
            equipment_data[cat] = new_item_data
            save_ujson(EQUIPMENT_FILE, equipment_data)

            new_item_name = list(new_item_data.keys())[0]
            process_item_buffs(new_item_data[new_item_name][0], status_data, sign=1)

    save_ujson(STATUS_FILE, status_data)
    subprocess.Popen(['python', 'Anime Version/Equipment/gui.py'])
    window.quit()

def equip_item(cat,item_full_data, window):

    if cat!="ORDER":
        with open('Files/Player Data/Inventory.json', 'r') as fout:
            data=ujson.load(fout)
            rol=list(data.keys())
        with open('Files/Player Data/Equipment.json', 'r') as first_equipment_file:
            first_equipment_file_data=ujson.load(first_equipment_file)
            if first_equipment_file_data[cat]!={}:
                item_old_name=list(first_equipment_file_data[cat].keys())[0]
                old_item_buff_main=list(first_equipment_file_data[cat][item_old_name][0]["buff"].keys())
                try:
                    # ? HELM BUFF 1 
                    old_item_boost_1_name=old_item_buff_main[0]
                    if old_item_boost_1_name=="AGIbuff":
                        oldbuff_1_name="AGI"
                    elif old_item_boost_1_name=="STRbuff":
                        oldbuff_1_name="STR"
                    elif old_item_boost_1_name=="VITbuff":
                        oldbuff_1_name="VIT"
                    elif old_item_boost_1_name=="INTbuff":
                        oldbuff_1_name="INT"
                    elif old_item_boost_1_name=="PERbuff":
                        oldbuff_1_name="PER"
                    elif old_item_boost_1_name=="MANbuff":
                        oldbuff_1_name="MAN"

                    oldbuff1_value=data[cat][item_old_name][0]["buff"][old_item_boost_1_name]

                    # ? HELM BUFF 2
                    old_item_boost_2_name=old_item_buff_main[1]
                    if old_item_boost_2_name=="AGIbuff":
                        oldbuff_2_name="AGI"
                    elif old_item_boost_2_name=="STRbuff":
                        oldbuff_2_name="STR"
                    elif old_item_boost_2_name=="VITbuff":
                        oldbuff_2_name="VIT"
                    elif old_item_boost_2_name=="INTbuff":
                        oldbuff_2_name="INT"
                    elif old_item_boost_2_name=="PERbuff":
                        oldbuff_2_name="PER"
                    elif old_item_boost_2_name=="MANbuff":
                        oldbuff_2_name="MAN"

                    oldbuff2_value=data[cat][item_old_name][0]["buff"][old_item_boost_2_name]
                except:
                    print("",end='')

                try:
                    old_item_debuff_main=list(first_equipment_file_data[cat][item_old_name][0]["debuff"].keys())
                    # ? HELM BUFF 1 
                    old_item_deboost_1_name=old_item_debuff_main[0]
                    if old_item_deboost_1_name=="AGIbuff":
                        olddebuff_1_name="AGI"
                    elif old_item_deboost_1_name=="STRdebuff":
                        olddebuff_1_name="STR"
                    elif old_item_deboost_1_name=="VITdebuff":
                        olddebuff_1_name="VIT"
                    elif old_item_deboost_1_name=="INTdebuff":
                        olddebuff_1_name="INT"
                    elif old_item_deboost_1_name=="PERdebuff":
                        olddebuff_1_name="PER"
                    elif old_item_deboost_1_name=="MANdebuff":
                        olddebuff_1_name="MAN"

                    olddebuff1_value=data[cat][item_old_name][0]["debuff"][old_item_deboost_1_name]

                    # ? HELM BUFF 2
                    old_item_deboost_2_name=old_item_debuff_main[1]
                    if old_item_deboost_2_name=="AGIdebuff":
                        olddebuff_2_name="AGI"
                    elif old_item_deboost_2_name=="STRdebuff":
                        olddebuff_2_name="STR"
                    elif old_item_deboost_2_name=="VITdebuff":
                        olddebuff_2_name="VIT"
                    elif old_item_deboost_2_name=="INTdebuff":
                        olddebuff_2_name="INT"
                    elif old_item_deboost_2_name=="PERdebuff":
                        olddebuff_2_name="PER"
                    elif old_item_deboost_2_name=="MANdebuff":
                        olddebuff_2_name="MAN"

                    olddebuff2_value=data[cat][item_old_name][0]["debuff"][old_item_deboost_2_name]
                except:
                    print("",end='')

                with open("Files/Player Data/Status.json", 'r') as status_file_eq:
                    status_file_eq_data=ujson.load(status_file_eq)
                    try:
                        status_file_eq_data["equipment"][0][oldbuff_1_name]=-oldbuff1_value
                        status_file_eq_data["equipment"][0][oldbuff_2_name]=-oldbuff2_value
                    except:
                        print()

                    try:
                        status_file_eq_data["equipment"][0][olddebuff_1_name]=+olddebuff1_value
                        status_file_eq_data["equipment"][0][olddebuff_2_name]=+olddebuff2_value
                    except:
                        print()

                first_equipment_file_data[cat]={}

                with open('Files/Player Data/Equipment.json', 'w') as second_write_equipment_file:
                    ujson.dump(first_equipment_file_data, second_write_equipment_file, indent=6)

                with open('Files/Player Data/Status.json', 'w') as second_write_status_file:
                    ujson.dump(status_file_eq_data, second_write_status_file, indent=4)

        if cat in ["HELM", "CHESTPLATE", "FIRST GAUNTLET", "SECOND GAUNTLET", "BOOTS", "COLLAR", "RING"]:
            with open('Files/Player Data/Equipment.json', 'r') as finale_equip:
                finale_equip_data=ujson.load(finale_equip)
                finale_equip_data[cat]=item_full_data

            with open('Files/Player Data/Equipment.json', 'w') as inject:
                ujson.dump(finale_equip_data, inject, indent=6)

            with open('Files/Player Data/Equipment.json', 'r') as second_equipment_file:
                second_equipment_file_data=ujson.load(second_equipment_file)
                item_new_name=list(second_equipment_file_data[cat].keys())[0]
                new_item_buff_main=list(second_equipment_file_data[cat][item_new_name][0]["buff"].keys())

                # ? HELM BUFF 1 
                new_item_boost_1_name=new_item_buff_main[0]
                if new_item_boost_1_name=="AGIbuff":
                    newbuff_1_name="AGI"
                elif new_item_boost_1_name=="STRbuff":
                    newbuff_1_name="STR"
                elif new_item_boost_1_name=="VITbuff":
                    newbuff_1_name="VIT"
                elif new_item_boost_1_name=="INTbuff":
                    newbuff_1_name="INT"
                elif new_item_boost_1_name=="PERbuff":
                    newbuff_1_name="PER"
                elif new_item_boost_1_name=="MANbuff":
                    newbuff_1_name="MAN"

                newbuff1_value=second_equipment_file_data[cat][item_new_name][0]["buff"][new_item_boost_1_name]

                try:
                    # ? HELM BUFF 2
                    new_item_boost_2_name=new_item_buff_main[1]
                    if new_item_boost_2_name=="AGIbuff":
                        newbuff_2_name="AGI"
                    elif new_item_boost_2_name=="STRbuff":
                        newbuff_2_name="STR"
                    elif new_item_boost_2_name=="VITbuff":
                        newbuff_2_name="VIT"
                    elif new_item_boost_2_name=="INTbuff":
                        newbuff_2_name="INT"
                    elif new_item_boost_2_name=="PERbuff":
                        newbuff_2_name="PER"
                    elif new_item_boost_2_name=="MANbuff":
                        newbuff_2_name="MAN"

                    newbuff2_value=second_equipment_file_data[cat][item_new_name][0]["buff"][new_item_boost_2_name]
                except:
                    print("",end='')

                try:
                    new_item_debuff_main=list(second_equipment_file_data[cat][item_new_name][0]["debuff"].keys())
                    # ? HELM BUFF 1 
                    new_item_deboost_1_name=new_item_debuff_main[0]
                    if new_item_deboost_1_name=="AGIdebuff":
                        newbuff_1_name="AGI"
                    elif new_item_deboost_1_name=="STRdebuff":
                        newbuff_1_name="STR"
                    elif new_item_deboost_1_name=="VITdebuff":
                        newbuff_1_name="VIT"
                    elif new_item_deboost_1_name=="INTdebuff":
                        newbuff_1_name="INT"
                    elif new_item_deboost_1_name=="PERdebuff":
                        newbuff_1_name="PER"
                    elif new_item_deboost_1_name=="MANdebuff":
                        newbuff_1_name="MAN"

                    newdebuff1_value=data[cat][item_new_name][0]["debuff"][new_item_deboost_1_name]

                    # ? HELM BUFF 2
                    new_item_deboost_2_name=new_item_buff_main[1]
                    if new_item_deboost_2_name=="AGIdebuff":
                        newdebuff_2_name="AGI"
                    elif new_item_deboost_2_name=="STRdebuff":
                        newdebuff_2_name="STR"
                    elif new_item_deboost_2_name=="VITdebuff":
                        newdebuff_2_name="VIT"
                    elif new_item_deboost_2_name=="INTdebuff":
                        newdebuff_2_name="INT"
                    elif new_item_deboost_2_name=="PERdebuff":
                        newdebuff_2_name="PER"
                    elif new_item_deboost_2_name=="MANdebuff":
                        newdebuff_2_name="MAN"

                    newdebuff2_value=data[cat][item_new_name][0]["debuff"][new_item_deboost_2_name]
                except:
                    print("",end='')

                with open("Files/Player Data/Status.json", 'r') as status2_file_eq:
                    status2_file_eq_data=ujson.load(status2_file_eq)
                    try:
                        status2_file_eq_data["equipment"][0][newbuff_1_name]=status2_file_eq_data["equipment"][0][newbuff_1_name]+newbuff1_value
                        status2_file_eq_data["equipment"][0][newbuff_2_name]=status2_file_eq_data["equipment"][0][newbuff_2_name]+newbuff2_value
                    except:
                        print()

                    try:
                        status2_file_eq_data["equipment"][0][olddebuff_1_name]=-newdebuff1_value
                        status2_file_eq_data["equipment"][0][olddebuff_2_name]=-newdebuff2_value
                    except:
                        print()

                with open('Files/Player Data/Equipment.json', 'w') as second_final_write_equipment_file:
                    ujson.dump(second_equipment_file_data, second_final_write_equipment_file, indent=6)

                with open('Files/Player Data/Status.json', 'w') as second_final_write_status_file:
                    ujson.dump(status2_file_eq_data, second_final_write_status_file, indent=4)

            with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
                theme_data=ujson.load(themefile)
                theme=theme_data["Theme"]
            with open("Files/Player Data/Tabs.json",'r') as tab_son:
                tab_son_data=ujson.load(tab_son)

            if tab_son_data["Inventory"]=='Close':
                subprocess.Popen(['python', f'{theme} Version/Equipment/gui.py'])
            window.quit()

    elif cat.upper()=="RUNE STONE":

        # Get the name of the Rune Stone from item_full_data
        # item_full_data is a dict like {"Rune of Fire": [ ... ]}
        rune_name = list(item_full_data.keys())[0]

        # Load the full skill list
        with open("Files/Data/Skill_List.json", "r") as skill_list_file:
            skill_list_data = ujson.load(skill_list_file)

        # Load the player's skills
        skill_json_path = "Files/Player Data/Skill.json"
        if os.path.exists(skill_json_path):
            with open(skill_json_path, "r") as player_skill_file:
                player_skill_data = ujson.load(player_skill_file)
        else:
            player_skill_data = {}

        # Add or update the skill
        if rune_name in player_skill_data:
            # Skill already exists, increment level
            current_lvl = player_skill_data[rune_name][0].get("lvl", 1)
            if isinstance(current_lvl, str) and current_lvl == "MAX":
                pass  # Already maxed, do nothing
            else:
                try:
                    new_lvl = int(current_lvl) + 1
                    if new_lvl >= 10:
                        player_skill_data[rune_name][0]["lvl"] = "MAX"
                    else:
                        player_skill_data[rune_name][0]["lvl"] = new_lvl
                except Exception:
                    player_skill_data[rune_name][0]["lvl"] = 2  # fallback if something is wrong
        else:
            # Add the skill from the skill list, set lvl to 1
            if rune_name in skill_list_data:
                # Deep copy to avoid reference issues
                import copy
                skill_entry = copy.deepcopy(skill_list_data[rune_name])
                if isinstance(skill_entry, list) and len(skill_entry) > 0:
                    skill_entry[0]["lvl"] = 1
                    skill_entry[0]["pl_point"] = 0
                player_skill_data[rune_name] = skill_entry

        # Save the updated skills
        with open(skill_json_path, "w") as player_skill_file:
            ujson.dump(player_skill_data, player_skill_file, indent=4)

        # Remove or decrement the Rune Stone from inventory
        with open("Files/Player Data/Inventory.json", "r") as inv_file:
            inv_data = ujson.load(inv_file)

        if rune_name in inv_data:
            qty = inv_data[rune_name][0].get("qty", 1)
            if qty > 1:
                inv_data[rune_name][0]["qty"] = qty - 1
            else:
                del inv_data[rune_name]

        with open("Files/Player Data/Inventory.json", "w") as inv_file:
            ujson.dump(inv_data, inv_file, indent=6)

        # Refresh the GUI
        with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
            theme_data = ujson.load(themefile)
            theme = theme_data["Theme"]
        subprocess.Popen(['python', f'{theme} Version/Inventory/gui.py'])
        window.quit()

    if cat=="ORDER":
        with open("Files/Player Data/Inventory.json", 'r') as fson:
            data_fininv=ujson.load(fson)
        del data_fininv["The Orb of Order"]

        subprocess.Popen(['python', "First/The Order/gui.py"])
        window.quit()




