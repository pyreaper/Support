import json 

def add_to_json(key: any, value: any, filename: str) -> None:
    with open(f"./data/{filename}.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        c_data[key] = value

    with open(f"./data/{filename}.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)


def get_value(key: any, filename: str) -> any:
    with open(f"./data/{filename}.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        return c_data[key]