#!/usr/bin/env python

import serial
from sys import stdout
import time
import threading
import raspi_neopixel_lib

import Adafruit_CharLCD as LCD


# Raspberry Pi pin configuration:
lcd_rs        = 26
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11
lcd_backlight = 9
#Neopixel Config
LED_COUNT_1 = 24
LED_PIN_1 = 18
LED_FREQ_HZ_1 = 800000
LED_DMA_1 = 5
LED_BRIGHTNESS_1 = 255
LED_INVERT_1 = False

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2
timer = 0
# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# Print a two line message
lcd.set_backlight(0)
lcd.message('Starting')

ser = serial.Serial('/dev/ttyACM0',9600)
s = []
CORSICA = raspi_neopixel_lib.Adafruit_NeoPixel(LED_COUNT_1, LED_PIN_1, LED_FREQ_HZ_1,
                                                     LED_DMA_1, LED_INVERT_1, LED_BRIGHTNESS_1)
CORSICA.begin()
while True:
        read_serial=ser.readline()
        stripped = read_serial.rstrip()
        s.append(stripped)
        if len(s) >= 20:
                s.pop(0)
                for val in s:
                        if not val.isdigit():
                                s.remove(val)
                v = list(map(int, s))
                average = int(sum(v)/len(v))
                image = ((58.0/1023.0)*float(average))
                print ("%.0f" %image)
                kilovolts = ((10.0/1023.0)*float(average)) #(19.0/3410.0)*x+4.3 for 4.3-10.0
                if timer == 50:
			CORSICA.color_gradient_rg((image/58.0)*100)
                        timer = 0
                        lcd.clear()
                        lcd.message('Voltage\n%.1f KV' %kilovolts)
        stdout.flush()
        timer += 1
