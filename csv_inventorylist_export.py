import json
import csv

with open("Files/Skills/Skill_List.json", 'r') as fson:
    json_data = json.load(fson)

csv_file_path="skill_list.csv"

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["id", "name", "lvl", "type", "desc", "base", "rewards", "condition 1", "condition 2"])
    
    # Initialize an ID counter for primary key
    id_counter = 1

    # Flatten the JSON structure based on the schema
    for name, details in json_data.items():
        skill_info = details[0]
        rewards_json = skill_info["rewards"]
        conditions = details[1].get("Condition", [])
        
        # Write the row
        writer.writerow([
            id_counter,                       # id
            name,                             # name
            skill_info["lvl"],                # lvl
            skill_info["type"],               # type
            skill_info["desc"],               # desc
            skill_info["base"],               # base
            str(rewards_json),                # rewards (JSON stringified)
            conditions[0] if conditions else "NULL",  # condition 1
            conditions[1] if len(conditions) > 1 else "NULL"  # condition 2
        ])
        id_counter += 1
