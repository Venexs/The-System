from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import csv
import sched
import time
from datetime import datetime, timedelta, date
import subprocess
import subprocess
subprocess.Popen(['python', 'sfx.py'])
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def update_timer(end_time):
    # Calculate the remaining time
    remaining_time = end_time - datetime.now()

    # Check if the remaining time is positive
    if remaining_time.days < 0:
        canvas.itemconfig(timer, text="Time's up!")
        return

    # Format the remaining time as hours, minutes, and seconds
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Update the text on the Canvas
    timer_text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    canvas.itemconfig(timer, text=timer_text)

    # Schedule the next update after 1000 milliseconds (1 second)
    window.after(1000, update_timer, end_time)

# Calculate the end time (12:00 AM next day)
end_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

window = Tk()
window.geometry("555x957")
window.configure(bg="#FFFFFF")
window.attributes('-alpha',0.8)

# Global variables to hold player data
pl_push = 0
pl_sit = 0
pl_squat = 0
pl_run = 0

today = date.today()
today_date_str = today.strftime("%Y-%m-%d")

# Load player data from CSV
with open('Files/Daily quest Player Num.csv', 'r') as fout:
    fr = csv.reader(fout)
    for k in fr:
        pl_push = int(k[0])
        pl_sit = int(k[1])
        pl_squat = int(k[2])
        pl_run = float(k[3])

# Load quest data from CSV
check=False
full_check=False

def penalty_check():
    # Get today's date
    today = datetime.now().date()

    # Calculate yesterday's date
    yesterday = today - timedelta(days=1)
    with open('Files/Checks/Today_Quest', 'r', newline='') as fout:
        fr=csv.reader(fout)
        for k in fr:
            status=k[0]
            date=k[1]

    p_date=datetime.strptime(date, "%Y-%m-%d").date()
    if yesterday!=p_date:
        subprocess.Popen(['python', 'Daily Quest/build/gui.py'])


with open('Files/Daily quest Final Num.csv', 'r') as fout:
    fr = csv.reader(fout)
    for k in fr:
        push_ups = gl_push = int(k[0])
        sit_ups = gl_sit = int(k[1])
        squats = gl_squat = int(k[2])
        run = gl_run = float(k[3])
        date_old=k[4]

date_from_string = datetime.strptime(date_old, "%Y-%m-%d").date()
if date_from_string < today:
    check=True
    with open('Files/Daily quest Final Num.csv', 'w', newline='') as fout:
        fw = csv.writer(fout)
        rec=[10,10,10,5,today_date_str]
        fw.writerow(rec)

if check==True:
    with open('Files/Daily quest Final Num.csv', 'r') as fout:
        fr = csv.reader(fout)
        for k in fr:
            push_ups = gl_push = int(k[0])
            sit_ups = gl_sit = int(k[1])
            squats = gl_squat = int(k[2])
            run = gl_run = float(k[3])
            date_old=k[4]

elif date_from_string==today:
    if pl_push>=gl_push and pl_run>=gl_run and pl_squat>=gl_squat and pl_sit>=gl_sit:
        full_check=True

