import ollama as llm
import speech_recognition as sr
import pyttsx3 as engine

from localstorage import get_history, add_history

model = "ren"
text = ""

r = sr.Recognizer()
messages = get_history()

voice = engine.init()
voice.setProperty('rate', 225)
voices = voice.getProperty('voices')

voice.setProperty('voice', voices[1].id) #changing index changes voices but ony 0 and 1 are working here
voice.runAndWait()

def save_latest(history):
    add_history([history[len(history) - 1]['role'], history[len(history) - 1]['content']])

def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                print("[REN IS LISTENING...]")
                audio2 = r.listen(source2)
                user_input = r.recognize_google(audio2)
                print("USER >>> " + user_input)
                return user_input

        except sr.UnknownValueError as e: return ""
        except sr.RequestError as e: return ""
        
def respond(chat):
    
    messages.append({
      'role': 'user',
      'content': chat,
    })

    save_latest(messages)
    
    stream = llm.chat(model=model, 
                         messages=messages,
                         stream=True)

    full_response = ""
    response = ""

  
    for chunk in stream:
        part = chunk['message']['content']
        print(part, end = '', flush = True)
         
        response += part
        full_response += part

        if (part == ".") or (part == "!") or (part == "?") or (part == ",") or (part == ";") or (part == ":") or (part == "\n"):
            voice.say(response)
            voice.runAndWait()
            response = ""
    
    messages.append({
        'role': 'assistant',
        'content': full_response,
    })
    
    save_latest(messages)

    print("")

while True:
    chat = input(">>> ")
    if chat == "/bye": break
    elif chat == "goodbye": messages = []
    elif len(chat) > 0: respond(chat)