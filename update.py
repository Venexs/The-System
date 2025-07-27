import requests
import pandas as pd
from packaging import version
import zipfile
import shutil
import os
from io import BytesIO
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk

# --- CONFIGURATION ---

root = tk.Tk()
root.title("System Updater")
root.geometry("500x200")

canvas = tk.Canvas(root)
canvas.place(relwidth=1, relheight=1)

status_label = tk.Label(canvas, text="Starting update...", anchor="center", font=("Segoe UI", 11))
status_label.place(relx=0.5, rely=0.2, anchor="center")

progress = ttk.Progressbar(canvas, orient="horizontal", mode="determinate", length=300)
progress.place(relx=0.5, rely=0.5, anchor="center")
progress["maximum"] = 100
progress["value"] = 0

close_btn = tk.Button(canvas, text="Close", command=root.destroy)
close_btn.place(relx=0.5, rely=0.75, anchor="center")
close_btn.lower()  # Hide until done

def log(msg):
    status_label.config(text=msg)
    root.update_idletasks()
    print(msg)

def finish_update():
    progress["value"] = 100
    close_btn.lift()

# --- CONFIGURATION ---

github_csv_url = "https://raw.githubusercontent.com/Venexs/The-System/refs/heads/Update_RAW/version.csv"
local_csv_path = "version.csv"
repo_zip_url = "https://github.com/Venexs/The-System/archive/refs/heads/Update_RAW.zip"
target_directory = "."

def github_blob_to_raw(url):
    return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

def create_backup(source_dir, backup_dir="Update Backup"):
    # Remove existing zip backups
    if os.path.exists(backup_dir):
        for file in os.listdir(backup_dir):
            if file.endswith(".zip"):
                try:
                    os.remove(os.path.join(backup_dir, file))
                    log(f"Deleted old backup: {file}")
                except Exception as e:
                    log(f"Failed to delete {file}: {e}")

    # Create backup filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}.zip")

    log(f"Creating backup at: {backup_path}")

    def zipdir(path, ziph):
        for root_dir, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'Update Backup']]
            for file in files:
                full_path = os.path.join(root_dir, file)
                rel_path = os.path.relpath(full_path, path)
                ziph.write(full_path, rel_path)

    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(source_dir, zipf)

    log("Backup complete.")

def get_remote_version(raw_csv_url):
    try:
        df = pd.read_csv(raw_csv_url, header=None)
        if df.empty:
            raise ValueError("Remote CSV is empty.")
        return str(df.iloc[0, 0]).strip()
    except Exception as e:
        log(f"Error reading remote CSV: {e}")
        return None

def get_local_version(local_path):
    try:
        df = pd.read_csv(local_path, header=None)
        if df.empty:
            raise ValueError("Local CSV is empty.")
        return str(df.iloc[0, 0]).strip()
    except Exception as e:
        log(f"Error reading local CSV: {e}")
        return None

def is_file_locked(filepath):
    try:
        with open(filepath, 'a'):
            return False
    except IOError:
        return True

def safe_move(src, dst):
    for _ in range(3):
        if not is_file_locked(src):
            try:
                shutil.move(src, dst)
                return True
            except Exception as e:
                log(f"Error moving {src} to {dst}: {e}")
        log(f"Retrying move for: {src}")
        time.sleep(1)
    log(f"Failed to move: {src}")
    return False

def force_remove(path):
    if os.path.isdir(path):
        for _ in range(3):
            try:
                shutil.rmtree(path, ignore_errors=False)
                return
            except PermissionError:
                log(f"Retrying delete of folder: {path}")
                time.sleep(1)
    elif os.path.exists(path):
        for _ in range(3):
            try:
                os.remove(path)
                return
            except PermissionError:
                log(f"Retrying delete of file: {path}")
                time.sleep(1)

def download_zip_with_progress(url, output_path):
    log("Starting download...")
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    downloaded = 0
    chunk_size = 8192  # 8KB

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = (downloaded / total) * 100 if total else 0
                progress["value"] = percent
                log(f"Downloading... {percent:.2f}%")
    log("Download complete.")

def download_and_replace(zip_url, destination):
    temp_zip_path = "__temp_download__.zip"
    temp_extract_dir = "__temp_extract__"

    download_zip_with_progress(zip_url, temp_zip_path)

    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_extract_dir)

    extracted_folder = os.path.join(temp_extract_dir, os.listdir(temp_extract_dir)[0])
    total_files = sum([len(files) for r, d, files in os.walk(extracted_folder)])
    moved_files = 0

    for item in os.listdir(extracted_folder):
        s = os.path.join(extracted_folder, item)
        d = os.path.join(destination, item)

        if os.path.exists(d):
            if os.path.isdir(s):
                for root_dir, dirs, files in os.walk(s):
                    rel_path = os.path.relpath(root_dir, s)
                    target_subdir = os.path.join(d, rel_path)
                    os.makedirs(target_subdir, exist_ok=True)
                    for file in files:
                        src_file = os.path.join(root_dir, file)
                        dst_file = os.path.join(target_subdir, file)
                        if os.path.exists(dst_file):
                            force_remove(dst_file)
                        safe_move(src_file, dst_file)
                        moved_files += 1
                        progress["value"] = 100 * moved_files / total_files
                        log(f"Updating: {file}")
            else:
                force_remove(d)
                safe_move(s, d)
                moved_files += 1
                progress["value"] = 100 * moved_files / total_files
        else:
            safe_move(s, d)
            moved_files += 1
            progress["value"] = 100 * moved_files / total_files

    os.remove(temp_zip_path)
    shutil.rmtree(temp_extract_dir, ignore_errors=True)
    log("Update process finished.")
    finish_update()
def run_update_thread():
    try:
        raw_url = github_blob_to_raw(github_csv_url)
        remote_ver = get_remote_version(raw_url)
        local_ver = get_local_version(local_csv_path)

        if remote_ver is None or local_ver is None:
            log("Could not read one or both version files.")
            return

        log(f"Local version: {local_ver}")
        log(f"Remote version: {remote_ver}")

        if version.parse(remote_ver) > version.parse(local_ver):
            log("Newer version found on GitHub.")
            create_backup(target_directory)
            download_and_replace(repo_zip_url, target_directory)
            with open(local_csv_path, "w") as f:
                f.write(remote_ver)
            log("Local version file updated.")
        else:
            log("You already have the latest version.")
            finish_update()
    except Exception as e:
        log(f"[Update Thread] Error: {e}")
        finish_update()

if __name__ == "__main__":
    threading.Thread(target=run_update_thread, daemon=True).start()
    root.mainloop()