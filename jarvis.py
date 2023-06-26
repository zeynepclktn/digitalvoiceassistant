import pyttsx3  # pip install pyttsx3
import datetime
import speech_recognition as sre  # pip install SpeechRecognition
import smtplib
from email.message import EmailMessage
import webbrowser as wb
from time import sleep
import wikipedia  # pip install wikipedia
import pywhatkit
import requests
from newsapi import NewsApiClient  # pip install newsapi-python
import clipboard
import os
import pyjokes  # pip install pyjokes
import pyautogui  # pip install pyautogui
import string
import random
import psutil as ps  # pip install psutil
import ctypes
import sqlite3
from sqlite3 import Error
import tkinter as tk
from threading import Thread
import threading
from PIL import Image, ImageTk
from itertools import count, cycle
from cryptography.fernet import Fernet


veritabani_lock = threading.Lock()
breakartık = 0

class SpeechRecognition:
    def __init__(self):
        self.recognizer = sre.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[2].id)
        self.personal_asssistant = "Jarvis"
        self.text = ""

    def start_recognition(self, gui):
        self.wishme()
        gui.set_jarvis_text("What can I do for you?")
        while breakartık != 1:
            with sre.Microphone() as source:
                sr.speak("What can I do for you?")
                gui.changestatus_toListening()
                print("Listening...")
                audio = self.recognizer.listen(source)
            try:
                if breakartık==1:
                    break
                text = self.recognizer.recognize_google(audio, language='en-US')
                print("Recognizning: " + text)
                gui.set_user_text(text)
                main_func(text.lower())
            except sre.UnknownValueError:
                print("Sound not understood.")
            except sre.RequestError as e:
                print("API Error: {0}".format(e))
        gui.set_jarvis_text("See you soon!")

    def takeCommand(self, gui):
        while breakartık != 1:
            with sre.Microphone() as source:
                gui.changestatus_toListening()
                print("Listening...")
                audio = self.recognizer.listen(source)
            try:
                print("geldim1")
                if breakartık==1:
                    break
                print("geldim2")
                self.text = self.recognizer.recognize_google(audio, language='en-US')
                print("Recognizning: " + self.text)
                gui.set_user_text(self.text)
            except sre.UnknownValueError:
                print("Sound not understood.")
            except sre.RequestError as e:
                print("API Error: {0}".format(e))
            return self.text
        gui.set_jarvis_text("See you soon!")
    def speak(self, text):
        gui.changestatus_toTalking()
        gui.set_jarvis_text(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def wishme(self):
        self.speak("Welcome back sir!")
        self.greeting()
        sr.speak(sr.personal_asssistant + " at your service,")

    def wish(self):
        self.speak(" ")

    def greeting(self):
        hour = datetime.datetime.now().hour
        if 6 <= hour < 12:
            self.speak("Good morning")
        elif 12 <= hour < 18:
            self.speak("Good afternoon")
        elif 18 <= hour < 24:
            self.speak("Good evening")
        else:
            self.speak("Good night")
        # speak("You look beautiful as always, boss.")

    def changeAssistant(self):
        self.engine.setProperty('voice', self.voices[2].id)
        self.speak("Hello sir  .  I'm Jarvis.")
        self.engine.setProperty('voice', self.voices[1].id)
        self.speak("Hello sir. I'm Catherine.")
        self.engine.setProperty('voice', self.voices[0].id)
        self.speak("Which assistant do you want to continue with? Please say the assistant's name")
        gui.set_jarvis_text("1-Jarvis \n2-Catherine")
        print("""    
                    1-Jarvis 
                    2-Catherine. """)
        global personal_asssistant
        while True:
            query = self.takeCommand(gui).lower()
            try:
                if 'arvis' in query:
                    print("Jarvisi seçtin")
                    gui.changeAssistant_Jarvis()
                    self.engine.setProperty('voice', self.voices[2].id)
                    personal_asssistant = "Jarvis"
                    self.speak("Thank you for choosing me.")
                    return True
                elif 'atherine' in query:
                    print("Catherine seçtin")
                    gui.changeAssistant_Catherine()
                    self.engine.setProperty('voice', self.voices[1].id)
                    personal_asssistant = "Catherine"
                    self.speak("Thank you for choosing me.")
                    return True
            except Error as e:
                self.speak("I can't understand, please say it again")


sr = SpeechRecognition()
query = ' '
path_dictionary = {}
email_list = {}


class ImageLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
        sr.speak("I got a error boss")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        sr.speak("I got a error boss")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        sr.speak("I got a error boss")


class GUI:
    sr = SpeechRecognition()

    def __init__(self, master):
        self.master = master
        self.bg_image = tk.PhotoImage(file='deneme.png')
        # BUTTON IMAGE
        self.stopbutton_image = tk.PhotoImage(file="icons8-microphone-64.png")
        self.dataButton_button = tk.PhotoImage(file="icons8-input-50.png")
        self.global_option=0
        self.password=" "
        # LABEL IMAGE
        self.talking_status_image = tk.PhotoImage(file='talking.gif')
        self.listening_Status_image = tk.PhotoImage(file='listening.gif')
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.jarvis_image = tk.PhotoImage(file="male.png")
        self.catherine_image = tk.PhotoImage(file="female.png")
        self.stopbutton_image2 = tk.PhotoImage(file="stop.png")

        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.status = ImageLabel(root)
        self.status.pack()
        self.status.load("talking.gif")
        self.status.place(x=930, y=50)
        self.status.config(borderwidth=2,  bg="#01FFFF")

        self.assistant = tk.Label(root, image=self.jarvis_image, borderwidth=0, highlightthickness=0, bg="#000614")
        self.assistant.place(x=30, y=50)
        self.assistant_text = tk.Label(root, text=sr.personal_asssistant, font=('OCR A Extended', 12), bg='#000614',
                                       fg='#FFFFFF')
        self.assistant_text.place(x=60, y=180)

        self.continue_button = tk.Button(root, image=self.stopbutton_image, borderwidth=0, highlightthickness=0,
                                     bg="#000614", command= self.continueloop)

        self.stop_button = tk.Button(root, image=self.stopbutton_image2, borderwidth=0, highlightthickness=0,
                                     bg="#000614", command=self.stop)
        self.stop_button.place(x=1050, y=660)

        self.dataButton = tk.Button(root, image=self.dataButton_button, borderwidth=0, highlightthickness=0,
                                    bg="#000614", command=self.open_popup)
        self.dataButton.place(x=1150, y=660)

        self.jarvis_text = tk.Label(root, text="Jarvis", font=('OCR A Extended', 12), bg='#000614', fg='#FFFFFF')
        self.jarvis_text.place(relx=0.2, rely=0.1)
        self.jarvis_text.config(wraplength=550)

        self.user_text = tk.Label(root, text=" ", font=('OCR A Extended', 12), bg='#000614', fg='#FFFFFF')
        self.user_text.place(relx=0.2, rely=0.6)
        self.user_text.config(wraplength=550)
    def stop(self):
        self.stop_button.place_forget()
        self.status.place_forget()
        self.continue_button.pack()
        self.jarvis_text.config(text="See you soon!")
        self.user_text.config(text=" ")
        self.continue_button.place(x=1050, y=650)
        global breakartık
        breakartık=1

    def continueloop(self):
        self.continue_button.place_forget()
        self.jarvis_text.config(text="Welcome back!")
        self.status.place(x=930, y=50)
        self.stop_button.place(x=1050, y=660)
        global breakartık
        breakartık = 0
        main()


    def set_jarvis_text(self, text):
        self.jarvis_text.config(text=text)

    def set_user_text(self, text):
        self.user_text.config(text=text)

    def changestatus_toListening(self):
        self.status.load("listening.gif")

    def changestatus_toTalking(self):
        self.status.load("talking.gif")

    def changeAssistant_Jarvis(self):
        self.assistant.config(image=self.jarvis_image)
        self.assistant_text.config(text="Jarvis")
        sr.personal_asssistant = "Jarvis"
        self.assistant_text.place(x=60, y=180)

    def changeAssistant_Catherine(self):
        self.assistant.config(image=self.catherine_image)
        self.assistant_text.config(text="Catherine")
        sr.personal_asssistant = "Catherine"
        self.assistant_text.place(x=50, y=180)

    def open_popup(self):
        global breakartık
        breakartık=1
        self.status.place_forget()
        self.jarvis_text.config(text="See you soon!")
        self.user_text.config(text=" ")
        self.popup = tk.Toplevel(root)
        self.popup.geometry("300x300")
        self.popup.configure(bg='#000614')
        self.popup.title("Data Entry")
        self.popup.protocol("WM_DELETE_WINDOW", self.close_window)
        self.radio = tk.IntVar()
        self.option_1 = tk.Radiobutton(self.popup, text="Add Daha Path", variable=self.radio, value=1, bg="#000614",
                                       fg='#FFFFFF', command=lambda: self.select_option(1))
        self.option_2 = tk.Radiobutton(self.popup, text="Add E-Mail", variable=self.radio, value=2, bg="#000614",
                                       fg='#FFFFFF', command=lambda: self.select_option(2))
        self.option_1.pack(side="top", padx=10, pady=10)
        self.option_2.pack(side="top", padx=10, pady=10)

        self.entry1 = tk.Entry(self.popup)
        self.entry2 = tk.Entry(self.popup)
        self.email_name_label = tk.Label(self.popup, text="E-Mail User Name:", bg="#000614", fg='#FFFFFF')
        self.email_label = tk.Label(self.popup, text="E-Mail Address:", bg="#000614", fg='#FFFFFF')
        self.data_path_label = tk.Label(self.popup, text="Data Path:", bg="#000614", fg='#FFFFFF')
        self.data_name_label = tk.Label(self.popup, text="App Name:", bg="#000614", fg='#FFFFFF')
        ok_button = tk.Button(self.popup, text="Tamam", command=self.show_text, borderwidth=0, highlightthickness=0,
                              bg="#000614", fg='#FFFFFF')
        ok_button.pack(side="bottom", pady=10)
    def close_window(self):
        self.continue_button.place_forget()
        self.jarvis_text.config(text="Welcome back!")
        self.status.place(x=930, y=50)
        self.popup.destroy()
        global breakartık
        breakartık=0
        main()
    def show_text(self):
        try:
            data = self.entry1.get()
            name = self.entry2.get()
            values = "\"" + name + "\",\"" + data + "\")"
            print(self.global_option)
            if self.global_option == 2:
                insert_values = "INSERT INTO EMAIL(USER_NAME,EMAIL) VALUES (" + values
                email_list[name] = data
            elif self.global_option == 1:
                insert_values = "INSERT INTO PATH(APP_NAME,PATH) VALUES (" + values
                path_dictionary[name] = data
            veritabani_lock.acquire()
            execute_query(connection, insert_values)
            veritabani_lock.release()
            print(insert_values)
            global breakartık
            breakartık=0
            self.popup.destroy()
            self.status.place(x=930, y=50)
            main()
        except:
            sr.speak(" ")

    def select_option(self, option):
        self.radioption = option
        self.global_option = option
        if option == 1:
            self.option_2.config(state="disabled")
            self.data_path_label.pack(side="top", padx=10, pady=5)
            self.entry1.pack(pady=10, anchor="center")
            self.data_name_label.pack(side="top", padx=10, pady=5)
            self.entry2.pack(pady=10, anchor="center")
            self.email_name_label.pack_forget()
            self.email_label.pack_forget()
        elif option == 2:
            self.option_1.config(state="disabled")
            self.email_label.pack(side="top", padx=10, pady=5)
            self.entry1.pack(pady=10, anchor="center")
            self.email_name_label.pack(side="top", padx=10, pady=5)
            self.entry2.pack(pady=10, anchor="center")
            self.data_path_label.pack_forget()
            self.data_name_label.pack_forget()
    def email_password(self):
        self.popup = tk.Toplevel(root)
        self.popup.geometry("300x200")
        self.popup.configure(bg='#000614')
        self.popup.title("Password Entry")
        label_email = tk.Label(self.popup, text="Please enter your password",font=('OCR A Extended', 10), bg='#000614', fg='#FFFFFF')
        label_email.pack(pady=10, anchor="center")
        label_password = tk.Label(self.popup, text="Password:",font=('OCR A Extended', 10), bg='#000614', fg='#FFFFFF')
        label_password.pack(pady=10, anchor="center")
        self.entry_password = tk.Entry(self.popup, show="*")
        self.entry_password.pack(pady=10, anchor="center")

        login_button = tk.Button(self.popup, text="Enter", command=self.login, borderwidth=0, highlightthickness=0,
                              bg="#000614", fg='#FFFFFF')
        login_button.pack(pady=10, anchor="center")
    def login(self):
        self.password = cipher_suite.encrypt((self.entry_password.get()).encode("utf-8"))
        print(self.password)
        query="insert into crypt values ("+self.password+")"
        veritabani_lock.acquire()
        execute_query(connection,query)
        veritabani_lock.release()

        #plain_text = cipher_suite.decrypt(self.password)
        #print(plain_text.decode("utf-8"))
weeknumber = 0
months = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}

