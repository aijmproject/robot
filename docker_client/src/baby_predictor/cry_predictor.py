

import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import os
import librosa # library traitement du son (audio to image )  
import librosa.display
import IPython.display
from glob import glob
from scipy.io.wavfile import write
import os
from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten 
from keras.layers import Dense

class BabyCryPredictor():
    """
    Class to classify a new audio signal and determine if it's a baby cry
    """

    def __init__(self, path_dir):
        self.path_dir = path_dir
        self.filepath = self.path_dir + '/trained_model/cnn_baby.hdf5'
        self.filename = 'record.wav'
        self.path_filename= self.path_dir + '/temp'
        self.path_to_save = self.path_dir + '/temp/'
        self.image_path = self.path_dir + "/temp/record.wav.png"
        self.audio_path = self.path_dir + "/temp/record.wav"

    def reader(self):
        fs = 22050
        duration = 7
        print('speak')
        x = sd.rec(int(duration * fs), fs , 1, blocking=True)
        print('stop')
        
        x = np.squeeze(x)
        write(self.path_dir + '/temp/record.wav', fs, x)
        
    def create_spectrogram(self):
       
                       
        plt.interactive(False)
        clip, sample_rate = librosa.load(self.path_filename + '/' + self.filename, sr=None, duration = 5.0)
        fig = plt.figure(figsize=[0.72,0.72])
        ax = fig.add_subplot(111)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.set_frame_on(False)
        S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)
        librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
        image_record  = os.path.basename(self.filename) + '.png'
        plt.savefig(self.path_to_save + image_record, dpi=400, bbox_inches='tight',pad_inches=0)
        plt.close()    
        fig.clf()
        plt.close(fig)
        plt.close('all')   
        
    def model(self):
        classifier = Sequential()
        #adding a convolution layer
        classifier.add(Convolution2D(32 , 3 , 3 , input_shape = (64 , 64 , 3) , activation = 'relu'))
        classifier.add(MaxPooling2D(pool_size = (2,2)))


        #adding the second convolution layer
        classifier.add(Convolution2D(32 , 3, 3, activation = 'relu'))
        classifier.add(MaxPooling2D(pool_size = (2,2)))


        classifier.add(Flatten())

        classifier.add(Dense(output_dim =  128 , activation = 'relu'))
        classifier.add(Dense(output_dim = 128 , activation = 'relu'))
        classifier.add(Dense(output_dim = 1 , activation = 'sigmoid'))
        return classifier
        
        
    
    def predict(self):
        self.reader()
        self.create_spectrogram()
        
        test_image = image.load_img(self.image_path, target_size = (64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        cnn_model = self.model()
        cnn_model.load_weights(self.filepath)
        result = cnn_model.predict(test_image)
        #training_set.class_indices
        if result[0][0] == 1:
            prediction = False
    
        else:
            prediction = True
        os.remove(self.image_path)
        os.remove(self.audio_path)
        return prediction
    
if __name__ == '__main__':
    app = BabyCryPredictor()
    app.predict()
    