if full_check==False:
    # Function to update player data and CSV
    def push_new_rec():
        global pl_push, pl_sit, pl_squat, pl_run
        with open('Files/Daily quest Player Num.csv', 'w', newline='') as fout:
            fw = csv.writer(fout)
            rec = [pl_push, pl_sit, pl_squat, pl_run]
            fw.writerow(rec)
            checking()

    def update_push():
        global pl_push
        pl_push += 1
        push_new_rec()
        # Update text object for push-ups
        canvas.itemconfig(push_text, text=f"[{pl_push}/{push_ups}]")

    def update_sit():
        global pl_sit
        pl_sit += 1
        push_new_rec()
        # Update text object for sit-ups
        canvas.itemconfig(sit_text, text=f"[{pl_sit}/{sit_ups}]")

    def update_squat():
        global pl_squat
        pl_squat += 1
        push_new_rec()
        # Update text object for squats
        canvas.itemconfig(squat_text, text=f"[{pl_squat}/{squats}]")

    def update_run():
        global pl_run
        pl_run += 0.1
        push_new_rec()
        # Update text object for running
        canvas.itemconfig(run_text, text=f"[{pl_run:.1f}/{run}km]")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=957,
        width=555,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        277.0,
        478.0,
        image=image_image_1
    )

    canvas.create_rectangle(
        0.0,
        866.9999999999999,
        539.0,
        883.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        0.0,
        87.0,
        520.9990367889404,
        103.98248827329371,
        fill="#FFFFFF",
        outline="")

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        286.9999999999999,
        483.9999999999999,
        image=image_image_2
    )

    canvas.create_text(
        208.0,
        170.0,
        anchor="nw",
        text="QUEST INFO",
        fill="#FFFFFF",
        font=("Inter Medium", 26 * -1)
    )

    canvas.create_text(
        251.0,
        294.0,
        anchor="nw",
        text="GOAL",
        fill="#FFFFFF",
        font=("Inter Bold", 24 * -1)
    )

    timer=canvas.create_text(
        208.0,
        761.0,
        anchor="nw",
        text="00:00:00",
        fill="#FFFFFF",
        font=("Inter Bold", 40 * -1)
    )

    canvas.create_rectangle(
        226.0,
        320.0,
        345.0,
        323.0000000254082,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        226.0,
        325.0,
        345.0,
        328.0000000254082,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        200.0,
        198.0,
        371.0,
        201.00000003679816,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        136.0,
        254.0,
        anchor="nw",
        text="[Daily Quest: Strength Training has arrived]",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        74.0,
        374.0,
        anchor="nw",
        text="Push-ups",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )

    canvas.create_text(
        74.0,
        424.0,
        anchor="nw",
        text="Sit-ups",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )

    canvas.create_text(
        74.0,
        473.0,
        anchor="nw",
        text="Squats",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )

    canvas.create_text(
        74.0,
        523.0,
        anchor="nw",
        text="Running",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )

    # Quest info
    canvas.create_text(
        405.0,
        371.0,
        anchor="nw",
        text=f"[{pl_push}/{push_ups}]",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )
    push_text = canvas.find_all()[-1]  # Get the id of the last item (push-up text)

    canvas.create_text(
        405.0,
        423.0,
        anchor="nw",
        text=f"[{pl_sit}/{sit_ups}]",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )
    sit_text = canvas.find_all()[-1]  # Get the id of the last item (sit-up text)

    canvas.create_text(
        405.0,
        475.0,
        anchor="nw",
        text=f"[{pl_squat}/{squats}]",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )
    squat_text = canvas.find_all()[-1]  # Get the id of the last item (squat text)

    canvas.create_text(
        390.0,
        527.0,
        anchor="nw",
        text=f"[{pl_run:.1f}/{run}km]",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )
    run_text = canvas.find_all()[-1]  # Get the id of the last item (running text)

    canvas.create_text(
        181.0,
        609.0,
        anchor="nw",
        text="WARNING: Failure to complete\n",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )

    canvas.create_text(
        181.0,
        638.0,
        anchor="nw",
        text="the daily quest will result in",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )

    canvas.create_text(
        181.0,
        667.0,
        anchor="nw",
        text="an appropriate ",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )

    canvas.create_text(
        279.0,
        667.0,
        anchor="nw",
        text="penalty",
        fill="#FF0000",
        font=("Inter", 15 * -1)
    )

    def checking():
        if pl_push>=gl_push and pl_run>=gl_run and pl_squat>=gl_squat and pl_sit>=gl_sit:
            lvl_chk_bool=False
            with open('Files/Daily quest Final Num.csv', 'w', newline='') as fout:
                fw = csv.writer(fout)
                fw.writerow([10,10,10,5,today])
            with open('Files/Checks/Today_Quest', 'w', newline='') as fout:
                fw = csv.writer(fout)
                fw.writerow(['Complete',today])
            
            # Append today's date to the CSV file
            with open('Files/Leveler_Chk.csv', 'a', newline='') as fout_lvler:
                writer = csv.writer(fout_lvler)
                writer.writerow([today_date_str])

            with open('Files/Leveler_Chk.csv', 'r') as fout_lvler:
                fr = csv.reader(fout_lvler)
                c=0
                for mrv in fr:
                    c+=1
                if c==3:
                    print('Level up Available')
                    lvl_chk_bool=True

            if lvl_chk_bool==True:
                fout=open('Files/Leveler_Chk.csv', 'w', newline='')
                fout.truncate()
                fout.close()

            with open('Files/Leveler_Chk.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([today_date_str])

            subprocess.Popen(['python', 'STR Daily Quest Rewards/build/gui.py'])
            window.quit()

    # Buttons
    canvas.create_rectangle(
        471.0,
        369.0,
        491.0,
        389.0,
        fill="#D9D9D9",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=update_push,
        relief="flat"
    )
    button_1.place(
        x=471.0,
        y=369.0,
        width=20.0,
        height=20.0
    )

    canvas.create_rectangle(
        471.0,
        423.0,
        491.0,
        443.0,
        fill="#D9D9D9",
        outline="")

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=update_sit,
        relief="flat"
    )
    button_2.place(
        x=471.0,
        y=423.0,
        width=20.0,
        height=20.0
    )

    canvas.create_rectangle(
        471.0,
        474.0,
        491.0,
        494.0,
        fill="#D9D9D9",
        outline="")

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=update_squat,
        relief="flat"
    )
    button_3.place(
        x=471.0,
        y=474.0,
        width=20.0,
        height=20.0
    )

    canvas.create_rectangle(
        471.0,
        528.0,
        491.0,
        548.0,
        fill="#D9D9D9",
        outline="")

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=update_run,
        relief="flat"
    )
    button_4.place(
        x=471.0,
        y=528.0,
        width=20.0,
        height=20.0
    )

    end_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    update_timer(end_time)
    window.resizable(False, False)
    window.mainloop()

else:
    subprocess.Popen(['python', 'Completed Quest/build/gui.py'])
    window.quit()

# Create a scheduler
scheduler = sched.scheduler(time.time, time.sleep)

# Get the current time
now = datetime.now()

# Calculate the time until midnight
midnight = datetime(now.year, now.month, now.day) + timedelta(days=1)
time_until_midnight = (midnight - now).total_seconds()

# Schedule the task to run at midnight
scheduler.enter(time_until_midnight, 1, penalty_check)

# Run the scheduler
scheduler.run()
