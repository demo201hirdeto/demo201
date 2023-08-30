import json
import os


def next_id() -> int:
    highest_id = 0

    for file in os.listdir("hirdetesek"):
        if not file.endswith(".json"):
            continue

        print(file)

        try:
            file_id = int(file.replace(".json", ""))
            if file_id > highest_id:
                highest_id = file_id
        except:
            continue

    return highest_id + 1


class Ad:
    def __init__(self, name, description, time, save):
        self.name = name
        self.description = description
        self.time = time
        if save:
            with open("hirdetesek/" + str(next_id()) + ".json", mode="w+") as f:
                f.write(json.dumps({"name": name, "description": description, "time": time}))
