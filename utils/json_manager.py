import json

# Json Core Version:
version = "2.1"


def load_json(file):
    with open("database/" + file + ".json", "r") as load:
        name = json.load(load)
    return name


def save_json(file, name):
    with open("database/" + file + ".json", "w") as save:
        json.dump(name, save, indent=4)
    return name
