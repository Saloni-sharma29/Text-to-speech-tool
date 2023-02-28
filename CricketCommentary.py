from cProfile import label
from hashlib import new 
from tkinter import *
from tkinter import ttk 
from webbrowser import get
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import speech_recognition as sr
# how to convert text to speech
import pyttsx3
# convert text to pdf
from fpdf import FPDF
from tkinter.filedialog import *
#text-to-speech 
import re
import wave
import pyaudio
import _thread
import time

root = Tk()
# Set the background colour of GUI window 
# Set the configuration of GUI window (WidthxHeight) 
width=root.winfo_screenwidth()
height=root.winfo_screenheight()

root.geometry("%dx%d" % (width, height))
# set the name of tkinter GUI window 
root.title("Cricket Commentary: User's Voice")
root.configure(bg='ghost white')
Label(root, text='Designing a Prototype model of English Text-to-Speech system in User voice', fg='black' ,font='arial 12 bold').pack(pady=20)

#left text box TTS
textTTS= Text(root, height=20, width=60)
textTTS.place(x=30, y=160)
Label(root, text= "Text-to-Speech", fg='black' ,font='arial 12 bold').place(x=225 ,y=132)
#TTSbtn=Button(text='Text-To-Speech', width=14, height=2).place(y=550, x=180)
#VolBtn=Button(text='Volume', width=14, height=2).place(y=550 ,x=250)

#right text box STT
textSTT= Text(root,height=10, width=60)
textSTT.place(x=750, y=150)
textsumm=Text(root, height=10, width=60)
textsumm.place(x=750, y=400)
Label(root, text= "Speech-to-Text", fg='black' ,font='arial 12 bold').place(x=950 ,y=120)
#listenBtn=Button(text='Start Listening', command=listenn, width=14, height=2).place(y=550, x=920)
#SummaryBtn=Button(text='View Report Summary', width=18, height=2).place(y=600, x=820)
#ReportBtn=Button(text='Download Report', width=16, height=2, command=report).place(y=600, x=990)
def delete():
    textTTS.delete("1.0","end")
DeleteButton1= Button(text="Clear", width=10, height=2, command= delete).place(y=550, x=400)
#DeleteButton2= Button(text="Clear", width=10, height=2, command= delete).place(y=320, x=990)

def listenn():
    r=sr.Recognizer()
    def SpeakText(command):
        
        # Initialize the engine
        engine = pyttsx3.init('dummy')
        engine.say(command)
        engine.runAndWait()
        
        
    # Loop infinitely for user to speak

    while(1):	
        
        # Exception handling to handle
        # exceptions at the runtime
        try:
            
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                #listens for the user's input
                audio2 = r.listen(source2)
                # Using ggogle to recognize audio
                MyText = r.recognize_google(audio2)
                                
                MyText = MyText.lower()

                print(MyText)
                SpeakText(MyText)
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("Say Someting")
        textSTT.insert("end", r.recognize_google(audio2))

listenBtn=Button(text='Start Listening', command=listenn, width=14, height=2).place(y=320, x=930)


stopwords=set(stopwords.words('english'))
def summmary():
    text= textSTT.get("1.0","end")
    #print(text)
    #tokenizing text
   
    words= word_tokenize(text)

    #frequency table : if word come for the first time in frequency table, then its occurance will be counted as 1 otherwise its count incremented by 1
    #in dict, word is key and its value is the number of times its occurance
    freqtable=dict()
    for word in words:
        word=word.lower()
        if word in stopwords:
            continue
        if word in freqtable:
            freqtable[word]+=1

        else:
            freqtable[word]=1
    #crearing dictionary to keep score of each sentance
    sentances=sent_tokenize(text)
    sentanceValue=dict()

    for sentance in sentances:
        for word, freq in freqtable.items():
            if word in sentance.lower():
                if sentance in sentanceValue:
                    sentanceValue[sentance]+=freq
                else:
                    sentanceValue[sentance]=freq

    sumValue=0
    for sentance in sentanceValue:
        sumValue+= sentanceValue[sentance]    

    average= int(sumValue/len(sentanceValue))

    summary=''
    for sentance in sentances:
        if(sentance in sentanceValue) and (sentanceValue[sentance]>(1.2*average)):
            summary+=' '+sentance

    #textSTT.delete(self, '1.0', 'END')
    textsumm.insert("1.0", summary)


