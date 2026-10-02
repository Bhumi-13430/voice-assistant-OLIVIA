import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from openai import OpenAI
import musicLib
import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
newsapi_key = os.getenv("NEWS_API_KEY")


recognizer = sr.Recognizer()  
newsapi = "<YOUR_NEWS_API_KEY>"

engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def aiProcess(command):
    client = OpenAI(
        api_key="<YOUR_OPENAI_API_KEY>",
    )
    completion = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[
            {
                "role": "system",
                "content": "You are a general assistant named Olivia, skilled in general tasks like Alexa and Google Assistant. Give short answers"
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedIn" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif  "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif  "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLib.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(
    f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
)
        if r.status_code == 200:
            # parse the JSON response
            data = r.json()

            # extract the articles
            articles = data.get('articles', [])

            # print the headlines
            for article in articles:
                speak(article['title'])

    else:
        #let openAI handle the request
        output = aiProcess(c)
        speak(output)
     
if __name__ == "__main__":
    speak("Initializing olivia...")

    while True:
        # Listen for the wake word Nova
        # obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing....")

        try:
            with sr.Microphone() as source:
                print("Listening")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)

            word = r.recognize_google(audio)

            if word.lower() == "olivia":
                speak("yes")

                # listen for command
                with sr.Microphone() as source:
                    print("olivia is here...")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                command = r.recognize_google(audio)
                
                processCommand(command)

        except Exception as e:
            print("error: ".format(e))