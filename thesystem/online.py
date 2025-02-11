
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Listbox, Frame, Scrollbar, messagebox, Toplevel, Label
import json
import csv
import subprocess
import random
import cv2
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import threading
import sys
import os
import webbrowser
import thesystem.system

def ex_close(win):
    with open("Files/Tabs.json",'r') as tab_son:
        tab_son_data=json.load(tab_son)

    with open("Files/Tabs.json",'w') as fin_tab_son:
        json.dump(tab_son_data,fin_tab_son,indent=4)
    subprocess.Popen(['python', 'Files\Mod\default\sfx_close.py'])
    thesystem.system.animate_window_close(win, win.winfo_width(), win.winfo_height(), step=50, delay=1)

def get_url(client):
    return "https://smewvswweqnpwzngdtco.supabase.co"
def get_key(client):
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNtZXd2c3d3ZXFucHd6bmdkdGNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyMDY2NjcsImV4cCI6MjA0OTc4MjY2N30.0SSN0bbwzFMCGC47XUuwqyKfF__Zikm_rJHqXWf78PU"



def get_current_user_id(supabase_client, session):  # Add supabase_client parameter
    try:
        user_response = supabase_client.auth.get_user(session["access_token"])  # Use the client object
        if user_response and user_response.user:
            return user_response.user.id
        else:
            print("User is not authenticated.")  # Add logging for better debugging
            return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


# Function to get the user's name from the `status` table
def get_user_name(supabase_client, session):  # Add supabase_client parameter
    try:
        # Step 1: Get current user ID using the access token
        user_id = get_current_user_id(supabase_client, session)  # Pass the client
        
        if user_id is None:
            return None
        
        # Step 2: Query the `status` table for the row with the matching user ID
        response = supabase_client.table('status').select('name').eq('user_id', user_id).single().execute()

        # Step 3: Extract the user's name from the response
        user_name = response.data.get('name', 'No name found')  # Adjust column name if necessary
        return user_name
    
    except Exception as e:
        print(f"Error retrieving user name: {e}")
        return None

def join_guild(guild_id, supabase_client, session): # Add supabase_client parameter
    # Fetch guild details
    response = supabase_client.table('Guilds').select('*').eq('id', guild_id).execute()
    guild = response.data[0] if response.data else None

    if guild:
        # Assuming 'user_id' is stored in the 'status' table under the 'name' column
        user_response = supabase_client.table('status').select('name').eq('user_id', get_current_user_id(supabase_client, session)).execute()
        
        # Extract the user ID from the response data
        user_id = user_response.data[0]['name'] if user_response.data else None  # Make sure to handle missing data

        if not user_id:
            print("User not found.")
            return

        # Check if the user is already a member
        membership_check = supabase_client.table('Members').select('*').eq('user_id', user_id).eq('guild_id', guild_id).execute()
        if membership_check.data:
            return

        # Add user to the guild
        insert_response = supabase_client.table('Members').insert({'user_id': user_id, 'guild_id': guild_id}).execute()
    else:
        print("Guild not found.")

def GuildOption(eve,name,window):
    if name == "Create":
        subprocess.Popen(['python', f'Anime Version/Create Guild/gui.py'])
        ex_close(window)
    elif name == "Join":
        subprocess.Popen(['python', f'Anime Version/Guild List/gui.py'])
        ex_close(window)
    elif name == "Invite":
        subprocess.Popen(['python', f'thesystem/invite.py'])
        webbrowser.open("https://discord.gg/Fqpvg7ykp7", new=0, autoraise=True)
        ex_close(window)
    elif name == "Guild Raid":
        subprocess.Popen(['python', f'Anime Version/Guild Raids/gui.py'])
        ex_close(window)
        
def get_current_user_guild_leader_id(supabase_client, session):
    try:
        # Get the current user's guild_id
        guild_id = get_current_guild_id(supabase_client=supabase_client, session=session)  # Ensure this function returns the correct guild_id
        user_id = get_current_user_id(supabase_client=supabase_client, session=session)  # Ensure this function returns the correct user_id
        # Query the Guilds table for the leader_id where guild_id matches
        if guild_id:
            response = supabase_client.table("Guilds").select("leader_id").eq("id", guild_id).execute()
            if response.data and len(response.data) > 0:
                # Assuming the result contains a single row with the leader_id column
                return response.data[0]["leader_id"]
            else:
                print("No matching guild found or no leader_id available.")
                return None
        else:
            print("User is not associated with a guild.")
            return None
    except Exception as e:
        print(f"Error retrieving leader_id: {e}")
        return None
    


def switch_guild(user_id, new_guild_id, supabase_client, session): # Add supabase_client parameter
    # Remove the user from the current guild
    supabase_client.table('Members').delete().eq('user_id', get_current_user_id(supabase_client=supabase_client, session=session)).execute()
    
    # Add the user to the new guild
    supabase_client.table('Members').insert({'user_id': user_id, 'guild_id': new_guild_id}).execute()
    print(f"Switched to guild with ID: {new_guild_id}")

