import json
import os
import subprocess
import time
import thesystem.system



def load_session_from_file():
    SESSION_FILE_PATH = "Files/Data/session.json"
    try:
        if os.path.exists(SESSION_FILE_PATH) and os.path.getsize(SESSION_FILE_PATH) > 0:
            with open(SESSION_FILE_PATH, 'r') as f:
                session_data = json.load(f)
                required_keys = ["access_token", "refresh_token", "expires_at"]
                
                # Ensure the required keys are present
                if all(key in session_data for key in required_keys):
                    # Check if the token has expired
                    current_time = time.time()
                    if current_time < session_data["expires_at"]:
                        # Token is valid; proceed with the GUI
                        print("Session is valid. Launching GUI...")
                        subprocess.Popen(["python", "gui.py"])
                        exit()
                    else:
                        # Token expired; refresh it
                        print("Token has expired. Attempting to refresh...")
                        if refresh_token(session_data):
                            subprocess.Popen(["python", "gui.py"])
                            exit()
                        else:
                            print("Failed to refresh token. Opening sign-in page...")
                else:
                    print("Invalid session structure in file.")
        else:
            print(f"Session file is empty or missing: {SESSION_FILE_PATH}.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading session file: {e}")

    # If the session is invalid or file is empty, open sign_in.py
    print("Opening sign_in.py...")
    subprocess.Popen(["python", "E:\\System\\Edited\\SystemUpdate3\\System_SL-main\\Logs\\Sign in\\sign_in.py"])
    exit()
def refresh_token(session_data):
    """Attempt to refresh the access token using the refresh token."""
    try:
        # Assuming you use Supabase's `auth.refresh_session` method
        from supabase import create_client, Client

        SUPABASE_URL = "your_supabase_url"
        SUPABASE_KEY = "your_supabase_key"
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

        response = supabase.auth.refresh_session({"refresh_token": session_data["refresh_token"]})
        if response and response.session:
            # Update session data
            new_session_data = {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "expires_at": time.time() + response.session.expires_in,  # Calculate new expiry time
            }
            save_session_to_json(SESSION_FILE_PATH, new_session_data)
            print("Token refreshed successfully.")
            return True
        else:
            print("Token refresh failed.")
            return False
    except Exception as e:
        print(f"Error refreshing token: {e}")
        return False

def save_session_to_json(file_path, session_data):
    """Save session data to a JSON file."""
    try:
        with open(file_path, 'w') as session_file:
            json.dump(session_data, session_file, indent=4)
        print("Session saved successfully.")
    except Exception as e:
        print(f"Error saving session: {e}")
        
        
        
try:
    file_path= "Files/Data/Vow_status.json"
    with open(file_path, 'r') as vow_file:
        vow_status = json.load(vow_file)
        vow=vow_status["Vow"]
except:
    vow=False



if vow==False:
    load_session_from_file()


else:
    thesystem.system.message_open("System Deleted")