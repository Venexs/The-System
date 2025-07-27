import ujson
import os
from PIL import Image, ImageTk
import thesystem.system

STAT_MAP = {
    "AGIbuff": "AGI",
    "STRbuff": "STR",
    "VITbuff": "VIT",
    "INTbuff": "INT",
    "PERbuff": "PER",
    "MANbuff": "MAN",
    "AGIdebuff": "AGI",
    "STRdebuff": "STR",
    "VITdebuff": "VIT",
    "INTdebuff": "INT",
    "PERdebuff": "PER",
    "MANdebuff": "MAN"
}

def extract_boosts(item_data):
    """
    Given the item data (a list with one dictionary) returns a list of boost strings.
    Each boost string is formatted as 'STAT +value'
    """
    boosts = []
    buff_data = item_data.get("buff", {})
    if isinstance(buff_data, dict):
        for key in list(buff_data.keys())[:2]:  # get up to two buffs
            stat = STAT_MAP.get(key, key)
            boosts.append(f"{stat} +{thesystem.system.equipment_value_plus(buff_data[key])}")
    return boosts

def extract_deboosts(item_data):
    """
    Extract debuff values and return a dict mapping stat to value.
    """
    debuffs = {}
    debuff_data = item_data.get("debuff", {})
    if isinstance(debuff_data, dict):
        for key in list(debuff_data.keys())[:2]:
            stat = STAT_MAP.get(key, key)
            debuffs[stat] = debuff_data[key]
    return debuffs

def get_equipment():
    """
    Reads equipment from the Equipment.json file and returns a two-item list:
    - The first element is a list of equipment names (or '-' if not present)
    - The second element is a list of boost strings for each item
    """
    equip_keys = ["HELM", "CHESTPLATE", "FIRST GAUNTLET", "SECOND GAUNTLET", "BOOTS", "RING", "COLLAR"]
    equipment = {key: "-" for key in equip_keys}
    boosts = {key: ["", ""] for key in equip_keys}  # store up to two boosts per item

    with open('Files/Player Data/Equipment.json', 'r') as fin:
        data = ujson.load(fin)

    for key in equip_keys:
        try:
            # Get the first item for the category
            item_name = list(data[key].keys())[0]
            equipment[key] = item_name
            item_info = data[key][item_name][0]
            item_boosts = extract_boosts(item_info)
            # Ensure two boost strings (empty string if not available)
            boosts[key] = item_boosts + [""] * (2 - len(item_boosts))
        except Exception:
            # If any error, leave defaults
            continue

    # Flatten the equipment and boosts dictionaries into lists in the order of equip_keys
    equipment_list = [equipment[k] for k in equip_keys]
    boosts_list = [boost for k in equip_keys for boost in boosts[k]]
    return [equipment_list, boosts_list]

