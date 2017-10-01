import bluetooth
import json
import time
import requests

client_id="a2fd64e4-0d67-4545-b353-475f14123ee0"
client_secret="H7xS3yK2oS3uO0hU4xL5dQ4aI6rL7kC8cJ5uG2lM6cW8fM7tV2"
building_id=9990000508

headers = {
    'x-ibm-client-id': client_id,
    'x-ibm-client-secret': client_secret,
    'accept': "application/vnd.collection+json",
    'content-type': "application/vnd.collection+json"
    }

def post_elevator_call(building_id, from_area, to_area):
    payload = """{
        "template": {
            "data": [
                {"name":"sourceAreaId", "value": "%s"},
                {"name":"destinationAreaId", "value": "%s"}
            ]
        }
    }""" % (from_area, to_area)
    response = requests.post("https://api.kone.com/api/building/%s/call" % building_id, headers=headers, data=payload)
    return response




sergei = '64:BC:0C:E8:6D:4D'
artem = 'F0:DB:E2:F2:D4:59'
iaroslav = '8C:1A:BF:CC:A9:35'
booked_clients = list([sergei, artem, iaroslav])

print("performing inquiry...")

while True:
	nearby_devices = bluetooth.discover_devices(lookup_names=True)
	for mac, name in nearby_devices:
		if mac in booked_clients:
			print 'call lift for %s' % name
			post_elevator_call(building_id,0,1)
