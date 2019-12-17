import pyaudio
import wave
import sys

class AudioPlayer:

    def __init__(self):
        self.chunk = 1024

    def play(self, filename):
        # open the file for reading.
        wf = wave.open(filename, 'rb')
        # create an audio object
        p = pyaudio.PyAudio()
        # open stream based on the wave object which has been input.
        stream = p.open(format =
                        p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)
        # read data (based on the chunk size)
        data = wf.readframes(self.chunk)

        # play stream (looping from beginning of file to the end)
        while data != '':
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(self.chunk)

            if data == b'':
                break
            #break

        # cleanup stuff.
        stream.close() 
        p.terminate()