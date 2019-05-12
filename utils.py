import json

def read_json(filename):
    success=False

    while not success:
        try:
            with open(filename, "r") as f:
                raw_json = f.readlines()
                # print(raw_json)/
                # print(raw_json[0])
            json_dict = json.loads(raw_json[0])
            success=True
        except (IndexError, json.decoder.JSONDecodeError):
            pass
    return json_dict

def write_json(object, filename):
    dump = json.dumps(object)
    with open(filename, "w") as f:
        f.write(dump)
