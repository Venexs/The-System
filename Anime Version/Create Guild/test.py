from tkinter import Tk, Listbox, Button
from supabase import create_client
import os
from infisical_client import ClientSettings, InfisicalClient, GetSecretOptions, AuthenticationOptions, UniversalAuthMethod

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

URL = get_url()
KEY = get_key()

# Initialize Supabase client
supabase = create_client(URL, KEY)

# Fetch guilds and populate listbox
def load_guilds(listbox):
    response = supabase.table('Guilds').select('id', 'name').execute()
    guilds = response.data if response.data else []
    listbox.delete(0, 'end')  # Clear existing listbox entries
    for guild in guilds:
        listbox.insert('end', f"{guild['name']} (ID: {guild['id']})")

# Tkinter GUI setup
window = Tk()
window.title("Guild System")

guild_listbox = Listbox(window, width=50, height=15)
guild_listbox.pack()

refresh_button = Button(window, text="Load Guilds", command=lambda: load_guilds(guild_listbox))
refresh_button.pack()

window.mainloop()