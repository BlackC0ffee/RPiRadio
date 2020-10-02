#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

#Resources: http://site2241.net/november2014.htm, https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/

LCD_RS=7 #Register, 0 = command; 1 = Data
#LCD_RW= #Register, 0 = Write; 1 = Read
LCD_E=8 #enable pin

#Skipping DB 0-3 because 4 bit mode
LCD_DB4=25
LCD_DB5=24
LCD_DB6=23
LCD_DB7=18

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_DB4, GPIO.OUT)
    GPIO.setup(LCD_DB5, GPIO.OUT)
    GPIO.setup(LCD_DB6, GPIO.OUT)
    GPIO.setup(LCD_DB7, GPIO.OUT)

    initLCD()
    pass

def initLCD():
    #page 46 > HD44780U (LCD-II)
    time.sleep(0.1)
    GPIO.output(LCD_DB7, 0)
    GPIO.output(LCD_DB6, 0)
    GPIO.output(LCD_DB5, 1)
    GPIO.output(LCD_DB4, 1)
    #send 3 times the init signal. 
    enable(0.1)
    enable(0.1)
    enable(0.1)
    
    #start the config
    GPIO.output(LCD_DB7, 0)
    GPIO.output(LCD_DB6, 0)
    GPIO.output(LCD_DB5, 1)
    GPIO.output(LCD_DB4, 0)
    enable(0.1)
    send_command(0b00101000) #Config lines and dot size
    """                |└ 1 = 5x10 dots, 0 = 5x8 dots
                       └ 1 = 2 lines, 0 = 1 line LCD """
    time.sleep(0.5)
    send_command(0b00001111) #Display, cursor and blink control
    """                 ||└ 1 = Blink on, 0 = blink off
                        |└ 1 = Cursor on, 0 = cursor off
                        └ 1 = Display on, 0 = display off """
    send_command(0b00000001) #Display clear
    time.sleep(0.5)
    send_command(0b00000110) #Entry mode
    time.sleep(0.5)                
    send_command(0b00010100)
    send_string("Hello World! Let|s Party like it is 1999!| But Don't forget, pigs can fly.")
    
    #entry mode set
    pass

#
def bit_query(input,bin_q):
    """
    This functions performs bitmask query, where bin_q is the bit(s) that require to be checked.
    E.g.: input 0b101010 and bin_q 0b10 will returen true becuase:
        0b101010
    AND     0b10
    ------------
          000010 => (0b10)
    
    This function probably esists somwhere in Python but meh...
    """
    if (input & bin_q) == bin_q:
        return True
    else:
        return False
    pass

def send_string(string):
    for c in string:
        send_data(ord(c))
    pass

def send_data(i):
    send_command(i,1)
    pass

def send_command(i, isData=0):
    #set register in command mode
    GPIO.output(LCD_RS, isData)

    GPIO.output(LCD_DB4, 1) if bit_query(i, 0b00010000) else GPIO.output(LCD_DB4, 0)
    GPIO.output(LCD_DB5, 1) if bit_query(i, 0b00100000) else GPIO.output(LCD_DB5, 0)
    GPIO.output(LCD_DB6, 1) if bit_query(i, 0b01000000) else GPIO.output(LCD_DB6, 0)
    GPIO.output(LCD_DB7, 1) if bit_query(i, 0b10000000) else GPIO.output(LCD_DB7, 0)

    enable()

    GPIO.output(LCD_DB4, 1) if bit_query(i, 0b00000001) else GPIO.output(LCD_DB4, 0)
    GPIO.output(LCD_DB5, 1) if bit_query(i, 0b00000010) else GPIO.output(LCD_DB5, 0)
    GPIO.output(LCD_DB6, 1) if bit_query(i, 0b00000100) else GPIO.output(LCD_DB6, 0)
    GPIO.output(LCD_DB7, 1) if bit_query(i, 0b00001000) else GPIO.output(LCD_DB7, 0)

    enable()
    pass

def enable(ms=0.005):
    time.sleep(ms)
    GPIO.output(LCD_E, 1)
    time.sleep(ms)
    GPIO.output(LCD_E, 0)
    pass

def final():
    GPIO.cleanup()
    pass

if __name__ == "__main__":
    
    setup()
    time.sleep(15)
    final()
    pass