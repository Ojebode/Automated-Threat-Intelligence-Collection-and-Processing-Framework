from Elastic import shipperManager
import requests
import json
import os

url = "https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.json"
index = 'enrichment_osint_feodotracker'

wrapper = shipperManager.Shipper(index)
count = 0


def format_template(initial_data):
    intel = {}
    intel["category"] = "threat_intelligence"
    intel["type"] = "ip_address"
    intel["value"] = initial_data["ip_address"]
    intel["confidence"] = ""
    intel["first_seen"] = initial_data["first_seen"]
    intel["last_seen"] = initial_data["last_online"]
    intel["active"] = initial_data["status"]
    intel["meta"] = initial_data
    return intel


try:
    content = requests.get(url)
    output = content.json()
    new_output = []

    for data in output:
        call = format_template(data)
        new_output.append(call)

    json_formatted_str = json.dumps(new_output, indent=4)
    for data in new_output:
        ship = wrapper.push(data)
        if isinstance(ship, dict):
            count += 1
            print("OUTCOME: {0}".format(ship))
        else:
            print(ship)
    print("\nTOTAL Events Shipped: ", count)

    # list files a directory
    length = len(os.listdir(r'D:\D\PycharmProjects\Use-Cases\Intel_1'))
    # Writing to sample.json
    with open("intel_{}.json".format(length), "w") as writer:
        writer.write(json_formatted_str)
except Exception as e:
    print(str(e))
