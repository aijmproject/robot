import speech_recognition as sr
#import sys, os, pyttsx
#import aiml, string, pyaudio
#import nltk
import urllib
import json
#from nltk.corpus import stopwords
from collections import Counter
#from google import search

class SpeechToTextMakerGoogle:

    def get_text(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone(device_index=1)
        return self._recognize_speech_from_mic(recognizer, mic)

    def _recognize_speech_from_mic(self, recognizer, microphone):
        """Transcribe speech from recorded from `microphone`.
        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                successful
        "error":   `None` if no error occured, otherwise a string containing
                an error message if the API could not be reached or
                speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source) # #  analyze the audio source for 1 second
            audio = recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #   update the response object accordingly
        try:
            response["transcription"] = recognizer.recognize_google(audio, language="fr-FR")
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable/unresponsive"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response


if __name__ == "__main__":
    app = SpeechToTextMakerGoogle()
    response = app.get_text()
    print(type(response["transcription"]))