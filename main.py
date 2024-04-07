# https://github.com/ollama/ollama/blob/main/docs/import.md

import ollama
import speech_recognition as sr
import pyttsx3

model = "ren"
messages = []
r = sr.Recognizer()
text=""
engine = pyttsx3.init()

engine.setProperty('rate', 225)
def record_text():
    # Loop in case of errors
    while True:
        try:
            # use the microphone as source for input
            with sr.Microphone() as source2:
                # listens for the user's input
                print("[REN IS LISTENING...]")
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                print("USER >>> " + MyText)
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
    
    stream = ollama.chat(model=model, 
                         messages=messages,
                         stream=True,
    )

    full_response = ""
    response = ""

  
    for chunk in stream:
        part = chunk['message']['content']
        print(part, end='', flush=True)
         
        response += part
        full_response += part

        if (part == ".") or (part == "!") or (part == "?") or (part == ",") or (part == ";") or (part == ":") or (part == "\n"):
            engine.say(response)
            engine.runAndWait()
            response = ""
    
    messages.append({
      'role': 'assistant',
      'content': full_response,
    })

    print("")

while True:
    chat = record_text()

    if chat == "/bye": break
    elif chat == "goodbye": messages = []
    elif len(chat) > 0: send(chat)