#include <Wire.h>
#define I2C_SLAVE_ADDR 0x08//endereço I2C

void setup() {
  //inicia a biblioteca wire no I2C no endereco
  Wire.begin(I2C_SLAVE_ADDR);
  
  //função de retorno funciona ao receber dados
  Wire.onReceive(receberDados);
  
  //pino do led da placa como saida
  pinMode(LED_BUILTIN, OUTPUT);
  
  //LED começa desligado
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
}

void loop() {
}

//ligado automaticamente quando a raspberry manda bytes
//dado_byte armazena o número de bytes do barramento
void receberDados(int dado_byte) {
  while (Wire.available()) {
    // leitura do byte 
    int leitura_byte = Wire.read();
    
    Serial.print("Comando recebido: ");
    Serial.println(leitura_byte);
    
    //a ideia é que quando for 1, o led liga e quando for 0 desliga
    if (leitura_byte==1) {
      digitalWrite(LED_BUILTIN, HIGH);} 
      
    else if (leitura_byte == 0) {
      digitalWrite(LED_BUILTIN, LOW);}
  }
}
