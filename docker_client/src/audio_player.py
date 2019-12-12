import pyaudio
import wave
import sys

class AudioPlayer:

    def __init__(self):
        self.chunk = 1024

    def play(self, filename):

        # validation. If a wave file hasn't been specified, exit.
        #if len(sys.argv) < 2:
        #    print "Plays a wave file.\n\n" +\
        #        "Usage: %s filename.wav" % sys.argv[0]
        #    sys.exit(-1)

        '''
        ************************************************************************
            This is the start of the "minimum needed to read a wave"
        ************************************************************************
        '''
        # open the file for reading.
        print("step 1")
        wf = wave.open(filename, 'rb')
        print("step 2")
        # create an audio object
        p = pyaudio.PyAudio()
        print("step 3")
        # open stream based on the wave object which has been input.
        stream = p.open(format =
                        p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)
        print("step 4")
        # read data (based on the chunk size)
        data = wf.readframes(self.chunk)

        # play stream (looping from beginning of file to the end)
        while data != '':
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            print("step 5")
            data = wf.readframes(self.chunk)
            print("step 6")
            break

        # cleanup stuff.
        print("step 7")
        stream.close() 
        print("step 8")   
        p.terminate()