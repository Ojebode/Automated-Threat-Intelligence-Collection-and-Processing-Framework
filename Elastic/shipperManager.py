import os
import requests
import json
import datetime


index = 'datasource_posts_linkedin'
now = datetime.datetime.now()
send = now.strftime("%b %d, %Y @ %H:%M:%S.%f")[:-3]
# print(send)

conf = {'Server Address': os.environ.get('ES_SERVER_ADDRESS', 'https://process.thetech.net/'),
        'Username': os.environ['ES_USERNAME'],
        'Password': os.environ['ES_PASSWORD'],
        'Authenticate': 'True',
        'Verify SSL': os.environ.get('ES_VERIFY_SSL', 'True')}

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
            response = requests.post(url, headers=headers, json=event, verify=verify_ssl, timeout=30)
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
            return {"success": False, "message": str(e)}
