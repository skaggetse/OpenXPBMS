import os
import curses
import tui
import time
import RPi.GPIO as GPIO

cmd = 'python3 BMS.py'

p = os.popen(cmd)
p.read()

GPIO.output(16,GPIO.LOW)

# clear the screen
tui.screen.clear()

# reverse terminal settings
curses.nocbreak()
tui.screen.keypad(False)
curses.echo()

# close the application
curses.endwin()