import ujson
import subprocess
from datetime import datetime
import csv

def dailys_init():
    with open("Files/Player Data/Daily_Quest.json", 'r') as daily_quest_file:
        daily_quest_data=ujson.load(daily_quest_file)
        # ? =======================================================
        # ? Players
        pl_push=daily_quest_data["Player"]["Push"]
        pl_sit=daily_quest_data["Player"]["Sit"]
        pl_sqat=daily_quest_data["Player"]["Squat"]
        pl_run=daily_quest_data["Player"]["Run"]

        pl_int=daily_quest_data["Player"]["Int_type"]
        pl_slp=daily_quest_data["Player"]["Sleep"]
        # ? =======================================================
        # ? Final
        fl_push=daily_quest_data["Final"]["Push"]
        fl_sit=daily_quest_data["Final"]["Sit"]
        fl_sqat=daily_quest_data["Final"]["Squat"]
        fl_run=daily_quest_data["Final"]["Run"]

        fl_int=daily_quest_data["Final"]["Int_type"]
        fl_slp=daily_quest_data["Final"]["Sleep"]
        # ? =======================================================
        # ? Name
        push_name=daily_quest_data["Change"][0]["1"][0]
        sit_name=daily_quest_data["Change"][1]["2"][0]
        squat_name=daily_quest_data["Change"][2]["3"][0]
        run_name=daily_quest_data["Change"][3]["4"][0]

        int_name=daily_quest_data["Change"][4]["5"][0]
        slp_name=daily_quest_data["Change"][5]["6"][0]
        # ? =======================================================
    return [[daily_quest_data], [pl_push, pl_sit, pl_sqat, pl_run, pl_int, pl_slp], [fl_push, fl_sit, fl_sqat, fl_run, fl_int, fl_slp], [push_name, sit_name, squat_name, run_name, int_name, slp_name]]

def get_rank():
    with open("Files/Player Data/Status.json", 'r') as rank_check_file:
        rank_check_data=ujson.load(rank_check_file)
        lvl=rank_check_data["status"][0]['level']

        if lvl>=1 and lvl<=10:
            rank="E"
        elif lvl>=11 and lvl<=20:
            rank="D"
        elif lvl>=21 and lvl<=30:
            rank="C"
        elif lvl>=31 and lvl<=45:
            rank="B"
        elif lvl>=46 and lvl<=65:
            rank="A"
        elif lvl>=66 and lvl<=80:
            rank="S"
        elif lvl>=81 and lvl<=90:
            rank="SS"
        elif lvl>=91 and lvl<=100:
            rank="SSS"
        elif lvl>=101:
            rank="National"
    return rank

def get_check_rew():
    reward=False
    with open("Files\Temp Files\Daily Rewards.csv", 'r') as csv_open:
        fr=csv.reader(csv_open)
        for k in fr:
            type_re=k[0]
        if type_re=='Secret' or type_re=='Reward' or type_re=='Great Reward':
            reward=True
        return [reward, type_re]

def get_streak():
    with open("Files/Player Data/Daily_Quest.json", 'r') as streak_file:
        streak_file_data = ujson.load(streak_file)
        streak=streak_file_data["Streak"]["Value"]
    return streak

def get_titles():
    streak=get_streak()
    with open("Files/Data/Title_list.json", "r") as list_of_titles:
        list_of_titles_data=ujson.load(list_of_titles)
        list_of_titles_keys=list(list_of_titles_data.keys())

        if streak>=0 and streak<=3:
            title=list_of_titles_keys[0]
        elif streak>=4 and streak<=8:
            title=list_of_titles_keys[1]
        elif streak>=9 and streak<=14:
            title=list_of_titles_keys[2]
        elif streak>=15 and streak<=20:
            title=list_of_titles_keys[3]
        elif streak>=21 and streak<=30:
            title=list_of_titles_keys[4]
        elif streak>=31 and streak<=40:
            title=list_of_titles_keys[5]
        elif streak>=41 and streak<=50:
            title=list_of_titles_keys[6]
        elif streak>=51 and streak<=70:
            title=list_of_titles_keys[7]
        elif streak>=71 and streak<=90:
            title=list_of_titles_keys[8]
        elif streak>=91:
            title=list_of_titles_keys[9]
    return title, list_of_titles_data

def daily_preview(window):
    with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
            rew_fw=csv.writer(rew_csv_open)
            rew_fw.writerow(["Preview"])
    with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
        theme_data=ujson.load(themefile)
        theme=theme_data["Theme"]
    subprocess.Popen(['python', f'{theme} Version/Daily Quest Rewards/gui.py'])

