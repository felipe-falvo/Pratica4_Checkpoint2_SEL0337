import smbus
from time import sleep

# inicia o I2C
barramento = smbus.SMBus(1)

# configurando o endereço
endereco = 0x08

while True:
    try:
        # lendo 2 bytes do endereço
        dados =bus.read_i2c_block_data(endereco, 0, 2)
        
        # byte mais significativo
        byte_alto =dados[0]

        # byte menos significativo
        byte_baixo =dados[1]

        # coloca o byte alto para a esquerda e junta com o byte baixo
        valor_final =(byte_alto<<8) | byte_baixo
        print("Valor recebido:", valor_final)
        
    except OSError:
        # ignora algum problema de comunicação
        pass    
    sleep(0.5)
