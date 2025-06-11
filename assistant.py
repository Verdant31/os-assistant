import speech_recognition as sr


class Assistant:
    def __init__(self, language="pt-BR"):
        self.language = language

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language=self.language)
                print("Captured text: {}".format(text))
                return text.lower()
            except sr.UnknownValueError:
                print("Captured text but could not understand audio")
                return ""
            except sr.RequestError as e:
                print(
                    "Could not request results from Google Speech Recognition service; {0}".format(e))
                return ""
