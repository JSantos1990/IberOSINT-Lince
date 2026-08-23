import json
from pathlib import Path
import config

SETTINGS_FILE = Path(config.PROJECT_ROOT) / "settings.json"


def load_settings():

    if not SETTINGS_FILE.exists():

        data = {
            "last_directory": ""
        }

        SETTINGS_FILE.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

        return data

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_settings(data):

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def get_last_directory():

    return load_settings().get(
        "last_directory",
        ""
    )


def set_last_directory(path):

    data = load_settings()

    data["last_directory"] = path

    save_settings(data)