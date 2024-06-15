import pyttsx3
import self
import speech_recognition as sr
import datetime
import os
import wikipedia
import pywhatkit
import pyautogui
import pyjokes
from youtube import youtube
import webbrowser as wb
from news import speak_news, getNewsUrl
import smtplib
import webbrowser
import pywhatkit as kit
from requests import get
from online import find_my_ip, send_email
import time
import imdb
import requests
from sys import platform
import os
import wmi
import openai


API_KEY = "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"
openai.api_key = API_KEY



wmi_service = wmi.WMI(namespace='wmi')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    

def commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source , duration=1)
        audio=r.listen(source)
    try:
        print("Wait for few moments...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You just said: {query}\n")
    except Exception as e:
        print(e)
        speak("Please tell me again")
        query="none"
    
    return query

def wishing():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        print("Good morning Boss")
        speak("Good morning Boss")
    elif 12 <= hour < 18:
        print("Good afternoon Boss")
        speak("Good afternoon Boss")
    else:
        print("Good evening Boss")
        speak("Good evening Boss")
    print("I am Jarvis. How can I assist you today?")    
    speak("I am Jarvis. How can I assist you today?")

def screenshot():
            img = pyautogui.screenshot()
            img.save("D:/PROJECT/SCREENSHOT/screen.jpeg")
    
def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)

def search_on_google(query):
    kit.search(query)

def chat_with_openai(user_message, chat_log):
    chat_log.append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log
    )
    assistant_response = response['choices'][0]['message']['content']
    print("JARVIS...:", assistant_response.strip("\n").strip())
    if "code" in user_message.lower():
        save_code(assistant_response.strip("\n").strip())
        speak("The code has been saved.")
    else:
        speak(assistant_response.strip("\n").strip())
    chat_log.append({"role": "assistant", "content": assistant_response.strip("\n").strip()})
    
def save_code(code):
    filename = "answer.txt"
    with open(filename, "a") as file:
        file.write(code + "\n\n")
    print("Code saved to", filename)

