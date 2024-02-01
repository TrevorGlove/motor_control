Los códigos de control estan calibrados para un motor de 12V 130RPM. Para otros valores de motor se debe experimentar con los resultados.

Módulos utilizados:
- Driver L298N.
- Sensor ACS712 (se recomienda 5A)
- Sensor FZ0430.
- 
Retroalimentación de Estados: Se debe realizar un modelo en espacio de estados para determinar las ganancias de retroalimentación.

# Control-de-motor-DC-(C++)
Control PID y Control por Retroalimentación de Estados de Velocidad y Posición en lenguaje C++ para Arduino IDE.
Los pines estan configurados para ESP32. 

# Control-de-motor-DC-(Micropython)
Control PID de Estados de Velocidad y Posición en micropython.
Los pines estan configurados para Raspberrry Pi Pico.

# Próximamente
- Observador de Estados en C++ (en especial para sensar voltaje de motor ya que el modulo sensor no es eficiente por polaridad)
- Control Fuzzy en micropython (El problema de aqui es la cantidad de procesamiento matemático que ejecuta el código que hay que optimizar)


# Fuentes:
El código de PID  de Velocidad me basé en el siguiente video: https://www.youtube.com/watch?v=bl2k6eXDAGM&t=2186s&ab_channel=JesusCorrea-PLC.
El código para la obtención de la dirección del motor me basé en la siguiente página: https://www.joober.eu/angulo-y-direccion-de-giro-mediante-encoders/
La ecuación de diferencias para Retroaleimentación de Estados lo obtuve del libro de Sistema de Control en Tiempo Discreto, Katsuhiko Ogata, Página 461 

