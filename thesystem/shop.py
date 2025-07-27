import random
import ujson
import subprocess
import thesystem.system

def quests_add(rank, vals, read_status_file_data, window):
    ab_points = ["STR", "AGI", "VIT", "INT", "PER", "MAN"]
    random_ab = random.choice(ab_points)

    try:
        with open("Files/Player Data/Active_Quests.json", 'r') as f:
            active_quests = ujson.load(f)
    except Exception:
        active_quests = {}
    active_count = len(active_quests)
    active_names = list(active_quests.keys())

    if active_count < 13:
        # --- Quest Name Selection ---
        with open("Files/Data/Quest_Names.json", 'r') as f:
            quest_names = ujson.load(f)
        if random_ab in ["STR", "AGI", "VIT"]:
            names_list = quest_names.get("STR", [])
            rew3 = "STRav"
        else:
            names_list = quest_names.get("INT", [])
            rew3 = "INTav"
        available_names = [name for name in names_list if name not in active_names]
        quest_name = random.choice(available_names) if available_names else random.choice(names_list)

        # --- Quest Description ---
        with open("Files/Data/Quest_Desc.json", 'r') as f:
            quest_desc = ujson.load(f)
        if rank in ["E", "D"]:
            desc_list = quest_desc.get("Easy", [])
        elif rank in ["C", "B"]:
            desc_list = quest_desc.get("Intermediate", [])
        elif rank in ["A", "S"]:
            desc_list = quest_desc.get("Hard", [])
        findesc = random.choice(desc_list) if desc_list else ""

        # --- Rewards: Coin Bag and Inventory Reward ---
        amt = {"S": 250000, "A": 130000, "B": 80000, "C": 5000, "D": 500, "E": 300}
        coinval = amt.get(rank, 0)
        rew1 = f"Coin Bag {coinval}"

        with open("Files/Data/Inventory_List.json", 'r') as f:
            reward_names = ujson.load(f)

        # Define rarity weights
        rarity_weights = {
            "Common": 60,
            "Rare": 25,
            "Epic": 10,
            "Legendary": 5
        }

        # Weighted selection for quest-only rewards
        weighted_rewards = []
        for name, data in reward_names.items():
            item = data[0]
            if item.get("rank") == rank and item.get("quest") == True:
                rarity = item.get("rarity", "Common")
                weight = rarity_weights.get(rarity, 1)
                weighted_rewards.append((name, weight))


        if weighted_rewards:
            names, weights = zip(*weighted_rewards)
            rew2 = random.choices(names, weights=weights, k=1)[0]
        else:
            # fallback: pick any matching rank reward
            final_rewards_list = [
                k for k, v in reward_names.items()
                if v[0].get("rank") == rank and v[0].get("quest") == True
            ]
            rew2 = random.choice(final_rewards_list) if final_rewards_list else ""

        # --- Quest Info ---
        file_name = f"Files/Workout/{random_ab}_based.json"
        with open(file_name, 'r') as f:
            quest_main_names = ujson.load(f)
        quest_main_keys = list(quest_main_names.keys())
        final_quest_main_name = random.choice(quest_main_keys) if quest_main_keys else ""
        details = quest_main_names.get(final_quest_main_name, [{}])[0]

        # --- Build Rewards Dictionary ---
        rew_dict = {rew1: 1}
        if rew2:
            rew_dict[rew2] = 1
        if rank == "S":
            rew_dict["LVLADD"] = 1
            rew_dict[rew3] = 4
        elif rank == "A":
            rew_dict[rew3] = 3
        elif rank == "B":
            rew_dict[rew3] = 2

        # --- Update Quest Details ---
        if details.get("type") == 'Learn':
            details["obj_desc"] = details.get("desc")
        details["desc"] = findesc
        details["rank"] = rank
        details["ID"] = random.randrange(1, 999999)

        adjustments = {
            "D": {"amt": {50: 10, 15: 5, 2: 1, 30: 15, 1: 1},
                  "time": {60: 60, 45: 15, 1: 1}},
            "C": {"amt": {50: 20, 15: 15, 2: 1, 30: 30, 1: 2},
                  "time": {45: 30, 60: 120, 1: 2}},
            "B": {"amt": {50: 50, 15: 35, 2: 3, 30: 60, 1: 3},
                  "time": {45: 45, 60: 240, 1: 4}},
            "A": {"amt": {50: 100, 15: 60, 2: 5, 30: 70, 1: 4},
                  "time": {45: 65, 60: 360, 1: 6}},
            "S": {"amt": {50: 150, 15: 85, 2: 8, 30: 90, 1: 5},
                  "time": {45: 75, 60: 540, 1: 9}},
        }

        if rank in adjustments:
            adj = adjustments[rank]
            if "amt" in details:
                orig_amt = details["amt"]
                if orig_amt in adj["amt"]:
                    details["amt"] += adj["amt"][orig_amt]
            elif "time" in details:
                orig_time = details["time"]
                if orig_time in adj["time"]:
                    details["time"] += adj["time"][orig_time]

        details["Rewards"] = rew_dict
        details["skill"] = final_quest_main_name

        # --- Save the New Quest ---
        active_quests[quest_name] = [details]
        with open("Files/Player Data/Active_Quests.json", 'w') as f:
            ujson.dump(active_quests, f, indent=6)

        with open("Files/Player Data/Skill.json", 'r') as f:
            skill_data = ujson.load(f)

        addition = 0
        if thesystem.system.skill_use("Negotiation", (0), False) and ("Negotiation" in skill_data):
            lvl = skill_data["Negotiation"][0]["lvl"]
            if isinstance(lvl, str):
                lvl = 10

            percentile = 0.015 * lvl
            addition = abs(vals) * percentile

        # --- Update Status ---
        read_status_file_data["status"][0]['coins'] -= int(vals-addition)
        with open("Files/Player Data/Status.json", 'w') as f:
            ujson.dump(read_status_file_data, f, indent=4)

    else:
        thesystem.system.message_open("Quest Slot Filled")

    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data = ujson.load(themefile)
        theme = theme_data["Theme"]

    with open("Files/Player Data/Tabs.json", 'r') as tab_son:
        tab_son_data = ujson.load(tab_son)

    if tab_son_data["Shop"] == 'Close':
        with open("Files/Player Data/Tabs.json", 'w') as fin_tab_son:
            tab_son_data["Shop"] = 'Open'
            ujson.dump(tab_son_data, fin_tab_son, indent=4)

        inv_name = f"{theme} Version/Shop/gui.py"
        subprocess.Popen(['python', inv_name])

    window.quit()