Este repositorio contiene códigos y librerías para implementar controladores para motor DC con microcontrolador. Los valores utilizados están calibrados segun el enconder y especificaciones técnicas del motor utilizado.

Módulos utilizados:
- Driver L298N.
- Current Sensor (Ejemplo: ACS712 / 5A)
- Hall Sensor (Encoder)

## FuzzyLib
Librería en micropython para implementar una lógica difusa. Las funciones contenidas estan diseñadas para no utlizar linspace debido al tiempo de procesamiento (mayor a 100 ms en tamaños mayores a 50 aprox) lo cual no es recomendable para control de este sistema. Por ello, se recomienda definir las funciones de membresia de entrada correctamente para que la libreria reconozca los extremos como universos correctamente.
Tomar en cuenta que en la función _Defuzzy(membership_out, universe, n)_ se está usando un linspace de tamaño _n_, por lo que hay que equilibrar entre calidad de precisión y tiempo de procesamiento (n = 50 se llega a 20 ms aprox).

```python
def Defuzzy(membership_out, universe, n):
    ...
    # Se establece la defuzificación por método de centroide
    for i in range(n):
        x = universe[0] + i * delta_x 
        
        max_value = 0.0
        
        for membresia in membership_out.values():
            mf_value = Trapzmf(x, membresia)
            max_value = max(max_value, mf_value)
        
        sumy += max_value
        sumy_x += max_value * x
    
    if sumy == 0:
        return 0.0  
    else:
        return sumy_x / sumy
```

## Próximamente
- Observador de Estados en C++ (Arduino) (en especial para sensar corriente de motor cuando el sensor no es eficiente)
- DQN (Aprendizaje por refuerzo)

## Fuentes:
- El código de PID  de Velocidad me basé en el siguiente video: https://www.youtube.com/watch?v=bl2k6eXDAGM&t=2186s&ab_channel=JesusCorrea-PLC.
- El código para la obtención de la dirección del motor me basé en la siguiente página: https://www.joober.eu/angulo-y-direccion-de-giro-mediante-encoders/
- La ecuación de diferencias para Retroalimentación de Estados lo obtuve del libro de Sistema de Control en Tiempo Discreto, Katsuhiko Ogata, Página 461 

