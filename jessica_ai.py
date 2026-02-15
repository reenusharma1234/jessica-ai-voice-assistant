import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyautogui
import random
import pyjokes
import pywhatkit
import cv2
import threading
import time
import requests
import psutil
import smtplib
import platform

news_api_key = "your_news_api_key_here"
weather_api_key = "your_openweathermap_api_key_here"

EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_password"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"[Jessica]: {text}")
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jessica. Please tell me how I may help you.")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        print(" Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"[YOU SAID]: {query}")
        return query.lower()
    except:
        speak("Sorry, I didn't get that.")
        return "None"

def start_timer():
    speak("For how many seconds should I set the timer?")
    seconds = int(take_command())
    speak(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    speak("Time's up!")

def tell_date():
    today = datetime.date.today()
    speak(f"Today's date is {today.strftime('%B %d, %Y')}")

def battery_status():
    battery = psutil.sensors_battery()
    percent = battery.percent
    speak(f"Battery is at {percent} percent")

def system_info():
    sys = platform.uname()
    speak(f"System: {sys.system}, Node: {sys.node}, Version: {sys.version}")

def send_email():
    speak("Who should I send the email to?")
    receiver = input("Enter receiver's email: ")
    speak("What should be the subject?")
    subject = take_command()
    speak("What is the message?")
    message = take_command()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        body = f"Subject: {subject}\n\n{message}"
        server.sendmail(EMAIL_ADDRESS, receiver, body)
        server.quit()
        speak("Email sent successfully.")
    except:
        speak("Failed to send email.")


def get_weather():
    speak("Tell me the city name.")
    city = take_command()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(url).json()
    try:
        main = response['main']
        temp = main['temp']
        weather = response['weather'][0]['description']
        speak(f"The temperature in {city} is {temp}°C with {weather}")
    except:
        speak("Sorry, I couldn't fetch the weather report.")

def run_jessica():
    wish_me()
    while True:
        query = take_command()

        if query == "None":
            continue

        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except:
                speak("I couldn't find anything.")

        elif "open google" in query:
            webbrowser.open("https://google.com")

        elif "play music" in query:
            music_dir = 'C:\\Users\\Admin\\Downloads'
            songs = [s for s in os.listdir(music_dir) if s.endswith(('.mp3','.wav'))]
            if songs:
                os.startfile(os.path.join(music_dir, random.choice(songs)))
            else:
                speak("No music found.")

        elif "screenshot" in query:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(filename)
            speak(f"Screenshot saved as {filename}")

        elif "shutdown" in query:
            os.system("shutdown /s /t 1")

        elif "restart" in query:
            os.system("shutdown /r /t 1")

        elif "lock" in query:
            os.system("rundll32.exe user32.dll,LockWorkStation")

        elif "file" in query:
            speak("Name the file to search.")
            fname = take_command()
            for r, d, f in os.walk("C:\\"):
                for file in f:
                    if fname in file.lower():
                        os.startfile(os.path.join(r, file))
                        speak(f"Opening {file}")
                        return
            speak("File not found.")

        elif "joke" in query:
            speak(pyjokes.get_joke())

        elif "youtube" in query:
            speak("What should I play?")
            topic = take_command()
            pywhatkit.playonyt(topic)

        elif "alarm" in query or "reminder" in query:
            speak("Set alarm in HH:MM")
            alarm_time = take_command()
            h, m = map(int, alarm_time.split(":"))
            def alarm():
                while True:
                    now = datetime.datetime.now()
                    if now.hour == h and now.minute == m:
                        speak("Time to wake up!")
                        break
                    time.sleep(30)
            threading.Thread(target=alarm).start()

        elif "news" in query:
            try:
                url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}"
                data = requests.get(url).json()
                for i, a in enumerate(data['articles'][:5], 1):
                    speak(f"News {i}: {a['title']}")
            except:
                speak("Couldn't fetch news.")

        elif "calculate" in query:
            speak("Speak your calculation.")
            try:
                calc = take_command()
                result = eval(calc)
                speak(f"The answer is {result}")
            except:
                speak("I couldn't calculate that.")

        elif "quote" in query:
            try:
                q = requests.get("https://api.quotable.io/random").json()
                speak(q['content'])
            except:
                speak("Couldn't fetch quote.")

        elif "whatsapp" in query:
            speak("Enter phone number with country code:")
            phone = input("Phone: ")
            speak("Your message?")
            msg = take_command()
            speak("Hour?")
            hr = int(take_command())
            speak("Minute?")
            min = int(take_command())
            pywhatkit.sendwhatmsg(phone, msg, hr, min)
            speak("Message scheduled.")

        elif "camera" in query:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                filename = f"photo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, frame)
                speak(f"Photo saved as {filename}")
            cap.release()

        elif "date" in query:
            tell_date()

        elif "timer" in query:
            start_timer()

        elif "battery" in query:
            battery_status()

        elif "system info" in query:
            system_info()

        elif "email" in query:
            send_email()

        elif "weather" in query:
            get_weather()

        elif "time" in query:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {now}")

        elif "exit" in query or "stop" in query:
            speak("Goodbye!")
            break

        else:
            speak("I didn't catch that.")

if __name__ == "__main__":
    run_jessica()