week_days = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}
msg = EmailMessage()
psw = " "
def insertdictionary():
    result = execute_read_query(connection, "SELECT APP_NAME,PATH FROM PATH")
    for veri in result:
        key = veri[0]
        value = veri[1]
        path_dictionary[key] = value
    result = execute_read_query(connection, "SELECT USER_NAME,EMAIL FROM EMAIL")
    for veri in result:
        key = veri[0]
        value = veri[1]
        email_list[key] = value


connection = create_connection("jarvis.db")
create_planner_table = """CREATE TABLE IF NOT EXISTS PLANNER (TASK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    WEEKNUMBER int,
                                    DAYNUMBER int,
                                    START_TIME time,
                                    END_TIME time,
                                    TASK_DETAIL varchar(255));"""
weeknumber = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month,
                           datetime.datetime.now().day).isocalendar().week
update_table = " DELETE FROM PLANNER WHERE WEEKNUMBER<" + str(weeknumber)

execute_query(connection, create_planner_table)
execute_query(connection, update_table)
insertdictionary()


def whatsupthisweek():
    select_query = "SELECT WEEKNUMBER,DAYNUMBER,TASK_DETAIL, START_TIME,END_TIME FROM PLANNER WHERE WEEKNUMBER=" + str(
        weeknumber)
    veritabani_lock.acquire()
    connection = create_connection("jarvis.db")
    query_result = execute_read_query(connection, select_query)
    veritabani_lock.release()
    sayac = len(query_result)
    for s in range(sayac):
        for i, k in week_days.items():
            if k == query_result[s][1]:
                day = i
        planning_detail = 'You have a plan to ' + query_result[s][2] + ' between ' + str(
            query_result[s][3]) + ' and ' + str(query_result[s][4]) + 'o\'clock on ' + day
        print(planning_detail)
        sr.speak(planning_detail)


