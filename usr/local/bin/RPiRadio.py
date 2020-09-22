#!/usr/bin/env python3
import RPi.GPIO as GPIO
import bluetooth
import time
import dbus
import os
import subprocess
from sh import bluetoothctl

pin = 15
PowerOffPin = 3
btMac= "FC:58:FA:82:B0:EC"
btMac= "88:C6:26:50:81:A0"
port = 1

def button_callback(channel):
    print("button pushed " + str(channel))
    if ConnectToBTSpeaker():
        time.sleep(10)
        RestartMPD()

def ConnectToBTSpeaker():
    #Attempt 2
    bluetoothctl("connect", btMac)
    return True

def RestartMPD():
    print("Restarting MPD")
    os.system("sudo systemctl restart mpd.service")
    pass

def ShutdownRpi(channel): #Based on https://scribles.net/adding-power-switch-on-raspberry-pi/
    print("Shutdown Rpi, goodnight")
    os.system("sudo shutdown -h now")
    pass

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin,GPIO.RISING,callback=button_callback,bouncetime=1000) #High bouncetime because this button is not Hulk-proof
    
    GPIO.setup(PowerOffPin, GPIO.IN)
    GPIO.add_event_detect(PowerOffPin,GPIO.RISING,callback=ShutdownRpi,bouncetime=1000)

    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()

