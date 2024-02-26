Este repositorio tiene códigos para implementar controladores para motor DC con microcontrolador. Los valores utilizados están calibrados segun el enconder y especificaciones técnicas del motor utilizado.

Módulos utilizados:
- Driver L298N.
- Currente Sensor (ACS712 / 5A)
- Hall Sensor (Encoder)

## Próximamente
- Observador de Estados en C++ (Arduino) (en especial para sensar corriente de motor cuando el sensor no es eficiente)
- Control Fuzzy (El problema de aqui es la cantidad de procesamiento matemático que ejecuta el código que hay que optimizar)


## Fuentes:
- El código de PID  de Velocidad me basé en el siguiente video: https://www.youtube.com/watch?v=bl2k6eXDAGM&t=2186s&ab_channel=JesusCorrea-PLC.
- El código para la obtención de la dirección del motor me basé en la siguiente página: https://www.joober.eu/angulo-y-direccion-de-giro-mediante-encoders/
- La ecuación de diferencias para Retroalimentación de Estados lo obtuve del libro de Sistema de Control en Tiempo Discreto, Katsuhiko Ogata, Página 461 

