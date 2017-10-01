import bluetooth
import json
import time
import requests
from satori.rtm.client import make_client

client_id="a2fd64e4-0d67-4545-b353-475f14123ee0"
client_secret="H7xS3yK2oS3uO0hU4xL5dQ4aI6rL7kC8cJ5uG2lM6cW8fM7tV2"
building_id=9990000508

endpoint = "wss://n0cy74ab.api.satori.com"
appkey = "CF1EDbdeFC3aC712Ac8cAB5bbdDF8fdB"

headers = {
    'x-ibm-client-id': client_id,
    'x-ibm-client-secret': client_secret,
    'accept': "application/vnd.collection+json",
    'content-type': "application/vnd.collection+json"
    }

def get_call_object(call_object_url):
    # Read current call status
    response = requests.get(call_object_url, headers=headers)
    return response

def get_deckstate_object(deckstate_object_url):
    # Read current deckstate status
    response = requests.get(deckstate_object_url, headers=headers)
    return response

def get_building_areas(building_id):
    # Read building areas
    response = requests.get("https://api.kone.com/api/building/%s/area" % building_id, headers=headers)
    return response

def publish_user(building_id, mac):
    with make_client(endpoint=endpoint, appkey=appkey) as client:
        print('Connected to Satori RTM!')

        def on_publish_ack(pdu):
            if pdu['action'] == 'rtm/publish/ok':
                print('Publish confirmed')
            else:
                print('Failed to publish. RTM replied with the error {0}: {1}'.format(pdu['body']['error'], pdu['body']['reason']))

        message = {"building": building_id, 'user': mac}
        client.publish("channel1", message, callback=on_publish_ack)
    
def publish_lift(location):
    with make_client(endpoint=endpoint, appkey=appkey) as client:
        print('Connected to Satori RTM!')

        def on_publish_ack(pdu):
            if pdu['action'] == 'rtm/publish/ok':
                print('Publish of location confirmed')
            else:
                print('Failed to publish location. RTM replied with the error {0}: {1}'.format(pdu['body']['error'], pdu['body']['reason']))

        # Follow the call until it is completed (7) or cancelled (8)
        callstate=None
        decklevel=None
        while True:
            response = get_call_object(location)
            response = json.loads(response.content.decode('utf-8'))
            # Find the current callState value from the response
    
            for item in response["collection"]["items"][0]["data"]:
                if item["name"] == "callState":
                    callstate = item["value"]
                    break
            # Find information where the elevator is
            for item in response["collection"]["links"]:
                if item["rel"] == "deckstate item":
                    deckstate = item["href"]
                    break
        
            # Call object itself is created immediately, but callState will be available shortly after call creation. It is an async call.
            if callstate:
                response = get_deckstate_object(deckstate)
                response = json.loads(response.content.decode('utf-8'))
                for item in response["collection"]["items"][0]["data"]:
                    if item["name"] == "level":
                        decklevel = item["value"]
                        break

            message = {"callState": callstate, "deckLevel": decklevel} 
            client.publish("channel2", message, callback=on_publish_ack)
            print ("Current callState=%s and deck level=%s" % (callstate, decklevel))
            if callstate == 7 or callstate == 8:
                break
            time.sleep(1)
    
        print ("Elevator call has finished")


def post_elevator_call(building_id):
    #The floors to go FROM and TO
    from_floor = 1
    to_floor = 5

    # Read buliding areas
    response = get_building_areas(building_id)
    response = json.loads(response.content.decode('utf-8'))
    areas_list = response["collection"]["items"]

    floors = {}

    areas_len = len(areas_list)
    for i in range(0, areas_len):
        for item in areas_list[i]["data"]:
            if item["name"] == "id":
                floors[i-1] = item["value"]

    first_area = floors[from_floor]
    second_area = floors[to_floor]

    payload = """{
        "template": {
            "data": [
                {"name":"sourceAreaId", "value": "%s"},
                {"name":"destinationAreaId", "value": "%s"}
            ]
        }
    }""" % (first_area, second_area)
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
			lift = post_elevator_call(building_id)
			publish_user(building_id, mac)
			publish_lift(lift.headers["Location"])
			print 'success'
