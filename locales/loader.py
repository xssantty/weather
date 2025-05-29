import json
from pathlib import Path
from storage.user_data import get_language

LOCALES_DIR = Path(__file__).parent

with open(LOCALES_DIR / "ru.json", encoding="utf-8") as f:
    RU = json.load(f)

with open(LOCALES_DIR / "en.json", encoding="utf-8") as f:
    EN = json.load(f)

def get_text(key: str, context=None) -> str:
    user_id = None
    if hasattr(context, "from_user"):
        user_id = context.from_user.id
    elif hasattr(context, "message") and hasattr(context.message, "from_user"):
        user_id = context.message.from_user.id

    lang = get_language(user_id) if user_id else "ru"
    return (EN if lang == "en" else RU).get(key, f"[{key}]")
