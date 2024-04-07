import ollama
import speech_recognition as sr
import pyttsx3
import datetime
import threading
# import os 
# from gtts import gTTS 


messages = []
# Initialize the recognizer
r = sr.Recognizer()
ollama.pull("tinydolphin")
text=""
# text to speech
engine = pyttsx3.init()
# language = 'en'

engine.setProperty('rate', 200)
def record_text():
    # Loop in case of errors
    while True:
        try:
            # use the microphone as source for input
            with sr.Microphone() as source2:
                # listens for the user's input
                print("Listening...")
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                print("I think I heard you say, '" + MyText + "'")
                return MyText

        except sr.UnknownValueError as e:
            
            return ""
        except sr.RequestError as e:
            
            return ""
        
def send(chat):
    
    messages.append({
      'role': 'user',
      'content': chat,
    })
    
    stream = ollama.chat(model='tinydolphin', 
                         messages=messages,
                         stream=True,
    )

    full_response = ""
    response = ""

  
    for chunk in stream:
        part = chunk['message']['content']
        print(part, end='', flush=True)
         
        response = response + part
        full_response = full_response + part

        if (part == ".") or (part == "!") or (part == "?") or (part == ",") or (part == ";") or (part == ":") or (part == "\n"):
            engine.say(response)
            engine.runAndWait()
            response = ""
    
    messages.append({
      'role': 'assistant',
      'content': response,
    })

    print("")

while True:
    chat = record_text()

    if chat == "/exit":
        break
    elif len(chat) > 0:
        send(chat)