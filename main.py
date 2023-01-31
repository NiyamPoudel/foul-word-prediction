from google.cloud import speech
import os
import io
from app.worker import celery
import librosa
import numpy as np
import soundfile
import ctypes
import easygui
from datetime import datetime
import datetime
import pymongo
from tkinter import Tk
from tkinter.messagebox import Message 
from _tkinter import TclError
import pyautogui

@celery.task(name="process.run")
def run(filename):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['admin']
    mycol = mydb["Audio"]

    print(filename)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'audio-prediction-c6e04524c4b2.json'
    client = speech.SpeechClient()

    y, sr = librosa.load(filename + ".wav", mono=False)
    ymean = np.mean(y,axis=0)
    soundfile.write(filename + "_final" + ".wav", ymean, samplerate=22100)

    file_name = filename + "_final" + ".wav"
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)


    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=1,
        language_code="en-US",
        profanity_filter=False,
        model="latest_short"
    )


    
    word_list = ["cunt", "wanker", "motherfucker", "fuck", "bastard"]

    response = client.recognize(request={"config": config, "audio": audio})
    
    for result in response.results:
        transcript = result.alternatives[0].transcript.split()
        print(transcript)
        i=set.intersection(set(transcript),set(word_list))
        print(i)
        if any(x in transcript for x in word_list):
            print("Suggested Word Detected")
            seconds_since_epoch = datetime.datetime.now().timestamp()
            if (len(list(mydb.Audio.find())) == 0):
                print("Foul Word Detected for the fitst time")
                wordCount = 1
                mydict = { "name": "Audio", "wordCount": wordCount, "createdAt": seconds_since_epoch }
                x = mycol.insert_one(mydict)
            else:
                print("Foul Word Detected after first time")
                data = list(mydb.Audio.find())
                # check if this data is older than 10 minutes
                # print(data[0]['createdAt'], data[0]['createdAt'] + 600, datetime.datetime.now().timestamp())
                # print("Previous timestamp",data[0]['createdAt'])
                # print("current timestamp",datetime.datetime.now().timestamp())
                # print("current timestamp plus 60",data[0]['createdAt'] + 600)
                if ((datetime.datetime.now().timestamp()) > (data[0]['createdAt'] + 600)):
                    print("Resetting Cache")
                    myquery1 = { "name": "Audio" }
                    newvalues1 = { "$set": { "wordCount": 0 } }
                    mycol.update_one(myquery1, newvalues1)
                
                    wordCount = 1
                    myquery = { "name": "Audio" }
                    newvalues = { "$set": { "wordCount": wordCount, "createdAt": seconds_since_epoch } }
                    mycol.update_one(myquery, newvalues)
                else:
                    wordCount = data[0]['wordCount'] + 1
                    myquery = { "name": "Audio" }
                    newvalues = { "$set": { "wordCount": wordCount, "createdAt": seconds_since_epoch } }
                    mycol.update_one(myquery, newvalues)

                root = Tk() 
                root.withdraw()
                try:
                    root.after(1000, root.destroy) 
                    if (wordCount == 3):
                        Message(title="Foul Word Detected", message="Foul word/s has been detected: " + str(i) + " . Next time the wifi will be switched off", master=root).show()
                    else:

                        Message(title="Foul Word Detected", message="Foul word/s has been detected: " + str(i), master=root).show()

                except TclError:
                    pass
        
            if (wordCount > 3):
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save('/home/nimai/workspace/audio_prediction/screenshot/shot1.png')
                os.system("nmcli radio wifi off")
                myquery = { "name": "Audio" }
                newvalues = { "$set": { "wordCount": 0 } }
                mycol.update_one(myquery, newvalues)
            
    os.remove(filename + ".wav")
    os.remove(filename + "_final" + ".wav")
if __name__ == "__main__":
    print("main")
    celery.signature("process.run", args=[wavfilename], queue="violet").delay()