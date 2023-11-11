import json


def save_json_to_file(file_path, data):
    with open(file_path, "w") as outfile:
        json.dump(data, outfile)
