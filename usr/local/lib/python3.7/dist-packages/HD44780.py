import RPi.GPIO as GPIO
import time

class LCD():  

    #Resources: http://site2241.net/november2014.htm, https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/, https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
    #Sure there are multiple HD44780 drivers on the interwebz, but this one has bitmask and other cool stuff

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LCD_RS, GPIO.OUT)
        GPIO.setup(self.LCD_E, GPIO.OUT)
        GPIO.setup(self.LCD_DB4, GPIO.OUT)
        GPIO.setup(self.LCD_DB5, GPIO.OUT)
        GPIO.setup(self.LCD_DB6, GPIO.OUT)
        GPIO.setup(self.LCD_DB7, GPIO.OUT)

        self.initLCD()
        pass

    def initLCD(self):
        #page 46 > HD44780U (LCD-II)        
        self.__send_command(0b00110011) #init signal
        self.__send_command(0b00110010) #init signal + start config
        self.__send_command(0b00101000) #Config lines and dot size
        """                |└ 1 = 5x10 dots, 0 = 5x8 dots
                           └ 1 = 2 lines, 0 = 1 line LCD """
        time.sleep(0.5)
        self.__send_command(0b00001111) #Display, cursor and blink control
        """                 ||└ 1 = Blink on, 0 = blink off
                            |└ 1 = Cursor on, 0 = cursor off
                            └ 1 = Display on, 0 = display off """
        self.__send_command(0b00000001) #Display clear
        self.__send_command(0b00000110) #Entry mode
        pass

    def __bit_query(self, input, bin_q):
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

    def send_string(self, string):
        for c in string:
            self.__send_data(ord(c))
            self.LCD_Cursor
            self.LCD_Cursor += 1
            if self.LCD_Cursor == 16: #move to second line
                self.LCD_Cursor = 40
                self.__send_command(0b11000000)
            if self.LCD_Cursor == 56:
                self.LCD_Cursor = 0
                self.__send_command(0b10000000)
        pass

    def __send_data(self, i):
        self.__send_command(i,1)
        pass

    def __send_command(self, i, isData=0):
        #set register in command mode
        GPIO.output(self.LCD_RS, isData)

        GPIO.output(self.LCD_DB4, 1) if self.__bit_query(i, 0b00010000) else GPIO.output(self.LCD_DB4, 0)
        GPIO.output(self.LCD_DB5, 1) if self.__bit_query(i, 0b00100000) else GPIO.output(self.LCD_DB5, 0)
        GPIO.output(self.LCD_DB6, 1) if self.__bit_query(i, 0b01000000) else GPIO.output(self.LCD_DB6, 0)
        GPIO.output(self.LCD_DB7, 1) if self.__bit_query(i, 0b10000000) else GPIO.output(self.LCD_DB7, 0)
        self.__enable()

        GPIO.output(self.LCD_DB4, 1) if self.__bit_query(i, 0b00000001) else GPIO.output(self.LCD_DB4, 0)
        GPIO.output(self.LCD_DB5, 1) if self.__bit_query(i, 0b00000010) else GPIO.output(self.LCD_DB5, 0)
        GPIO.output(self.LCD_DB6, 1) if self.__bit_query(i, 0b00000100) else GPIO.output(self.LCD_DB6, 0)
        GPIO.output(self.LCD_DB7, 1) if self.__bit_query(i, 0b00001000) else GPIO.output(self.LCD_DB7, 0)
        self.__enable()
        pass

    def __enable(self, ms=0.005):
        time.sleep(ms)
        GPIO.output(self.LCD_E, 1)
        time.sleep(ms)
        GPIO.output(self.LCD_E, 0)
        time.sleep(ms)
        pass

    def __init__(self, LCD_RS=7, LCD_E=8, LCD_DB4=25, LCD_DB5=24, LCD_DB6=23, LCD_DB7=18):

        self.LCD_RS=LCD_RS #Register, 0 = command; 1 = Data
        #LCD_RW= #Register, 0 = Write; 1 = Read #TODO or not TODO, that is the question.
        self.LCD_E=LCD_E #enable pin
        #Skipping DB 0-3 because 4 bit mode #TODO Make it 4/8 bit with inheritence.
        self.LCD_DB4=LCD_DB4
        self.LCD_DB5=LCD_DB5
        self.LCD_DB6=LCD_DB6
        self.LCD_DB7=LCD_DB7
        self.LCD_Cursor=0

        self.__setup()
        pass

    def __del__(self):
        GPIO.cleanup()
        pass
    pass

