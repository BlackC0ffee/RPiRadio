#!/usr/bin/env python3
import RPi.GPIO as GPIO
import bluetooth
import time
import dbus
import os
import subprocess
from sh import bluetoothctl

pin = 15
btMac= "FC:58:FA:82:B0:EC"
btMac= "88:C6:26:50:81:A0"
port = 1

def button_callback(channel):
    print("button pushed " + str(channel))
    if ConnectToBTSpeaker():
        time.sleep(10)
        RestartMPD()

def ConnectToBTSpeaker():
    #Attempt 1
    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    client_sock.setblocking(True)
    try:
        client_sock.connect((btMac, port))

        print(str(btMac) + " Connected")
        return True
    except bluetooth.btcommon.BluetoothError:
        print("Unable to connect to " + str(btMac))
        return False 



def RestartMPD():
    print("Restarting MPD")
    os.system("sudo systemctl restart mpd.service")
    """ sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
    job = manager.RestartUnit('mpd.service', 'fail') #Thank you https://stackoverflow.com/questions/33646374/starting-a-systemd-service-via-python
    #hmm: https://zignar.net/2014/09/08/getting-started-with-dbus-python-systemd/ """
    pass

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin,GPIO.RISING,callback=button_callback,bouncetime=1000) #High bouncetime because this button is not Hulk-proof

    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()

