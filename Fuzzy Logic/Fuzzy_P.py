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

# Pin Serial ADC
PinSerial = 28

# -----Declaración de variables----

contador = 0   # Pulsos de encoder (para velocidad)
contadorp = 0  # Pulsos de encodor (para posición)
pv = 486       # Total de pulsos por vuelta

vA1 = 0        # vA(k-1)
vB1 = 0        # vB(k-1)

dirmotor = False  # F dirección hacia atras y V dirección hacia adelante
gr = 0         # Grados de giro del motor

# Fuzzy

x = (0, 0)  # (error, velocidad)

e_u = (-500, 500)        # Universo de error (grados)
v_u = (-500, 500)        # Universo de Velocidad (grados/s)
dc_u = (-65535, 65535)   # Universo de Data cycle (bits)

# Funciones de membresía de entrada

ENL = (-500, -500, -300, -15)  # Error Negativo Lejano
ENC = (-300, -50, 0)           # Error Negativo Cercano
E0 = (-1, 0, 1)                # Error Cero
EPC = (0, 50, 300)             # Error Positivo Cercano
EPL = (15, 300, 500, 500)      # Error Positivo Lejano

E = [ENL, ENC, E0, EPC, EPL]

VN = (-500, -500, -100, -1)  # Velocidad Negativo
V0 = (-2, 0, 2)              # Velocidad Cero
VP = (1, 100, 500, 500)      # Velocidad Positivo
V = [VN, V0, VP]


# Funciones de membresía de salida

DNA = (-65535, -65535, -43690, -500)   # Data cycle Alto Negativo
DNB = (-10000, -500, 1000)                # Data cycle Bajo Negativo
D0 = (-500, 0, 500)                      # Data cycle Cero
DPB = (100, 500, 10000)                  # Data cycle Bajo Positivo
DPA = (500, 43690, 65535, 65535)       # Data cycle Alto Positivo

DC = [DNA, DNB, D0, DPB, DPA]

# Reglas Difusas

R = [(ENL, VN, DNA),    # r1
     (ENL, V0, DNA),    # r2
     (ENL, VP, DNA),    # r3
     (ENC, VN, DNB),    # r4
     (ENC, V0, DNB),    # r5
     (ENC, VP, DNB),    # r6
     ( E0, VN, DPB),    # r7
     ( E0, V0,  D0),    # r8
     ( E0, VP, DNB),    # r9
     (EPC, VN, DPB),    # r10
     (EPC, V0, DPB),    # r11
     (EPC, VP, DPB),    # r12
     (EPL, VN, DPA),    # r13
     (EPL, V0, DPA),    # r14
     (EPL, VP, DPA)]    # r15

# Variables de Control

sp = 0     # Setpoint (grados)
c = 0.0    # Variable de Control (bits)
e = 0.0    # Error (grados)
Ts = 0.1

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
    global gr, contador, pot, sp, c, e, pv, Ts, x, dc_u

    # -----Valores para Vector de entradas------
    gr += contador*360/pv           # Posición
    vl = contador*360/(pv*Ts)       # Velocidad
    contador = 0
    sp = pot*540/65535 - 270        # Setpoint
    e = sp - gr                     # Error

    # -----Fuzzy Control------
    
    print(("Sp", int(sp), "Gr", int(gr)))    
    
    x = (e, vl)                        # Vector de Entrada
    Val = Fuzzy(R, x, (E, V))          # Fuzzificación
    Lines_cut = Proyect(Val)           # Proyecciòn de valores en U. de Velocidad
    Trapezoids = Cut(Lines_cut, Val)   # Func. de membresia cortadas
    c = Defuzzy(Trapezoids, dc_u, 40)  # Defuzzificación


# -----Configuración de pines----

# Lectura dfel ADC
adc = ADC(PinSerial)

# Interrupción en Pin A
A = Pin(Pin_Encoder['A'], Pin.IN)
B = Pin(Pin_Encoder['B'], Pin.IN)
A.irq(trigger=Pin.IRQ_RISING, handler=interrupcion)

# Control de motor
motor1 = L298N(Pin_L298N['IN1'], Pin_L298N['IN2'], Pin_L298N['ENA'])

# Interrucpión por Timer
tim = Timer()
tim.init(period=int(Ts * 1000), mode=Timer.PERIODIC, callback=Fuzzyficator)


while True:
    pot = adc.read_u16()
    motor1.speed(c)


