import os, requests, time
from xml.etree import ElementTree
#import soundfile as sf
from audio_player import AudioPlayer
import os

class TextToSpeech(object):
    def __init__(self):
        self.subscription_key = "7312fdabc95d4f61b94408d74612f4ea"
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
        self.audioPlayer =  AudioPlayer()

    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''
    def _get_token(self):
        fetch_token_url = "https://francecentral.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def speak(self, sentence):

        #get token 
        self._get_token()

        base_url = 'https://francecentral.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'fr-FR')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'fr-FR')
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice (fr-FR, Julie, Apollo)')
        voice.text = sentence
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        
        if response.status_code == 200:
            filename = 'sample-' + self.timestr + '.wav'
            with open(filename, 'wb') as audio:
                audio.write(response.content)
                self.audioPlayer.play(filename)
            'delete created file '
            os.remove(filename)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
            print("Reason: " + str(response.reason) + "\n")

if __name__ == "__main__":
    app = TextToSpeech()
    app.speak("Bonjour mon pote")
    # Get a list of voices https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#get-a-list-of-voices
    # app.get_voices_list()
