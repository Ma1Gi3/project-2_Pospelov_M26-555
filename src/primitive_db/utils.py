import json
import os


def load_metadata(filepath):
    """Загружает структуру таблицы"""
    if not os.path.exists(filepath):
        return {}

    with open(filepath, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return metadata


def save_metadata(filepath, data):
    """Сохраняет структуру таблицы"""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_table_data(table_name):
    """Загружает записи указанноц таблицы"""
    filepath = f"data/{table_name}.json"

    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def save_table_data(table_name, data):
    """Сохраняет записи указанной таблицы"""
    os.makedirs("data", exist_ok=True)

    filepath = f"data/{table_name}.json"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
 