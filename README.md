# SEL0337 — Projetos em Sistemas Embarcados

## Prática 4

**Autores:**
- Felipe Assis Bernardes Falvo — Nº USP: 15004433
- Kayke Malaquias Gregorio — Nº USP: 15651561

---

# 1. Introdução

Essa prática tem como foco entender os protocolos de comunicação utilizados em sistemas embarcados.

O projeto utiliza uma Raspberry Pi que executa programas em Python, e um Arduino Uno, que executa programas e permite realizar operações de baixo nível, como aquisição de sinais analógicos e controle.

A atividade é dividida em três checkpoints:

- **Checkpoint 1: Comunicação I2C:** comunicação entre Raspberry Pi e Arduino para controlar o LED do microcontrolador.
- **Checkpoint 2: Aquisição analógica:** leitura de um potenciômetro pelo Arduino e transmissão do valor para a Raspberry Pi por I2C.
- **Checkpoint 3: RFID e SPI:** desenvolvimento de um sistema de controle de acesso utilizando um leitor RFID.

---

# 2. Checkpoint 1

## 2.1. Objetivo

Estabelecer uma comunicação serial entre o Raspberry Pi e o Arduino Uno utilizando a comunicação I2C.

A Raspberry Pi envia comandos pelo terminal, e o Arduino interpreta os valores recebidos para controlar o LED interno da placa. Dessa forma, o funcionamento da comunicação pode ser verificado tanto pelo LED, quanto pelo Monitor Serial do Arduino.

## 2.2. Funcionamento

A comunicação é dividida entre duas plataformas:

- **Raspberry Pi:** atua como controlador, iniciando a comunicação e enviando os comandos utilizando a biblioteca `SMBus`.
- **Arduino Uno:** atua como dispositivo controlado, recebendo os comandos pela biblioteca `Wire`, interpretando os valores e alterando o estado do LED interno.

O endereço I2C configurado no Arduino é `0x08`.

O funcionamento esperado é:

* **Digitar `1`:** O Arduino acende o LED interno (`LED_BUILTIN`).
* **Digitar `0`:** O Arduino apaga o LED interno (`LED_BUILTIN`).
* **Digitar qualquer outro valor:** O programa é encerrado.

Quando recebe um comando, o Arduino também mostra seu valor no Monitor Serial.

## 2.3. Protocolo I2C

O I2C é um protocolo de comunicação serial síncrona que utiliza duas linhas:

- **SDA (Data):** transmissão dos dados.
- **SCL (Clock):** clock utilizado para sincronizar a comunicação.

A Raspberry Pi inicia as transferências, enquanto o Arduino responde no endereço configurado.

## 2.4. Hardware

Como a Raspberry Pi utiliza níveis lógicos de 3,3 V e o Arduino Uno utiliza 5 V, foi utilizado um conversor de nível lógico bidirecional para adaptar os sinais do barramento e proteger as GPIOs da Raspberry Pi.

- **Alimentação de baixa tensão:** Conecta o Pino 1 da Raspberry Pi (3,3 V) ao pino **LV** do conversor.
- **Alimentação de alta tensão:** Conecta o pino 5V do Arduino Uno ao pino **HV** do conversor.
- **Referência:** Conecta o GND da Raspberry Pi e o GND do Arduino ao pino **GND** comum do conversor.
- **Barramento SDA:** Conecta a GPIO 2 da Raspberry Pi ao pino **LV3** e o pino A4 do Arduino ao pino **HV3**.
- **Barramento SCL:** Conecta a GPIO 3 da Raspberry Pi ao pino **LV4** e o pino A5 do Arduino ao pino **HV4**.


## 2.5. Arquivos do checkpoint

