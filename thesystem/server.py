import json
from supabase import create_client, Client
import jwt

def get_user_id_from_session():
    session_file_path = "Files/Player Data/Session.json"
    """Extract the authenticated user's ID from the session JSON."""
    try:
        # Load session data
        with open(session_file_path, "r") as file:
            session_data = json.load(file)
        
        # Decode the access token
        access_token = session_data.get("access_token")
        if not access_token:
            print("Access token not found in session file.")
            return None
        
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        user_id = decoded_token.get("sub")  # Extract the 'sub' field (user ID)
        
        if user_id:
            print(f"Authenticated user ID: {user_id}")
            return user_id
        else:
            print("User ID not found in access token.")
            return None
    except Exception as e:
        print(f"Error extracting user ID: {e}")
        return None