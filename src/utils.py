import json
from typing import Any
from pathlib import Path

DEFAULT_JSON_INDENT = 4


def loadJSON(path: str) -> dict:
    try:
        with open(path, "r", encoding="UTF-8") as file:
            f = json.load(file)
        return f
    except Exception as e:
        print(f"{e}")


def saveJSON(path: str, data: dict, indent: int = DEFAULT_JSON_INDENT) -> bool:
    with open(path, "w", encoding="UTF-8") as file:
        try:
            json.dump(data, file, indent=indent)
            return True
        except IOError as e:
            print(f"Saving file error: {e}")
            return False


def updateJSON(
    data: dict, key: str, value: Any, path: str, indent: int = DEFAULT_JSON_INDENT
) -> bool:
    result = _recursiveUpdateJSON(data, key, value)
    if result:
        saveJSON(path, data, indent)

    return result


def _recursiveUpdateJSON(currentDict: dict, key: str, value: Any) -> bool:
    if key in currentDict:
        currentDict[key] = value
        return True

    for v in currentDict.values():
        if isinstance(v, dict):
            if _recursiveUpdateJSON(v, key, value):
                return True

    return False


def getDownloadsPath() -> str:
    return str(Path.home() / "Downloads")