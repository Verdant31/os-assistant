import speech_recognition as sr

WAKE_PHRASE = "hello assistant"


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake phrase...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="pt-BR")
            print("You said: {}".format(text))
            return text.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""


while True:
    text = get_audio()
    if WAKE_PHRASE in text:
        print("Wake phrase detected! Assistant is ready.")
        # Place assistant functionalities here
        break  # Exit loop after wake word is detected, remove to keep listening
    else:
        print("Listening...")
