import numpy as np
import os
import matplotlib.pyplot as plt
import librosa
import librosa.display
import glob
import cv2 
from pydub import AudioSegment
from keras.models import load_model
from typing import Tuple


class Mp3_to_png:

    """
    transformation des fichiers mp3 en images (Mel Spectrogram)
    chargement et traitement des images
    prédictions des images
    mise en dictionnaire des résultats pour envoi en JSON par api
    """

    def __init__(self) -> None:
        self.sec = 30 * 1000
        self.debut = 10 *1000
        self.samplerate = 41000
        self.thirty_seconds = self.debut + (self.sec)
        self.export_temp = './temp/temp.wav'
        self.model = None
        self.size = None
        self.noms_images = []
        self.architecture = None
        self.channels = None
        self.model = None
        self.seuil = 0.5


    def to_wave(self, filename: str) -> None:
        """
        transforme un mp3 en wave
        """
        
        song = AudioSegment.from_mp3(filename)
        song_reshaped = song[self.debut:self.thirty_seconds]
        song_reshaped.export('./temp/temp.wav', format="wav")


    def mel_to_img(self) -> None:
        """
        transforme un fichier wav en image (mel spectrogram)
        """

        for name in glob.glob('./archives/*.mp3'):
            nom_image = name.replace('archives', 'im')
            nom_image = nom_image.replace('mp3', 'png')
            
            self.to_wave(name)
            y, sr = librosa.load('./temp/temp.wav', sr=self.samplerate, mono=True)

            melspectrum = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=512,window='hann', n_mels=256)
            plt.figure()
            fig, ax = plt.subplots()
            S_dB = librosa.power_to_db(melspectrum, ref=np.max)
            img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, ax=ax)
            plt.axis('off')
            plt.savefig(nom_image)
            plt.clf()

    
    def load_ims(self) -> Tuple[(np.ndarray, list)]:
        """
        chargement des images
        conserver les noms de fichiers    
        """
    
        images = []
        fichiers = []
        
        for name in glob.glob('./im/*.png'):
            nom_fichier = name.split('/')[2]
            nom_fichier = nom_fichier.replace('png', 'mp3')
            fichiers.append(nom_fichier)
            if self.channels == 1:
                img = cv2.imread(name, 0)
            else:
                img = cv2.imread(name)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            img = cv2.resize(img, (self.size,self.size))/255.
            images.append(img)
            
        return np.array(images), fichiers
        
        
    def pred(self) -> dict:
        """ 
            effectue la prédiction
            renvoie un dictionnaire pour envoi JSON via API
        """
        
        predictions = []
        dico = dict()
        images, fichiers = self.load_ims()

        # prédiction        
        predi = load_model(self.model).predict(images)
        predi2 = load_model("./models/vgg2.h5").predict(images)
        
        # mise en forme des résultats
        for i in range(len(predi)):
            if predi[i][0]<self.seuil:
                predictions.append('song')
            else:
                if predi2[i][0]>self.seuil:
                    predictions.append('instrumental')
                else:
                    predictions.append('slowair')
        
        for i in range(len(predictions)):
            dico[fichiers[i]] = str(predictions[i])
            
        
            
        return dico


    def main(self, architecture: str) -> dict:
        
        """ 
            le choix de l'architecture du modèle (lstm, cnn, vgg16) se fait selon l'url de requête à l'api
        """
        
        if architecture == 'lstm':
            self.size = 100
            self.channels = 1
            self.architecture = 'lstm'
            self.model = './models/lstm.h5'
        elif architecture == 'cnn':
            self.size = 100
            self.channels = 3
            self.architecture = 'cnn'
            self.model = './models/cnn.h5'
        elif architecture == 'vgg':
            self.size = 224
            self.channels = 3
            self.architecture = 'vgg'
            self.model = './models/vgg.h5'
            
            
        self.mel_to_img()
        return self.pred()