# Fetch guilds and populate listbox
def load_guilds(treeview, supabase, rank_priority): # Add supabase_client parameter
    # Fetch guilds from Supabase
    response = supabase.table('Guilds').select('id', 'name', 'rank', 'member_count').execute()

    guilds = response.data if response.data else []

    # Sort guilds based on the custom rank priority
    sorted_guilds = sorted(guilds, key=lambda guild: rank_priority.get(guild['rank'], float('inf')))

    # Clear existing Treeview entries
    for item in treeview.get_children():
        treeview.delete(item)

    # Insert sorted guilds into the Treeview
    for guild in sorted_guilds:
        print(f"Inserting guild with ID: {guild['id']}")  # Debugging
        treeview.insert('', 'end', iid=guild['id'], values=(
            guild['name'], guild['rank'], guild['member_count'], ""))  # Empty Join initially
        
        
def CreateGuild(name, leader_id, window, supabaseclient, session):
    guild_name = name
    leader_id = get_current_user_id(supabase_client=supabaseclient, session=session)

    # Check for existing guild
    check_response = supabaseclient.table('Guilds').select('id').eq('name', guild_name).execute()
    
    if check_response.data:
        subprocess.Popen(['python', 'Anime Version/Create Guild/error.py'])
        pass
    else:
        try:
            # 1. CREATE THE GUILD FIRST
            create_response = supabaseclient.table('Guilds').insert({
                'name': guild_name,
                'leader_id': leader_id
            }).execute()

            # 2. GET NEW GUILD ID FROM INSERT RESPONSE
            guild_id = create_response.data[0]['id']
            print("New guild ID:", guild_id)

            # 3. UPDATE STATUS TABLE
            update_response = supabaseclient.table('status').update(
                {'guild_id': guild_id}
            ).eq('user_id', leader_id).execute()

            print("Update response data:", update_response.data)  # Should show updated rows
            
            # 4. Verify update
            if len(update_response.data) > 0:
                subprocess.Popen(['python', 'Anime Version/Create Guild/success.py'])
                ex_close(window)
            else:
                print("No rows updated - user might not exist in status table")
                subprocess.Popen(['python', 'Anime Version/Create Guild/error.py'])
                
        except Exception as e:
            print(f"Operation failed: {str(e)}")
            subprocess.Popen(['python', 'Anime Version/Create Guild/error.py'])




def update_guild_status(supabase_client, session, treeview): # Add supabase_client parameter
    # Get the current user ID
    user_id = get_current_user_id(supabase_client=supabase_client, session=session)
    if not user_id:
        print("User not authenticated.")
        return

    # Check which guild the player is currently in
    membership_response = supabase_client.table('status').select('guild_id').eq('user_id', get_current_user_id(supabase_client=supabase_client, session=session)).execute()
    current_guild_id = membership_response.data[0]['guild_id'] if membership_response.data else None

    # Update the Treeview
    for item in treeview.get_children():
        guild_id = item  # Treeview item's ID corresponds to the guild's ID
        if guild_id == current_guild_id:
            # For the current guild
            treeview.item(item, values=(
                treeview.item(item, "values")[0],  # Guild Name
                treeview.item(item, "values")[1],  # Rank
                treeview.item(item, "values")[2],  # Members
                "In Guild"  # Text for the current guild
            ))
        else:
            # For other guilds
            treeview.item(item, values=(
                treeview.item(item, "values")[0],  # Guild Name
                treeview.item(item, "values")[1],  # Rank
                treeview.item(item, "values")[2],  # Members
                "Switch Guild"  # Text for other guilds
            ))

def get_current_guild_id(supabase_client, session):
    # Fetch current user's guild
    user_id = get_current_user_id(supabase_client=supabase_client, session=session)
    membership_response = supabase_client.table('status').select('guild_id').eq('user_id', get_current_user_id(supabase_client=supabase_client, session=session)).execute()
    current_guild_id = membership_response.data[0]['guild_id'] if membership_response.data else None
    return current_guild_id

class CustomMessageBox:
    def __init__(self, master, title, message, message_type="info"):
        self.top = Toplevel(master)  # Create a new window
        self.top.title(title)  # Set the title of the message box
        self.top.geometry("300x150")  # Set the size of the message box

        # Add a label to display the message
        self.label = Label(self.top, text=message, font=("Montserrat", 12), padx=10, pady=10)
        self.label.pack(pady=20)

        # Add buttons based on the message type
        if message_type == "error":
            self.button = Button(self.top, text="Okay", command=self.top.destroy, bg="red", fg="white")
        else:  # Default to "info"
            self.button = Button(self.top, text="Okay", command=self.top.destroy, bg="green", fg="white")
        self.button.pack(pady=10)

        # Center the message box on the screen
        self.center_window()

    def center_window(self):
        window_width = 300
        window_height = 150
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        
        # Calculate position
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        
        # Position the message box in the center of the screen
        self.top.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

    def show(self):
        self.top.mainloop()