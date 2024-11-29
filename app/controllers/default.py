import RPi.GPIO as gpio
import time as delay
from app import app
from flask import render_template, jsonify
import requests
from urllib.request import urlopen

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

ledVermelho, ledVerde = 11, 12

statusVermelho = ""
statusVerde = ""
isEmpty = False
pin_t = 15
pin_e = 16
lixeira_v = 20
 
urlBase = 'https://api.thingspeak.com/update?api_key=BHLWH975A4RASC6G&'
field1 = 'field1='
field2 = 'field2='

gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)

gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)

gpio.output(ledVermelho, gpio.LOW)
gpio.output(ledVerde, gpio.LOW)

def distancia():
    gpio.output(pin_t, True)
    delay.sleep(0.000001)
    gpio.output(pin_t, False)
    tempo_i = delay.time()
    tempo_f = delay.time()
    while gpio.input(pin_e) == False:
        tempo_i = delay.time()
    while gpio.input(pin_e) == True:
        tempo_f = delay.time()
    temp_d = tempo_f - tempo_i
    distancia = (temp_d*34300) / 2
    return distancia

def isEmpty(distancia):
    valorRecebido = distancia

    print("Distancia = %.1f CM" % valorRecebido)
    espaco_d = (valorRecebido/lixeira_v)*100

    print("Espaço disponível = %.1f" % espaco_d, '%' )
    espaco_o = 100 - espaco_d
    
    print("Espaço ocupado = %.1f" % espaco_o, '%')

    if espaco_d > 15:
        return False
    else:
        return True

def ocupacaoLixeira():
    valorRecebido = distancia()
    espaco_d = (valorRecebido/lixeira_v)*100
    espaco_o = 100 - espaco_d

    espaco_o = round(espaco_o)
    print(espaco_o)
    return espaco_o

def enviarStatusLixeira (statusLixeira, ocupacao=None):
    urlDados = (urlBase + field2 + statusLixeira + '&' + field1 + str(ocupacao))
    print(urlDados)
    retorno = requests.get(urlDados)
    if retorno.status_code == 200:
        print('Dados envidados com sucesso')
    else:
        print('Erro ao enviar dados: '+ retorno.status_code)
        delay.sleep(20)

@app.route("/")
def index():
    templateData = {
        'ocupacaoo': ocupacaoLixeira(),
        'ocupacaoWidth': '=width:'+ str(ocupacaoLixeira()) +'%;'
    }
    return render_template('index.html', **templateData)

@app.route("/lixeira/<action>")
def lixeira(action):
    templateData = {
        'ocupacaoo': ocupacaoLixeira(),
        'ocupacaoWidth': '=width:'+ str(ocupacaoLixeira()) +'%;'
    }
    if action == 'abrir':
        print(distancia())
        enviarStatusLixeira('Tampa Aberta', 'null')

        distancia_real = distancia()

        if isEmpty(distancia_real):
            for i in range(3):
                gpio.output(ledVermelho, gpio.LOW)
                gpio.output(ledVerde, gpio.HIGH)
                delay.sleep(0.5)

                gpio.output(ledVerde, gpio.LOW)
                delay.sleep(0.5)

        else:
            for i in range(3):
                gpio.output(ledVerde, gpio.LOW)
                gpio.output(ledVermelho, gpio.HIGH)
                delay.sleep(0.5)

                gpio.output(ledVermelho, gpio.LOW)
                delay.sleep(0.5)

        if isEmpty(distancia_real):
            gpio.output(ledVerde, gpio.HIGH)
            gpio.output(ledVermelho, gpio.LOW)
        else:
            gpio.output(ledVermelho, gpio.HIGH)
            gpio.output(ledVerde, gpio.LOW)
        


        
    if action == 'fechar':
        distancia_real= distancia()
        enviarStatusLixeira('Tampa Fechada',distancia_real)
        
    return render_template('index.html', **templateData)