- [`arduino.ino`](Pratica4_checkpoint_1/arduino.ino): código do Arduino, responsável por configurar o endereço I2C, receber os comandos e controlar o LED.
- [`codigo_python.py`](Pratica4_checkpoint_1/codigo_python.py): código Python executado na Raspberry Pi, responsável por ler os comandos do usuário e enviar para o Arduino.
- [`hardware.jpeg`](Pratica4_checkpoint_1/hardware.jpeg): foto da montagem.
- [`video_prova.mp4`](Pratica4_checkpoint_1/video_prova.mp4): vídeo de demonstração do funcionamento.

## 2.6. Configuração e execução

Primeiramente, é necessário habilitar a interface I2C na Raspberry Pi:

```bash
sudo raspi-config
```

No menu, acessar:

`Interface Options → I2C → Enable`

Em seguida, verificar se o Arduino está sendo detectado no barramento:

```bash
sudo i2cdetect -y 1
```

O dispositivo deverá aparecer no endereço `0x08`.

Após gravar o programa no Arduino e conectar a montagem, abrir o Monitor Serial. No terminal da Raspberry Pi, executar:

```bash
python3 codigo_python.py
```

Os comandos `1` e `0` devem acender e apagar o LED, respectivamente. Qualquer outro valor desliga o programa.

## 2.7. Demonstração

**Montagem física:**

![Montagem física do Checkpoint 1](Pratica4_checkpoint_1/hardware.jpeg)

**Vídeo de demonstração:** [Assistir ao vídeo do Checkpoint 1](Pratica4_checkpoint_1/video_prova.mp4).

---

# 3. Checkpoint 2

## 3.1. Objetivo

Nesse segundo checkpoint a ideia é obter informação por meio da leitura analógica de um potenciômetro.

Assim, o Arduino realiza a aquisição do sinal, organiza o valor e envia os dados pelo barramento I2C. A Raspberry Pi recebe os bytes e reconstrói o valor.

## 3.2. Aquisição

O potenciômetro é ligado a uma entrada analógica do Arduino Uno. Seu terminal é conectado ao pino `A0`, enquanto os outros terminais são conectados à alimentação e ao GND.

Ao girar o potenciômetro, a tensão aplicada à entrada analógica varia entre 0 e 5 V.

O conversor analógico-digital (ADC) de 10 bits do Arduino transforma essa tensão em um valor digital entre 0 e 1023.

| Tensão aproximada | Leitura digital |
|---|---:|
| 0 V | 0 |
| 2,5 V | 512, aproximadamente |
| 5 V | 1023 |

Esses valores são aproximados e dependem da tensão de referência e das condições do circuito.

## 3.3. Transmissão de dados de 10 bits

O barramento I2C transmite dados em unidades de 8 bits, enquanto a leitura do ADC do Arduino possui 10 bits.

Por isso, um único byte não é suficiente para representar todos os valores possíveis do potenciômetro. Para preservar a informação, o valor é dividido em dois bytes:

- **Byte alto:** contém os bits mais significativos.
- **Byte baixo:** contém os bits menos significativos.

No Arduino, as funções `highByte()` e `lowByte()` separam essas partes do valor original.

```cpp
byte dados[2];

dados[0] = highByte(valor_potenciometro);
dados[1] = lowByte(valor_potenciometro);

Wire.write(dados, 2);
```

O Arduino envia os dois bytes quando a Raspberry Pi solicita os dados por I2C.

Na Raspberry Pi, os bytes recebidos são combinados utilizando deslocamento de bits e a operação OR:

```python
valor_final = (byte_alto << 8) | byte_baixo
```

A operação `<< 8` desloca o byte alto oito posições para a esquerda, enquanto `|` combina os bits das duas partes. Dessa forma, é possível reconstruir o valor original de 10 bits.

## 3.4. Funcionamento dos programas

### Programa do Arduino

O arquivo `codigo_arduino.ino` utiliza a biblioteca `Wire` para configurar o dispositivo no endereço `0x08`.

A função `Wire.onRequest()` registra a função que será executada quando a Raspberry Pi solicitar os dados. Nessa função, o Arduino:

