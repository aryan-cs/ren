import speech_recognition as sr
import ollama
import cv2 as cv
import time
from threading import Thread





class ThreadedCamera(object):
    def __init__(self, src=0):
        self.capture = cv.VideoCapture(src, cv.CAP_DSHOW)
        self.capture.set(cv.CAP_PROP_BUFFERSIZE, 2)
       
        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)
        
        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(self.FPS)
            
    def show_frame(self):
        cv.imshow('frame', self.frame)
        key = cv.waitKey(self.FPS_MS)
        if key == ord('q'):  # Check if 'q' is pressed
            self.capture.release()  # Release the camera
            cv.destroyAllWindows()  # Close OpenCV windows
            exit()  # Exit the program








def transcribe_speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Set pause threshold for a faster response to speech
    recognizer.pause_threshold = 0.2  # Extremely responsive
    # Ensure non_speaking_duration is less than or equal to pause_threshold
    recognizer.non_speaking_duration = 0.1

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        # print("Please wait. Calibrating microphone...")
        # Listen for a short period to calibrate the energy threshold for ambient noise levels
        recognizer.adjust_for_ambient_noise(source, duration=1)
        # print("Calibrated. Please speak.")

        # Capture the audio
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google's speech recognition
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            # Error: recognizer could not understand the audio
            return None
        except sr.RequestError as e:
            # Error: could not request results from Google's speech recognition service
            return None

def ollama_response(input_text):
    
    response = ollama.chat(model='tinydolphin', messages=[
        {
            'role': 'user',
            'content': input_text,
        },
    ])
    return response['message']['content']
    
if __name__ == '__main__':
    src = 0
    threaded_camera = ThreadedCamera(src)
    while True:
        time = time.localtime
        try:
            threaded_camera.show_frame()
            
            text = transcribe_speech()
            if text:
                response = ollama_response(text)
                print(response)
                
        except AttributeError:
            pass
