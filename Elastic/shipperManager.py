import requests
import json
import datetime


index = 'datasource_posts_linkedin'
now = datetime.datetime.now()
send = now.strftime("%b %d, %Y @ %H:%M:%S.%f")[:-3]
# print(send)
# https://process.thetechdream.net/api/send_data

conf = {'Server Address': 'https://process.thetech.net/',
        'Username': 'osint',
        'Password': 'yG?xx2]T3f8a£',
        'Authenticate': 'True',
        'Verify SSL': "False"}

# Example Consts:
SCRIPT_NAME = "ElasticSearch - Push"  # For logging

server_address = conf['Server Address']
username = conf['Username']
password = conf['Password']
authenticate = conf['Authenticate'].lower() == 'true'
verify_ssl = conf['Verify SSL'].lower() == 'true'

headers = {
    'Content-Type': 'application/json',
    'ES-Username': conf["Username"],
    'ES-Password': conf['Password']
}


class Shipper:
    def __init__(self, index):
        self.index = index

    def push(self, event):
        try:
            url = "{0}".format(server_address)
            response = requests.post(url, headers=headers, json=event, verify=False)
            if response.status_code == 200:
                try:
                    # Try to return JSON response
                    return response.json()
                except json.JSONDecodeError:
                    # If response is not JSON formatted
                    return {"success": False, "message": "Non-JSON response received", "data": response.text}
            else:
                # Return error status and message
                return {"success": False, "status_code": response.status_code, "message": response.text}
        except Exception as e:
            print(u"Error performing action: {}".format(e))
