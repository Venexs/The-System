import ujson
import subprocess
import csv
import thesystem.system
import ctypes
import sys

def complete(entry_1, entry_2, window):
    hr=entry_1.get()
    mn=entry_2.get()

    true_file1_name='NONE'
    true_file2_name='NONE'

    data0={}
    with open("Files/Player Data/Penalty_Info.json", "w") as pen_info_file:
        data0["Penalty Info"]=[true_file1_name,true_file2_name]
        data0["Penalty Time"]=f"{hr}:{mn}"
        ujson.dump(data0, pen_info_file, indent=4)

    with open("Files/Player Data/First_open.csv", 'w', newline='') as first_open_check_file:
        fw=csv.writer(first_open_check_file)
        fw.writerow(["True"])

    subprocess.Popen(['python', 'gui.py'])
    ex_close(window)

def ex_close(window):
    subprocess.Popen(['python', 'Files/Mod/default/sfx_close.py'])
    thesystem.system.animate_window_close(window, window.winfo_height(), window.winfo_width(), step=30, delay=1)

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-launch the script as an administrator if it's not already running with admin privileges."""
    if not is_admin():
        # Try to relaunch the script with administrator privileges
        try:
            # ShellExecuteW will re-run the script with elevated privileges
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit()  # Exit the original process
        except Exception as e:
            print(f"Failed to run as admin: {str(e)}")
            sys.exit()




