import os
import json
import sys

CWD = os.path.abspath(os.path.dirname(sys.executable))
save_file = "save.json"


def write(key: str, entry: dict):
    save = load_file()
    if save.keys().__contains__(key):
        key_data = save[key]
        key_data.append(entry)
    else:
        save[key] = [entry]

    with open(os.path.join(CWD, save_file), mode='w', encoding='utf-8') as f:
        json.dump(save, f)


def load_file() -> dict:
    """
    load the specified save file
    returns: dict of save, or empty dict if no save file
    """
    try:
        f = open(os.path.join(CWD, save_file))
    except OSError as err:
        return {}
    data = json.load(f)
    return data


def delete_save() -> None:
    """
    deletes save file
    """
    try:
        os.remove(os.path.join(CWD, save_file))
    except FileNotFoundError:
        print("No save file exists")
