import RPi.GPIO as GPIO
import time
import subprocess
import I2C_LCD_driver
GPIO.setmode(GPIO.BCM)  
  
# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.  
# Both ports are wired to connect to GND on button press.  
# So we'll be setting up falling edge detection for both  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
  
# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press  
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
  
# now we'll define two threaded callback functions  
# these will run in another thread when our events are detected  
def my_callback(channel):  
    print "falling edge detected on 23"
    process = subprocess.Popen("~/lcdtest/play-pause --command pause", shell=True, stdout=subprocess.PIPE)
    process.wait()
    print process.returncode
def my_callback2(channel):  
    print "falling edge detected on 24"
    process = subprocess.Popen("~/lcdtest/play-pause --command play", shell=True, stdout=subprocess.PIPE)
    process.wait()
    print process.returncode
def my_callback3(channel):  
    print "falling edge detected on 25"
    process = subprocess.Popen("~/lcdtest/play-pause --command next", shell=True, stdout=subprocess.PIPE)
    process.wait()
    print process.returncode

#raw_input("Press Enter when ready\n>")  
  
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback, bouncetime=1000)  
GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback2, bouncetime=1000)  
GPIO.add_event_detect(25, GPIO.FALLING, callback=my_callback3, bouncetime=1000)  

try:
#    while(True):
#        time.sleep(1) 
    mylcd = I2C_LCD_driver.lcd()
    while True:
        mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 1)
        mylcd.lcd_display_string("Date: %s" %time.strftime("%d/%m/%Y"), 2)  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on normal exit  
