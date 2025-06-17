import json
import os
import random
from aiogram import types

MOODS_FILE = "data/moods.json"
IMAGES_PATH = "data/images"

def get_user_name(user):
    return user.first_name or "друг"

def remember_mood(user_id: str, mood: str):
    try:
        with open(MOODS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[user_id] = {"mood": mood}

    with open(MOODS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_random_image():
    images = [f for f in os.listdir(IMAGES_PATH) if f.endswith(('.jpg', '.png'))]
    if images:
        return types.InputFile(os.path.join(IMAGES_PATH, random.choice(images)))
    return None
