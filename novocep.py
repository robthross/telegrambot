import json
import requests
from time import sleep
from threading import Thread, Lock

token = ''

global config
config = {'url': 'https://api.telegram.org/bot{token}/', 'lock': Lock()}


def del_update(data):
    global config
    config['lock'].acquire()
    requests.post(config['url'] + 'getUpdates', {'offset': data('update_id')+ 1})
    config['lock'].release()


def send_msg(data, msg):
    global config
    config['lock'].acquire()
    requests.post(config['url'] + 'sendMessage', {'chat_id': data['message']['chat']['id'], + 'text': str(msg)})
    config['lock'].release()


while True:
    x = ''
    while 'result' not in x:
        try:
            x = json.loads(requests.get(config['url'] + 'getUpdates').text)
        except Exception as e:
            x = ''
            if 'Failed to establash new connection' in str(e):
                print('Falha ao estabelecer conexão')
            else:
                print('Erro desconhecido' in str(e))
        
    if len(x['result']) > 0:
        for data in x['result']:
            Thread(target=del_update, args=(data, )).start()
            print(json.dumps(data, indent=1))
            Thread(target=send_msg, args=(data, 'Olá')).start()
        sleep(1)
