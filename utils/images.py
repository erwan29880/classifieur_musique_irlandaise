import sys 
sys.path.append('/home/erwan/Musique/')
from bdd import connect
import numpy as np
import os
import matplotlib.pyplot as plt
import librosa
import librosa.display
from pydub import AudioSegment
import shutil


class Mp3_to_png:

    """
    transformation des fichiers mp3 en images (Mel Spectrogram)
    """


    def __init__(self):
        self.conn = connect.Conn()
        self.sec = 30 * 1000
        self.debut = 40 *1000
        self.samplerate = 22500
        self.thirty_seconds = self.debut + (self.sec)
        self.export_temp = './temp/temp.wav'
        self.path_dossier_sons = '/home/erwan/Musique/sonid/'
        self.path_dossier_images = '/home/erwan/Musique/data/images/'
        self.images = None
        self.sons = None


    def to_wave(self, filename:str) -> None:
        """
        transforme un mp3 en wave
        """
        assert filename.endswith('.mp3') or filename.endswith('.MP3')
        
        song = AudioSegment.from_mp3(filename)
        song_reshaped = song[self.debut:self.thirty_seconds]
        song_reshaped.export(self.export_temp, format="wav")



    def mel_to_img(self, filename:str) -> None:
        """
        transforme une fichier wav en image (mel spectrogram)
        """

        y, sr = librosa.load(self.export_temp, sr=self.samplerate, mono=True)

        D = librosa.stft(y)
        D_harmonic, D_percussive = librosa.decompose.hpss(D)
        rp = np.max(np.abs(D))
        librosa.display.specshow(librosa.amplitude_to_db(np.abs(D_percussive), ref=rp),
                                y_axis='log')
                            
        plt.savefig(filename)
        plt.clf()
        

    def get_files(self) -> None:
        """
        récupère les ids en base de donnée, les ids correspondent aux noms des fichiers mp3
        """

        res = self.conn.fetch("""select id_irish from irish limit 2;""")
        self.images = [os.path.join(self.path_dossier_images, str(x)+'.png') for x in res]
        self.sons = [os.path.join(self.path_dossier_sons, str(x)+'.mp3') for x in res]
        


    def make_dirs(self) -> None:
        """
        créé le dossier images
        """

        assert os.path.exists(self.path_dossier_sons)
        
        if os.path.exists(self.path_dossier_images):
            shutil.rmtree(self.path_dossier_images)
        os.mkdir(self.path_dossier_images)



    def main(self) -> None:
        self.make_dirs()
        self.get_files()
        
        assert len(self.sons)==len(self.images)

        for i in range(len(self.sons)):
            try:
                print(f'----> {self.sons[i]}')
                self.to_wave(self.sons[i])
                self.mel_to_img(self.images[i])
                print(True)
            except:
                print(False)
                continue
            plt.clf()



if __name__=='__main__':
    cl=Mp3_to_png()
    cl.main()
   