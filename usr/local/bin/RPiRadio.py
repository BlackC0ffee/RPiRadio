#!/usr/bin/env python3
import RPi.GPIO as GPIO
#import bluetooth
import time
#import dbus
import os
#import subprocess
from sh import bluetoothctl

ConnectPin = 15
PowerOffPin = 3
btMac= "FC:58:FA:82:B0:EC"
btMac= "88:C6:26:50:81:A0"
port = 1

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
    GPIO.setup(ConnectPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(ConnectPin,GPIO.RISING,callback=connect,bouncetime=1000) #High bouncetime because this button is not Hulk-proof
    
    GPIO.setup(PowerOffPin, GPIO.IN)
    GPIO.add_event_detect(PowerOffPin,GPIO.RISING,callback=shutdownRpi,bouncetime=1000)

    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()