import azure.cognitiveservices.speech as speechsdk


class SpeechToText:
    def __init__(self):
        self.speech_key = "7312fdabc95d4f61b94408d74612f4ea"
        self.service_region = "francecentral"
        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region, speech_recognition_language='fr-FR')


    def get_text(self):
        # Creates an instance of a speech config with specified subscription key and service region.
        # Replace with your own subscription key and service region (e.g., "westus").
        speech_key, service_region = "7312fdabc95d4f61b94408d74612f4ea", "francecentral"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language='fr-FR')

        # Creates a recognizer with the given settings
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

        result = speech_recognizer.recognize_once()

        # Checks result.
        text_result = ""
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
            text_result = result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
        
        return text_result

if __name__ == "__main__":
    app = SpeechToText()
    app.get_text()