1. Lê o valor analógico do pino `A0` por meio de `analogRead()`.
2. Separa o valor em dois bytes utilizando `highByte()` e `lowByte()`.
3. Envia os bytes pelo barramento I2C com `Wire.write()`.
4. Exibe o valor original no Monitor Serial.

A comunicação serial é configurada para 9600 baud, permitindo acompanhar os valores enviados.

### Programa da Raspberry Pi

O arquivo `codigo_python.py` utiliza a biblioteca `SMBus` para acessar o barramento I2C número 1.

O programa solicita os dados ao Arduino, separa os bytes recebidos e reconstrói o valor original. O resultado é exibido no terminal da Raspberry Pi, permitindo compará-lo com a leitura apresentada no Monitor Serial do Arduino.

O intervalo de 0,5 segundo entre as leituras permite acompanhar as mudanças de posição do potenciômetro.

## 3.5. Arquivos do checkpoint

- [`codigo_arduino.ino`](Pratica4_checkpoint_2/codigo_arduino.ino): realiza a leitura do potenciômetro, separa o valor em dois bytes e transmite os dados por I2C.
- [`codigo_python.py`](Pratica4_checkpoint_2/codigo_python.py): solicita os dados, reconstrói o valor de 10 bits e apresenta o resultado no terminal.
- [`hardware.jpeg`](Pratica4_checkpoint_2/hardware.jpeg): fotografia da montagem física.
- [`video_prova.mp4`](Pratica4_checkpoint_2/video_prova.mp4): vídeo de demonstração.

## 3.6. Execução e validação

Com o Arduino programado e conectado à Raspberry Pi, executar o programa Python:

```bash
python3 codigo_python.py
```

Girar o potenciômetro e observar os valores apresentados nos dois terminais.

A validação deve confirmar que:

- A leitura do potenciômetro varia de acordo com sua posição.
- O Arduino envia os dados solicitados pela Raspberry Pi.
- Os dois bytes são interpretados na ordem correta.
- O valor reconstruído permanece na faixa de 0 a 1023.
- O valor apresentado pela Raspberry Pi corresponde ao valor lido pelo Arduino.

**Observação sobre a implementação:** no código Python utilizado, a variável que representa o barramento foi criada com o nome `barramento`. Portanto, a chamada de leitura deve utilizar esse mesmo nome. Além disso, o método `read_i2c_block_data()` segue as convenções de leitura em bloco SMBus, que precisam ser compatíveis com o formato de resposta enviado pelo Arduino. Caso a leitura não corresponda aos dois bytes enviados, será necessário ajustar o método de leitura ou o formato da resposta para garantir a reconstrução correta.

## 3.7. Demonstração

**Montagem física:**

![Montagem física do Checkpoint 2](Pratica4_checkpoint_2/hardware.jpeg)

**Vídeo de demonstração:** [Assistir ao vídeo do Checkpoint 2](Pratica4_checkpoint_2/video_prova.mp4).

---

# 4. Checkpoint 3

## 4.1. Objetivo

Nesse terceiro checkpoint, a ideia é  utilizar um leitor RFID MFRC522 conectado à Raspberry Pi, no qual o sistema identifica as tags aproximadas do leitor e verifica se a identificação é o cartão autorizado.

## 4.2. RFID e comunicação SPI

RFID (Radio-Frequency Identification) é uma ferramente que identifica objetos por radiofrequência, no qual o leitor estabelece comunicação com uma tag e obtém informações de identificação e pode armazenar dados dentro dela.

O SPI é um protocolo serial síncrono que utiliza linhas para as funções de comunicação:

- **MOSI:** transmissão de dados do controlador para o dispositivo controlado.
- **MISO:** transmissão de dados do dispositivo controlado para o controlador.
- **SCK:** sinal de clock.
- **SS/CS:** seleção do dispositivo.

## 4.3. Funcionamento do sistema

