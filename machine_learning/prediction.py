import cv2
import os
import psycopg2 
import time
import sys
import numpy as np
sys.path.append('/home/erwan/Musique/')
from bdd import connect
from tkinter import *
os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'
from keras.models import load_model


class Pred:
    
    """ 
        effetcuer les prédictions sur les images des airs de la base de données, selon trois architectures (lstm, cnn, vgg16)
        une fenêtre de sélection s'ouvre pour choisir le modèle, une colonne est créée dans la base de données 
        les résultats sont entrés dans la bdd
    """
    
    def __init__(self) -> None:
        self.size=100
        self.connect = connect.Conn()
        self.architecture = None
        self.modele = None
        self.model = None
        self.timest = str(int(time.time()))
        self.column = None
        self.root = None 
        self.song_box = None

   
    def get_active(self) -> None:
        self.modele = self.song_box.get(ACTIVE)
        self.root.quit()


    def window(self, test=False):
        self.root = Tk()
        self.root.geometry('400x400')
        self.root.title("choisir le modèle")
        
        listbox_frame = Frame(self.root)
        listbox_frame.pack(ipadx=20, pady=10)
        self.song_box = Listbox(listbox_frame, bg = 'black', fg = 'white', width=80, height=12)
        self.song_box.pack(ipady=20)
        for i in os.listdir('./models/'):
            self.song_box.insert(END, i)
        butt = Button(self.root, text='valider', command=self.get_active).pack()
        if test==False:
            self.root.mainloop()

        return True
        
        
    def window_alert(self, test=False):
        """fenêtre de confirmation apprentissage"""
        root=Tk()
        root.geometry('300x100')
        root.title("alert")
        
        listbox_frame = Frame(root)
        listbox_frame.pack(ipadx=20, pady=10)
        my_text = Label(listbox_frame, text="prédictions effectuées").pack()
        butt = Button(listbox_frame, text="ok", command=root.quit).pack()
        if test==False:
            root.mainloop()
        return True
        
        
    def load(self, nb_im:int = 20, test:bool = False) -> list:
        """chargement des id à partir de la base de donnés"""
        if test:
            self.column = 'test'
        sql = f"select id_irish from irish_demo where {self.column} IS NULL limit {nb_im};"
        idx = self.connect.fetch(sql)

        return idx


    def load_images(self, nb_im:int=500, test:bool = False):
        idx = self.load(nb_im = 5, test=True) if test else self.load(nb_im = nb_im)
        resu = [f'/media/bob/media/images/{str(x)}.png' for x in idx] 
        ims = []
        idx2 = []
        for im in range(len(resu)):
            try:
                if self.architecture=='lstm':
                    img = cv2.imread(resu[im],0)
                else:
                    img = cv2.imread(resu[im])
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                img = cv2.resize(img, (self.size, self.size))/255.
                ims.append(img)
                idx2.append(idx[im])
            except:
                print(resu[im])
                
        ims = np.array(ims)
        
        return ims, idx2


    def choix_modele(self, test:bool = False) -> None:
        
        if test: 
            self.modele = "./test/lstm_2023_03_26_1679821324.h5"

        if 'lstm' in self.modele:
            self.architecture='lstm'
            self.size=100
            assert self.architecture == 'lstm'
        elif 'cnn' in self.modele:
            self.architecture='cnn'
            self.size=100
        elif 'vgg' in self.modele:
            self.architecture='vgg'
            self.size=224
            
        if test == False: 
            self.model = load_model('./models/'+self.modele)
            self.column = self.architecture+'_'+self.timest
            sql = """alter table irish_demo add {} float;""".format(self.column)
            self.connect.insert(sql)
        else:
            self.model = load_model(self.modele)
            return self.size, self.architecture



    def predict(self, nb_im:int = 500, test:bool = False) -> None:
        nb_im = 5 if test else nb_im
        ims, idx2 = self.load_images(nb_im = nb_im, test = test)
        
        pred = self.model.predict(ims)
        req=[]
        for i in range(len(pred)):
            pre = pred[i][0]
            pre = round(float(pre), 3)
            id = idx2[i]
            table = 'irish_demo' if test else 'irish2' 
            sql = """update '{}' set {}={} where id_irish={};""".format(table, self.column, pre, int(id))
            req.append(sql)

        if test == False:
            self.connect.insert(req)
        else:
            return True


    
    def compte(self, test:bool = False) -> None:
        
        """  
            découper le nombre d'entrées de la base de données en lots, et lancer la fonction de prédiction
        """
        
        nb_images_par_prediction = 500 
        table = 'irish2' if test else 'irish_demo' 
        sql = f"select count(*) from {table} where {self.column} IS NULL;"
        print(sql)
        res = self.connect.fetch(sql)[0]

        nb_restant = res%nb_images_par_prediction
        nb_iters = res//nb_images_par_prediction   
        if test:
            return nb_iters
        print(nb_iters, nb_restant)

        for i in range(nb_iters):
            self.predict(nb_im = nb_images_par_prediction)
                
        if nb_restant>0:
            self.predict(nb_im = nb_restant)
 

    def main(self) -> None:
        
        """  
            choix du modèle 
            création d'une colonne dans la base de données
            lancer le programme de prédictions
        
        """   
     
        self.window()
        self.choix_modele()
        self.compte()
        self.window_alert()


if __name__=="__main__":
    cl = Pred()
    # cl.compte()
    