def find_time():
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    print(Time)
    sr.speak("The current time is:")
    sr.speak(Time)


def date():
    year = str(datetime.datetime.now().year)
    month = datetime.datetime.now().month
    day = str(datetime.datetime.now().day)
    day_name = str(datetime.datetime.now().strftime('%A'))
    current_date = "The current date is: " + day + " " + str(months[month]) + " " + year + " " + day_name
    print(current_date)
    sr.speak(current_date)


def takeCommandCMD():
    query = input("please tell me how can i help you? \n")
    return query


def love():
    sr.speak("Love you too boss.")


def sendEmail(msg):
    if psw != " ":
        msg['From'] = "...@gmail.com" #MAIL ADDRESS
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("...@gmail.com", ) #MAIL ADDRESS, PASSWORD
        server.send_message(msg)
        sr.speak("Mail sended.")
        server.quit()
    else:
        gui.email_password()


def goodbye():
    sr.speak("Good bye sir")
    return 0


search_words = {"can", "could", "you", "please", "on", "on wikipedia", "on Wikipedia", "wikipedia", "search on",
                "search", "Wikipedia", "about", "for"}  # wikipedia


def searchwikipedia(answer):
    answer2 = ''
    str(answer).lower()
    for i in search_words:
        if i in str(answer):
            answer = str(answer).replace(i, "")
    sr.speak("I will search on wikipedia this sentence: \n ")
    sr.speak(answer)
    print(answer)
    sr.speak("If it right sentence? I'll waiting for answer, yes or no.")
    answer2 = sr.takeCommand(gui).lower()
    if 'yes' or 'Yes' in answer2:
        sr.speak("Searching on wikipedia...")
        try:
            result = wikipedia.summary(answer, sentences=2)
            print(result)
            sr.speak(result)
            sr.speak("I go back to main menu.")
        except:
            sr.speak("I can't find anything about this sentence. What can I search for you on wikipedia?")
            answer2 = sr.takeCommand(gui).lower()
            if 'don\'t' in answer2:
                sr.speak("I go back to main menu.")
            else:
                searchwikipedia(answer2)
    elif 'no' in answer2:
        sr.speak("Could you please say again, what would you search on wikipedia?")
        answer2 = sr.takeCommand(gui).lower()
        searchwikipedia(answer2)
    else:
        sr.speak("I didn't understand, I go back to main menu.")


