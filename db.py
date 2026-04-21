from supabase import create_client, Client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def check_user(login, password):
    response = supabase.table("users").select("password").eq("login", login).execute()
    data = response.data
    if data[0]["password"] == password:
        return True
    else: return False

check_user("bohdan", "")