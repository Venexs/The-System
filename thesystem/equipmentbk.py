import ujson
import os
from PIL import Image, ImageTk

def get_equipment():
    helm=chest=f_gaun=s_gaun=boot=ring=collar='-'
    helmboost_1=chestboost_1=f_gaunboost_1=s_gaunboost_1=bootboost_1=ringboost_1=collarboost_1=''
    helmboost_2=chestboost_2=f_gaunboost_2=s_gaunboost_2=bootboost_2=ringboost_2=collarboost_2=''
    with open('Files/Equipment.json', 'r') as fout:
        data=ujson.load(fout)
        try:
            helm=list(data['HELM'].keys())[0]
            if type(data["HELM"][helm][0]["buff"]) is dict:
                helm_buff_main=list(data["HELM"][helm][0]["buff"].keys())

                # ? HELM BUFF 1 
                helmboost_1_name=helm_buff_main[0]
                if helmboost_1_name=="AGIbuff":
                    helmbuff_1_name="AGI"
                elif helmboost_1_name=="STRbuff":
                    helmbuff_1_name="STR"
                elif helmboost_1_name=="VITbuff":
                    helmbuff_1_name="VIT"
                elif helmboost_1_name=="INTbuff":
                    helmbuff_1_name="INT"
                elif helmboost_1_name=="PERbuff":
                    helmbuff_1_name="PER"
                elif helmboost_1_name=="MANbuff":
                    helmbuff_1_name="MAN"
                    
                helmboost_1=helmbuff_1_name+' +'+str(data["HELM"][helm][0]["buff"][helmboost_1_name])

                # ? HELM BUFF 2
                helmboost_2_name=helm_buff_main[1]
                if helmboost_2_name=="AGIbuff":
                    helmbuff_2_name="AGI"
                elif helmboost_2_name=="STRbuff":
                    helmbuff_2_name="STR"
                elif helmboost_2_name=="VITbuff":
                    helmbuff_2_name="VIT"
                elif helmboost_2_name=="INTbuff":
                    helmbuff_2_name="INT"
                elif helmboost_2_name=="PERbuff":
                    helmbuff_2_name="PER"
                elif helmboost_2_name=="MANbuff":
                    helmbuff_2_name="MAN"
                    
                helmboost_2=helmbuff_2_name+' +'+str(data["HELM"][helm][0]["buff"][helmboost_2_name])
        except:
            print('',end='')

        try:
            chest=list(data['CHESTPLATE'].keys())[0]
            if type(data["CHESTPLATE"][chest][0]["buff"]) is dict:
                chest_buff_main=list(data["CHESTPLATE"][chest][0]["buff"].keys())

                # ? CHEST BUFF 1 
                chestboost_1_name=chest_buff_main[0]
                if chestboost_1_name=="AGIbuff":
                    chestbuff_1_name="AGI"
                elif chestboost_1_name=="STRbuff":
                    chestbuff_1_name="STR"
                elif chestboost_1_name=="VITbuff":
                    chestbuff_1_name="VIT"
                elif chestboost_1_name=="INTbuff":
                    chestbuff_1_name="INT"
                elif chestboost_1_name=="PERbuff":
                    chestbuff_1_name="PER"
                elif chestboost_1_name=="MANbuff":
                    chestbuff_1_name="MAN"
                    
                chestboost_1=chestbuff_1_name+' +'+str(data["CHESTPLATE"][chest][0]["buff"][chestboost_1_name])

                # ? CHEST BUFF 2
                chestboost_2_name=chest_buff_main[1]
                if chestboost_2_name=="AGIbuff":
                    chestbuff_2_name="AGI"
                elif chestboost_2_name=="STRbuff":
                    chestbuff_2_name="STR"
                elif chestboost_2_name=="VITbuff":
                    chestbuff_2_name="VIT"
                elif chestboost_2_name=="INTbuff":
                    chestbuff_2_name="INT"
                elif chestboost_2_name=="PERbuff":
                    chestbuff_2_name="PER"
                elif chestboost_2_name=="MANbuff":
                    chestbuff_2_name="MAN"
                    
                chestboost_2=chestbuff_2_name+' +'+str(data["CHESTPLATE"][chest][0]["buff"][chestboost_2_name])
        except:
            print('',end='')

        try:
            f_gaun=list(data['FIRST GAUNTLET'].keys())[0]
            if type(data["FIRST GAUNTLET"][f_gaun][0]["buff"]) is dict:
                f_gaun_buff_main=list(data["FIRST GAUNTLET"][f_gaun][0]["buff"].keys())

                # ? First Gauntlet BUFF 1 
                f_gaunboost_1_name=f_gaun_buff_main[0]
                if f_gaunboost_1_name=="AGIbuff":
                    f_gaunbuff_1_name="AGI"
                elif f_gaunboost_1_name=="STRbuff":
                    f_gaunbuff_1_name="STR"
                elif f_gaunboost_1_name=="VITbuff":
                    f_gaunbuff_1_name="VIT"
                elif f_gaunboost_1_name=="INTbuff":
                    f_gaunbuff_1_name="INT"
                elif f_gaunboost_1_name=="PERbuff":
                    f_gaunbuff_1_name="PER"
                elif f_gaunboost_1_name=="MANbuff":
                    f_gaunbuff_1_name="MAN"
                    
                f_gaunboost_1=f_gaunbuff_1_name+' +'+str(data["FIRST GAUNTLET"][f_gaun][0]["buff"][f_gaunboost_1_name])

                # ? First Gauntlet BUFF 2 
                f_gaunboost_2_name=f_gaun_buff_main[1]
                if f_gaunboost_2_name=="AGIbuff":
                    f_gaunbuff_2_name="AGI"
                elif f_gaunboost_2_name=="STRbuff":
                    f_gaunbuff_2_name="STR"
                elif f_gaunboost_2_name=="VITbuff":
                    f_gaunbuff_2_name="VIT"
                elif f_gaunboost_2_name=="INTbuff":
                    f_gaunbuff_2_name="INT"
                elif f_gaunboost_2_name=="PERbuff":
                    f_gaunbuff_2_name="PER"
                elif f_gaunboost_2_name=="MANbuff":
                    f_gaunbuff_2_name="MAN"
                    
                f_gaunboost_2=f_gaunbuff_2_name+' +'+str(data["FIRST GAUNTLET"][f_gaun][0]["buff"][f_gaunboost_2_name])
        except:
            print('',end='')

        try:
            s_gaun=list(data['SECOND GAUNTLET'].keys())[0]
            if type(data["SECOND GAUNTLET"][s_gaun][0]["buff"]) is dict:
                s_gaun_buff_main=list(data["SECOND GAUNTLET"][s_gaun][0]["buff"].keys())

                # ? Second Gauntlet BUFF 1 
                s_gaunboost_1_name=s_gaun_buff_main[0]
                if s_gaunboost_1_name=="AGIbuff":
                    s_gaunbuff_1_name="AGI"
                elif s_gaunboost_1_name=="STRbuff":
                    s_gaunbuff_1_name="STR"
                elif s_gaunboost_1_name=="VITbuff":
                    s_gaunbuff_1_name="VIT"
                elif s_gaunboost_1_name=="INTbuff":
                    s_gaunbuff_1_name="INT"
                elif s_gaunboost_1_name=="PERbuff":
                    s_gaunbuff_1_name="PER"
                elif s_gaunboost_1_name=="MANbuff":
                    s_gaunbuff_1_name="MAN"
                    
                s_gaunboost_1=s_gaunbuff_1_name+' +'+str(data["SECOND GAUNTLET"][s_gaun][0]["buff"][s_gaunboost_1_name])

                # ? Second Gauntlet BUFF 2 
                s_gaunboost_2_name=s_gaun_buff_main[1]
                if s_gaunboost_2_name=="AGIbuff":
                    s_gaunbuff_2_name="AGI"
                elif s_gaunboost_2_name=="STRbuff":
                    s_gaunbuff_2_name="STR"
                elif s_gaunboost_2_name=="VITbuff":
                    s_gaunbuff_2_name="VIT"
                elif s_gaunboost_2_name=="INTbuff":
                    s_gaunbuff_2_name="INT"
                elif s_gaunboost_2_name=="PERbuff":
                    s_gaunbuff_2_name="PER"
                elif s_gaunboost_2_name=="MANbuff":
                    s_gaunbuff_2_name="MAN"

                s_gaunboost_2=s_gaunbuff_2_name+' +'+str(data["SECOND GAUNTLET"][s_gaun][0]["buff"][s_gaunboost_2_name])
        except:
            print('',end='')

        try:
            boot=list(data['BOOTS'].keys())[0]
            if type(data["BOOTS"][boot][0]["buff"]) is dict:
                boot_buff_main=list(data["BOOTS"][boot][0]["buff"].keys())

                # ? BOOT BUFF 1 
                bootboost_1_name=boot_buff_main[0]
                if bootboost_1_name=="AGIbuff":
                    bootbuff_1_name="AGI"
                elif bootboost_1_name=="STRbuff":
                    bootbuff_1_name="STR"
                elif bootboost_1_name=="VITbuff":
                    bootbuff_1_name="VIT"
                elif bootboost_1_name=="INTbuff":
                    bootbuff_1_name="INT"
                elif bootboost_1_name=="PERbuff":
                    bootbuff_1_name="PER"
                elif bootboost_1_name=="MANbuff":
                    bootbuff_1_name="MAN"
                    
                bootboost_1=bootbuff_1_name+' +'+str(data["BOOTS"][boot][0]["buff"][bootboost_1_name])

                # ? BOOT BUFF 2 
                bootboost_2_name=boot_buff_main[1]
                if bootboost_2_name=="AGIbuff":
                    bootbuff_2_name="AGI"
                elif bootboost_2_name=="STRbuff":
                    bootbuff_2_name="STR"
                elif bootboost_2_name=="VITbuff":
                    bootbuff_2_name="VIT"
                elif bootboost_2_name=="INTbuff":
                    bootbuff_2_name="INT"
                elif bootboost_2_name=="PERbuff":
                    bootbuff_2_name="PER"
                elif bootboost_2_name=="MANbuff":
                    bootbuff_2_name="MAN"
                    
                bootboost_2=bootbuff_2_name+' +'+str(data["BOOTS"][boot][0]["buff"][bootboost_2_name])
        except:
            print('',end='')

        try:
            collar=list(data['COLLAR'].keys())[0]
            if type(data["COLLAR"][collar][0]["buff"]) is dict:
                collar_buff_main=list(data["COLLAR"][collar][0]["buff"].keys())

                # ? COLLAR BUFF 1 
                collarboost_1_name=collar_buff_main[0]
                if collarboost_1_name=="AGIbuff":
                    collarbuff_1_name="AGI"
                elif collarboost_1_name=="STRbuff":
                    collarbuff_1_name="STR"
                elif collarboost_1_name=="VITbuff":
                    collarbuff_1_name="VIT"
                elif collarboost_1_name=="INTbuff":
                    collarbuff_1_name="INT"
                elif collarboost_1_name=="PERbuff":
                    collarbuff_1_name="PER"
                elif collarboost_1_name=="MANbuff":
                    collarbuff_1_name="MAN"
                    
                collarboost_1=collarbuff_1_name+' +'+str(data["COLLAR"][collar][0]["buff"][collarboost_1_name])

                # ? COLLAR BUFF 2 
                collarboost_2_name=collar_buff_main[1]
                if collarboost_2_name=="AGIbuff":
                    collarbuff_2_name="AGI"
                elif collarboost_2_name=="STRbuff":
                    collarbuff_2_name="STR"
                elif collarboost_2_name=="VITbuff":
                    collarbuff_2_name="VIT"
                elif collarboost_2_name=="INTbuff":
                    collarbuff_2_name="INT"
                elif collarboost_2_name=="PERbuff":
                    collarbuff_2_name="PER"
                elif collarboost_2_name=="MANbuff":
                    collarbuff_2_name="MAN"
                    
                collarboost_2=collarbuff_2_name+' +'+str(data["COLLAR"][collar][0]["buff"][collarboost_2_name])
        except:
            print('',end='')

        try:
            ring=list(data['RING'].keys())[0]
            if type(data["RING"][ring][0]["buff"]) is dict:
                ring_buff_main=list(data["RING"][ring][0]["buff"].keys())

                # ? RING BUFF 1 
                ringboost_1_name=ring_buff_main[0]
                if ringboost_1_name=="AGIbuff":
                    ringbuff_1_name="AGI"
                elif ringboost_1_name=="STRbuff":
                    ringbuff_1_name="STR"
                elif ringboost_1_name=="VITbuff":
                    ringbuff_1_name="VIT"
                elif ringboost_1_name=="INTbuff":
                    ringbuff_1_name="INT"
                elif ringboost_1_name=="PERbuff":
                    ringbuff_1_name="PER"
                elif ringboost_1_name=="MANbuff":
                    ringbuff_1_name="MAN"
                    
                ringboost_1=ringbuff_1_name+' +'+str(data["RING"][ring][0]["buff"][ringboost_1_name])

                # ? RING BUFF 2
                ringboost_2_name=ring_buff_main[1]
                if ringboost_2_name=="AGIbuff":
                    ringbuff_2_name="AGI"
                elif ringboost_2_name=="STRbuff":
                    ringbuff_2_name="STR"
                elif ringboost_2_name=="VITbuff":
                    ringbuff_2_name="VIT"
                elif ringboost_2_name=="INTbuff":
                    ringbuff_2_name="INT"
                elif ringboost_2_name=="PERbuff":
                    ringbuff_2_name="PER"
                elif ringboost_2_name=="MANbuff":
                    ringbuff_2_name="MAN"
                    
                ringboost_2=ringbuff_2_name+' +'+str(data["RING"][ring][0]["buff"][ringboost_2_name])
        except:
            print('',end='')

    return [[helm, chest, f_gaun, s_gaun, boot, ring, collar], [helmboost_1, helmboost_2, chestboost_1, chestboost_2, f_gaunboost_1, f_gaunboost_2, s_gaunboost_1, s_gaunboost_2, bootboost_1, bootboost_2, ringboost_1, ringboost_2, collarboost_1, collarboost_2]]

