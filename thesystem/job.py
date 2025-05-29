import ujson


def speedster():
    with open('Files/Player Data/Skill.json', 'r') as skill_file:
        skill_file_data=ujson.load(skill_file)
        skill_file_data["Force of Speed"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"A certain Force of Speed has bonded with you. Your Agility will improve faster from this point",
            "pl_point":0,
            
            "base":"STR",
            "rewards":{
                "STRav":10,
                "Gauntlet of Lightning":1
            }
        }]

        skill_file_data["Lightweight"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"Your body will get lighter and nimble as you get faster",
            "pl_point":0,
            
            "base":"STR",
            "rewards":{
                "STRav":10,
                "Golden Boots of Agility":1
            }
        }]

    with open('Files/Player Data/Skill.json', 'w') as fin_skill_file:
        ujson.dump(skill_file_data, fin_skill_file, indent=6)

    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
    data["status"][1]['job']="Speedster"

    with open("Files/Player Data/Status.json", 'w') as fson:
        ujson.dump(data, fson, indent=6)

def beserker():
    with open('Files/Player Data/Skill.json', 'r') as skill_file:
        skill_file_data=ujson.load(skill_file)
        skill_file_data["Strength Augmentation"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"You have a Greater Strength Augumentation than the Average Man",
            "pl_point":0,
            
            "base":"STR",
            "rewards":{
                "STRav":10,
                "Gauntlet of the Eternal Guardian":1
            }
        }]

        skill_file_data["Exponential Strength"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"All Strength Gains are faster than they were before. Results show faster as well",
            "pl_point":0,
            
            "base":"STR",
            "rewards":{
                "STRav":10,
                "Amulet of Protection":1
            }
        }]

    with open('Files/Player Data/Skill.json', 'w') as fin_skill_file:
        ujson.dump(skill_file_data, fin_skill_file, indent=6)

    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
    data["status"][1]['job']="Beserker"

    with open("Files/Player Data/Status.json", 'w') as fson:
        ujson.dump(data, fson, indent=6)

def tank():
    with open('Files/Player Data/Skill.json', 'r') as skill_file:
        skill_file_data=ujson.load(skill_file)
        skill_file_data["Quick Heal"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"Your Body will heal itself quicker than normal and your pain reduces",
            "pl_point":0,
            
            "base":"STR",
            "rewards":{
                "STRav":10,
                "Gauntlet of Lightning":1
            }
        }]

        skill_file_data["Detox"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"Your body slowly but surely removes Toxins from the body the more VIT is increased",
            "pl_point":0,
            
            "base":"STR",
            "rewards":{
                "STRav":10,
                "Golden Boots of Agility":1
            }
        }]

    with open('Files/Player Data/Skill.json', 'w') as fin_skill_file:
        ujson.dump(skill_file_data, fin_skill_file, indent=6)

    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
    data["status"][1]['job']="Tank"

    with open("Files/Player Data/Status.json", 'w') as fson:
        ujson.dump(data, fson, indent=6)

def shadow_monarch():
    with open('Files/Player Data/Skill.json', 'r') as skill_file:
        skill_file_data=ujson.load(skill_file)
        skill_file_data["Shadow Extraction"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"Extracts Mana from a fallen body and transforms them into a shadow",
            "pl_point":0,
            
            "base":"INT",
            "rewards":{
                "INTav":10,
                "Red Knights Helmet":1
            }
        }]

        skill_file_data["Shadow Storage"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"Allows one to store the Extracted Shadows for later uses",
            "pl_point":0,
            
            "base":"STR",
            "rewards":{
                "STRav":10,
                "Gauntlet of Lightning":1
            }
        }]

    with open('Files/Player Data/Skill.json', 'w') as fin_skill_file:
        ujson.dump(skill_file_data, fin_skill_file, indent=6)

    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
    data["status"][1]['job']="Shadow Monarch"

    with open("Files/Player Data/Status.json", 'w') as fson:
        ujson.dump(data, fson, indent=6)

def commander():
    with open('Files/Player Data/Skill.json', 'r') as skill_file:
        skill_file_data=ujson.load(skill_file)
        skill_file_data["Charismatic Presence"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"Your Charisma and Confidence draws people towards you",
            "pl_point":0,
            
            "base":"INT",
            "rewards":{
                "INTav":10,
                "High-Minister's Amulet":1
            }
        }]

        skill_file_data["Rise"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"A unique ability to be a natural leader and have people rise to your aid",
            "pl_point":0,
            
            "base":"INT",
            "rewards":{
                "INTav":10,
                "Ring of Arcane Mastery":1
            }
        }]

    with open('Files/Player Data/Skill.json', 'w') as fin_skill_file:
        ujson.dump(skill_file_data, fin_skill_file, indent=6)

    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
    data["status"][1]['job']="Commander"

    with open("Files/Player Data/Status.json", 'w') as fson:
        ujson.dump(data, fson, indent=6)

def observer():
    with open('Files/Player Data/Skill.json', 'r') as skill_file:
        skill_file_data=ujson.load(skill_file)
        skill_file_data["Heightened Perception"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"Your keen eyes and senses allow you to capture everything that happens around you",
            "pl_point":0,
            
            "base":"INT",
            "rewards":{
                "INTav":10,
                "Chameleon Cloak":1
            }
        }]

        skill_file_data["Puzzle Snap"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"Even with limited information, You can puzzle together a full picture with limited information",
            "pl_point":0,
            
            "base":"INT",
            "rewards":{
                "INTav":10,
                "Ring of Arcane Mastery":1
            }
        }]

    with open('Files/Player Data/Skill.json', 'w') as fin_skill_file:
        ujson.dump(skill_file_data, fin_skill_file, indent=6)

    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
    data["status"][1]['job']="Observer"

    with open("Files/Player Data/Status.json", 'w') as fson:
        ujson.dump(data, fson, indent=6)

def artificer():
    with open('Files/Player Data/Skill.json', 'r') as skill_file:
        skill_file_data=ujson.load(skill_file)
        skill_file_data["Quick Thought"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"Your Creativity will lay dormant for a period of time and explode into a bunch of creative thoughts and Ideas",
            "pl_point":0,
            
            "base":"INT",
            "rewards":{
                "INTav":10,
                "Archmage's Robes":1
            }
        }]

        skill_file_data["Learner"]=[{
            "lvl":1,
            "type":"Job",
            "desc":"You have an increased ability to retain and remember Useful information",
            "pl_point":0,
            
            "base":"INT",
            "rewards":{
                "INTav":10,
                "Sovereign's Veil":1
            }
        }]

    with open('Files/Player Data/Skill.json', 'w') as fin_skill_file:
        ujson.dump(skill_file_data, fin_skill_file, indent=6)

    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
    data["status"][1]['job']="Artificer"

    with open("Files/Player Data/Status.json", 'w') as fson:
        ujson.dump(data, fson, indent=6)