def searchgoogle():
    try:
        sr.speak("What should I search for sir?")
        search = sr.takeCommand(gui).lower()
        wb.open('https://www.google.com/search?q=' + search)
    except:
        sr.speak("I got an error. I'm going back to the main menu.")


def news():
    try:
        newsapi = NewsApiClient(api_key='#KEY')
        data = newsapi.get_everything(language='en', page_size=3, q='news')
        newsdata = data['articles']
        for x, y in enumerate(newsdata):
            print(f'{y["title"]}{y["description"]}')
            sr.speak((f'{y["title"]}{y["description"]}'))
        sr.speak("that's it for now i'll update you in some time")
    except:
        sr.speak("I got an error. I'm going back to the main menu.")


def whatistheweather():
    city = 'Istanbul'
    try:
        while True:
            sr.speak('I am looking at the weather forecast for the city of {}'.format(city))
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=8c148c2ba7d4f1ac5ee61edd2f412c8d&units=metric'
            res = requests.get(url)
            data = res.json()
            weather = data['weather'][0]['main']
            temp = data['main']['temp']
            desp = data['weather'][0]['description']
            # temp= round((temp - 32 )*5/9)
            sr.speak(f'weather in {city} city is like')
            sr.speak('Temperature is {} degree celcius'.format(round(temp)))
            sr.speak('Weather is {}'.format(desp))
            sr.speak('Would you like to check the weather in another city?')
            query = sr.takeCommand(gui).lower()
            if 'yes' in query:
                sr.speak(' Please just say the name of the city.')
                query = sr.takeCommand(gui).lower()
                city = query
            elif 'no' in query:
                break
    except:
        sr.speak("I got an error. I'm going back to the main menu.")


