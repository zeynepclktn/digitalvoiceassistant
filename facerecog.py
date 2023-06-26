import cv2
import face_recognition
from deepface import DeepFace
import tkinter as tk
from pygame import *
import pyttsx3  # pip install pyttsx3
import random
from threading import Thread
import threading
import os
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
emotion=" "
veritabani_lock = threading.Lock()


happy=["Your radiant smile just brightened up my day.","glad to see you! Your happy face is contagious.","Your beaming happiness is like a ray of sunshine.","Well, hello! Your cheerful demeanor is a wonderful sight to behold.","You look very happy, boss. Did I mention how beautiful you look when you smile?"]
angry=["I can sense a bit of frustration. Take a deep breath, and let's tackle this together.","You look angry boss. You should drink chamomile tea.","Although I sense some anger, remember that I'm here to help and support you.","I can see that something's bothering you. Take a moment to relax, and let's find a solution.","I noticed a hint of irritation on your face. Let's take a moment to address any concerns you have."]
fear =["You look scared. Don't be afraid because I'm always there to protect you","I can sense a bit of fear in your expression. Don't worry, I'm here to provide reassurance and support.","Your anxious look tells me you might be feeling scared. Remember, I'm here to help and keep you safe.","HI can see a hint of fear in your eyes. Don't be afraid, I'll do my best to make you feel secure.","I noticed a sense of unease on your face. Just know that I'm here to alleviate your fears and offer guidance."]
sad =["Hey, you look sad. Tell whoever upset you and I'll send a virus to their computer!","I can see a hint of sadness in your expression. Remember, I'm here to listen and offer support if you'd like to talk.","Your downcast look tells me something might be bothering you. Feel free to share what's on your mind, and I'm here to lend an ear."," I noticed a tinge of sadness on your face. If there's anything I can do to help or if you want to talk, know that I'm here for you.","it seems like something's troubling you. Don't hesitate to reach out if you need a comforting conversation or any assistance."]
surprise =["Your look of surprise caught my attention. Is there anything I can assist you with?","You look surprised, I hope it's nothing bad"," Your expression of astonishment has piqued my curiosity. How can I be of help to you today?"," I can see you're taken aback by something. Don't worry, I'm here to provide any information or support you may need.","Your look of disbelief has intrigued me. Feel free to share what has surprised you, and I'll do my best to assist you."]
neutral = ["It's great to see you looking your usual self today.","You look so beautiful boss"," You have a calm and composed expression today.","You're looking perfectly normal and ready for whatever comes your way.","Your neutral expression tells me that you're in a relaxed state."]

class GUI:
    def __init__(self, master):
        self.master = master
        self.bg_image = tk.PhotoImage(file='facerecog.png')


        self.bg_label = tk.Label(new_root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.jarvis_image = tk.PhotoImage(file="male.png")
        self.assistant = tk.Label(new_root, image=self.jarvis_image, borderwidth=0, highlightthickness=0, bg="#000614")
        self.assistant.place(x=30, y=50)
        self.assistant_text = tk.Label(new_root, text="Assistant", font=('OCR A Extended', 12), bg='#000614',
                                       fg='#FFFFFF')
        self.assistant_text.place(x=50, y=180)
        self.jarvis_text = tk.Label(new_root, text="Waiting connection...", font=('OCR A Extended', 12), bg='#000614', fg='#FFFFFF')
        self.jarvis_text.place(relx=0.3, rely=0.25)
        self.jarvis_text.config(wraplength=550)
    def set_jarvis_text(self, text):
        self.jarvis_text.config(text=text)

def emotions(emotion):
    engine.setProperty('voice', voices[2].id)
    if emotion == "happy":
        random_element = random.choice(happy)
        speak(random_element)
    elif emotion == "angry":
        random_element = random.choice(angry)
        speak(random_element)
    elif emotion == "fear":
        random_element = random.choice(fear)
        speak(random_element)
    elif emotion == "sad":
        random_element = random.choice(sad)
        speak(random_element)
    elif emotion == "surprise":
        random_element = random.choice(surprise)
        speak(random_element)
    elif emotion == "neutral":
        random_element = random.choice(neutral)
        speak(random_element)
    speak("Redirecting to main program...")
    time.sleep(1)
    new_root.withdraw()
    os.system('python jarvis.py')
    new_root.destroy()
def others():
    known_image = face_recognition.load_image_file("Facedetect.png")
    unknown_image = face_recognition.load_image_file("Facedetect2.png")

    zeynep_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces([zeynep_encoding], unknown_encoding)

    if results[0]:
        engine.setProperty('voice', voices[2].id)
        speak("access granted")
        gui.assistant_text.config(text="Jarvis")
        gui.assistant_text.place(x=60, y=180)
        img_path = "Facedetect2.png"
        obj = DeepFace.analyze(img_path="Facedetect2.png", actions=['age', 'gender', 'race', 'emotion'])
        print(obj[0]['age'])
        print(obj[0]['dominant_emotion'])
        emotion = obj[0]['dominant_emotion']
        emotions(emotion)

    elif not results[0]:
        speak("access denied")
        mixer.init()
        mixer.music.load('ses.ogg')
        mixer.music.play()
        while mixer.music.get_busy():
            time.Clock().tick(10)

def speak(text):
    gui.set_jarvis_text(text)
    engine.say(text)
    engine.runAndWait()

def takePhotoLocal(filename):
    engine.setProperty('voice', voices[0].id)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    speak("Hello, welcome to the digital voice assistant program. I need to take your photo so I can verify your identity. Please press ESC when you are ready.")

    while True:
        result, image = cam.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow(filename, image)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            cv2.imwrite((filename + ".png"), image)
            cv2.destroyWindow(filename)
            break
    others()

def takePhoto(filename,voice):
    engine.setProperty('voice', voices[voice].id)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    while True:
        result, image = cam.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow(filename, image)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            cv2.imwrite((filename + ".png"), image)
            cv2.destroyWindow(filename)
            break

def main():

    new_root.geometry("900x400")
    new_root.title("Digital Virtual Assistant")
    screen_width = new_root.winfo_screenwidth()
    screen_height = new_root.winfo_screenheight()
    x = (screen_width - 900) // 2
    y = (screen_height - 400) // 2
    new_root.geometry(f"+{x}+{y}")

    speech_thread = Thread(target=takePhotoLocal, args=("Facedetect2",))
    speech_thread.start()
    new_root.mainloop()

if __name__ == "__main__":
    new_root = tk.Tk()
    gui = GUI(new_root)
    main()