SummaryBtn=Button(text='View Report Summary', width=18, height=2, command=summmary ).place(y=567, x=845)

 
#saving the summarized report
def report():
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.cell(200,20, txt= "Cricket Summarized Report", ln=1, align='C')
    #print(textsumm.get('1.0', END))
    #pdf.cell(200,20, txt=textsumm.get('1.0', END) , ln=2, align="C" )
    #pdf.multi_cell(200,20, txt=textsumm.get('1.0', END),border=0, align='J')
    pdf.multi_cell(h=15.0, align='L', w=0, txt=textsumm.get('1.0', END), border=0)

    pdf.output(asksaveasfilename(filetypes=[("PDF file", "*.pdf")]), "F")
ReportBtn=Button(text='Download Report', width=16, height=2, command=report).place(y=567, x=990)
Label(root, text= "View Summary and Download Report", fg='black' ,font='arial 12 bold').place(x=850 ,y=373)
class TextToSpeech:
    
    CHUNK = 1024

    def __init__(self,words_pron_dict:str = 'F:/Python tutorial/TTS/cmudict-0.7b.txt'):
        self._l = {}
        self._load_words(words_pron_dict)

    def _load_words(self, words_pron_dict:str):
        with open(words_pron_dict, 'r') as file:
            for line in file:
                if not line.startswith(';;;'):
                    key, val = line.split('  ',2)
                    self._l[key] = re.findall(r"[A-Z]+",val)

    def get_pronunciation(self, str_input):
        list_pron = []
        for word in re.findall(r"[\w']+",str_input.upper()):
            if word in self._l:
                list_pron += self._l[word]
        print("Phonemes are: ", list_pron)
        delay=0
        for pron in list_pron:
            _thread.start_new_thread( TextToSpeech._play_audio, (pron,delay,))
            delay += 0.380
    
    def _play_audio(sound, delay):
        try:
            time.sleep(delay)
            wf = wave.open("F:/Python tutorial/TTS/sounds/"+sound+".wav", 'rb')       
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
            
            data = wf.readframes(TextToSpeech.CHUNK)
            
            while data:
                stream.write(data)
                data = wf.readframes(TextToSpeech.CHUNK)
        
            stream.stop_stream()
            stream.close()

            #p.terminate()
            return
        except:
            pass

  
def speech():
    text_to_speech= TextToSpeech()
    text= textTTS.get("1.0","end")
    text_to_speech.get_pronunciation(text)


TTSbtn=Button(text='User Voice', width=14, height=2, command=speech).place(y=490, x=50)

def changeVoice1():
 
    text= textTTS.get("1.0","end") 
    # Initialize the converter
    converter = pyttsx3.init()
  
    # Set properties before adding
    # Things to say
    voices = converter.getProperty('voices')
  
    for voice in voices:
        # to get the info. about various voices in our PC 
        print(voice, voice.id)
        print("Voice:")
        print("ID: %s" %voice.id)
        print("Name: %s" %voice.name)
        print("Age: %s" %voice.age)
        print("Gender: %s" %voice.gender)
        print("Languages Known: %s" %voice.languages)
        
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    # Use female voice
    converter.setProperty('voice', voice_id)

    
    # Sets speed percent 
    # Can be more than 100
    #converter.setProperty('rate', 150)
 
    # Set volume 0-1
    converter.setProperty('volume', 0.7)
  
    # Queue the entered text 
    # There will be a pause between
    # each one like a pause in 
    # a sentence
    converter.say(text)
      
    # Empties the say() queue
    # Program will not continue
    # until all speech is done talking
    converter.runAndWait()




