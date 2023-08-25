//Declarando variables

volatile int contador = 0;   //Contador de pulsos

unsigned long previousMillis = 0;  //Tiempo previo del pulso
float pot;  //Lectura de Potenciómetro
float motor; //PWM del motor
float rpm;  //Revoluciones por minuto
float sp;   //Valor del setpoint
int pv = 486; //Pulsos por vuelta de encoder 
int  dir; //Dirección del motor
int i; //Lectura de corriente
int x1; //Variable x1 de estado
int x2; //Variable x2 de estado

int e;  //r(n) = x(n)- y(n)
int e1 = 0; //e(n-1)
float v; //v(n)
float v1; //v(n-1)
float c; //c(n)

float Ki = 1;
float K1 = -0.8245;
float K2 = -8.4882;
float Ts = 0.1;


const int PinENA = 19;  //Pin ENA del L298N
const int PinIN1 = 18; //Pin IN1 del L298N
const int PinIN2 = 5; //Pin IN2 del L298N
const int PinA = 15; //pinA del encoder
const int PinB = 4; //PinB del encoder
const int PinPOT = 34; //Salida del potenciómetro (setpoint)
const int PinVol = 35; //Salida del ADC (Voltaje)
const int PinI = 32; //Salida del ADC (Corriente)


void setup() {
  Serial.begin(115200);

  pinMode(PinA,INPUT);
  pinMode(PinB,INPUT);
  pinMode(PinIN1,OUTPUT);
  pinMode(PinIN2,OUTPUT);
  pinMode(PinENA,OUTPUT);
  pinMode(PinPOT, INPUT);
  //Interrupcion externa en el Pin 15 cada flanco de subida
  attachInterrupt(digitalPinToInterrupt(PinA), interrupcion,RISING);
}


void loop() {
  unsigned long currentMillis = millis();
  if ((currentMillis - previousMillis) >= 100) {
    previousMillis = currentMillis;
    // ----- Sensar Estados -----//
    rpm = 10*contador*60/pv;
    contador = 0;
    i = analogRead(PinI); 


      // ----- Definiendo el setpoint -----//
    pot = analogRead(PinPOT); 
    sp = map(pot, 0, 4095, -45, 45); //0 - 4095 a -45 - 45 rpm
    e = sp - rpm;   // e(n) = r(n) - y(n)

    //----- Control Integral ------//  
    v = e + v1;
    v1 = v;

    //----- Retroalimentación ------//
    c = v*Ki - x1*K1 - x2*K2;
     
    x1 = rpm;
    x2 = i;
    x2 = x2/4000;
  }  

  //---- Definiendo limites del controlador ---- //
  if (c > 500) {c = 500;}
  if (c < -500) {c = -500;}
  
  motor = map(c, -500, 500, -255, 255);
  
  control_motor(motor);    //Salida de PWM de 0 a 255
  Serial.print(sp);
  Serial.print(",");
  Serial.println(rpm);//
  delay(10);
}

void interrupcion() {
  //if (digitalRead(PinB) == 1) {
  if (dir == 1) {
    contador++;    
  }
  else {
    contador--;    
  }
}

//Función de controlar motor
void control_motor(float velocidad) {
  if (velocidad > 0) {
    digitalWrite(PinIN1, LOW);
    digitalWrite(PinIN2, HIGH);
    dir = 1;
  }
  else if (velocidad < 0) {
    digitalWrite(PinIN1, HIGH);
    digitalWrite(PinIN2, LOW);
    dir = -1;
  }
  else {
    digitalWrite(PinIN1, LOW);
    digitalWrite(PinIN2, LOW);
    dir = 0;
  }
  analogWrite(PinENA, abs(velocidad));   
}
