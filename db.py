
from supabase import create_client, Client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def check_user(login, password):
    response = supabase.table("users").select("password").eq("login", login).execute()
    data = response.data
    print(data)
    if data[0]["password"] == password:
        return True
    else: return False

def create_user(login, password):
    response = supabase.table("users").insert({"login": login, "password": password}).execute()
    return response.data

def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data

def get_user_by_id(user_id):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return response.data

def get_user_by_login(login):
    response = supabase.table("users").select("*").eq("login", login).execute()
    return response.data

def update_user(user_id, login=None, password=None):
    data_to_update = {}
    if login: data_to_update["login"] = login
    if password: data_to_update["password"] = password
    
    response = supabase.table("users").update(data_to_update).eq("id", user_id).execute()
    return response.data

def delete_user(user_id):
    response = supabase.table("users").delete().eq("id", user_id).execute()
    return response.data


def create_occupation(name):
    response = supabase.table("occupations").insert({"name": name}).execute()
    return response.data

def get_occupations():
    response = supabase.table("occupations").select("*").execute()
    return response.data

def update_occupation(occupation_id, name):
    response = supabase.table("occupations").update({"name": name}).eq("id", occupation_id).execute()
    return response.data

def delete_occupation(occupation_id):
    response = supabase.table("occupations").delete().eq("id", occupation_id).execute()
    return response.data


def create_doctor(name, patronym, occupation_id):
    response = supabase.table("doctors").insert({
        "name": name, 
        "patronym": patronym, 
        "occupation": occupation_id
    }).execute()
    return response.data

def get_doctors():
    response = supabase.table("doctors").select("*").execute()
    return response.data

def get_doctors_with_occupation_names():
    """
    Advanced Read: Uses Supabase relational querying to join the tables
    and get the occupation name alongside the doctor details.
    """
    response = supabase.table("doctors").select("id, name, patronym, occupations(name)").execute()
    return response.data

def update_doctor(doctor_id, name=None, patronym=None, occupation_id=None):
    data_to_update = {}
    if name: data_to_update["name"] = name
    if patronym: data_to_update["patronym"] = patronym
    if occupation_id is not None: data_to_update["occupation"] = occupation_id
    
    response = supabase.table("doctors").update(data_to_update).eq("id", doctor_id).execute()
    return response.data


def create_appointment(appointed_at, doctor_id, user_id, comments=None):
    response = supabase.table("appointments").insert({
        "appointed_at": appointed_at,
        "doctor_id": doctor_id,
        "user_id": user_id,
        "comments": comments
    }).execute()
    return response.data

def get_appointments():
    response = supabase.table("appointments").select("*").execute()
    return response.data

def get_appointment_by_id(appointment_id):
    response = supabase.table("appointments").select("*").eq("id", appointment_id).execute()
    return response.data

def get_appointments_with_details():
    """
    Advanced Read: Fetches the appointment along with the doctor's name and user's login.
    """
    response = supabase.table("appointments").select(
        "id, appointed_at, comments, doctors(name, patronym), users(login)"
    ).execute()
    return response.data

def update_appointment(appointment_id, appointed_at=None, doctor_id=None, user_id=None, comments=None):
    data_to_update = {}
    if appointed_at is not None: data_to_update["appointed_at"] = appointed_at
    if doctor_id is not None: data_to_update["doctor_id"] = doctor_id
    if user_id is not None: data_to_update["user_id"] = user_id
    if comments is not None: data_to_update["comments"] = comments
    
    response = supabase.table("appointments").update(data_to_update).eq("id", appointment_id).execute()
    return response.data

def delete_appointment(appointment_id):
    response = supabase.table("appointments").delete().eq("id", appointment_id).execute()
    return response.data


def check_user(login, password):
    response = supabase.table("users").select("password").eq("login", login).execute()
    data = response.data
    if data and data[0]["password"] == password:
        return True
    else: 
        return False

def create_user(login, password, is_admin=False):
    response = supabase.table("users").insert({
        "login": login, 
        "password": password, 
        "is_admin": is_admin
    }).execute()
    return response.data

def update_user(user_id, login=None, password=None, is_admin=None):
    data_to_update = {}
    if login: data_to_update["login"] = login
    if password: data_to_update["password"] = password
    if is_admin is not None: data_to_update["is_admin"] = is_admin
    
    response = supabase.table("users").update(data_to_update).eq("id", user_id).execute()
    return response.data

def get_occupation_by_id(occ_id):
    response = supabase.table("occupations").select("*").eq("id", occ_id).execute()
    return response.data

def get_doctor_by_id(doc_id):
    response = supabase.table("doctors").select("*").eq("id", doc_id).execute()
    return response.data

def delete_doctor(doctor_id):
    response = supabase.table("doctors").delete().eq("id", doctor_id).execute()
    return response.data

#check_user("bohdan", "")
#print(get_doctors())
#print(get_occupations())
#print(get_appointments())
#print(get_user_by_login("bohdan"))
print(get_doctors_with_occupation_names())