O script está dividido em três códigos.

### Gravação da tag — `gravacao.py`

O programa utiliza a classe `SimpleMFRC522` para inicializar o leitor RFID e gravar o texto definido na variável `texto`.

Na implementação, o texto utilizado é:

```python
texto = "12345678"
```

Após iniciar o programa, é aproximado a tag do leitor. O conteúdo é gravado e o terminal mostra se a operação foi concluída.

### Leitura da tag — `leitura.py`

O programa inicializa o leitor e aguarda a aproximação de uma tag.

A função `read()` retorna:

- **ID:** identificador da tag.
- **Texto:** conteúdo armazenado na tag.

### Controle de acesso — `controle.py`

O programa utiliza o identificador de uma tag cadastrada para decidir se o acesso será liberado.

A tag autorizada é definida pela variável:

```python
id_cartao = 497379640221
```

O programa usa dois LEDs para indicar o resultado:

- **led verde:** indica que o cartão está autorizado.
- **led vermelho:** indica que o cartão não está cadastrado.

A cada leitura, os dois leds são inicialmente apagados. Em seguida, o ID obtido é comparado com o identificador autorizado, onde se os valores forem iguais, o terminal apresenta a mensagem de liberação e o led verde é aceso. Caso contrário, o terminal mostra que o acesso foi negado e o led vermelho é ligado.

## 4.4. Arquivos do checkpoint

- [`gravacao.py`](Pratica4_checkpoint_3/gravacao.py): grava um texto na tag RFID.
- [`leitura.py`](Pratica4_checkpoint_3/leitura.py): le o identificador e o conteúdo da tag.
- [`controle.py`](Pratica4_checkpoint_3/controle.py): verifica se a tag está autorizada e controla os leds.
- [`video_prova.mp4`](Pratica4_checkpoint_3/video_prova.mp4): vídeo de demonstração.

## 4.5. Configuração e execução

Antes de executar os programas, é necessário habilitar a interface SPI na Raspberry Pi:

```bash
sudo raspi-config
```

Acessar:

`Interface Options → SPI → Enable`

Instalar a biblioteca, caso ainda não esteja instalada:

```bash
pip3 install mfrc522
```

## 4.6 Mapeamento de Conexões
* **SDA/SS:** Conecta o pino SDA do módulo RFID à GPIO 8 da Raspberry Pi.
* **SCK:** Conecta o pino SCK do módulo RFID à GPIO 11 da Raspberry Pi.
* **MOSI:** Conecta o pino MOSI do módulo RFID à GPIO 10 da Raspberry Pi.
* **MISO:** Conecta o pino MISO do módulo RFID à GPIO 9 da Raspberry Pi.
* **RST:** Conecta o pino RST (reset) do módulo RFID à GPIO 25 da Raspberry Pi.
* **GND:** Conecta o pino GND do módulo RFID ao GND da Raspberry Pi.
* **3.3V:** Conecta o pino de alimentação do módulo RFID à saída de 3,3 V da Raspberry Pi.
* **IRQ:** Pino de interrupção que permanece não utilizado.

### Etapa 1 — Gravar a tag

Executar:

```bash
python3 gravacao.py
```

Aproximar a tag do leitor e aguardar a confirmação da gravação.

### Etapa 2 — Identificar a tag

Executar:

```bash
python3 leitura.py
```

Aproximar a mesma tag e pegar o ID mostrado no terminal.

### Etapa 3 — Testar o controle

Verificar se o ID mostrado é o valor configurado na variável `id_cartao` do arquivo `controle.py`, se não, atualizar a variável e executar:

```bash
python3 controle.py
```

Aproximar uma tag cadastrada e, em seguida, uma tag diferente para verificar os acessos liberado e negado.


## 4.7. Demonstração

**Vídeo de demonstração:** [Assistir ao vídeo do Checkpoint 3](Pratica4_checkpoint_3/video_prova.mp4).
