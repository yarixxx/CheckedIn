import RPi.GPIO as GPIO
from satori.rtm.client import make_client
from satori.rtm.client import *

endpoint = "wss://n0cy74ab.api.satori.com"
appkey = "CF1EDbdeFC3aC712Ac8cAB5bbdDF8fdB"

# We create a subscription observer object in order to receive callbacks
# for incoming data, state changes and errors.

def switch_on_pin(led_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.output(led_pin, GPIO.LOW)

 
class SubscriptionObserver(object):
 
    # Called when the subscription is established.
    def on_enter_subscribed(self):
        print('Subscribed to the channel')
 
    # This callback allows us to observe incoming messages
    def on_subscription_data(self, data):
        for message in data['messages']:
            print('Animal is received:', message)
 
    def on_enter_failed(self, reason):
        print('Subscription failed, reason:', reason)
        sys.exit(1)
 
 
subscription_observer = SubscriptionObserver()
 
# Send subscribe request. This call is asynchronous:
# client implementation internally queues the request and lets the
# function exit. Request is then processed from a background thread,
# while our main thiread goes on.


with make_client(endpoint=endpoint, appkey=appkey) as client:
	client.subscribe('channel3', SubscriptionMode.SIMPLE, subscription_observer)

while True:
	print '1'
	
