import json

def get_wireshark_file_path():
    try:
        with open('wireshark_config.json') as json_file:
            data = json.load(json_file)
            return data['wireshark_pcapng_path']
    except FileNotFoundError:
        print("Config file not found.")
        return None

get_wireshark_file_path()