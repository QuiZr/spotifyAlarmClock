import RPi.GPIO as GPIO
import I2C_LCD_driver
from subprocess import Popen, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR
GPIO.setmode(GPIO.BCM)  
import time
from threading import Thread
import unicodedata
from spotifyapi import SpotifyApi
import traceback
import datetime
import schedule
from os import getenv

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

p = Popen("./play-pause", shell=False, stdout=PIPE, stdin=PIPE)
nbsr = NBSR(p.stdout)

def switch_playback():
    sp.transfer_playback(getenv('SPOTIFY_DEVICE_ID'))

def my_callback(channel):  
    p.stdin.write("pause\n")
def my_callback2(channel):  
    switch_playback()
    p.stdin.write("play\n")
def my_callback3(channel):  
    p.stdin.write("next\n")

GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback, bouncetime=1000)  
GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback2, bouncetime=1000)  
GPIO.add_event_detect(25, GPIO.FALLING, callback=my_callback3, bouncetime=1000)  

printDate = True
trackId = None
global track_name
track_name = ""
global killSwitch
killSwitch = False

global sp
sp = SpotifyApi(getenv('SPOTIFY_USERNAME'))

def alarm():
    sp.start_playback(getenv('SPOTIFY_DEVICE_ID'), getenv('SPOTIFY_ALARM_ALBUM_ID'))
    sp.set_volume(100, getenv('SPOTIFY_DEVICE_ID'))

def track_nameGetThread():
    global track_name
    track_name = sp.get_song_name(trackId[:-1])

def screenThread():
    mylcd = I2C_LCD_driver.lcd()
    scroll_index = 0
    sleep_count = 0
    last_track_name = None
    while not killSwitch:
        try:
            if last_track_name != track_name:
                scroll_index = 0
                sleep_count = 0
                last_track_name = track_name
            if printDate:
                mylcd.lcd_display_string("                ", 1)
                scroll_index = 0
                sleep_count = 0
            else:
                if len(track_name) > 16:
                    if scroll_index >= len(track_name) - 16:
                        if sleep_count > 2:
                            scroll_index = 0
                            sleep_count = 0
                    else:
                        if sleep_count > 3:
                            scroll_index = scroll_index + 1
                            if scroll_index >= len(track_name) - 16:
                                sleep_count = 0
                mylcd.lcd_display_string(track_name[scroll_index:16 + scroll_index], 1)
                sleep_count = sleep_count + 1
            
            weekday = datetime.datetime.today().weekday()
            if weekday == 0:
                day = "pon."
            elif weekday == 1:
                day = "wt. "
            elif weekday == 2:
                day = "sr. "
            elif weekday == 3:
                day = "czw."
            elif weekday == 4:
                day = "pt. "
            elif weekday == 5:
                day = "sob."
            else:
                day = "ndz."
            bottom_bar = "%s %s" %(day, time.strftime("%d.%m %H:%M"))
            mylcd.lcd_display_string(bottom_bar, 2)
            time.sleep(0.8)
        except:
            print(traceback.print_exc())
            thread.exit()
try:
    screenThread = Thread(target = screenThread)
    screenThread.start()
    schedule.every().monday.at("05:11").do(alarm)
    schedule.every().tuesday.at("07:46").do(alarm)
    schedule.every().wednesday.at("05:01").do(alarm)
    schedule.every().thursday.at("05:01").do(alarm)
    schedule.every().friday.at("05:11").do(alarm)
    schedule.every().saturday.at("09:00").do(alarm)
    schedule.every().sunday.at("09:00").do(alarm)
    while True:
        raw = None
        try:
            raw = nbsr.readline(1)
        except KeyboardInterrupt:
            raise
        except:
            try:
                p.kill()
            except:
                pass
            p = Popen("./play-pause", shell=False, stdout=PIPE, stdin=PIPE)
            nbsr = NBSR(p.stdout)
        if raw != None:
            response = raw.split('|')
            if len(response) == 7:
                if response[2] == "kPlayStatusPlay" and response[6] != "dupa\n":
                    if trackId != response[6]:
                        trackId = response[6]
                        track_name = "   Loading...   "
                        thread = Thread(target = track_nameGetThread)
                        thread.start()
                    printDate = False
                else:
                    printDate = True
            else:
                print(raw[:-1])
                print('^werid response')
        schedule.run_pending()
except:
    traceback.print_exc()
    killSwitch = True
    p.kill()
    GPIO.cleanup()
