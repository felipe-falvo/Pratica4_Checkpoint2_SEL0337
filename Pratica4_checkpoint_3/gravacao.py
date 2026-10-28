import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

lendo_cartao = SimpleMFRC522()

# gravando esse valor no cartão
texto = "12345678" 

print("Aproxime a tag")
lendo_cartao.write(texto)#gravando o texto no cartão
print("Concluido")
