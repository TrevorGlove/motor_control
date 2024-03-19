from machine import Pin, PWM

class L298N:
    def __init__(self, in1_pin, in2_pin, ena_pin):
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.ena = Pin(ena_pin, Pin.OUT)
        
        self.pwm = PWM(self.ena)
        
        self.speed(0)
    
    def speed(self, value):
        
        if value < 0:
            self.in1.off()
            self.in2.on()
        else:
            self.in1.on()
            self.in2.off()
            
        value = abs(value)  
        self.pwm.freq(1000)  
        self.pwm.duty_u16(value)
      
