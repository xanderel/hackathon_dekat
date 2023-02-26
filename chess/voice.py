import speech_recognition as sr
import string

def record():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Speak something!")
        audio = r.listen(source,timeout = 5, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio)
        text.lower()
        if(text[2] != " "):
            print("processing")
            text1 = text[0:2] + " "
            text2 = text[2:4]
            text = text1+text2   
        if((text[0].isalpha() and text[3].isalpha()) and (text[1].isdigit() and text[4].isdigit())):
            print("You said: ", text)
            return text
        else:
            record()
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        record()
    except sr.RequestError as e:
        print("Sorry, an error occurred while trying to recognize your speech. Error: ", e)
        record()
