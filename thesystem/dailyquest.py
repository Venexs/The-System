import json
import csv

def dailys_init():
    with open("Files/Data/Daily_Quest.json", 'r') as daily_quest_file:
        daily_quest_data=json.load(daily_quest_file)
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
    return [[daily_quest_data], [pl_push, pl_sit, pl_sqat, pl_run, pl_int, pl_slp], [fl_push, fl_sit, fl_sqat, fl_run, fl_int, fl_slp]]

def get_rank():
    with open("Files/status.json", 'r') as rank_check_file:
        rank_check_data=json.load(rank_check_file)
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
    with open("Files/Data/Daily_Quest.json", 'r') as streak_file:
        streak_file_data = json.load(streak_file)
        streak=streak_file_data["Streak"]["Value"]
    return streak

def get_titles():
    streak=get_streak()
    with open("Files/Titles/Title_list.json", "r") as list_of_titles:
        list_of_titles_data=json.load(list_of_titles)
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
