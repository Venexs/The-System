import json
import os
import time
import threading
from supabase import create_client, Client



URL = "https://smewvswweqnpwzngdtco.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNtZXd2c3d3ZXFucHd6bmdkdGNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyMDY2NjcsImV4cCI6MjA0OTc4MjY2N30.0SSN0bbwzFMCGC47XUuwqyKfF__Zikm_rJHqXWf78PU"

supabase: Client = create_client(URL, KEY)




SESSION_FILE = "Files/Data/session.json"

def load_session():
    """Load session data from the session file."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return None

def save_session(session_data):
    """Save session data to the session file."""
    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f)

def refresh_token():
    """Refresh the user's access token."""
    session_data = load_session()
    if not session_data:
        print("No session found. Exiting refresh process.")
        return

    refresh_token = session_data.get("refresh_token")
    if not refresh_token:
        print("Refresh token not found. Exiting refresh process.")
        return

    try:
        response = supabase.auth.refresh_session(refresh_token)
        if response and response.session:
            # Update session data
            session_data["access_token"] = response.session.access_token
            session_data["refresh_token"] = response.session.refresh_token
            session_data["expires_in"] = response.session.expires_in
            save_session(session_data)
            print("Token refreshed successfully.")
        else:
            print("Failed to refresh token.")
    except Exception as e:
        print(f"Error refreshing token: {e}")

def refresh_token_loop():
    """Run the token refresh process periodically."""
    while True:
        session_data = load_session()
        if session_data:
            expires_in = session_data.get("expires_in", 3600)  # Default to 1 hour if not found
            # Refresh 5 minutes before expiration
            sleep_time = max(500, 1000)
            print(f"Sleeping for {sleep_time} seconds before next refresh.")
            time.sleep(sleep_time)
            refresh_token()
        else:
            print("No session found. Stopping token refresh loop.")
            break

if __name__ == "__main__":
    threading.Thread(target=refresh_token_loop, daemon=True).start()
    while True:
        time.sleep(1)  # Keep the main thread alive