import time

from satori.rtm.client import make_client

endpoint = "wss://n0cy74ab.api.satori.com"
appkey = "CF1EDbdeFC3aC712Ac8cAB5bbdDF8fdB"

def main():

    with make_client(endpoint=endpoint, appkey=appkey) as client:
        print('Connected to Satori RTM!')

        while True:

            def on_publish_ack(pdu):
                if pdu['action'] == 'rtm/publish/ok':
                    print('Publish confirmed')
                else:
                    print(
                        'Failed to publish. '
                        'RTM replied with the error {0}: {1}'.format(
                            pdu['body']['error'], pdu['body']['reason']))

            message = {"building": 1234, 'user': 'mac'}
            client.publish(u"checkins", message, callback=on_publish_ack)

            time.sleep(1)


if __name__ == '__main__':
  main()
