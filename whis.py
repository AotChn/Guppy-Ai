
import openai
import os 
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

os.environ['OPENAI_API_KEY'] = ""

client = openai.OpenAI()
print("select a topic: ")
print("[1] cats")
print("[2] dogs")
print("[3] rivers")
print("[4] random")
print("[5] custom")

t = input("please select a topic: ")
prepTime = int(input("select an amount to prep time: "))
speechTime = int(input("select an amount to perform: "))


if(t == "1"):
    t = "cats"

if(t == "2"):
    t = "dogs"

if(t == "3"):
    t = "rivers"

if(t == "4"):
    t = "random"

if(t == "5"):
    t = input("enter custom topic: ")


random_topics = [
    "Artificial Intelligence",
    "Space exploration",
    "Cryptocurrency",
    "Virtual reality",
    "Climate change",
    "Renewable energy",
    "Neuroscience",
    "Ancient civilizations",
    "Robotics",
    "Ethical hacking",
    "Machine learning algorithms",
    "Bioinformatics",
    "Augmented reality",
    "Internet of Things (IoT)",
    "Quantum computing",
    "3D printing technology",
    "Future of work",
    "Biotechnology",
    "Urban planning",
    "Marine biology",
    "Astrobiology",
    "Big data analytics",
    "Nanotechnology",
    "Cognitive psychology",
    "Blockchain technology",
    "Medical ethics",
    "Cybersecurity threats",
    "Digital marketing trends",
    "Economic inequality",
    "Geopolitics",
    "Human rights movements",
    "Cryptographic protocols",
    "Data privacy laws",
    "Genetic engineering",
    "History of mathematics",
    "Philosophy of mind",
    "Sustainable agriculture",
    "Virtual currencies",
    "Space tourism",
    "Artificial neural networks",
    "Game theory applications",
    "Environmental conservation",
    "Music composition techniques",
    "Remote sensing technologies",
    "Cultural anthropology",
    "Psychological disorders",
    "Internet censorship",
    "Ethics in technology",
    "Human-computer interaction"
]

import random

t.lower()
if (t == 'random'):
    t = str(random.choice(random_topics))

def getTopic(topic):
    return "You are an expert with extensive knowledge in " + topic

import time 

def fillSpace(r):
    for i in range(r):
        print(".\n")
  
def countdown(t, endQuote): 
    
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1) 
        t -= 1
      
    print(endQuote) 

fillSpace(100)
print("\n you be given ", prepTime, " to prep your impromtu speech on ", t)
print("BE PREPARED STARTING IN 10 SECONDS")
countdown(10, "prep time")

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": getTopic(t)},
    {"role": "user", "content": "give 10 facts in your area of expertise as 5 short sentences that are less than 5 words each"}
  ],
  stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

fillSpace(1)
countdown(prepTime, "begin your speech!") 

fillSpace(100)


# Sampling frequency
freq = 44100

# Recording duration
duration = 10

# Start recorder with the given values of 
# duration and sample frequency
recording = sd.rec(int(duration * freq), 
                   samplerate=freq, channels=1)

# Record audio for the given number of seconds
countdown(10, "Finished !")
sd.wait()

# This will convert the NumPy array to an audio
# file with the given sampling frequency
write("recording0.wav", freq, recording)

# Convert the NumPy array to audio file
wv.write("recording1.wav", recording, freq, sampwidth=2)


os.environ['OPENAI_API_KEY'] = "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"

client = openai.OpenAI()

audio_file = open("recording1.wav", "rb")
result = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file, 
  response_format="text",
  prompt="make all Um, um, uh, ums, eh, in the output"
)

placeholderWords = ["Um", "um", "uh", "ums", "eh", "yeah", "hmm", "hm", "ya"]
print(result)

PLACEHOLDERS = 0
for i in placeholderWords:
    if i in result:
        PLACEHOLDERS += 1

print("place holder words detected : ", PLACEHOLDERS)

rateSpeech = "given this speech give a rating from 0 to 100 in the cateories of structure, information relevance to " + t + " clarity, and overall score be a little friendly: " + result

coach = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are a world renovned speech coach"},
    {"role": "user", "content": rateSpeech}
  ],
  stream=True
)

for chunk in coach:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")


def countWords(s):
    # Check if the string is null
    # or empty then return zero
    if s.strip() == "":
        return 0
    # Splitting the string
    words = s.split()
    return len(words)

def wordsPerMinute(words, s):
    return words * (60/s)

print("words in speech: ", countWords(result))
print("words per minutes ", wordsPerMinute(countWords(result), speechTime))

