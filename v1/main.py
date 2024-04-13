import ollama as llm
import speech_recognition as sr
import pyttsx3 as engine
from localstorage import get_history, add_history
from emotion import detect_emotion
model = "ren"

r = sr.Recognizer()
messages = get_history()
detected_emotion = "neutral"
voice = engine.init()
voice.setProperty('rate', 225)
voices = voice.getProperty('voices')

voice.setProperty('voice', voices[1].id)
voice.runAndWait()
emotions = []

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
    
def main():
    while True:
        emotions = detect_emotion()
        print(f"emotions: {emotions}")
        
        chat = record_text()
        if chat == "goodbye" or chat == "/bye":
            messages = []
            print("Goodbye! until Next time!")
            break
        elif len(chat) > 0: respond(f"{chat} NOTE: THE USER IS CURRENTLY FEELING {emotions}") 
        
if __name__ == "__main__":
    main()