#!/usr/bin/python3
import RPi.GPIO as GPIO

# https://cdn.sparkfun.com/datasheets/Components/General/EC12PLGRSDVF.pdf
# https://github.com/sparkfun/Rotary_Encoder_Breakout-Illuminated/blob/master/Firmware/RG_Rotary_Encoder/RG_Rotary_Encoder.ino

ROT_A=5
ROT_B=6
ROT_Counter=0

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ROT_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ROT_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(ROT_A, GPIO.RISING, callback=roteryIRQ, bouncetime=200)
    pass

def roteryIRQ(channel):
    
    rota = "Low"
    rotb = "Low"

    if GPIO.input(ROT_A):
        rota = "High"
    if GPIO.input(ROT_B):
        rotb = "High"
    print("A: " + rota + ", B: " + rotb)
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