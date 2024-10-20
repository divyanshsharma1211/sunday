import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import smtplib
import requests
import wolframalpha

# Initialize the voice engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak('Welcome, guest.')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception:
        print("Didn't get that, please try again.")
        speak("Didn't get that, please try again.")
        return "None"

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Make sure to use secure methods to store credentials
        server.login('your_email@gmail.com', 'your_password')
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send this email.")

def getWeather(city_name):
    api_key = "your_api_key"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city_name}"
    response = requests.get(complete_url)
    return response.json()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'who created you' in query:
            speak('I was created by Divyansh Sharma.')

        elif 'who are you' in query:
            speak('I am Sunday, an artificial intelligence created by Divyansh Sharma.')

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'news' in query:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India. Happy reading.')

        elif 'search' in query:
            statement = query.replace("search", "")
            webbrowser.open_new_tab(statement)

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'send a mail' in query:
            speak("What should I say?")
            content = takeCommand()
            to = "recipient_email@gmail.com"  # Change to the recipient's email
            sendEmail(to, content)

        elif 'weather' in query:
            speak("What's the city name?")
            city_name = takeCommand()
            weather_data = getWeather(city_name)
            if weather_data["cod"] != "404":
                main = weather_data["main"]
                current_temperature = main["temp"]
                current_humidity = main["humidity"]
                weather_description = weather_data["weather"][0]["description"]
                speak(f"Temperature in Kelvin is {current_temperature}, humidity is {current_humidity}%, and the description is {weather_description}.")
                print(f"Temperature: {current_temperature}K, Humidity: {current_humidity}%, Description: {weather_description}")
            else:
                speak("City not found.")
