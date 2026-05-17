from Elastic import shipperManager
import requests
import os
import re
import json
import datetime


threatIntel = []
format_threatIntel = []
url = "https://www.botvrij.eu/data/ioclist.ip-dst"
index = 'enrichment_osint_botvrij'
wrapper = shipperManager.Shipper(index)
count = 0


def format_template(initial_data):
    intel = {}
    intel["type"] = "ip_address"
    intel["category"] = "threat_intelligence"
    intel["value"] = initial_data["value"]
    intel["description"] = initial_data["details"]
    intel["confidence"] = ""
    intel["first_seen"] = ""
    intel["last_seen"] = ""
    intel["active"] = ""
    intel["meta"] = initial_data
    return intel


try:
    content = requests.get(url)
    resp = content.text
    length = len(os.listdir(r'D:\D\PycharmProjects\Use-Cases\Intel_2'))
    with open("intel_{}.json".format(length), "w") as writer:
        writer.write(resp)
    with open("intel_{}.json".format(length), "r") as reader:
        lines = reader.readlines()[6:]
        # print(lines)
        for i in lines:
            jsn = {"source": "Botvrij"}
            x = re.split("[# '\\s -']+", i, 3)
            jsn["type"] = x[1]
            jsn["value"] = x[0]
            jsn["details"] = x[3]
            threatIntel.append(jsn)

    for data in threatIntel:
        call = format_template(data)
        format_threatIntel.append(call)
        ship = wrapper.push(call)
        if isinstance(ship, dict):
            count += 1
            print("OUTCOME: {0}".format(ship))
        else:
            print(ship)
    print("TOTAL Events Shipped: ", count)
    now = datetime.datetime.now()
    send = now.strftime("%b %d, %Y @ %H:%M:%S.%f")[:-3]
    print("\nTime Completed:", send)

    with open("intel_{}.json".format(length), "w") as writer:
        writer.write(json.dumps(format_threatIntel, indent=4))

    # print(json.dumps(threatIntel, indent=4))

except Exception as e:
    print(str(e))