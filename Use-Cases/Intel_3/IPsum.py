from Elastic import shipperManager
import requests
import os
import re
import json
import datetime


threatIntel = []
format_threatIntel = []
last_updated = None
count = 0

url = "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt"
index = 'enrichment_osint_ipsum'
wrapper = shipperManager.Shipper(index)


def format_template(initial_data):
    intel = {}
    intel["type"] = "ip_address"
    intel["category"] = "threat_intelligence"
    intel["value"] = initial_data["value"]
    intel["blacklist_count"] = initial_data["blacklist_count"]
    intel["confidence"] = ""
    intel["first_seen"] = ""
    intel["last_seen"] = ""
    intel["active"] = ""
    intel["meta"] = initial_data
    return intel


try:
    content = requests.get(url)
    resp = content.text
    length = len(os.listdir(r'D:\D\PycharmProjects\Use-Cases\Intel_3'))
    with open("intel_{}.json".format(length), "w") as writer:
        writer.write(resp)
    with open("intel_{}.json".format(length), "r") as reader:
        date = reader.readlines()[3:4]
        ops = re.split("[#:]+", date[0], 2)
        last_updated = ops[2]
        # print(last_updated)

    with open("intel_{}.json".format(length), "r") as reader:
        lines = reader.readlines()[7:]
        for i in lines:
            jsn = {"last_updated": last_updated,
                   }
            x = re.split("[\t\n]+", i, 2)
            jsn["value"] = x[0]
            jsn["blacklist_count"] = x[1]
            threatIntel.append(jsn)
    # print(intel)
    for data in threatIntel:
        call = format_template(data)
        format_threatIntel.append(call)
        ship = wrapper.push(call)
        if isinstance(ship, dict):
            count += 1
            print("OUTCOME: {0} : {1}".format(ship, count))
        else:
            print(ship)
    print("TOTAL Events Shipped: ", count)
    now = datetime.datetime.now()
    send = now.strftime("%b %d, %Y @ %H:%M:%S.%f")[:-3]
    print("\nTime Completed:", send)

    with open("intel_{}.json".format(length), "w") as writer:
        writer.write(json.dumps(format_threatIntel, indent=4))

except Exception as e:
    print(str(e))