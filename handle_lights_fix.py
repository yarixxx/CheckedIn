#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import time

from satori.rtm.client import make_client, SubscriptionMode

import RPi.GPIO as GPIO

endpoint = "wss://n0cy74ab.api.satori.com"
appkey = "CF1EDbdeFC3aC712Ac8cAB5bbdDF8fdB"

# We create a subscription observer object in order to receive callbacks
# for incoming data, state changes and errors.

bathroom = 27
general = 22

def toggle_light(led_pin, status):
	print('toggle: %s %s ' % (led_pin, status))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.HIGH)
	if status:
	        GPIO.output(led_pin, GPIO.LOW)
	else:
		GPIO.output(led_pin, GPIO.HIGH)


def main():
    import logging
    logging.basicConfig(level=logging.WARNING)

    class SubscriptionObserver(object):
        def on_enter_subscribed(self):
            print('Subscribed to: lights')

        def on_subscription_data(self, pdu):
            for light in pdu['messages']:
		gLight = light['generalLight']
		bLight = light['bathroomLight']
                toggle_light(bathroom, bLight)
		toggle_light(general, gLight)

        def on_enter_failed(self, reason):
            print('Subscription failed:', reason, file=sys.stderr)

    with make_client(endpoint=endpoint, appkey=appkey) as client:
        print('Connected to Satori RTM!')

        observer = SubscriptionObserver()
        client.subscribe('channel3', SubscriptionMode.SIMPLE, observer)

        print('Press CTRL-C to exit', file=sys.stderr)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
