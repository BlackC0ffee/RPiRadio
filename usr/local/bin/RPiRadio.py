#!/usr/bin/env python3
import RPi.GPIO as GPIO
import bluetooth
import time
import dbus
import os
import subprocess
from sh import bluetoothctl ## sh needs to be installed as root

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
    #Attempt 2
    bluetoothctl("connect", btMac)

    #Attempt 3
    #subprocess.call('bluetoothctl')
    #subprocess.call('connect 88:C6:26:50:81:A0')

    #Attempt 4
    #https://blog.kevindoran.co/bluetooth-programming-with-python-3/
serverMACAddress = '00:1f:e1:dd:08:3d'
port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))
while 1:
    text = raw_input() # Note change to the old (Python 2) raw_input
    if text == "quit":
    break
    s.send(text)
sock.close()




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

