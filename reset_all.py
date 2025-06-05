import ujson
import csv

stat_data={
    "status": [
        {
            "name": "Sung Jin-Woo",
            "hp": 100,
            "mp": 100,
            "level": 1,
            "str": 10,
            "int": 10,
            "agi": 10,
            "vit": 10,
            "per": 10,
            "man": 10,
            "XP": 10,
            "coins": 100,
            "fatigue_max": 40,
            "fatigue": 0,
            "last_level": 0
        },
        {
            "title_bool": "False",
            "title": "None",
            "job": "None"
        }
    ],
    "avail_eq": [
        {
            "str_based": 3,
            "int_based": 3
        }
    ],
    "equipment": [
        {
            "STR": 0,
            "AGI": 0,
            "VIT": 0,
            "INT": 0,
            "PER": 0,
            "MAN": 0
        }
    ],
    "cal_data": [
        {
            "age": "17",
            "gender": "M",
            "height": "162",
            "weight": "65",
            "calorie calc": 2000,
            "final calorie calc": 2100,
            "result": "MILD WEIGHT LOSS",
            "BMI": 23
        }
    ]
}

inv_data={}

equip_data={
      "HELM": {},
      "CHESTPLATE": {},
      "SECOND GAUNTLET": {},
      "BOOTS": {},
      "RING": {},
      "FIRST GAUNTLET": {},
      "COLLAR": {}
}

daily_data={
    "Player": {
        "Push": 0,
        "Sit": 0,
        "Squat": 0,
        "Run": 0.0,
        "Int_type": 0.0,
        "Sleep": 0
    },
    "Final": {
        "Push": 10,
        "Sit": 10,
        "Squat": 10,
        "Run": 1.0,
        "Int_type": 1.0,
        "Sleep": 1
    },
    "Change":[
        {"1":["Push-ups"]},
        {"2":["Sit-ups"]},
        {"3":["Squats"]},
        {"4":["Running"]},
        {"5":["Chapter Reading"]},
        {"6":["Proper Last Night Sleep"]}
    ],
    "Steps":[0.5,5,100,10],
    "Streak": {
        "Value": 0,
        "Greater_value": 0
    }
}

job_info ={
    "status": [
        {
            "job_active": "False",
            "job_check": "False",
            "job_confirm": "False",
        },
        {
            "STR": 1,
            "AGI": 1,
            "VIT": 1,
            "INT": 1,
            "PER": 1,
            "MAN": 1,
            "plSTR": 0,
            "plAGI": 0,
            "plVIT": 0,
            "plINT": 0,
            "plPER": 0,
            "plMAN": 0,
            "job_confirm": "False"
        }
    ]
}

quest_data={
      "Rebirth of the Strong": [
            {
                  "ID": 0,
                  "obj": "Get Strong",
                  "rank": "?",
                  "type": "Unknown",
                  "desc": "Quest given by The Architect",
                  "Rewards": {
                        "LVLADD": 10
                  }
            }
      ]
}

title_data={}

skill_data={}

with open("Files/Player Data/Skill.json", 'w') as skill_file:
    ujson.dump(skill_data, skill_file, indent=4)

with open("Files/Player Data/Titles.json", 'w') as title_file:
    ujson.dump(title_data, title_file, indent=4)

with open("Files/Player Data/Status.json", 'w') as status_file:
    ujson.dump(stat_data, status_file, indent=4)

with open("Files/Player Data/Inventory.json", 'w') as inv_file:
    ujson.dump(inv_data, inv_file, indent=4)

with open("Files/Player Data/Equipment.json", 'w') as equip_file:
    ujson.dump(equip_data, equip_file, indent=4)

with open("Files/Player Data/Daily_Quest.json",'w') as daily_file:
    ujson.dump(daily_data, daily_file, indent=4)

with open("Files/Player Data/Active_Quests.json", 'w') as quest_file:
    ujson.dump(quest_data, quest_file, indent=6)

with open("Files/Player Data/Job_info.json", 'w') as job_file:
    ujson.dump(job_info, job_file, indent=4)

with open("Files/Player Data/First_open.csv", 'w', newline='') as info_open:
    fw=csv.writer(info_open)
    fw.writerow(["False"])

with open("Files/Player Data/Prove_file.csv", 'w', newline='') as info_open2:
    fw1=csv.writer(info_open2)
    fw1.writerow(["True"])

print("Done")