def text2speech():
    text = clipboard.paste()
    sr.speak(text)


def screenshot():
    try:
        Time = datetime.datetime.now().strftime("%I.%M.%S")
        year = int(datetime.datetime.now().year)
        month = int(datetime.datetime.now().month)
        day = int(datetime.datetime.now().day)
        name_img = str(day) + '.' + str(month) + '.' + str(year) + '.' + Time
        name_img = f'C:\\Users\\{name_img}.png'
        img = pyautogui.screenshot(name_img)
        img.show()
    except:
        sr.speak("I got an error. I'm going back to the main menu.")


def passwordgen():
    s1 = string.ascii_uppercase
    s2 = string.ascii_lowercase
    s3 = string.digits
    s4 = string.punctuation

    passlen = 8
    s = []
    s.extend(list(s1))
    s.extend(list(s2))
    s.extend(list(s3))
    s.extend(list(s4))

    random.shuffle(s)
    newpass = ("".join(s[0:passlen]))
    print(newpass)
    sr.speak(newpass)


def flip():
    sr.speak("Okey sir, flipping a coin")
    sleep(1)
    coin = ['heads', 'tails']
    toss = []
    toss.extend(coin)
    random.shuffle(toss)
    toss = ("".join(toss[0]))
    sr.speak("I flipped the coin and result is : \n" + toss)


