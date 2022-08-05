import csv
import requests
import json


def interview_script(csv_file: str, commands: list):
    devices = csv_reader(csv_file)
    for device in devices:
        api_responses = nx_api(device, commands)
        if api_responses != list():
            dump_to_json(api_responses, device.get("ip"))
        



def csv_reader(csv_file: str):
    with open(csv_file, "r") as csv_file:
        csv_content = csv.DictReader(csv_file, delimiter=",")
        lines = list()
        for line in csv_content:
            lines.append(line)
    return lines

def nx_api(device: dict, commands: list):
    api_responses = []
    my_headers = {'content-type': 'application/json-rpc'}
    url = f'http://{device.get("ip")}/ins'
    for cmd in commands:
        payload = [{'jsonrpc': '2.0', 'method': 'cli', 'params': [cmd, 1], 'id': '1'}]
        my_data = json.dumps(payload)
        try:
            response = requests.post(url, data=my_data, headers=my_headers, auth=(device.get("user"), device.get("pw")))
        except:
            print(f"Unreachable Router IP: {device.get('ip')}")
            return list()
        if response.status_code != 200:
            print(f"Device {device.get('ip')} Returned Bad Response Code: {response.status_code}")
            return list()
        api_responses.append(response)
    return api_responses


def dump_to_json(api_responses: list, ip: str):
    software_inventory_response = api_responses[0]
    hardware_inventory_response = api_responses[1]
    with open(f"output/{ip}_software_inventory", "w") as f:
        f.write(json.dumps(software_inventory_response.json()))
    with open(f"output/{ip}_hardware_inventory", "w") as f:
        f.write(json.dumps(hardware_inventory_response.json()))

        
