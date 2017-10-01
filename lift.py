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

def get_building(building_id):
    # Test that the building can be accessed with given credentials
    response = requests.get("https://api.kone.com/api/building/%s" % building_id, headers=headers)
    return response

def get_building_areas(building_id):
    # Read building areas
    response = requests.get("https://api.kone.com/api/building/%s/area" % building_id, headers=headers)
    return response

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

def get_call_object(call_object_url):
    # Read current call status
    response = requests.get(call_object_url, headers=headers)
    return response

def get_deckstate_object(deckstate_object_url):
    # Read current deckstate status
    response = requests.get(deckstate_object_url, headers=headers)
    return response


if __name__ == "__main__":
    #The floors to go FROM and TO
    from_floor = 1
    to_floor = 5

    # Test that our credentials are ok.
    response = get_building(building_id)
    print ("Trying %s responded with code %s" % (building_id, response.status_code))
    if response.status_code != 200:
        exit(1)

    # Read buliding areas
    response = get_building_areas(building_id)
    response = json.loads(response.content.decode('utf-8'))
    areas_list = response["collection"]["items"]

    floors = {}

    print(len(areas_list))
    print(areas_list[0]["data"])
    print(areas_list[1]["data"])
    print(areas_list[2]["data"])
    print(areas_list[3]["data"])
    print(areas_list[18]["data"])
    print(areas_list[19]["data"])
    # print(json.dumps(json.loads(str(areas_list))), indent=4, sort_keys=True)
    # For simplicity, select the first and second area ids for elevator call
    areas_len = len(areas_list)
    for i in range(0, areas_len):
        for item in areas_list[i]["data"]:
            if item["name"] == "id":
                floors[i] = item["value"]
#                break
#    for item in areas_list[5]["data"]:
#        if item["name"] == "id":
#            second_area = item["value"]
#            break
    first_area = floors[from_floor]
    second_area = floors[to_floor]
    # Make an elevator call
    response = post_elevator_call(building_id, first_area, second_area)
    # Will respond with 201 Created without message body. Call object is in headers "Location"
    if response.status_code != 201:
        print ("Elevator call responded with bad status code: %s" % response.status_code)
        print (response.headers)
        print (response.content)
        exit(1)
    call_object = response.headers["Location"]
    print("Call object location: %s" % call_object)

    # Follow the call until it is completed (7) or cancelled (8)
    callstate=None
    decklevel=None
    while True:
        response = get_call_object(call_object)
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
        
        # HOMEWORK: parse the floor information and door state from the deckstate object
        # Call object itself is created immediately, but callState will be available shortly after call creation. It is an async call.
        if callstate:
            response = get_deckstate_object(deckstate)
            response = json.loads(response.content.decode('utf-8'))
            for item in response["collection"]["items"][0]["data"]:
                if item["name"] == "level":
                    decklevel = item["value"]
                    break

        print ("Current callState=%s and deck level=%s" % (callstate, decklevel))
        if callstate == 7 or callstate == 8:
            print(response)
            break
        time.sleep(1)
    
    print ("Elevator call has finished")
