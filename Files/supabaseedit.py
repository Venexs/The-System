import json
import os
import sys
from supabase import create_client, Client
from infisical_client import ClientSettings, InfisicalClient, GetSecretOptions, AuthenticationOptions, UniversalAuthMethod
import jwt

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '../'))

sys.path.insert(0, project_root)

import thesystem.online
import thesystem.system

client = InfisicalClient(ClientSettings(
    auth=AuthenticationOptions(
        universal_auth=UniversalAuthMethod(
            client_id="0fa8dbf8-92ee-4889-bd48-1b5dd2d22e87",
            client_secret="a2c9a58bda26c914e333e6c0f7c35e019b30c3afa67b5dc8419a142ee8b2aec8",
        )
    )
))


def get_url():
    # access value
    name = client.getSecret(options=GetSecretOptions(
        environment="dev",
        project_id="a7b312a2-feb6-42bc-92cb-387e37463076",
        secret_name="SUPABASE_URL"
    ))
    return f"{name.secret_value}"
def get_key():
    # access value
    name = client.getSecret(options=GetSecretOptions(
        environment="dev",
        project_id="a7b312a2-feb6-42bc-92cb-387e37463076",
        secret_name="SUPABASE_KEY"
    ))
    return f"{name.secret_value}"

URL = "https://smewvswweqnpwzngdtco.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNtZXd2c3d3ZXFucHd6bmdkdGNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyMDY2NjcsImV4cCI6MjA0OTc4MjY2N30.0SSN0bbwzFMCGC47XUuwqyKfF__Zikm_rJHqXWf78PU"

supabase = create_client(URL, KEY)

session_file_path = "Files/Data/session.json"

# Path to your JSON file
json_file_path = "Files/Status.json"

def transform_data(data):
    """Transforms Supabase data to match the desired JSON structure."""

    try:
        with open(json_file_path, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {  # Correct default structure: No nested lists within "status"
            "status": [{}, {}],
            "avail_eq": [{}],
            "equipment": [{}],
            "cal_data": [{}]
        }

    # Extract user-related data from Supabase response and update existing status[0]
    status_data = {
        "name": data.get("name", ""),
        "hp": data.get("hp", 0),
        "mp": data.get("mp", 0),
        "level": data.get("level", 0),
        "str": data.get("str", 0),
        "int": data.get("int", 0),
        "agi": data.get("agi", 0),
        "vit": data.get("vit", 0),
        "per": data.get("per", 0),
        "man": data.get("man", 0),
        "XP": data.get("XP", 0),
        "coins": data.get("coins", 0),
        "fatigue_max": data.get("fatigue_max", 0),
        "fatigue": data.get("fatigue", 0),
        "last_level": data.get("last_level", 0),
    }
    existing_data["status"][0].update(status_data)

    # Metadata from Supabase, update existing status[1]
    metadata_data = {
        "title_bool": str(data.get("title_bool", False)),
        "title": data.get("title", "None"),
        "job": data.get("job", "None")
    }
    existing_data["status"][1].update(metadata_data)


    # Update avail_eq based on your Supabase data if needed
    # The example uses the raw str and int for the avail_eq, adjust to suit the actual use case
    existing_data["avail_eq"][0].update({
        "str_based": data.get("str_based", 0),
        "int_based": data.get("int_based", 0)
    })

    return existing_data


def get_user_id_from_session():
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

def fetch_user_row(user_id):
    try:
        response = supabase.table("status").select("*").eq("user_id", user_id).execute()
        data = response.data
        return data[0]  # Return the first matching row
    except Exception as e:
        print(f"An error occurred while fetching user row: {e}")
        return None



def update_json_file(data):
    """
    Update the JSON file with transformed data, updating the status and avail_eq sections.
    """
    try:
        with open(json_file_path, "r") as file:
            json_data = json.load(file)

        # Transform the data and update both sections
        transformed_data = transform_data(data)
        json_data["status"] = transformed_data["status"]  # Update 'status' section
        json_data["avail_eq"] = transformed_data["avail_eq"]  # Update 'avail_eq' section

        # Write the updated JSON back to the file
        with open(json_file_path, "w") as file:
            json.dump(json_data, file, indent=4)

        print("JSON file updated successfully.")
    except Exception as e:
        print(f"Error updating JSON file: {e}")
        import traceback
        traceback.print_exc() # Print the traceback for detailed information.



def main():
    # Get user ID from session file
    user_id = get_user_id_from_session()
    if not user_id:
        print("Could not retrieve user ID from session.")
        return

    # Fetch the user's row from Supabase
    specific_row = fetch_user_row(user_id)
    if specific_row:
        # Update the JSON file with the user's data
        update_json_file(specific_row)
    else:
        print(f"No data available for user_id: {user_id}")


if __name__ == "__main__":
    main()