#!/usr/bin/python3
import RPi.GPIO as GPIO

# https://cdn.sparkfun.com/datasheets/Components/General/EC12PLGRSDVF.pdf
# https://github.com/sparkfun/Rotary_Encoder_Breakout-Illuminated/blob/master/Firmware/RG_Rotary_Encoder/RG_Rotary_Encoder.ino
# https://www.ozeki.hu/index.php?owpn=3054

ROT_A=5
ROT_B=6
ROT_Counter=0
ROT_Bounce=0
ROT_Tolerance=2

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ROT_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ROT_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(ROT_A, GPIO.RISING, callback=roteryIRQ)
    pass

def roteryIRQ(channel):
    global ROT_Bounce
    if GPIO.input(ROT_A)==GPIO.input(ROT_B):
        ROT_Bounce -= 1 #Move left detected
    else:
        ROT_Bounce += 1 #Move right detected
    CheckBounce()
    print(ROT_Counter)
    pass

def CheckBounce(): #This prevents false positives
    global ROT_Bounce, ROT_Counter
    if ROT_Bounce == ROT_Tolerance:
        ROT_Counter += 1 #Move counter up/right
        ROT_Bounce = 0 # Reset our bounce
        #pass

    if ROT_Bounce == -ROT_Tolerance:
        ROT_Counter -= 1 #Move counter up/right
        ROT_Bounce = 0 # Reset our bounce
    pass

if __name__ == "__main__":
    try:
        setup()
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
    pass