ChangevoiceBtn=Button(text='Female_English1', width=14, height=2, command=changeVoice1 ).place(y=490, x=160)  

#male voice
def changeVoice2():
 
    text= textTTS.get("1.0","end") 
    # Initialize the converter
    converter = pyttsx3.init()
  
    # Set properties before adding
    # Things to say
    voices = converter.getProperty('voices')
  
    for voice in voices:
        # to get the info. about various voices in our PC 
        print(voice, voice.id)
        print("Voice:")
        print("ID: %s" %voice.id)
        print("Name: %s" %voice.name)
        print("Age: %s" %voice.age)
        print("Gender: %s" %voice.gender)
        print("Languages Known: %s" %voice.languages)
        
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enIN_RaviM"
    # Use female voice
    converter.setProperty('voice', voice_id)

    
    # Sets speed percent 
    # Can be more than 100
    #converter.setProperty('rate', 150)
 
    # Set volume 0-1
    converter.setProperty('volume', 0.7)
  
    # Queue the entered text 
    # There will be a pause between
    # each one like a pause in 
    # a sentence
    converter.say(text)
      
    # Empties the say() queue
    # Program will not continue
    # until all speech is done talking
    converter.runAndWait()


ChangevoiceBtn=Button(text='Male_English', width=14, height=2, command=changeVoice2 ).place(y=490, x=271)  

#Female indian voice
def changeVoice3():
 
    text= textTTS.get("1.0","end") 
    # Initialize the converter
    converter = pyttsx3.init()
  
    # Set properties before adding
    # Things to say
    voices = converter.getProperty('voices')
  
    for voice in voices:
        # to get the info. about various voices in our PC 
        print(voice, voice.id)
        print("Voice:")
        print("ID: %s" %voice.id)
        print("Name: %s" %voice.name)
        print("Age: %s" %voice.age)
        print("Gender: %s" %voice.gender)
        print("Languages Known: %s" %voice.languages)
        
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enIN_HeeraM"
    # Use female voice
    converter.setProperty('voice', voice_id)

    
    # Sets speed percent Can be more than 100
    converter.setProperty('rate', 150)
 
    # Set volume 0-1
    converter.setProperty('volume', 0.7)
  
    # Queue the entered text 
    # There will be a pause between
    # each one like a pause in 
    # a sentence
    converter.say(text)
      
    # Empties the say() queue
    # Program will not continue
    # until all speech is done talking
    converter.runAndWait()




ChangevoiceBtn=Button(text='Fmale_English2', width=14, height=2, command=changeVoice3 ).place(y=490, x=380)  

#Female indian voice
def changeVoice4():
 
    text= textTTS.get("1.0","end") 
    # Initialize the converter
    converter = pyttsx3.init()
  
    # Set properties before adding
    # Things to say
    voices = converter.getProperty('voices')
  
    for voice in voices:
        # to get the info. about various voices in our PC 
        print(voice, voice.id)
        print("Voice:")
        print("ID: %s" %voice.id)
        print("Name: %s" %voice.name)
        print("Age: %s" %voice.age)
        print("Gender: %s" %voice.gender)
        print("Languages Known: %s" %voice.languages)
        
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_KalpanaM"
    # Use female voice
    converter.setProperty('voice', voice_id)

    
    # Sets speed percent 
    # Can be more than 100
    #converter.setProperty('rate', 150)
 
    # Set volume 0-1
    converter.setProperty('volume', 0.7)
  
    # Queue the entered text 
    # There will be a pause between
    # each one like a pause in 
    # a sentence
    converter.say(text)
      
    # Empties the say() queue
    # Program will not continue
    # until all speech is done talking
    converter.runAndWait()




ChangevoiceBtn=Button(text='Fmale_Hindi', width=14, height=2, command=changeVoice4 ).place(y=550, x=50) 
"""engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop()"""

Label(text="Developed By- Saloni Sharma").place(x=1100, y=630)
root.mainloop()
