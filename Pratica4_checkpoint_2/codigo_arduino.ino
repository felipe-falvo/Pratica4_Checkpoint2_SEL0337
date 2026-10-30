#include <Wire.h>

void setup() {
  Wire.begin(0x08);//endereço
  Wire.onRequest(dados_enviados); //função com o potenciometro
  Serial.begin(9600);}

void loop() {
  delay(100);
}

void dados_enviados() {
  int valor_potenciometro = analogRead(A0);//lendo o potenciometro
  
  byte dados[2];//vetor de 2 bytes
  dados[0] =highByte(valor_potenciometro);//guarda o primeiro byte
  dados[1] =lowByte(valor_potenciometro);//guarda byte menos significativo
  
  Wire.write(dados, 2);//enviando os dois bytes
  
  Serial.print("Valor enviado: ");
  Serial.println(valor_potenciometro);}
