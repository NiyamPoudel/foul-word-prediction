from google.cloud import speech
import os
import io

os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'audio-prediction-c6e04524c4b2.json'
client = speech.SpeechClient()
file_name = "test2_single.wav"
with io.open(file_name, "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    # enable_automatic_punctuation=True,
    audio_channel_count=1,
    language_code="en-US",
)

response = client.recognize(request={"config": config, "audio": audio})
print(response.results)
for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))

