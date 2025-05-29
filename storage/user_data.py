import json
import os

DB_PATH = "storage/users.json"

def load_users():
    if not os.path.exists(DB_PATH):
        return {"users": [], "banned": [], "languages": {}, "favorites": {}}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_user(user_id: int):
    data = load_users()
    uid = str(user_id)
    if uid not in data["users"]:
        data["users"].append(uid)
        save_users(data)

def is_banned(user_id: int) -> bool:
    return str(user_id) in load_users().get("banned", [])

def ban_user(user_id: int):
    data = load_users()
    uid = str(user_id)
    if uid not in data["banned"]:
        data["banned"].append(uid)
        save_users(data)

def get_all_users():
    return load_users().get("users", [])

def set_language(user_id: int, lang: str):
    data = load_users()
    uid = str(user_id)
    if "languages" not in data:
        data["languages"] = {}
    data["languages"][uid] = lang
    save_users(data)


def get_language(user_id: int) -> str:
    data = load_users()
    return data.get("languages", {}).get(str(user_id), "ru")

def add_favorite(user_id: int, city: str):
    data = load_users()
    uid = str(user_id)
    if "favorites" not in data:
        data["favorites"] = {}
    if uid not in data["favorites"]:
        data["favorites"][uid] = []
    if city not in data["favorites"][uid]:
        data["favorites"][uid].append(city)
    save_users(data)

def get_favorites(user_id: int) -> list:
    return load_users().get("favorites", {}).get(str(user_id), [])

def remove_favorite(user_id: int, city: str):
    data = load_users()
    uid = str(user_id)
    if city in data.get("favorites", {}).get(uid, []):
        data["favorites"][uid].remove(city)
        save_users(data)
