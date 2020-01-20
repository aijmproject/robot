import os
class AudioFileConvertor: 
    @staticmethod
    def convert_to_mono_16K(input_file):
        output_file = input_file + ".16k.wav"
                            
        convert_command = 'ffmpeg -i ' + input_file + ' -acodec pcm_s16le -ar 16000 -ac 1 ' + output_file
        os.system(convert_command)
        return output_file



    