def roll():
    sr.speak("I rolling a die for you \n\n")
    sleep(1)
    die = ['1', '2', '3', '4', '5', '6']
    roll = []
    roll.extend(die)
    random.shuffle(roll)
    roll = ("".join(roll[0]))
    sr.speak("I rolling a die and result is : \n" + roll)


def cpu():
    try:
        usage = str(ps.cpu_percent())
        print('cpu:' + usage)
        sr.speak('CPU is at \n' + usage)
        battery = ps.sensors_battery()
        print(battery)
        if battery != None:
            sr.speak('Battery is at \n')
            sr.speak(battery)
        else:
            sr.speak("You didn't have a battery sir.")
    except:
        sr.speak("I got an error. I'm going back to the main menu.")


def planner(querys):
    try:
        dayofnumber = int(finddaynumber(querys))
        weeknumber = int(findweeknumber(querys))
        meeting_time = getstartingtime(querys)
        ending_time = getendingtime(meeting_time)
        sr.speak("What is the name of the meeting?")
        meeting_name = sr.takeCommand(gui).lower()
        print(weeknumber, meeting_time, ending_time, meeting_name, dayofnumber)
        variables = str(weeknumber) + ",\"" + str(meeting_time) + "\",\"" + str(ending_time) + "\",\"" + str(
            meeting_name) + "\"," + str(dayofnumber)
        print(variables)
        create_plans = "INSERT INTO PLANNER(WEEKNUMBER,START_TIME,END_TIME,TASK_DETAIL,DAYNUMBER) VALUES (" + variables + ")"
        veritabani_lock.acquire()
        connection = create_connection("jarvis.db")
        execute_query(connection, create_plans)
        veritabani_lock.release()
        sr.speak("I added it to your agenda, sir.")
    except:
        sr.speak("I got an error. I'm going back to the main menu.")


def findweeknumber(querys):
    weeknumber = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month,
                               datetime.datetime.now().day).isocalendar().week
    todaynumber = int((datetime.datetime.now().strftime('%U'))[1]) - 1
    dayofnumber = finddaynumber(querys)
    if dayofnumber >= todaynumber:
        temp = dayofnumber - todaynumber
    else:
        temp = int(todaynumber) - dayofnumber
        weeknumber += 1  # week
    return weeknumber


def finddaynumber(querys):
    for i in week_days:
        if i in querys:
            dayofnumber = week_days[i]  # gün ismi
    return dayofnumber


def getstartingtime(querys):
    sayac = 0
    words = querys.split()
    for i in words:
        if 'at' == i:
            meeting_time = words[sayac + 1]
        sayac += 1
    sr.speak("Meeting starting time:")
    sr.speak(meeting_time)
    return meeting_time


def getendingtime(meeting_time):
    bayrak = 0
    for i in meeting_time:
        if i == ":":
            bayrak = 1

    if bayrak == 1:
        timesplit = meeting_time.split(":")
        ending_time = str(int(timesplit[0]) + 1) + ":" + timesplit[1]  # be smarter
    else:
        ending_time = int(meeting_time) + 1
    sr.speak("Meeting ending time:")
    sr.speak(ending_time)
    return ending_time


