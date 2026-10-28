#include <Wire.h>

void setup() {
  Wire.begin(0x08);//configura o endereço do I2C
  Wire.onRequest(dados_enviados); //relacionando a função com o potenciometro
  Serial.begin(9600);}

void loop() {
  delay(100);
}

void dados_enviados() {
  int valor_potenciometro = analogRead(A0);//lendo o potenciometro
  
  byte dados[2];//criando vetor de 2 bytes
  dados[0] = highByte(valor_potenciometro);//guarda o primeiro byte
  dados[1] = lowByte(valor_potenciometro);// Armazena o byte menos significativo[cite: 196]
  
  Wire.write(dados, 2);//enviando os dois bytes
  
  Serial.print("Valor enviado: ");
  Serial.println(valor_potenciometro);}