def finish(qty, equiipment_check):
    if qty == 1:
        with open('Files/Equipment.json', 'r') as first_equipment_file:
            cat=equiipment_check[0]
            first_equipment_file_data=ujson.load(first_equipment_file)
            if cat in["HELM","CHESTPLATE","FIRST GAUNTLET","SECOND GAUNTLET", "BOOTS", "RING", "COLLAR"]:
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

                        oldbuff1_value=first_equipment_file_data[cat][item_old_name][0]["buff"][old_item_boost_1_name]

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

                        oldbuff2_value=first_equipment_file_data[cat][item_old_name][0]["buff"][old_item_boost_2_name]
                    except:
                        print("",end='')

                    try:
                        old_item_debuff_main=list(first_equipment_file_data[cat][item_old_name][0]["debuff"].keys())
                        # ? HELM BUFF 1 
                        old_item_deboost_1_name=old_item_debuff_main[0]
                        if old_item_deboost_1_name=="AGIdebuff" or old_item_deboost_1_name=="AGIbuff":
                            olddebuff_1_name="AGI"
                        elif old_item_deboost_1_name=="STRdebuff" or old_item_deboost_1_name=="STRbuff":
                            olddebuff_1_name="STR"
                        elif old_item_deboost_1_name=="VITdebuff" or old_item_deboost_1_name=="VITbuff":
                            olddebuff_1_name="VIT"
                        elif old_item_deboost_1_name=="INTdebuff" or old_item_deboost_1_name=="INTbuff":
                            olddebuff_1_name="INT"
                        elif old_item_deboost_1_name=="PERdebuff" or old_item_deboost_1_name=="PERbuff":
                            olddebuff_1_name="PER"
                        elif old_item_deboost_1_name=="MANdebuff" or old_item_deboost_1_name=="MANbuff":
                            olddebuff_1_name="MAN"

                        olddebuff1_value=first_equipment_file_data[cat][item_old_name][0]["debuff"][old_item_deboost_1_name]

                        # ? HELM BUFF 2
                        old_item_deboost_2_name=old_item_debuff_main[1]
                        if old_item_deboost_2_name=="AGIdebuff" or old_item_deboost_2_name=="AGIbuff":
                            olddebuff_2_name="AGI"
                        elif old_item_deboost_2_name=="STRdebuff" or old_item_deboost_2_name=="STRbuff":
                            olddebuff_2_name="STR"
                        elif old_item_deboost_2_name=="VITdebuff" or old_item_deboost_2_name=="VITbuff":
                            olddebuff_2_name="VIT"
                        elif old_item_deboost_2_name=="INTdebuff" or old_item_deboost_2_name=="INTbuff":
                            olddebuff_2_name="INT"
                        elif old_item_deboost_2_name=="PERdebuff" or old_item_deboost_2_name=="PERbuff":
                            olddebuff_2_name="PER"
                        elif old_item_deboost_2_name=="MANdebuff" or old_item_deboost_2_name=="MANbuff":
                            olddebuff_2_name="MAN"

                        olddebuff2_value=first_equipment_file_data[cat][item_old_name][0]["debuff"][old_item_deboost_2_name]
                    except:
                        print("",end='')

                    with open("Files/status.json", 'r') as status_file_eq:
                        status_file_eq_data=ujson.load(status_file_eq)
                        try:
                            status_file_eq_data["equipment"][0][oldbuff_1_name]=-(oldbuff1_value/2)
                            status_file_eq_data["equipment"][0][oldbuff_2_name]=-(oldbuff2_value/2)
                        except:
                            print()

                        try:
                            status_file_eq_data["equipment"][0][olddebuff_1_name]=+olddebuff1_value
                            status_file_eq_data["equipment"][0][olddebuff_2_name]=+olddebuff2_value
                        except:
                            print()

                    del first_equipment_file_data[cat]
                    first_equipment_file_data[cat]={}

                    with open('Files/Equipment.json', 'w') as second_write_equipment_file:
                        ujson.dump(first_equipment_file_data, second_write_equipment_file, indent=6)

                    with open('Files/status.json', 'w') as second_write_status_file:
                        ujson.dump(status_file_eq_data, second_write_status_file, indent=4)

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



