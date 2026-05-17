"""Rescure Cyber Threat Intelligence Feeds Malicious IP Blacklist"""
from Elastic import shipperManager
import os
import requests
import re
import json
import datetime


format_threatIntel = []
intel = []
last_updated = None
count = 0


def format_template(initial_data):
    intel = {}
    intel["type"] = "ip_address"
    intel["category"] = "threat_intelligence"
    intel["value"] = initial_data["value"]
    intel["last_updated"] = initial_data["last_updated"]
    intel["confidence"] = ""
    intel["first_seen"] = ""
    intel["last_seen"] = ""
    intel["active"] = ""
    intel["meta"] = initial_data
    return intel


url = "https://rescure.me/rescure_blacklist.txt"
index = 'enrichment_osint_rescure'
wrapper = shipperManager.Shipper(index)


try:
    content = requests.get(url)
    resp = content.text
    length = len(os.listdir(r'D:\D\PycharmProjects\Use-Cases\Intel_4'))
    with open("intel_{}.json".format(length), "w") as writer:
        writer.write(resp)
    with open("intel_{}.json".format(length), "r") as reader:
        date = reader.readlines()[4:5]
        ops = re.split(r'at|\.', date[0])
        last_updated = ops[2]
        print(last_updated)

    with open("intel_{}.json".format(length), "r") as reader:
        lines = reader.readlines()[9:]
        for i in lines:
            jsn = {"last_updated": last_updated}
            x = re.split("\n", i)
            jsn["value"] = x[0]
            intel.append(jsn)
        print(intel)

    for data in intel:
        call = format_template(data)
        format_threatIntel.append(call)
        ship = wrapper.push(call)
        if isinstance(ship, dict):
            count += 1
            print("OUTCOME: {0}".format(ship))
        else:
            print(ship)
    print("Total Events Shipped: ", count)
    now = datetime.datetime.now()
    send = now.strftime("%b %d, %Y @ %H:%M:%S.%f")[:-3]
    print("\nTime Completed:", send)

    with open("intel_{}.json".format(length), "w") as writer:
        writer.write(json.dumps(format_threatIntel, indent=4))

except Exception as e:
    print(str(e))
