

import speech_recognition
import time
import subprocess
from module_text_to_speech import TextToSpeech
from text_command_mapper import TextCommandMapper
from response_random_provider import ResponseRandomProvider
from module_manager import ModuleManager
from audio_file_convertor import AudioFileConvertor
from client_db_api.surveillance_db_api import SurveillanceDbAPI
from utils import GlobalUtils
import os
import sys, traceback
from identify_file import IdentifyFile
from command_module_mapper import CommandModuleMapper
class RobotTrigger:
    def __init__(self):
        self.trigger = "robot"
        self.recognizer = speech_recognition.Recognizer()
        self.textToSpeech = TextToSpeech()
        self.command_mapper = TextCommandMapper()
        self.reponseRandomProvider = ResponseRandomProvider()
        self.moduleManager = ModuleManager()
        self.surveillanceDb = SurveillanceDbAPI()
        self.identifyFile = IdentifyFile()
        self.commandModuleMapper = CommandModuleMapper()
        self.files_to_delete = []
        self.empty_profile_id = "00000000-0000-0000-0000-000000000000"
        self.subscription_key = "b4736e77574f48fe802b55364a2b2e44"

    def clean_temp_files(self):
        #delete recorded wave file
        #https://stackoverflow.com/questions/1196074/how-to-start-a-background-process-in-python
        #execuyte this in background process
        for file in self.files_to_delete:
            if os.path.isfile(file):
                os.remove(file)
                print("file ", file, " deleted")

    def _get_trigger(self):

        print("Beginning to listen...")
        with speech_recognition.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)

        try:
            return self.recognizer.recognize_google(audio, language="fr-FR")
        except speech_recognition.UnknownValueError:
            print("Could not understand audio")
        return ""


    def listen(self):
        print("Trying to always listen...")
        
        while True:
            result = self._get_trigger()
            print(result)
            if result == self.trigger:
                self._listen_command()
                #self.current_process = subprocess.Popen('python module_main.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
            time.sleep(1)


    def _listen_command(self):
        try:
            self.textToSpeech.speak(self.reponseRandomProvider.bot_ask_to_speak())

            voice_recorder_file = GlobalUtils.randomString() + ".wav"
            self.files_to_delete.append(voice_recorder_file)

            print("listen to input command...")
            with speech_recognition.Microphone() as source:
                        self.recognizer.adjust_for_ambient_noise(source)
                        audio2 = self.recognizer.listen(source)
                        with open(voice_recorder_file, "wb") as f:
                            f.write(audio2.get_wav_data())

            command_text = ""
            try:
                command_text =  self.recognizer.recognize_google(audio2, language="fr-FR")
                print("sentence : ", command_text)
            except speech_recognition.UnknownValueError:
                print("Could not understand audio")
            
            command_code = self.command_mapper.get_code_by_text(command_text)
            if command_code == -1:
                self.textToSpeech.speak(self.reponseRandomProvider.not_undestand_command())
            else:
                voice_recorder_file_16k = AudioFileConvertor.convert_to_mono_16K(voice_recorder_file)
                self.files_to_delete.append(voice_recorder_file_16k)
                
                user_profile_ids = [item["mcs_sr_profile_id"] for item in self.surveillanceDb.get_all_users()]
                verified_user_profile_id = self.identifyFile.identify_file(self.subscription_key,voice_recorder_file_16k,"true",user_profile_ids)
                if verified_user_profile_id == self.empty_profile_id:
                    self.textToSpeech.speak(self.reponseRandomProvider.no_access_right())
                else:
                    self.textToSpeech.speak("Chargement du module {0}".format(self.commandModuleMapper.code_to_module[command_code]))
                    self.moduleManager.switch_to_module(command_code)

        except Exception as e:
            print(e)
            traceback.print_exc(file=sys.stdout)
            self.textToSpeech.speak(self.reponseRandomProvider.fatal_error_text())
        finally:
            self.clean_temp_files()

if __name__ == "__main__":
    app  = RobotTrigger()
    print("à l'écoute")
    app.listen()