def finish(qty, equipment_check):
    """
    Removes equipment and adjusts status from Equipment.json and status.json files.
    equipment_check: a two-element list returned by get_equipment() where
        the first element is a list of equipment names.
    """
    if qty != 1:
        return

    # equipment_check[0] is a list of equipment names in order:
    equip_keys = ["HELM", "CHESTPLATE", "FIRST GAUNTLET", "SECOND GAUNTLET", "BOOTS", "RING", "COLLAR"]
    # Expect equipment_check[0] to indicate which category is being processed.
    # For this function, we assume that equipment_check[0] contains exactly one category name.
    cat = equipment_check[0]
    if cat not in equip_keys:
        return

    with open('Files/Player Data/Equipment.json', 'r') as eq_file:
        eq_data = ujson.load(eq_file)

    if not eq_data.get(cat):
        return

    try:
        item_name = list(eq_data[cat].keys())[0]
        item_info = eq_data[cat][item_name][0]
        # Extract boost values
        buff_keys = list(item_info.get("buff", {}).keys())
        if len(buff_keys) >= 2:
            boost1_key = buff_keys[0]
            boost2_key = buff_keys[1]
            boost1_stat = STAT_MAP.get(boost1_key, boost1_key)
            boost2_stat = STAT_MAP.get(boost2_key, boost2_key)
            boost1_value = item_info["buff"][boost1_key]
            boost2_value = item_info["buff"][boost2_key]
        else:
            boost1_stat = boost2_stat = None
            boost1_value = boost2_value = 0
    except Exception:
        boost1_stat = boost2_stat = None
        boost1_value = boost2_value = 0

    try:
        debuffs = extract_deboosts(item_info)
        # Get the first two debuffs (if available)
        debuff_items = list(debuffs.items())
        if len(debuff_items) >= 2:
            debuff1_stat, debuff1_value = debuff_items[0]
            debuff2_stat, debuff2_value = debuff_items[1]
        else:
            debuff1_stat = debuff2_stat = None
            debuff1_value = debuff2_value = 0
    except Exception:
        debuff1_stat = debuff2_stat = None
        debuff1_value = debuff2_value = 0

    # Update status.json accordingly
    with open("Files/Player Data/Status.json", 'r') as status_file:
        status_data = ujson.load(status_file)

    try:
        if boost1_stat:
            status_data["equipment"][0][boost1_stat] = -(boost1_value)
        if boost2_stat:
            status_data["equipment"][0][boost2_stat] = -(boost2_value)
    except Exception:
        pass

    try:
        if debuff1_stat:
            status_data["equipment"][0][debuff1_stat] = debuff1_value
        if debuff2_stat:
            status_data["equipment"][0][debuff2_stat] = debuff2_value
    except Exception:
        pass

    # Remove the equipment item
    eq_data[cat] = {}

    with open('Files/Player Data/Equipment.json', 'w') as eq_file:
        ujson.dump(eq_data, eq_file, indent=6)

    with open('Files/Player Data/Status.json', 'w') as status_file:
        ujson.dump(status_data, status_file, indent=4)

def find_item_slot(name, equipment):
    for slot, items in equipment.items():
        if name in items:
            return [slot, True]
    return ["Item not found in any slot", False]

def process_attributes(attr, attr_type):
    attr_name_1, attr_value_1 = '', '-'
    attr_name_2, attr_value_2 = '', '-'

    if isinstance(attr, dict):
        try:
            keys = list(attr.keys())
            mapping = {
                "AGIbuff": "AGI", "STRbuff": "STR", "VITbuff": "VIT", 
                "INTbuff": "INT", "PERbuff": "PER", "MANbuff": "MAN",
                "AGIdebuff": "AGI", "STRdebuff": "STR", "VITdebuff": "VIT",
                "INTdebuff": "INT", "PERdebuff": "PER", "MANdebuff": "MAN",
            }
            
            attr_name_1 = mapping.get(keys[0], '')
            attr_value_1 = f"{'+' if attr_type == 'buff' else '-'}{attr[keys[0]]}"

            if len(keys) > 1:
                attr_name_2 = mapping.get(keys[1], '')
                attr_value_2 = f"{'+' if attr_type == 'buff' else '-'}{attr[keys[1]]}"
        except:
            pass
    return attr_name_1, attr_value_1, attr_name_2, attr_value_2

def get_armor_image(name, max_width=376, max_height=376):
    try:
        # Construct the absolute path to the Images folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_loc = os.path.join(script_dir, "Equipment Display")
        files = os.path.join(file_loc, name + '.png')
        if not os.path.exists(files):
            raise FileNotFoundError
    except:
        file_loc = os.path.join(script_dir, "Equipment Display")
        files = os.path.join(file_loc, "unknown.png")

    # Open the image
    image = Image.open(files)
    
    # Calculate the resize ratio
    width_ratio = max_width / image.width
    height_ratio = max_height / image.height
    resize_ratio = min(width_ratio, height_ratio)
    
    # Resize the image
    new_width = int(image.width * resize_ratio)
    new_height = int(image.height * resize_ratio)
    resized_image = image.resize((new_width, new_height))
    
    # Convert the image to PhotoImage
    photo_image = ImageTk.PhotoImage(resized_image)

    return photo_image



