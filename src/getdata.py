import json

USERS = "../static/user.json"

def read_JSON(filename):
    try:
        with open(filename, "r") as file_obj:
            return json.load(file_obj)
    except:
        return dict()

def write_JSON(data, filename):
    with open(filename, "w+") as file_obj:
        json.dump(data, file_obj)

def append_JSON(filename, new_data):
    with open(filename, "w+") as file_obj:
        try: 
            old_data = json.load(file_obj)
            old_data.update(new_data)
        except: #In case there is a .json file but its empty
            old_data = new_data

    write_JSON(old_data, filename)


