from google.cloud import speech
import os
import io

# @celery.task(name="process.run")
def run(filename):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'audio-prediction-c6e04524c4b2.json'
    client = speech.SpeechClient()
    # print(filename + " Processing started")
    sound = filename + '.wav'
    with io.open(sound, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation=True,
        audio_channel_count=2,
        language_code="en-US",
    )
    response = client.recognize(request={"config": config, "audio": audio})
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
    os.remove(sound)

# if __name__ == "__main__":
#     print("main")
#     celery.signature("process.run", args=[wavfilename], queue="violet").delay()