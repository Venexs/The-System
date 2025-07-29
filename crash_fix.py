import requests
import pandas as pd
import os
import shutil
import tempfile
import subprocess
import sys
import time
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading

# Try to import patoolib, and install it if not available
def ensure_patool_installed():
    try:
        import patoolib
        return patoolib
    except ImportError:
        print("📦 'patool' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "patool"])
        import patoolib
        return patoolib

patoolib = ensure_patool_installed()

CSV_PATH = "thesystem/update_with_paths.csv"  # Adjust path if needed
RAR_URL = "https://github.com/Venexs/The-System/releases/download/files/npy.files.rar"
RAR_PATH = "npy_files.rar"
EXTRACT_DIR = "__npy_temp_extract__"

# --- GUI ---
root = tk.Tk()
root.title("The System Bug Fixer")
root.geometry("600x400")

canvas = tk.Canvas(root)
canvas.place(relwidth=1, relheight=1)

status_label = tk.Label(canvas, text="Starting update...", anchor="center", font=("Segoe UI", 11))
status_label.place(relx=0.5, rely=0.05, anchor="center")

progress = ttk.Progressbar(canvas, orient="horizontal", mode="determinate", length=300)
progress.place(relx=0.5, rely=0.1, anchor="center")
progress["maximum"] = 100
progress["value"] = 0

log_display = scrolledtext.ScrolledText(canvas, font=("Consolas", 10), wrap=tk.WORD)
log_display.place(rely=0.2, relwidth=1, relheight=0.8)

# Thread-safe log
log_lock = threading.Lock()
def log(message):
    def safe_insert():
        with log_lock:
            log_display.insert(tk.END, message + "\n")
            log_display.see(tk.END)
            status_label.config(text=message)
    root.after(0, safe_insert)

def update_progress(value):
    def safe_update():
        progress["value"] = value
    root.after(0, safe_update)

def download_rar_file(url, dest, retries=3):
    headers = {"User-Agent": "Mozilla/5.0 (RAR Updater)"}
    for attempt in range(1, retries + 1):
        downloaded = 0
        mode = "wb"

        if os.path.exists(dest):
            downloaded = os.path.getsize(dest)
            headers["Range"] = f"bytes={downloaded}-"
            mode = "ab"

        log(f"⬇️ Attempt {attempt}: Downloading RAR from {url} (resuming at {downloaded} bytes)...")
        try:
            with requests.get(url, stream=True, timeout=60, headers=headers) as response:
                if response.status_code not in [200, 206]:
                    raise RuntimeError(f"Unexpected status code {response.status_code}")
                content_length = int(response.headers.get("Content-Length", 0))
                total_expected = downloaded + content_length
                last_reported_percent = -1

                with open(dest, mode) as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = int((downloaded / total_expected) * 100)
                            update_progress(percent)
                            if percent != last_reported_percent:
                                log(f"Downloading... {percent}%")
                                last_reported_percent = percent

                if total_expected and downloaded < total_expected:
                    raise IOError(f"Incomplete download: expected {total_expected}, got {downloaded}")

                log("✅ RAR download complete.")
                return  # success

        except Exception as e:
            log(f"❌ Download failed: {e}")
            if attempt < retries:
                log("🔁 Retrying in 3 seconds...")
                time.sleep(3)
            else:
                raise RuntimeError(f"Failed to download RAR after {retries} attempts: {e}")

def replace_npy_files_from_rar():
    try:
        download_rar_file(RAR_URL, RAR_PATH)

        os.makedirs(EXTRACT_DIR, exist_ok=True)
        patoolib.extract_archive(RAR_PATH, outdir=EXTRACT_DIR, verbosity=-1)

        df = pd.read_csv(CSV_PATH)
        npy_source_dir = os.path.join(EXTRACT_DIR, "npy files")

        for _, row in df.iterrows():
            local_path = str(row["local_file_path"]).strip().replace("\\", "/")
            filename = os.path.basename(local_path)
            replacement_path = os.path.join(npy_source_dir, filename)

            if not os.path.exists(replacement_path):
                log(f"⚠️ Replacement not found in RAR: {replacement_path}")
                continue

            if os.path.exists(local_path):
                try:
                    os.remove(local_path)
                    log(f"🗑️ Deleted: {local_path}")
                except Exception as e:
                    log(f"⚠️ Could not delete {local_path}: {e}")
                    continue

            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            try:
                with open(replacement_path, 'rb') as src, open(local_path, 'wb') as dst:
                    dst.write(src.read())
                log(f"✅ Replaced: {local_path}")
            except Exception as e:
                log(f"❌ Failed to copy {replacement_path} to {local_path}: {e}")

        os.remove(RAR_PATH)
        shutil.rmtree(EXTRACT_DIR, ignore_errors=True)
        log("\n✅ All .npy files replaced from RAR and temporary files removed.")
        update_progress(100)

    except Exception as e:
        log(f"Error during RAR replacement: {e}")

def run_thread():
    thread = threading.Thread(target=replace_npy_files_from_rar)
    thread.start()

if __name__ == "__main__":
    run_thread()
    root.mainloop()
