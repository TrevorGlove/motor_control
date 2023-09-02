# @TrevorGlove

from machine import Pin, ADC, Timer
from L298N import L298N

# -----Declaración de pines----

# L298N y encoder
Pin_L298N = {"IN2": 6, "IN1": 7, "ENA": 8}
Pin_Encoder = {"A": 4, "B": 5}

# Potenciómetro
PinPOT = 26

# -----Declaración de variables----

contador = 0  # Pulsos de encoder
pv = 486  # Total de pulsos por vuelta

vA1 = 0  # vA(k-1)
vB1 = 0  # vB(k-1)

dirmotor = False  # F dirección hacia atras y V dirección hacia adelante
rpm = 0  # Revoluciones por minuto

# PID
sp = 0
c = [0.0, 0.0, 0.0]  # [c, c(k-1), c(k-2)]
e = [0.0, 0.0, 0.0]  # [e, e(k-1), e(k-2)]
K = [8.05, 4.71, 0.001]  # [Kp, Ki, Kd]
Ts = 0.1

q = [K[0] + K[2] / Ts, -K[0] + K[1] * Ts - 2 * K[2] / Ts, K[2] / Ts]

# Valores auxilizares por transformacion PID de A/D
# q =  [1.458, 0.5521, -0.9039]

# -----Definición de funciones de interrupción----


def interrupcion(pin):
    global contador, vA, vA1, vA2, vB, dirmotor
    vA = A.value()  # Valor de Pin A de encoder
    if not vA1 and vA:
        vB = B.value()  # Valor de Pin B de encoder
        if vB == (False and dirmotor):
            dirmotor = False
        elif vB == (True and (not dirmotor)):
            dirmotor = True
    vA1 = vA

    contador += 1 if not dirmotor else -1


def PID(timer):
    global rpm, contador, pot, sp, c, e, pv, Ts, q
    
    rpm = int(contador * 60 / (pv * Ts))
    contador = 0

    sp = int(pot * 90 / 65535 - 45)
    e[0] = sp - rpm

    # -----Control PID----

    c[0] = c[1] + q[0] * e[0] + q[1] * e[1] + q[2] * e[2]

    c[1] = c[0]
    c[2] = c[1]
    e[1] = e[0]
    e[2] = e[1]
    
    print(("Sp", sp, "Rpm", rpm))
    
# -----Configuración de pines----

# Lectura dfel ADC
adc = ADC(PinPOT)

# Interrucpión en Pin A
A = Pin(Pin_Encoder["A"], Pin.IN)
B = Pin(Pin_Encoder["B"], Pin.IN)
A.irq(trigger=Pin.IRQ_RISING, handler=interrupcion)

# Control de motor
motor1 = L298N(Pin_L298N["IN1"], Pin_L298N["IN2"], Pin_L298N["ENA"], motor_num=1)

# Interrucpión por Timer
tim = Timer()
tim.init(period=int(Ts * 1000), mode=Timer.PERIODIC, callback=PID)

while True:
    
    pot = adc.read_u16()
    c = [min(max(value, -500), 500) for value in c]
    motor1.speed(int(c[0] * 65535 / 500))








