import RPi.GPIO as GPIO
import I2C_LCD_driver
from subprocess import Popen, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR
GPIO.setmode(GPIO.BCM)  
import time
from threading import Thread
import unicodedata
from getTrackNameAndArtist import getTrackNameAndArtist

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

p = Popen("./play-pause", shell=False, stdout=PIPE, stdin=PIPE)
nbsr = NBSR(p.stdout)

def my_callback(channel):  
    print "falling edge detected on 23"
    p.stdin.write("pause\n")
def my_callback2(channel):  
    print "falling edge detected on 24"
    p.stdin.write("play\n")
def my_callback3(channel):  
    print "falling edge detected on 25"
    p.stdin.write("next\n")

GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback, bouncetime=1000)  
GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback2, bouncetime=1000)  
GPIO.add_event_detect(25, GPIO.FALLING, callback=my_callback3, bouncetime=1000)  

printDate = True
trackId = None
global trackName
global killSwitch
killSwitch = False

global t
t = getTrackNameAndArtist('USERNAME')

def trackNameGetThread():
    global trackName
    print "threadLaunch: " + trackId[:-1]
    a = t.getSongName(trackId[:-1])
    trackName = unicodedata.normalize('NFKD', unicode(a)).encode('ascii','ignore')
    print trackName

def screenThread():
    mylcd = I2C_LCD_driver.lcd()
    while not killSwitch:
        try:
            if printDate:
                mylcd.lcd_display_string("Date: %s" %time.strftime("%d/%m/%Y"), 1)
            else:
                mylcd.lcd_display_string(trackName[0:16], 1)
            mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 2)
            time.sleep(0.5)
        except:
            thread.exit()
try:
    screenThread = Thread(target = screenThread)
    screenThread.start()
    while True:
        rawOutput = nbsr.readline(1)
        if rawOutput:
            #print rawOutput
            response = rawOutput.split('|')
            if len(response) == 7:
                if response[2] == "kPlayStatusPlay" and response[6] != "dupa\n":
                    if trackId != response[6]:
                        trackId = response[6]
                        trackName = "   Loading...   "
                        thread = Thread(target = trackNameGetThread)
                        thread.start()
                    printDate = False
                else:
                    printDate = True
except:
    killSwitch = True
    p.kill()
    GPIO.cleanup()
