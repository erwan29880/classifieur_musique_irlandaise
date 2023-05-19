import os 
import numpy as np 
import matplotlib.pyplot as plt 
import random
import librosa
import librosa.display
import pydub
import psycopg2
import argparse
from bdd import param, connect
from typing import Tuple, Generator



parser = argparse.ArgumentParser()
parser.add_argument('--label', type=str, required=True, help='options disponibles : instru, song, air')
args = parser.parse_args()

class Bdd(connect.Conn):
    
    def __init__(self):
        super().__init__()
    
    def instrus(self):
        sql = "select id_irish from irish2 where vgg_11_14>0.5 and cnn2<0.5;" # attention -> instrus !!
        return super().fetch(sql)
        
    def songs(self):
        sql = "select id_irish from irish2 where vgg_11_14<0.5;"
        return super().fetch(sql)
    
    def airs(self):
        sql = "select id_irish from irish2 where cnn2>0.5 and vgg_11_14>0.5;"
        return super().fetch(sql)
    
    
    
class Traitement_audio(Bdd):

    """Créer des spectrogrammes"""

    def __init__(self, label) -> None:
        super().__init__()
        self.label = label
        self.tempfile = 'tempfile.wav'
        self.PATH = '/media/bob/media/sonid/'
        self.files = None
        self.rate = 44100
        self.find_files()
        self.iter = self.__iter__()
        

    def find_files(self) -> None:
        """ trouve les chemins de fichiers des mp3 en fonction de la classification en bdd"""
        if self.label=='instru': 
            ids = super().instrus()
        elif self.label=='song':
            ids = super().songs()
        else:
            ids = super().airs()
        
        airs = [self.PATH+str(x)+'.mp3' for x in ids]
        for air in airs:
            if not os.path.exists(air):
                airs.remove(air)
                
        self.files = sorted(airs)
                

    def mp3_wave(self, path: str) -> np.ndarray:
        """conversion mp3 wave"""
        sound = pydub.AudioSegment.from_mp3(path)
        sound.export('tempfile.wav', format='wav')
        y,_ = librosa.load('tempfile.wav', sr=self.rate)
        return y


    def mel_to_img(self, y: np.ndarray, save_path: str) -> plt.figure:
        """
        transforme une fichier wav en image (mel spectrogram)
        """
        D = librosa.stft(y)
        D_harmonic, D_percussive = librosa.decompose.hpss(D)
        rp = np.max(np.abs(D))
        librosa.display.specshow(librosa.amplitude_to_db(np.abs(D_percussive), ref=rp),
                                y_axis='log')
        
        plt.axis('off')
        plt.savefig(save_path)
        plt.clf()
        
        
    def sound_to_mel(self, y: np.ndarray, fft:int = 1024, mels:int = 256) -> np.ndarray:
        return librosa.feature.melspectrogram(y=y, sr=self.rate, n_fft=fft, hop_length=mels)
        

    def random_window(self, y: np.ndarray) -> np.ndarray:
        debuts = [x for x in range(30, 80)]
        debut_rand = random.choice(debuts) * self.rate
        fin_rand = debut_rand + (30*self.rate)
        new_y = y[debut_rand:fin_rand]
        if len(new_y) == 30*self.rate:
            return new_y
        else:
            return None
        
           
    def run(self) -> None:
        assert self.files is not None
        for inc, air in enumerate(self.files):
            try:
                y = self.mp3_wave(air)
                for _ in range(10):
                    new_y = self.random_window(y)
                    if new_y is not None:
                        np.save(next(self.iter), self.sound_to_mel(new_y))
                if inc%15 == 0:
                    print(f'traitement fichier {air}, {len(self.files)-inc} restants')
            except:
                print(f"problème avec {air}")
            
        
    def __iter__(self) -> Generator:
        path = f'/media/bob/media/dataset_2023_02/{self.label}/'
        if not os.path.exists(path):
            os.mkdir(path)
            
        for i in range(200000):
            yield f"{path}{i}.npy"
            


if __name__ == '__main__':
    cl = Traitement_audio(args.label)
    cl.run()
