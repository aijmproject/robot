from module_speech_to_text_google import SpeechToTextMakerGoogle
from text_command_mapper import TextCommandMapper
from module_text_to_speech import TextToSpeech
from audio_recorder import AudioRecorder
from tempfile import NamedTemporaryFile
from client_db_api.surveillance_db_api import SurveillanceDbCreator
from identify_file import IdentifyFile
from audio_downsampling import AudioDownSampler
from response_random_provider import ResponseRandomProvider
#import IdentificationServiceHttpClientHelper
import sys, traceback
import os
import threading
import random
import string
class Listener:
    def __init__(self):
        self.speechtotextmaker = SpeechToTextMakerGoogle()
        self.command_mapper = TextCommandMapper()
        self.textToSpeech = TextToSpeech()
        self.audioRecorder = AudioRecorder()
        self.surveillanceDb = SurveillanceDbCreator()
        self.identifyFile = IdentifyFile()
        self.audioDownSampler = AudioDownSampler()
        self.reponseRandomProvider = ResponseRandomProvider()
        self.empty_profile_id = "00000000-0000-0000-0000-000000000000"

        self.subscription_key = "b4736e77574f48fe802b55364a2b2e44"
        self.srobot = "s robot"
        self.command_text_to_code = {"passe en mode surveillance bébé":1, "passe en mode surveillance maison":2}

        self._speech_to_text_result = None
        self.voice_recorder_result = None

    def _randomString(self,stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))
    
    def listen(self):
        files_to_delete = []
        while True:
            try:
                print("_voice_recorder...")
                voice_recorder_file = self._randomString() + ".wav"
                self.audioRecorder.record_to_file(voice_recorder_file)
                files_to_delete.append(voice_recorder_file)

                print("_speech_to_text...")
                self._speech_to_text_result = self.speechtotextmaker.get_text_by_audio(voice_recorder_file)

                if self._speech_to_text_result["error"] != None:
                    raise Exception("error occured" + self._speech_to_text_result["error"] )

                text = self._speech_to_text_result["transcription"]
                if text == None:
                    raise Exception("error occured")

                if self.srobot in text:
                    print("text : ", text)
                    command_text = text.replace(self.srobot,"").strip()
                    command_code = self.command_mapper.get_code_by_text(command_text)

                    if command_code == -1:
                        self.textToSpeech.speak(self.reponseRandomProvider.not_undestand_command())
                    else:
                        #speaker identification by voice
                        user_profile_ids = [item["mcs_sr_profile_id"] for item in self.surveillanceDb.get_all_users()]
                        #user.mcs_sr_profile_id : microsoft cognitive service speaker recognition profile id 
                        #voice_recorder_result : audio wav file created
                        voice_recorder_file_16k = voice_recorder_file + ".16k.wav"
                        
                        convert_command = 'ffmpeg -i ' + voice_recorder_file + ' -acodec pcm_s16le -ar 16000 -ac 1 ' + voice_recorder_file_16k
                        os.system(convert_command)

                        files_to_delete.append(voice_recorder_file_16k)
                        
                        verified_user_profile_id = self.identifyFile.identify_file(self.subscription_key,voice_recorder_file_16k,"true",user_profile_ids)
                        if verified_user_profile_id == self.empty_profile_id:
                            self.textToSpeech.speak(self.reponseRandomProvider.no_access_right())
                        else:
                            self.textToSpeech.speak("Chargement du module demandé")
                            break
                    #break
            except Exception as e:
                print(e)
                traceback.print_exc(file=sys.stdout)
            finally:
                #delete recorded wave file
                for file in files_to_delete:
                    if os.path.isfile(file):
                        os.remove(file)
                        print("file ", file, " deleted")


if __name__ == "__main__":
    app  = Listener()
    print("à l'écoute")
    app.listen()

                    


                
