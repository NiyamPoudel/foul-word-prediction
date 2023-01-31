import os
import time
from datetime import datetime
import ffmpeg
from app.worker import celery
import keyboard

try:
    while True:
        wavfilename = 'Audio-'+datetime.today().strftime('%Y%m%d-%H%M%S') 
        print('Recording for ' + wavfilename)
        cmd = "ffmpeg -loglevel quiet -y -f alsa -i hw:1 -t 5 {0}.wav".format(wavfilename)
        os.system(cmd)
        print('Starting Processing for ' + wavfilename)
        celery.signature("process.run", args=[wavfilename], queue="violet").delay()

except KeyboardInterrupt:
    print('Keyboard interrupted')
    pass



  