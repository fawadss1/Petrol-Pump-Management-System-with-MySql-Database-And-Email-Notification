import pyttsx3


def Narrator(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.getProperty('rate')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 200)
    print(command)
    engine.say(command)
    engine.runAndWait()
