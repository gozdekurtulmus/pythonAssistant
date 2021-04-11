import wikipedia
import wolframalpha
import pyttsx3
import keyboard
import speech_recognition as sr
import pygame
import datetime
import webbrowser
#from geopy.geocoders import Nominatim 
import requests
#import json
from googlesearch import search
from threading import Thread
import keyboard
import tkinter
from tkinter import*
import time


answer = ""
engine = pyttsx3.init()
pygame.mixer.init()



def send(event):
    #Sends the input user gives.
    
    input = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if input != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + input + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        
        command(input)
                    
            

#Appearence of the app
        
base = Tk()
base.title("Your Ultimate Genious Artificial Friend Y.U.G.A.F")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff')
SendButton.bind("<Button-1>", send)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

def botAnswer(answer):
    ChatLog.insert(END, "YUGAF: " + answer + '\n\n')
    ChatLog.config(state=DISABLED)
    ChatLog.yview(END)


def speak(audio):
    #Trying to avoid RuntimeError when the user keeps giving inputs.
    if engine.isBusy():
        engine.stop()
     
    engine.say(audio)
    engine.runAndWait()

def startThread(targetFunc,result):
    thread = Thread(target=targetFunc, args=(result,))
    thread.start()
    
    if not thread.isAlive():
        thread.join(not thread.isAlive())


def listen():
  
    #Now I'm adding the speech recognition feature.
    
    startThread(speak,"I'm listening.")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    #Now I'll catch the errors that we might get.
    try:
        command(input)
    except sr.UnknownValueError:
        speak("I couldn't understand what you're saying.")
        
    except sr.RequestError as e:
        answer = ("I couldn't request results for this; {0}.format(e)")
        botAnswer(answer)
        speak("Please check your internet connection. ")
        
def playSong(songName):
        pygame.mixer.music.load(songName)
        pygame.mixer.music.play()
    
            
def command(input):

      
    # Just for incase, I wanted to turn all of them to lower case.
    input = input.lower()

    if "talk" in input:
        listen()
        
    #Plays the wanted song.     
    if "play" in input:
                
        try:
            songName=input[5:]+".mp3"
            speak("That's a nice song choice.")
            startThread(playSong,songName) 
                        
        except:
            botAnswer("There is no song in that name.")
            startThread(speak,"I couldn't find the song.")

    #if ("stop") and ("song" or "music"):
     #   pygame.mixer.music.pause()

   # if ("resume" or "continue") and ("song" or "music"):
     #   pygame.mixer.music.unpause()
    

    #Shows the wanted location at google maps.
    elif ("where is" or "location of") in input:
        input = input.split(" ")
        startThread(speak,"I will show you the location on Google Maps. ")
        location=' '.join(input[2:])
        webbrowser.open('https://www.google.com/maps/place/' + location)

            
    #Gives us the current time as hour and minute. Like,'13:45'
    elif(input=="what time is it" or input=="time"):
        now= datetime.datetime.now()
        time=str(now.hour)+ ":" + str(now.minute)
        answer = "Local current time:" + time
        botAnswer(answer)
        startThread(speak,time)
        

    #Gives us the current day.Like, 2020-07-25
    #with controlling the length, i make sure that questions like "What day did Albert Einstein die/graduate/born" it doesnt just say the current day to us.
    elif("day" in input and len(input)<20):
        now=datetime.date.today()
        botAnswer(now)
        startThread(speak,now)
    

        
    #This will show the current weather.
    elif ("what is the weather" in input) :
        #using OpenWeather API. Got a key from there.
        key= "" #use your own key here
        weather_url="http://api.openweathermap.org/data/2.5/weather?q="
        try:
            input = input.split(" ")
            city= " ".join(input[5:])
        except:
            #Takes the current location to show weather.
            city= "Izmir"
            
        url = weather_url+city+"&appid="+key
        response = requests.get(url)
        if response.status_code== 200:
            data = response.json()
            main = data['main']
            temperature = round(main['temp']-273)
            report = data['weather']
            answer1= (f"Temperature : {temperature}")
            answer2=(f"Weather Report: {report[0] ['description']}")
            botAnswer(answer1)
            botAnswer(answer2)
            voiceAnswer= ("The weather in "+city+" is "+str(temperature)+" degrees.")
            startThread(speak,voiceAnswer)
            
        else:
            botAnswer("Error in the city name or HTTP request.")
            speak("Sorry.")
                      
        
    else:
    # I use Wolfram Alpha in try block and Wikipedia in except block.
        try:
            app_id = ""#use your own appid
            client = wolframalpha.Client(app_id)
            res= client.query(input)
            #To not get a spesific answer,graphic etc i need to make this.
            answer = next(res.results).text
            startThread(speak,answer)
            botAnswer(answer)
                
                
        except:
                #So, when the user says Who is or what is, it makes an error. To avoid this I split the input.
                #Also, I didn't want it to show all the article and read it. I made the asisstant only show 5 sentences and read the first one
            
            if "who is" in input:
                input2 = input.split(" ")
                if (len(input2)>2):
                    input2 = " ".join(input2[2:])
                    
                result=wikipedia.summary(input2,1)
                startThread(speak,result)
                botAnswer(wikipedia.summary(input2,3))

base.mainloop()
    
