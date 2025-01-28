from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import pyjokes
import urllib.request
import urllib.parse
import re
import pyowm
import random
# import openai

# Add your API keys and credentials here
# WOLFRAMALPHA_APP_ID = "EY5VAP-TAGVJU8QQY"
# OPENWEATHERMAP_API_KEY = "58b09f7bb3e32aef5c34a63698dcc6e5"
#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

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index to select a different voice

# Set activation word
activationword = 'sirius'

# Register Chrome browser
chrome_path = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# Initialize Wolfram Alpha client
# wolframClient = wolframalpha.Client(WOLFRAMALPHA_APP_ID)

# Initialize OpenWeatherMap client
# owm = pyowm.OWM(OPENWEATHERMAP_API_KEY)

def speak(text, rate=120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command..')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech..')
        query = listener.recognize_google(input_speech, language='en-US')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'

    return query

def search_wikipedia(query=''):
    try:
        wikipage = wikipedia.page(query)
        wikisummary = wikipage.summary
        return wikisummary
    except wikipedia.exceptions.DisambiguationError as e:
        # If there are multiple results, return the summary of the first result
        wikipage = wikipedia.page(e.options[0])
        wikisummary = wikipage.summary
        return wikisummary
    except wikipedia.exceptions.PageError as e:
        # If the page does not exist, return an error message
        speak(f"Page '{query}' does not exist on Wikipedia.")
        print(f"Page '{query}' does not exist on Wikipedia.")
        return f"Page '{query}' does not exist on Wikipedia."
    except Exception as e:
        # Handle any other exceptions that might occur
        speak("Sorry, I encountered an error while searching Wikipedia.")
        print(f"Error searching Wikipedia: {e}")
        return None


def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframalpha(query=''):
    response = wolframClient.query(query)

    if response['@success'] == 'false':
        return 'could not compute.'

    else:
        results = ''
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]

        if (results in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            results = listOrDict(pod1['subpod'])
            return results.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            return question.split('(')[0]

            speak('computation failed. Querying universal databank')
            return search_wikipedia(question)

def get_weather(city):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather

    temperature = weather.temperature('celsius')['temp']
    description = weather.detailed_status
    print(f"The weather in  {city} is {description} with a temperature of {temperature} degrees Celsius.")
    return f"The weather in  {city} is {description} with a temperature of {temperature} degrees Celsius."

def play_youtube_video(query):
    # Construct the YouTube search query
    search_query = ' '.join(query)
    # Encode the search query
    search_query_encoded = urllib.parse.quote(search_query)
    # Construct the YouTube search URL
    url = f"https://www.youtube.com/results?search_query={search_query_encoded}"
    # Open the URL in Chrome browser
    webbrowser.get('chrome').open_new(url)
    # Speak the action
    speak(f"Opening YouTube and searching for {search_query}")

def get_joke():
    joke = pyjokes.get_joke(language="en", category="neutral")
    return joke

if __name__ == '__main__':
    print("Hi sir , I am your friendly assistant.")
    print("what can i do for you sir?")
    speak('Hi sir , I am your friendly assistant.')
    speak("what can i do for you sir?")
    
    while True:
        query = parseCommand().lower().split()

        # Skip processing if the query is empty or matches the activation word
        if not query or query[0] == activationword:
            continue
        if 'your' in query and 'name' in query:
            speak("my name is"+ activationword + " What is your name sir?")
            print("my name is"+ activationword + ". "+" What is your name sir?")

        if 'meaning'  in query and "of" in query:
            speak(" Sirius comes from the Ancient Greek Seirios, which means glowing or scorcher. Sirius is the brightest star in the Earth's night sky and is located in the constellation Canis Major. It is also known colloquially as the Dog Star ")
            print(" Sirius comes from the Ancient Greek Seirios, which means glowing or scorcher. Sirius is the brightest star in the Earth's night sky and is located in the constellation Canis Major. It is also known colloquially as the Dog Star ")

        if 'question' in  query or 'questions' in  query:
            speak("yes sir,Tell what do you want?")
            print("yes sir , Tell what do you want?")
              
        if ('my' in query and 'name' in query) or (' Iam' in query):
            speak("greeting sir")
            print("greeting sir")

        if 'what' in query and 'about' in query and 'you' in query :
            speak("I am good")
            speak("what about you sir")
            print("I am good")
            print("what about you sir?")
        
        if 'good' in query or 'fine' in query or 'well' in query :
            speak("That's my pleasure sir")
            print("That's my pleasure sir")
        
        if "father" in query:
            speak('my fathers are sridhar , prabhu,harish,sam naveen')

        if 'tell' in query and 'me' in query and 'about' in query and 'you' in query or 'yourself' in query :
            speak("my name is " + activationword + " " + " i am 2024 model, me was created by a mini project group who are called as sridhar,prabhu,sam,harish. I am here to give you information")
            speak("Tell me what information do you want from me sir?")
            print("my name is " + activationword + "i am 2024 model, me was created by a mini project group who are called as sridhar,prabhu,sam,harish. I am here to give you information")
            print("Tell me what information do you want from me sir?")
        
        # List command
        if 'hello' in query:
            speak('Greetings, all.')
            print('Greetings,all')
        else:
            query.pop(0)
            speech = ' '.join(query)

            # Navigation
        if 'go' in query or 'open' in query:
            speak('Opening....')
            print("Opening ...")
            query = ' '.join(query[1:])
            webbrowser.get('chrome').open_new(query)

            # Wikipedia search
        if ('information' in query) or ("mean"in query and "by" in query):
            query = ' '.join(query[4:])
            speak('Querying the universal databank.')
            results = search_wikipedia(query)
            if results:
                print("Here's what I found:")
                print(results)
                speak("Here's what I found:")
                speak(results)
            else:
                print("Sorry, I couldn't find any information on that.")
                speak("Sorry, I couldn't find any information on that.")

        # Wolfram Alpha computation
        if query and (query[0] == 'compute' or query[0] == activationword):
            query = ' '.join(query[1:])
            speak('Computing..') 
            try:
                results = search_wolframalpha(query)
                print(results)
                speak(results)
            except:
                speak('Unable to compute.')

        # Weather information
        if len(query) >= 6 and query[0]=='what' and query[1]=='is' and query[2]=='the' and query[3]=='weather' and query[4]=='condition' and query[5]=='of':
            city = ' '.join(query[6:])  # Fixed this line
            speak(get_weather(city))

        if 'play' in query:
            # Extract the specific genre mentioned
            genre_index = query.index('play') + 1
            genre_query = query[genre_index:]
            # Play the YouTube video based on the genre query
            play_youtube_video(genre_query)
                
        # Get a joke
        if 'joke' in query or 'jokes' in query :
            joke = get_joke()
            speak(joke)
            print(joke)

        # Note taking
        if  'note' in query or 'notes' in query:
            query = ' '.join(query[3:])
            speak('Ready to record your note')
            newNote = parseCommand().lower()
            now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            with open('note_%s.txt' % now, 'w') as newFile:
                newFile.write(newNote)
            speak('Note written')
            print(newFile)

        if any(word in query for word in ['goodbye', 'bye', 'exit', 'quit', 'stop', 'later', 'end', activationword + ' exit']):
            speak('Thank you')
            print('Thank you')
            break
            