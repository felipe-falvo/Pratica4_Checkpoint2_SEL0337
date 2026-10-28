import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

# limpando configuração de antes porque não estava funcionando
GPIO.cleanup()

#pinos dos leds
led_verde = 11
led_vermelho = 13

GPIO.setup(led_verde,GPIO.OUT)
GPIO.setup(led_vermelho,GPIO.OUT)

#valor do id do cartão encontrado no script de leitura
id_cartao = 497379640221  

lendo_cartao = SimpleMFRC522()

print("Aproxime a tag")

try:
    while True:
        #led começa desligado
        GPIO.output(led_verde, GPIO.LOW)
        GPIO.output(led_vermelho, GPIO.LOW)
        
        #le o cartão
        id_leitura,texto =lendo_cartao.read()
        print("ID:",id_leitura)
        
        # se for o cartão cadastrado, led verde liga
        if id_leitura == id_cartao:
            print("liberado")
            GPIO.output(led_verde, GPIO.HIGH)
        else:
        # se não for, vai ligar o led vermelho
            print("Acesso negado")
            GPIO.output(led_vermelho, GPIO.HIGH)
            
        sleep(3)

except KeyboardInterrupt:
    GPIO.cleanup()
