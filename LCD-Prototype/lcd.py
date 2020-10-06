#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import sys
sys.path.append('/home/pi/Python/RPiRadio/usr/local/lib/python3.7/dist-packages/')
import HD44780

if __name__ == "__main__":
    
    lcd = HD44780.LCD()
    lcd.send_string("Hello World! Lets Party like it is 1999! But Don't forget, pigs can fly.")
    time.sleep(15)

    pass