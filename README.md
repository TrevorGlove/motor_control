Este repositorio tiene códigos para implementar controladores para motor DC con microcontrolador. Los valores utilizados están calibrados segun el enconder y especificaciones técnicas del motor utilizado.

Módulos utilizados:
- Driver L298N.
- Currente Sensor (ACS712 / 5A)
- Hall Sensor (Encoder)

## FuzzyLib
Librería en micropython para implementar una lógica difusa. Las funciones contenidas estan diseñadas para no utlizar linspace debido al tiempo de procesamiento (mayor a 100 ms) lo cual no es recomendable para control de estos sistemas. Por ello se recomienda definir los universos de entrada correctamente.
Tomar en cuenta que en la función _Defuzzy(membership_out, universe, n)_, si se está usando un linspace de tamaño _n_, por lo que hay que equilibrar entre calidad de precisión y tiempo de procesamiento (con valor de 50 se llega a 20 ms aprox).

## Próximamente
- Observador de Estados en C++ (Arduino) (en especial para sensar corriente de motor cuando el sensor no es eficiente)
- DQN (Aprendizaje por refuerzo)

## Fuentes:
- El código de PID  de Velocidad me basé en el siguiente video: https://www.youtube.com/watch?v=bl2k6eXDAGM&t=2186s&ab_channel=JesusCorrea-PLC.
- El código para la obtención de la dirección del motor me basé en la siguiente página: https://www.joober.eu/angulo-y-direccion-de-giro-mediante-encoders/
- La ecuación de diferencias para Retroalimentación de Estados lo obtuve del libro de Sistema de Control en Tiempo Discreto, Katsuhiko Ogata, Página 461 

