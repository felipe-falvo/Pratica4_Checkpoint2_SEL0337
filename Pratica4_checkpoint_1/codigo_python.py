import smbus

# barramento I2C
bus = smbus.SMBus(1)

# endereço I2C do Arduino
endereco = 0x08

while True:
    # entrada de dados no terminal
    botao = input("\nAperta 1 para acender e 0 para apagar e outro para sair: ")
    
    # se a entrada é 1, envia o byte 1 para ligar o LED
    if botao == "1":
        bus.write_byte(endereco, 1)
        
    # se a entrada é 0, envia o byte 0 para apagar o LED
    elif botao == "0":
        bus.write_byte(endereco, 0)
        
    # outro valor ou letra desliga o programa
    else:
        break
