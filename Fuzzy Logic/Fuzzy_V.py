"""
@TrevorGlove https://github.com/TrevorGlove/motor_control
Elaborado para Raspberry Pi Pico
"""

from machine import Pin, ADC, Timer
from L298N import L298N
from FuzzyLib import Fuzzy, Cut, Proyect, Defuzzy

# -----Declaración de pines----

# L298N y encoder
Pin_L298N = {'IN2': 6, 'IN1': 7, 'ENA': 8}
Pin_Encoder = {'A': 4, 'B': 5}

# Potenciómetro
PinPOT = 28

# -----Declaración de variables----

contador = 0   # Pulsos de encoder
pv = 486       # Total de pulsos por vuelta

vA1 = 0        # vA(k-1)
vB1 = 0        # vB(k-1)

dirmotor = False  # F dirección hacia atras y V dirección hacia adelante
rpm = 0         # Revoluciones por Minuto
ac = 0

# Fuzzy

x = (0, 0)  # (error derivado, error)

ed_u = (-50, 50)   # Universo de error derivado 
e_u = (-100, 100)    # Universo de error
dc_u = (-50000, 50000)   # Universo de Data cycle

# Funciones de membresía de entrada

EDN = (-50, -50, -30, -1)   # Error Derivado Negativo Alto
ED0 = (-2, 0, 2)            # Error Derivado Cero
EDP = (1, 30, 50, 50)       # Error Derivado Positivo Alto

EDC = [EDN, ED0, EDP]

ENL = (-100, -100, -60, -30)  # Error Negativo Lejano
ENC = (-60, -30, -1)           # Error Negativo Cercano
E0 = (-5, 0, 5)            # Error Cero
EPC = (1, 30, 60)             # Error Positivo Cercano
EPL = (30, 60, 100, 100)     # Error Positivo Lejano

E = [ENL, ENC, E0, EPC, EPL]

# Funciones de membresía de salida

DAN = (-50000, -50000, -40000, -20000)   # Data cycle Alta Negativa
DBN = (-8000, -2000, 0)                # Data cycle Baja Negativa
D0 = (-100, 0, 100)                  # Data cycle Cero
DBP = (0, 2000, 8000)                  # Data cycle Baja Negativa
DAP = (20000, 40000, 50000, 50000)       # Data cycle Alta Positiva

DC = [DAN, DBN, D0, DBP, DAP]

# Reglas Difusas

R = [(EDN, ENL, DAN),
     (ED0, ENL, DAN),     
     (EDP, ENL, DAN),  
     (EDN, ENC, DBN),
     (ED0, ENC, DBN),    
     (EDP, ENC, DBN),
     (EDN,  E0, DBN),
     (ED0,  E0,  D0),
     (EDP,  E0, DBP),
     (EDN, EPC, DBP),
     (ED0, EPC, DBP),
     (EDP, EPC, DBP),    
     (EDN, EPL, DAP),
     (ED0, EPL, DAP),
     (EDP, EPL, DAP)]

# Variables de Control

sp = 0     # Setpoint
c = 0.0    # Variables de Control
e = [0, 0]    # Error [e(k), e(k-1)] 
pwm = 0.0  # PWM actual
Ts = 0.1

# Filtro
af = [1.0000, -1.6475, 0.7009]
bf = [0.0134,  0.0267,  0.0134]
sint = [0, 0, 0, 0]
sout = [0, 0, 0, 0]

# -----Definición de funciones de interrupción----

def interrupcion(pin):
    global contador, vA, vA1, vA2, vB, dirmotor
    vA = A.value()        # Valor de Pin A de encoder
    if not vA1 and vA:
        vB = B.value()    # Valor de Pin B de encoder
        if vB == (False and dirmotor):
            dirmotor = False
        elif vB == (True and (not dirmotor)):
            dirmotor = True
    vA1 = vA

    contador += 1 if not dirmotor else -1

def Fuzzyficator(timer):
    global rpm, contador, pot, sp, c, e, pv, Ts, x, dc_u, pwm, af, bf, sint, sout, ac

    # -----Valores para Vector de entradas------

    sint[0] = int(contador * 60 / (pv * Ts))   # Velocidad
    contador = 0
    
    sout[0] = - af[1]*sout[1] - af[2]*sout[2] + bf[0]*sint[0] + bf[1]*sint[1] + bf[2]*sint[2]
    
    sint[1] = sint[0]
    sint[2] = sint[1]    
    sout[1] = sout[0]
    sout[2] = sout[1]
    
    sp = int(pot * 180 / 65535 - 90)        # Setpoint
    e[0] = sp - sint[0]                           # Error
    ac = (e[0] - e[1])/Ts
    
    e[1] = e[0] 
    
    # -----Fuzzy Control------

    x = (ac, e[0])                        # Vector de Entrada
    Val = Fuzzy(R, x, (EDC, E))         # Fuzzificación
    Lines_cut = Proyect(Val)           # Proyecciòn de valores en U. de Velocidad
    Trapezoids = Cut(Lines_cut, Val)   # Func. de membresia cortadas
    c = Defuzzy(Trapezoids, dc_u, 50)  # Defuzzificación

    pwm += c*Ts

    print(("Sp", int(sp), "Rpm", int(sint[0] )))

# -----Configuración de pines----

# Lectura dfel ADC
adc = ADC(PinPOT)

# Interrupción en Pin A
A = Pin(Pin_Encoder['A'], Pin.IN)
B = Pin(Pin_Encoder['B'], Pin.IN)
A.irq(trigger=Pin.IRQ_RISING, handler=interrupcion)

# Control de motor
motor1 = L298N(Pin_L298N['IN1'], Pin_L298N['IN2'], Pin_L298N['ENA'], motor_num=1)

# Interrucpión por Timer
tim = Timer()
tim.init(period=int(Ts * 1000), mode=Timer.PERIODIC, callback=Fuzzyficator)


while True:

    pot = adc.read_u16()
    motor1.speed(pwm)


