// @TrevorGuante

//Declarando variables

volatile int contador = 0;   //Contador de pulsos

unsigned long previousMillis = 0;  //Tiempo previo del pulso
float pot;  //Lectura de Potenciómetro
float motor; //PWM del motor
float gr; //Posición del motor en grados
float sp;   //Valor del setpoint
int pv = 486; //Pulsos por vuelta de encoder
int  dir; //Dirección del motor

float c; //c(n)
float c1; //c(n-1)
float c2; //c(n-2)
float e; //e(n)
float e1; //e(n-1)
float e2; //e(n-2)

float Kp = 6;
float Ki = 1;
float Kd = 1;
float Ts = 0.1;

//PID
//float q0 = Kp + Kd/Ts;
//float q1 = -Kp+ Ki*Ts - 2*Kd/Ts;
//float q2 = Kd/Ts;

//PD
//float q0 = Kp + Kd/Ts;
//float q1 = -Kd/Ts;

//PI
//float q0 = Kp;
//float q1 = -Kp+Ki*Ts;

//Tambien se puede usar valores auxiliares

const int PinENA = 19;  //Pin ENA del L298N
const int PinIN1 = 18; //Pin IN1 del L298N
const int PinIN2 = 5; //Pin IN2 del L298N
const int PinA = 15; //pinA del encoder
const int PinB = 2; //PinB del encoder
const int PinPOT = 34; //Salida del potenciómetro  

void setup(){
  Serial.begin(115200);
  pinMode(PinA,INPUT);
  pinMode(PinB,INPUT);
  pinMode(PinIN1,OUTPUT);
  pinMode(PinIN2,OUTPUT);
  pinMode(PinENA,OUTPUT);
  //Interrupcion externa en el Pin 15 cada flanco de subida
  attachInterrupt(PinA, interrupcion, RISING);
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= 100) {
    previousMillis = currentMillis;
    gr = contador * 360.0 / pv;

    // ----- Definiendo el setpoint -----//
    
    pot = analogRead(PinPOT);
    sp = map(pot,0, 4095,-360, 360);
    e = sp - gr;

    //----- Control PID ------//

    
    c = c1 + q0*e + q1*e1 + q2*e2;
    //PD 
    //c = q0*e + q1*e1;
    //PI 
    //c = c1 + q0*e + q1*e1;
    
    c1 = c;
    c2 = c1;
    e1 = e;
    e2 = e1;
  }

  //---- Definiendo limites del controlador ---- //
  if (c > 500) {c = 500;}
  if (c < -500) {c = -500;}
    
  motor = map(c, -500, 500, -255, 255);
    
  control_motor(motor);
    
  Serial.print(sp);
  Serial.print(",");
  Serial.println(gr);
  delay(1);
}


void interrupcion() {
  //if (digitalRead(PinB) == 1) {contador++;}
  if (dir == HIGH) {contador++;}
  else {contador--;}
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