if __name__ == "__main__":
    wishing()
    chat_log = []
    while True:
        query = commands().lower()
        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak("Boss, The time is: " + strTime)
            print(strTime)

        if "how are you" in query:
                speak("I am absolutely fine sir. What about you")
        
            
        sleep_mode = False
        

        if 'open' in query:
            app_name = query.replace('open','')
            speak('opening '+ app_name)
            pyautogui.press('super')
            pyautogui.typewrite(app_name)
            pyautogui.sleep(0.5)
            pyautogui.press('enter')

        elif 'switch tab' in query:
            pyautogui.hotkey('crtl', 'tab')

        elif 'close tab' in query:
            pyautogui.hotkey('ctrl', 'w')   
       
        elif 'close' in query:
            pyautogui.hotkey('alt', 'f4')
            speak('Done Boss!')


        elif 'wikipedia' in query:
            speak("Searching in wikipedia")
            try:
                query=query.replace("wikipedia", '')
                results = wikipedia.summary(query, sentences=1)
                speak("According to wikipedia...")
                print(results)
                speak(results)
            except:
                print("No results found...")
                speak("No results found...")            
        
        elif 'play' in query:
            playquery=query.replace('play','')
            speak("Playing " + playquery)
            pywhatkit.playonyt(playquery) 
            
        elif 'type' in query:
            speak("please tell me what should i write")
            while True:
                typequery = commands().lower()
                if typequery == "exit typing":
                    speak("Done Boss")
                    break
                else:
                    pyautogui.write(typequery)
        
        elif 'minimize' in query or 'minimise' in query:
            pyautogui.moveTo(1232,15)
            pyautogui.leftClick()
            
        elif 'joke' in query:
            jarvisjoke = pyjokes.get_joke()
            print(jarvisjoke)
            speak(jarvisjoke)

        elif 'sleep' in query:
            speak('Ok boss, I am going to sleep but you can call me any time just say wake up and i will be there for you.')
            sleep_mode = True

        elif 'youtube download' in query or 'video download' in query:
            exec(open('youtube_downloader.py').read())
        
        elif "screenshot" in query:
            screenshot()
            speak("I've taken screenshot, please check it")
        
        elif "offline" in query or "exit" in query:
                quit()

        elif 'search on chrome' in query:
            speak('What do you want to search for?')
            search = commands()
            url = 'https://google.com/search?q=' + search
            webbrowser.get('chrome').open_new_tab(
                url)
            speak('Here is What I found for' + search)

        elif 'search on google' in query or 'search google' in query:
            speak('What do you want to search on Google, sir?')
            query = commands().lower()
            search_on_google(query)

        elif 'news' in query:
            speak('Of course sir..')
            speak_news()
            speak('Do you want to read the full news...')
            test = commands()
            if 'yes' in test:
                speak('Ok Sir, Opening browser...')
                wb.open(getNewsUrl())
                speak('You can now read the full news from this website.')
            else:
                speak('No Problem Sir')

        elif "remember that" in query:
            speak("What should I remember")
            data = commands()
            speak("You said me to remember that" + data)
            print("You said me to remember that " + str(data))
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        elif "do you remember anything" in query:
            remember = open("data.txt", "r")
            speak("You told me to remember that" + remember.read())
            print("You told me to remember that " + str(remember))

        elif "send whatsapp message" in query or 'send message' in query or 'whatsapp' in query:
            speak(
                'On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message sir?")
            message = commands().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")

        elif 'location' in query or 'where i am' in query or 'where am i' in query:
            speak('What is the location?')
            location = commands()
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get('chrome').open_new_tab(url)
            speak('Here is the location ' + location)

        elif 'what is your name' in query:
            speak('My name is JARVIS, i am ai voice assistant')

        elif 'github' in query:
            webbrowser.get('chrome').open_new_tab(
                'https://github.com/')
            
        elif 'chat gpt' in query or 'ai' in query:
            webbrowser.get('chrome').open_new_tab(
                'https://chat.openai.com/')
            
        elif 'voice' in query:
            if 'female' in query:
                engine.setProperty('voice', voices[0].id)
            else:
                engine.setProperty('voice', voices[1].id)
            speak("Hello Sir, I have switched my voice. How is it?")

        elif "send an email" in query:
                speak("On what email address do you want to send sir?. Please enter in the terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = commands().capitalize()
                speak("What is the message ?")
                message = commands().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error log")

        elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(
                    f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')

        elif "shutdown" in query:
            speak("Shutting down the system. Goodbye!")
            os.system("shutdown /s /t 1")
        elif "restart" in query:
                speak("Restarting the system. See you in a moment!")
                os.system("shutdown /r /t 1") 

        elif 'resume song' in query or 'stop song' in query:
                pyautogui.moveTo(955, 955, 0)
                pyautogui.click(x=955, y=955, clicks=1, interval=0,)
        
        elif 'like song' in query:
                pyautogui.moveTo(55, 310, 0)
                pyautogui.click(x=55, y=310, clicks=1, interval=0,)
                pyautogui.moveTo(170, 540, 0)
                pyautogui.click(x=170, y=540, clicks=1, interval=2,)

        elif 'take photo' in query or 'take video' in query:
                pyautogui.moveTo(1860, 520, 0)
                pyautogui.click(x=1860, y=520, clicks=1, interval=3,)
        
        elif 'video mode' in query or 'photo mode' in query:
                pyautogui.moveTo(1860, 455, 0)
                pyautogui.click(x=1860, y=455, clicks=1, interval=0,)

        elif 'turn on wi-fi' in query:
                pyautogui.moveTo(1670, 1050, 0)
                pyautogui.click(x=1670, y=1050, clicks=1, interval=0,)
                pyautogui.moveTo(1520, 570, 0.5)
                pyautogui.click(x=1520, y=570, clicks=1, interval=0,)

        elif 'turn on bluetooth' in query or 'turn off bluetooth' in query:
                pyautogui.moveTo(1670, 1050, 0)
                pyautogui.click(x=1670, y=1050, clicks=1, interval=0,)
                pyautogui.moveTo(1650, 570, 0.5)
                pyautogui.click(x=1650, y=570, clicks=1, interval=0,)

        elif 'turn on airplane mode' in query or 'turn off airplane' in query:
                pyautogui.moveTo(1670, 1050, 0)
                pyautogui.click(x=1670, y=1050, clicks=1, interval=0,)
                pyautogui.moveTo(1810, 570, 0.5)
                pyautogui.click(x=1810, y=570, clicks=1, interval=0,)

        elif 'increase brightness' in query:
            brightness = wmi_service.WmiMonitorBrightnessMethods()[0]
            brightness.WmiSetBrightness(100, 0)

        elif 'decrease brightness' in query:
            brightness = wmi_service.WmiMonitorBrightnessMethods()[0]
            brightness.WmiSetBrightness(0, 0)

        elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                text = commands()
                movies = movies_db.search_movie(text)
                speak("searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title}-{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline', 'plot summary not available')

                    print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
                          f"The plot summary of movie is {plot}")
                    
        elif "volume up" in query:
                pyautogui.press("volumeup")
        elif "volume down" in query:
                pyautogui.press("volumedown")
        elif "mute" in query:
                pyautogui.press("volumemute")
        elif "next" in query:
                pyautogui.press("nexttrack")
        elif "previous" in query:
                pyautogui.press("prevtrack")
                    
        else:
             if query =="none":
                  pass
             else:
                chat_with_openai(query, chat_log)
            
        while sleep_mode:
            query = commands().lower()
            print(query)
            if 'wake up' in query:
                speak('i am awake now. How can you help you Boss.')
                sleep_mode = False

        