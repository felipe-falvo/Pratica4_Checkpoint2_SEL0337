import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

lendo_cartao =SimpleMFRC522()

print("Aproxime a tag")

id_cartao,texto =lendo_cartao.read()#lendo o ID e o texto da tag
print("ID: {}\nTexto: {}".format(id_cartao,texto))
