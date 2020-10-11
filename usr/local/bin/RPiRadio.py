#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import os
from sh import bluetoothctl

ConnectPin = 15
PowerOffPin = 3 #Only pin 3 can power RPi on, but has a hard-wired Pull-Up resitor (This means the pin need to be connected to ground.)
btMac= "" #Enter BT address of speaker

def connect(channel):
    print("button pushed " + str(channel))
    if connectToBTSpeaker():
        time.sleep(10)
        restartMPD()

def connectToBTSpeaker():
    bluetoothctl("connect", btMac)
    return True

def restartMPD():
    print("Restarting MPD")
    os.system("sudo systemctl restart mpd.service")
    pass

def shutdownRpi(channel): #Based on https://scribles.net/adding-power-switch-on-raspberry-pi/
    print("Shutdown Rpi, goodnight")
    os.system("sudo shutdown -h now")
    pass

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ConnectPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #3.3v -> Button -> 10kΩ -> ConnectPin 
    GPIO.add_event_detect(ConnectPin,GPIO.RISING,callback=connect,bouncetime=1000) #High bouncetime because this button is not Hulk-proof
    
    GPIO.setup(PowerOffPin, GPIO.IN) #GND -> Button -> 10kΩ -> PowerOffPin
    GPIO.add_event_detect(PowerOffPin,GPIO.RISING,callback=shutdownRpi,bouncetime=1000)

    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()