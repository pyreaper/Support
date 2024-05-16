import json


class JsonStorer:
    def __init__(self, fileName: str):
        self.file_name = fileName

    def add_to_json(self, key: any, value: any) -> None:
        with open(f"./src/data/{self.file_name}.json", "r", encoding="utf-8") as f:
            c_data = json.load(f)
            c_data[key] = value

        with open(f"./src/data/{self.file_name}.json", "w", encoding="utf-8") as f:
            json.dump(c_data, f)

    def get_value(self, key: any) -> any:
        with open(f"./src/data/{self.file_name}.json", "r", encoding="utf-8") as f:
            c_data = json.load(f)
            if key in c_data:
                return c_data[key]
            else:
                return None