def check_daily_comp(today_date_str, window):
    with open("Files/Player Data/Daily_Quest.json", 'r') as daily_quest_file:
        daily_quest_data = ujson.load(daily_quest_file)
        
        # Player's daily progress
        pl_push = daily_quest_data["Player"]["Push"]
        pl_sit = daily_quest_data["Player"]["Sit"]
        pl_sqat = daily_quest_data["Player"]["Squat"]
        pl_run = daily_quest_data["Player"]["Run"]
        pl_int = daily_quest_data["Player"]["Int_type"]
        pl_slp = daily_quest_data["Player"]["Sleep"]

        # Final quest goals
        fl_push = daily_quest_data["Final"]["Push"]
        fl_sit = daily_quest_data["Final"]["Sit"]
        fl_sqat = daily_quest_data["Final"]["Squat"]
        fl_run = daily_quest_data["Final"]["Run"]
        fl_int = daily_quest_data["Final"]["Int_type"]
        fl_slp = daily_quest_data["Final"]["Sleep"]

        main_max_value = daily_quest_data["Steps"][2]
        side_max_value = daily_quest_data["Steps"][3]
        float_step = daily_quest_data["Steps"][0]
        int_step = daily_quest_data["Steps"][1]

    with open('Files/Player Data/Secret_Quest_Check.json', 'r') as secrer_quest:
        secrer_quest_data = ujson.load(secrer_quest)
        day_num = secrer_quest_data["Day"]
        tdy_week_num = datetime.today().weekday()

    # First check if today is the correct day to check completion
    if day_num == tdy_week_num:
        if (pl_push / 2) >= fl_push and (pl_run / 2) >= fl_run and (pl_sqat / 2) >= fl_sqat and (pl_sit / 2) >= fl_sit and (pl_int / 2) >= fl_int:
            if fl_push != main_max_value and fl_sit != main_max_value and fl_sqat != main_max_value:
                # Update final quest data with rewards
                daily_quest_data["Final"]["Push"] += int_step
                daily_quest_data["Final"]["Sit"] += int_step
                daily_quest_data["Final"]["Squat"] += int_step
                daily_quest_data["Final"]["Run"] += float_step
                daily_quest_data["Streak"]["Value"] += 1

                # Reset player data
                daily_quest_data["Player"]["Push"] = 0
                daily_quest_data["Player"]["Sit"] = 0
                daily_quest_data["Player"]["Squat"] = 0
                daily_quest_data["Player"]["Run"] = 0
                daily_quest_data["Player"]["Int_type"] = 0
                daily_quest_data["Player"]["Sleep"] = 0

                # Increment intellect if not already at max
                if round(fl_int, 1) != side_max_value:
                    daily_quest_data["Final"]["Int_type"] += float_step

                daily_quest_data["Streak"]["Value"]+=1
                daily_quest_data["Streak"]["Greater_value"]+=1

                # Save the updated quest data
                with open("Files/Player Data/Daily_Quest.json", 'w') as final_daily_quest_file:
                    ujson.dump(daily_quest_data, final_daily_quest_file, indent=4)

                # Record the completion time check
                with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as fin_daily_date_check_file:
                    fw1 = csv.writer(fin_daily_date_check_file)
                    fw1.writerow([today_date_str, "False", "Complete"])

                # Log reward info
                with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                    rew_fw = csv.writer(rew_csv_open)
                    rew_fw.writerow(["Secret"])

                # Execute the reward GUI based on the theme
                with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
                    theme_data = ujson.load(themefile)
                    theme = theme_data["Theme"]
                subprocess.Popen(['python', f'{theme} Version/Daily Quest Rewards/gui.py'])

                # Close the daily quest tab
                with open("Files/Player Data/Tabs.json", 'r') as tab_son:
                    tab_son_data = ujson.load(tab_son)

                with open("Files/Player Data/Tabs.json", 'w') as fin_tab_son:
                    tab_son_data["Daily"] = 'Close'
                    ujson.dump(tab_son_data, fin_tab_son, indent=4)

                window.quit()

        # Handle the condition where day_num != tdy_week_num
        if (pl_push) >= fl_push and (pl_run) >= fl_run and (pl_sqat) >= fl_sqat and (pl_sit) >= fl_sit and (pl_int) >= fl_int and (pl_slp) >= fl_slp:
            if fl_push != main_max_value and fl_sit != main_max_value and fl_sqat != main_max_value:
                # Update final quest data with rewards
                daily_quest_data["Final"]["Push"] += int_step
                daily_quest_data["Final"]["Sit"] += int_step
                daily_quest_data["Final"]["Squat"] += int_step
                daily_quest_data["Final"]["Run"] += float_step
                daily_quest_data["Streak"]["Value"] += 1

                # Reset player data
                daily_quest_data["Player"]["Push"] = 0
                daily_quest_data["Player"]["Sit"] = 0
                daily_quest_data["Player"]["Squat"] = 0
                daily_quest_data["Player"]["Run"] = 0
                daily_quest_data["Player"]["Int_type"] = 0
                daily_quest_data["Player"]["Sleep"] = 0

                # Increment intellect if not already at max
                if round(fl_int, 1) != side_max_value:
                    daily_quest_data["Final"]["Int_type"] += float_step

                # Log reward info
                if (pl_push) >= fl_push*3 and (pl_run) >= fl_run*3 and (pl_sqat) >= fl_sqat*3 and (pl_sit) >= fl_sit*3 and (pl_int) >= fl_int*3:
                    with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                        rew_fw = csv.writer(rew_csv_open)
                        rew_fw.writerow(["Great Reward"])
                        daily_quest_data["Streak"]["Greater_value"] += 1
                else:
                    with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                        rew_fw = csv.writer(rew_csv_open)
                        rew_fw.writerow(["Reward"])
                        daily_quest_data["Streak"]["Greater_value"]=0
                        daily_quest_data["Streak"]["Value"] += 1

                # Save the updated quest data
                with open("Files/Player Data/Daily_Quest.json", 'w') as final_daily_quest_file:
                    ujson.dump(daily_quest_data, final_daily_quest_file, indent=4)

                # Record the completion time check
                with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as fin_daily_date_check_file:
                    fw1 = csv.writer(fin_daily_date_check_file)
                    fw1.writerow([today_date_str, "True", "Complete"])

                # Execute the reward GUI based on the theme
                with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
                    theme_data = ujson.load(themefile)
                    theme = theme_data["Theme"]
                subprocess.Popen(['python', f'{theme} Version/Daily Quest Rewards/gui.py'])

                # Close the daily quest tab
                with open("Files/Player Data/Tabs.json", 'r') as tab_son:
                    tab_son_data = ujson.load(tab_son)

                with open("Files/Player Data/Tabs.json", 'w') as fin_tab_son:
                    tab_son_data["Daily"] = 'Close'
                    ujson.dump(tab_son_data, fin_tab_son, indent=4)

                window.quit()

    else:
        # Handle the condition where day_num != tdy_week_num
        if (pl_push) >= fl_push and (pl_run) >= fl_run and (pl_sqat) >= fl_sqat and (pl_sit) >= fl_sit and (pl_int) >= fl_int and (pl_slp) >= fl_slp:
            if fl_push != main_max_value and fl_sit != main_max_value and fl_sqat != main_max_value:
                # Update final quest data with rewards
                daily_quest_data["Final"]["Push"] += int_step
                daily_quest_data["Final"]["Sit"] += int_step
                daily_quest_data["Final"]["Squat"] += int_step
                daily_quest_data["Final"]["Run"] += float_step
                daily_quest_data["Streak"]["Value"] += 1

                # Reset player data
                daily_quest_data["Player"]["Push"] = 0
                daily_quest_data["Player"]["Sit"] = 0
                daily_quest_data["Player"]["Squat"] = 0
                daily_quest_data["Player"]["Run"] = 0
                daily_quest_data["Player"]["Int_type"] = 0
                daily_quest_data["Player"]["Sleep"] = 0

                # Increment intellect if not already at max
                if round(fl_int, 1) != side_max_value:
                    daily_quest_data["Final"]["Int_type"] += float_step

                # Log reward info
                if (pl_push) >= fl_push*3 and (pl_run) >= fl_run*3 and (pl_sqat) >= fl_sqat*3 and (pl_sit) >= fl_sit*3 and (pl_int) >= fl_int*3:
                    with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                        rew_fw = csv.writer(rew_csv_open)
                        rew_fw.writerow(["Great Reward"])
                        daily_quest_data["Streak"]["Greater_value"] += 1
                else:
                    with open("Files/Temp Files/Daily Rewards.csv", 'w', newline='') as rew_csv_open:
                        rew_fw = csv.writer(rew_csv_open)
                        rew_fw.writerow(["Reward"])
                        daily_quest_data["Streak"]["Greater_value"]=0
                        daily_quest_data["Streak"]["Value"] += 1

                # Save the updated quest data
                with open("Files/Player Data/Daily_Quest.json", 'w') as final_daily_quest_file:
                    ujson.dump(daily_quest_data, final_daily_quest_file, indent=4)

                # Record the completion time check
                with open("Files/Checks/Daily_time_check.csv", 'w', newline='') as fin_daily_date_check_file:
                    fw1 = csv.writer(fin_daily_date_check_file)
                    fw1.writerow([today_date_str, "True", "Complete"])

                # Execute the reward GUI based on the theme
                with open('Files/Player Data/Theme_Check.json', 'r') as themefile:
                    theme_data = ujson.load(themefile)
                    theme = theme_data["Theme"]
                subprocess.Popen(['python', f'{theme} Version/Daily Quest Rewards/gui.py'])

                # Close the daily quest tab
                with open("Files/Player Data/Tabs.json", 'r') as tab_son:
                    tab_son_data = ujson.load(tab_son)

                with open("Files/Player Data/Tabs.json", 'w') as fin_tab_son:
                    tab_son_data["Daily"] = 'Close'
                    ujson.dump(tab_son_data, fin_tab_son, indent=4)

                window.quit()

