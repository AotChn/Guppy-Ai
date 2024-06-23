from pywebio.input import input, FLOAT
from pywebio.output import put_text
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *


import openai
import os 
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

x = select('ENTER', options=['ok'])

put_text("WELCOME TO GUPPY")
put_text("your virtual speech companion")



x = select('Choose a prompt:', options=['Dog', 'Cats', 'Tree', 'Mountain', 'Beach', 'Bird', 'Flower', 'Car', 'House', 'River'])

x = select('Select the amount of time you will get to read about your selected prompt. When the time is up, you will then present a short impromptu speech about your chosen prompt.', options=['20 seconds', '30 seconds', '60 seconds'])

x = select('Select the amount of time you will get to present your impromptu speech.', options=['20 seconds', '30 seconds', '60 seconds'])

os.environ['OPENAI_API_KEY'] = "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"

client = openai.OpenAI()

def getTopic(topic):
    return "You are an expert with extensive knowledge in " + topic

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": getTopic("cats")},
    {"role": "user", "content": "give 5 facts in your area of expertise as 5 short sentence with less than 7 words per sentence"}
  ]
)

import time 
  
# define the countdown func. 
def countdown(t, endQuote): 
    
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1) 
        t -= 1
      
    print(endQuote) 

put_text("HERE IS SOME INFO ABOUT CATS")
put_text("*note you do not need to use this info in your speech :)")
countdown(3,"")

put_text(response.choices[0].message.content)

prepTime = 10
speechTime = 20


put_text("when prompted begin your speech")
countdown(prepTime, "begin your speech!")

put_text("BEGIN TALKING!")

# Sampling frequency
freq = 44100

# Recording duration
duration = speechTime

# Start recorder with the given values of 
# duration and sample frequency
recording = sd.rec(int(duration * freq), 
                   samplerate=freq, channels=1)

# Record audio for the given number of seconds
countdown(duration, "Finished !")
sd.wait()
put_text("[FINISHED!] ----- ANALYZING SPEECH ------------------")

put_text("　　　 　　／＞　　 フ")
put_text("　　　 　　| 　-　 -)  -- GOOD JOB !")
put_text("　 　　 　／` ミ＿xノ")
put_text("　　 　 /　　　 　 |")
put_text("　　　 /　 ヽ　　 ﾉ")
put_text("　 　 │　　|　|　|")
put_text("　／￣|　　 |　|　|")
put_text("　| (￣ヽ__ ヽ_) ヽ)")
put_text("　＼二つ")
# This will convert the NumPy array to an audio
# file with the given sampling frequency
write("recording0.wav", freq, recording)

# Convert the NumPy array to audio file
wv.write("recording1.wav", recording, freq, sampwidth=2)

audio_file = open("recording1.wav", "rb")
result = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file, 
  response_format="text",
  prompt="make all Um, um, uh, ums, eh, in the output"
)

placeholderWords = ["Um", "um", "uh", "ums", "eh", "yeah", "hmm", "hm", "ya", "Uh"]
put_text("YOUR SPEECH: ")
put_text(result)
put_text("---------------------------------------")
countdown(2, "")

PLACEHOLDERS = 0
for i in placeholderWords:
    if i in result:
        PLACEHOLDERS += 1

put_text("place holder words detected : ", PLACEHOLDERS)
if(PLACEHOLDERS > 0):
    put_text("please be more concious of using place holder words such as um")
countdown(2, "")

put_text("here are some things too look out for :)")
rateSpeech = "given this speech give a rating from 0 to 100 in the cateories of structure, information relevance to " + "cats" + " clarity, and overall score: " + result

coach = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are a world renowned speech coach"},
    {"role": "user", "content": rateSpeech}
  ]
)

put_text(coach.choices[0].message.content)