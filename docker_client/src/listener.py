from module_speech_to_text_google import SpeechToTextMakerGoogle
from text_command_mapper import TextCommandMapper
from module_text_to_speech import TextToSpeech
from audio_recorder import AudioRecorder
from tempfile import NamedTemporaryFile
from client_db_api.surveillance_db_api import SurveillanceDbCreator
from cognitive_speakerrecognition.identification.identify_file.py import IdentifyFile
#import IdentificationServiceHttpClientHelper
import os
import threading
class Listener:
    def __init__(self):
        self.speechtotextmaker = SpeechToTextMakerGoogle()
        self.command_mapper = TextCommandMapper()
        self.textToSpeech = TextToSpeech()
        self.audioRecorder = AudioRecorder()
        self.surveillanceDb = SurveillanceDbCreator()
        self.identifyFile = IdentifyFile()

        self.subscription_key = "b4736e77574f48fe802b55364a2b2e44"
        self.srobot = "SRobot"
        self.command_text_to_code = {"passe en mode surveillance bébé":1, "passe en mode surveillance maison":2}

        self._speech_to_text_result = None
        self.voice_recorder_result = None

    def _speech_to_text(self):
        print("_speech_to_text...")
        self._speech_to_text_result = self.speechtotextmaker.get_text()
    
    def _voice_recorder(self):
        print("_voice_recorder...")
        f = NamedTemporaryFile(delete=False)
        self.audioRecorder.record_to_file(f.name)
        self.voice_recorder_result = f.name

    def listen(self):
        
        while True:
            #parallelisation à la fois de la transformation de parole en text et de la validation de la personne
            t_speech_to_text = threading.Thread(target=self._speech_to_text)
            t_voice_recorder = threading.Thread(target=self._voice_recorder)
            t_speech_to_text.start()
            t_voice_recorder.start()
            t_speech_to_text.join()
            t_voice_recorder.join()
            #print(self.domain_ip, self.website_thumbnail)

            if self._speech_to_text_result["error"] != None:
                print("error occured",self._speech_to_text_result["error"] )
                continue

            text = self._speech_to_text_result["transcription"]
            if text == None:
                #tolog
                print("error occured")
                continue

            if self.srobot in text:
                command_text = text.replace("SRobot","")
                command_code = self.command_mapper.get_code_by_text(command_text)

                if command_code == -1:
                    self.textToSpeech.speak("Désolé, je n'ai pas compris la commande")
                else:
                     #speaker identification by voice
                     user_profile_ids = [item["mcs_sr_profile_id"] for item in self.surveillanceDb.get_all_users()]
                     #user.mcs_sr_profile_id : microsoft cognitive service speaker recognition profile id 
                     #voice_recorder_result : audio wav file created
                     verified_user_profile_id = self.identifyFile.identify_file(self.subscription_key,self.voice_recorder_result,user_profile_ids)
                     if verified_user_profile_id == "00000000-0000-0000-0000-000000000000":
                         self.textToSpeech.speak("Désolé, vous n'avez pas le droit nécessaire")
                     else:
                         self.textToSpeech.speak("Chargement du module demandé")
            
            #delete recorded wave file
            os.remove(self.voice_recorder_result)
            print("file ", self.voice_recorder_result, " deleted")



if __name__ == "__main__":
    app  = Listener()
    print("à l'écoute")
    app.listen()

                    


                