def addFace():
    try:
        sr.speak("Press ESC when you're ready.")
        from facerecog import takePhoto
        if(sr.personal_asssistant == "Jarvis"):
            takePhoto("Facedetect",2)
        else:
            takePhoto("Facedetect", 1)
        sr.speak("Added new face recognition")
    except:
        sr.speak("I got an error. I'm going back to the main menu.")


def reminderthat(query):
    try:
        my_string = query.split("that", 1)
        print(my_string)
        sr.speak("You said me to remember that " + my_string[1])
        remember = open('data.txt', 'w')
        remember.write(my_string[1])
        remember.close()
    except:
        sr.speak("I got an error. I'm going back to the main menu.")


def main_func(query):
    if 'time' in query:
        find_time()
    elif 'face' in query:
        addFace()
    elif 'date' in query:
        date()
    elif 'love' in query:
        love()
    elif 'change assistan' in query:
        sr.changeAssistant()
    elif 'email' in query:
        try:
            sr.speak("To whom you want to send the e-mail? ")
            name = sr.takeCommand(gui).lower()
            msg['To'] = email_list[name]
            sr.speak("What is the subject of the mail?")
            msg['Subject'] = sr.takeCommand(gui).lower()
            sr.speak("What sould I say?")
            content = sr.takeCommand(gui).lower()
            msg.set_content(content)
            addPasword()
            sendEmail(msg)
        except Exception as e:
            print(e)
            sr.speak("Unable to end the mail")
    elif 'wikipedia' in query:
        searchwikipedia(query)
    elif 'search' in query:
        searchgoogle()
    elif 'offline' in query:
        goodbye()
        # break
    elif 'youtube' in query:
        sr.speak("What should I search for on youtube?")
        topic = sr.takeCommand(gui).lower()
        pywhatkit.playonyt(topic)
    elif 'weather' in query:
        whatistheweather()
    elif 'news' in query:
        sr.speak('I am looking at news for you.')
        news()
    elif 'read' in query:
        text2speech()
    elif 'open' in query:
        try:
            query_list = query.split()
            indexnumber = query_list.index("open")
            app = query_list[indexnumber + 1]
            print(app)
            codepath = path_dictionary[app]
            sr.speak("Opening {}".format(app))
            sleep(0.5)
            os.startfile(codepath)
        except Exception as e:
            print(e)
            sr.speak("Unable instruction")
    elif 'joke' in query:
        joke = pyjokes.get_joke()
        sr.speak(joke)
        print(joke)
    elif 'screenshot' in query:
        screenshot()
    elif 'remember' in query:
        remember = open('data.txt', 'r')
        sr.speak("you told me to remember that " + remember.read())
    elif 'remind' in query:
        reminderthat(query)
    elif 'password' in query:
        passwordgen()
    elif 'flip' in query:
        flip()
    elif 'roll' in query:
        roll()
    elif 'cpu' in query:
        cpu()
    elif "where is" in query:
        query = query.replace("where is", "")
        location = query
        sr.speak("User asked to Locate")
        sr.speak(location)
        wb.open("https://www.google.com/maps/place/" + location + "")
    elif 'lock window' in query:
        sr.speak("locking the device")
        ctypes.windll.user32.LockWorkStation()
    elif 'calendar' in query:
        planner(query),
    elif 'week' in query:
        whatsupthisweek()
    else:
        sr.speak("I didn't understand, sorry boss. Please say again")


def start_speech_recognition(gui):
    sr = SpeechRecognition()
    sr.start_recognition(gui)


def main():
    sr = SpeechRecognition()
    sr.wish()
    speech_thread = Thread(target=start_speech_recognition, args=(gui,))
    speech_thread.start()
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x800")
    root.title("Digital Virtual Assistant")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 1280) // 2
    y = (screen_height - 800) // 2
    root.geometry(f"+{x}+{y}")
    gui = GUI(root)
    main()
