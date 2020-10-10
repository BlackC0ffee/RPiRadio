#!/usr/bin/python3
import RPi.GPIO as GPIO
import time


# https://cdn.sparkfun.com/datasheets/Components/General/EC12PLGRSDVF.pdf
# https://github.com/sparkfun/Rotary_Encoder_Breakout-Illuminated/blob/master/Firmware/RG_Rotary_Encoder/RG_Rotary_Encoder.ino
# https://www.ozeki.hu/index.php?owpn=3054

ROT_A=5
ROT_B=6
ROT_Counter=0
ROT_Bounce=0
ROT_Tolerance=2


class Event(object): 
    #https://www.geeksforgeeks.org/mimicking-events-python/
    def __init__(self): 
        self.__eventhandlers = [] 
  
    def __iadd__(self, handler): 
        self.__eventhandlers.append(handler) 
        return self
  
    def __isub__(self, handler): 
        self.__eventhandlers.remove(handler) 
        return self
  
    def __call__(self, *args, **keywargs): 
        for eventhandler in self.__eventhandlers: 
            eventhandler(*args, **keywargs)

class lcd(object):
    def data(self, object):
        print(object)
        pass
    pass

class Rotary(object):
    def __init__(self, RotaryPin_A, RotaryPin_B):
        self.OnChange = Event()
        self.__ROT_A = RotaryPin_A
        self.__ROT_B = RotaryPin_B
        self.__ROT_Counter=0
        self.__ROT_Bounce=0
        self.__ROT_Tolerance=2
        self.__setup()
        pass

    def __str__(self):
        return str(self.__ROT_Counter)
        pass

    def addSubscriber(self,objMethod): 
        self.OnChange += objMethod
        pass

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__ROT_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__ROT_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.__ROT_A, GPIO.RISING, callback=self.roteryIRQ)
        pass
    def roteryIRQ(self, channel):
        if GPIO.input(self.__ROT_A)==GPIO.input(self.__ROT_B):
            self.__ROT_Bounce -= 1 #Move left detected
        else:
            self.__ROT_Bounce += 1 #Move right detected
        
        if self.CheckBounce():
            self.OnChange(self)
        pass

    def CheckBounce(self): #This prevents false positives
        if self.__ROT_Bounce == self.__ROT_Tolerance:
            self.__ROT_Counter += 1 #Move counter up/right
            self.__ROT_Bounce = 0 # Reset our bounce
            return True

        if self.__ROT_Bounce == -self.__ROT_Tolerance:
            self.__ROT_Counter -= 1 #Move counter up/right
            self.__ROT_Bounce = 0 # Reset our bounce
            return True
        return False
    pass

if __name__ == "__main__":
    try:
        t=Rotary(ROT_A, ROT_B)
        a=lcd()
        t.addSubscriber(a.data)
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
    pass