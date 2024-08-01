import speech_recognition as sr  # used for speaking in computer microphone
import pyttsx3 as pt  # used to convert my voice into text
import webbrowser  # used to open webbrowser
import time  # used to control jarvis timing
import MUSIC # import my music url from other file
import requests # used to grt the request api of the site
from openai import OpenAI # used to search that it out of commad line

recogniizer = sr.Recognizer()   # make an object for my voice recohnizer
engine = pt.init()  # convert the voice recongnizer into the text
newsapi = "16df90485ebf43128ecb135c469d781a"  # this is my news api variable

def speak(text):  # this function will speak with you one on one
    engine.say(text) # its help to speak louding to you 
    engine.runAndWait() # after speaking its will wait for a while means give chance to user to undertsand anf speak


def AIProcess(commad): # will go to openai and such for your commad
    client = OpenAI(
    api_key="",  # your api key for openai
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant Jarvis, skilled in general talks like alexa and google cloud."},
        {"role": "user", "content": commad}
    ]
    )
    return (completion.choices[0].message)


def processCommad(c): # this function will do what you tell it to do according to its limit ( link open , songs , news ...)
    
    # links to open facebook , google , yahoo , youtube , linkdin ( while saying open in start ) 
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open yahoo" in c.lower():
        webbrowser.open("https://www.yahoo.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "linkdin song" in c.lower():
        webbrowser.open("https://www.linkdin.com")
    
    # play song which is store in MUSIC file as ( "one" , "two") --> you have to say ( play one , play two)
    elif c.lower().startswith("play"):  # if the statment start from ("play") --> which meant you have to play songs from file
        song = c.lower().split(" ")[1] # play song  --> its will break the words and store in list --> ["play","one"] --> you have to access list[1] --> one
        link = MUSIC.music[song] # than you give the index of that song which you get from above 
        webbrowser.open(link)    # and simply open the link of the song which you store in the MUSIC file in webbrowser
        
    # play news
    elif "news" in c.lower(): # if the text is "news" than this block of code will run
        r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2024-06-30&sortBy=publishedAt&apiKey={newsapi}") # request.get will go to the api and found the article and store in r variable
        if r.status_code ==200: # this status code =200 is the verification that your request has been satisfy
            data = r.json() # extracts and converts the JSON response from the API into a Python dictionary or list
            articles = data.get("articles",[])
            for article in articles:
                speak(article["title"])

    else:
        #let openAI handle the request of the user
        try:   
            output = AIProcess(c)
            speak(output)            
        except Exception as e:
            print("Error: ", e)    


if __name__ == "__main__":
    speak("Initializing Jarvis.......") # starting sentence of jarvis
    while True: # run till infinite
        r = sr.Recognizer() # user voice recognizer
        print("Recognizing.....") #print that its recoginizer the voice of user

        try:
            with sr.Microphone() as source:  # open mircophone and start litening the user
                print("Listening....") # indicate that it start litening
                audio = r.listen(source , timeout=3, phrase_time_limit=2) # it will start liten what you say
            word = r.recognize_google(audio) # with the help of google recongizer it will listen and store in variable
            if(word.lower()=="jarvis"): # if user said jarvis its will activate
                speak("Ya sir! How may i help you") # and said this line for you to commad more
                time.sleep(1) # take pause of 1 second after saying above line
                with sr.Microphone() as source: # again do the same for next commad
                    print("Jarvis Activate....") # indicate that the jarvisis activate now
                    audio1 = r.listen(source, timeout=3, phrase_time_limit=2) # listen the commad of the user
                    commad = r.recognize_google(audio1) # store into the variable 

                    processCommad(commad)  # pass the commad to the function to process the commad

        except Exception as e: # untill you are not saying jarvis its will run to avoid program crash
            print("Error, {0}".format(e)) # and display erroe ,meesage nor the actual error