import RPi.GPIO as gpio
import time as delay
from urllib.request import urlopen
import requests

urlBase = 'https://api.thingspeak.com/channels/'
readKey = '/last?key=EPU1LWLGRPCX2JSG'
channels = '2746109'
field1 = '/fields/1/'


def testaConexao():
    try:
        urlopen('https://www.materdei.edu.br/pt', timeout=1)
        return True
    except:
        return False

if testaConexao() == True:
    print('Conexão OK')

    while True:
        consultaDistancia = requests.get(urlBase + channels + field1 + readKey)

        print(consultaDistancia.text)
        delay.sleep(20)
else:
    print('Sem conexão com a INTERNET')