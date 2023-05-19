import os 
import glob
import time
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import seaborn as sns 
import tensorflow as tf
os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'
from datetime import datetime
from typing import Tuple 
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix 
from keras.models import Model, Sequential, load_model
from keras.layers import Rescaling
from keras.optimizers import Adam
from bdd.mg import Conn as Mg


class Train:

    """
        entraînement de différents modèles sur les images du dossier dataset10
        trois algorithmes disponibles : 
            - lstm 
            - cnn 
            - vgg16
    
    """


    def __init__(self, batch=4, epochs=2) -> None:
        self.size=None
        self.batch = batch
        self.epochs = epochs
        self.lstm_shape1 = None 
        self.lstm_shape2 = None
        self.timestamp = int(time.time())
        self.timest = self.nom_formatter()
        self.path_model=None 
        self.path_csv = None 
        self.path_confusion_matrix = None
        self.callback_patience = None 
        self.save_best = None
        self.chargement = None


    def nom_formatter(self) -> str:
        """définit un nom de fichier avec la date YYYY_MM_DD puis le timestamp"""
        
        my_date = datetime.fromtimestamp(self.timestamp)
        my_date = my_date.strftime("%Y_%m_%d")
        return my_date + '_' + str(self.timestamp)
        


    def load_dataset_cv2(self, train_test:bool =True, three_channels:bool =True, tanh:bool = False) -> Tuple[(np.ndarray, np.ndarray)]:
        
        """ 
            charger les images avec opencv ; pour les gros datasets il est déconseillé de l'utiliser
            avec le chargement opencv, les métriques sont disponibles
        """
        
        print("chargement des images")
        
        labels, paths = [], []
        for name in glob.glob("dataset10/**/*.png", recursive=True):
            if 'songimages' in name:
                labels.append(0)
                paths.append(name)
            else:
                labels.append(1)
                paths.append(name)
                

        labs = [];ims=[]

        for i in range(len(paths)):
            try:
                if three_channels==True:
                    img = cv2.imread(paths[i])
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                else:
                    img = cv2.imread(paths[i], 0)
            
                if tanh == True:
                    img = cv2.resize(img, (self.size,self.size))/255.
                else:
                    img = cv2.resize(img, (self.size,self.size))
                    img = (img-127.5)/127.5
                ims.append(img)
                labs.append(labels[i])
            except:
                continue
            
        
        ims = np.array(ims)
        labs = np.array(labs)    

        if train_test==True:
            X_train, X_test, y_train, y_test = train_test_split(ims, labs, test_size=0.1, random_state=3)
            return X_train, X_test, y_train, y_test
        else:
            return ims, labs
        


    def load_dataset_keras(self, mode:str = 'rgb', tanh:bool = False) -> Tuple[(tf.data.Dataset, tf.data.Dataset)]:
        
        """  
            charger un gros dataset avec un utilitaire de keras pour mieux gérer la mémoire
            les métriques sont désactivées        
        """
        
        dataset_train= tf.keras.preprocessing.image_dataset_from_directory(
            'dataset10',
            labels='inferred',
            label_mode='int',
            color_mode=mode,
            batch_size=self.batch,
            image_size=(self.size, self.size),
            shuffle=True,
            validation_split=0.1,
            subset='training',    
            seed=3
        )

        dataset_test= tf.keras.preprocessing.image_dataset_from_directory(
            'dataset10',
            labels='inferred',
            label_mode='int',
            color_mode=mode,
            batch_size=self.batch,
            image_size=(self.size, self.size),
            shuffle=True,
            validation_split=0.1,
            subset='validation',    
            seed=3
        )
        
        rescale = Rescaling(scale=1.0/255) if tanh==False else Rescaling(scale=1./127.5, offset=-1.)
        dataset_train = dataset_train.map(lambda image,label:(rescale(image),label))
        dataset_test = dataset_test.map(lambda image,label:(rescale(image),label))
        
        return dataset_train, dataset_test



    def model_cnn(self) -> Model:
        
        """  
            création d'un modèle avec couches de convolutions ; la taille des images est de 100x100, mode rgb
        """
        
        from keras.layers import Conv2D, BatchNormalization, MaxPool2D, Dense, Flatten, Dropout, Input, RandomZoom, RandomFlip
        
        input_shape = (self.size, self.size, 3)
        zoom = RandomZoom(0.2)
        
        model = Sequential()
        model.add(Input(shape=input_shape))
        model.add(zoom)
        model.add(RandomFlip('horizontal'))

        model.add(Conv2D(filters=64,kernel_size=(3,3),padding="same", activation='relu'))
        model.add(Conv2D(filters=64,kernel_size=(3,3),padding="same", activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.2))
        model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))

        model.add(Conv2D(filters=128,kernel_size=(3,3),padding="same", activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.2))
        model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))

        model.add(Conv2D(filters=256,kernel_size=(3,3),padding="same", activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.3))
        model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))

        model.add(Flatten())
        model.add(Dense(1000))
        model.add(Dropout(0.3))
        model.add(Dense(1000))
        model.add(Dense(1,activation="sigmoid"))

        return model



    def model_lstm(self, shape1:int, shape2:int) -> Model:
        
        """  
            modèle avec cellules Long-Short-Term-Memory, taille d'entrée 100x100, mode nuances de gris
        """
        
        from keras.layers import LSTM, Dense, Dropout
        input_shape=(self.size, self.size)
        model = Sequential()
        # model.add(LSTM(units=128, dropout=0.05, recurrent_dropout=0.35, return_sequences=True, input_shape=(shape1, shape2)))
        # model.add(LSTM(units=32,  dropout=0.05, recurrent_dropout=0.35, return_sequences=False))
        model.add(LSTM(units=256, return_sequences=True, input_shape=(shape1, shape2)))
        model.add(LSTM(units=256, return_sequences=False))
        # model.add(Dense(150, activation="relu"))
        model.add(Dropout(0.2))
        model.add(Dense(150, activation="relu"))
        model.add(Dense(1, activation="sigmoid"))
        
        return model



    def model_vgg16(self) -> Model:
        
        """  
            modèle VGG16 utilisé pour un transfert learning ; les poids des couches d'entrées conservent les poids 'imagenet'
            des couches full connected sont ajoutées en sortie pour l'apprentissage
            taille des images : 224x224, mode rgb
        """
        
        from keras.applications.vgg16 import VGG16
        from keras.layers import Flatten, Dense, RandomZoom, RandomFlip, Input, Dropout
        input_shape=(self.size, self.size, 3)
        
        zoom = RandomZoom(0.05)
        base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape) 
        for layer in base_model.layers: 
            layer.trainable = Famodel.add(LSTM(units=256, return_sequences=True, input_shape=(shape1, shape2)))
        model.add(LSTM(units=256, return_sequences=False))lse
        model = Sequential()
        model.add(Input(shape=input_shape))
        # model.add(zoom)
        # model.add(RandomFlip('horizontal'))
        model.add(base_model)
        model.add(Flatten()) 
        model.add(Dense(2000,activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(2000, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        return model



    def apprentissage_cnn(self) -> None:
        
        """ 
        lancer l'apprentissage du modèle cnn
        """
        
        self.call_backs()
        
        if self.chargement == 'keras':
            dataset_train, dataset_test = self.load_dataset_keras()
        else:
            X_train, X_test, y_train, y_test = self.load_dataset_cv2()

        
        print("création du modèle")
        model = self.model_cnn()
        
        model.compile(optimizer=Adam(learning_rate=0.001),
                    loss='binary_crossentropy',
                    metrics=['accuracy', tf.keras.metrics.Recall(),tf.keras.metrics.Precision()])

        
        print("apprentissage")
        
        if self.chargement == 'keras':
            history = model.fit(dataset_train, epochs=self.epochs,batch_size=self.batch, validation_data=(dataset_test), callbacks=[self.save_best, self.callback_patience])
        else:
            history = model.fit(X_train, y_train, epochs=self.epochs,batch_size=self.batch, validation_data=(X_test, y_test), callbacks=[self.save_best, self.callback_patience])
        pd.DataFrame(history.history).to_csv(self.path_csv, index=False)


        if self.chargement !='keras':
            print("metrics")
            model = load_model(self.path_model)
            pred = self.pred_to_numpy(model.predict(X_test))
    
            plt.figure()
            plt.title='Matrice de confusion _ '+ self.path_model[:-3]
            sns.heatmap(confusion_matrix(y_test, pred) , annot=True)
            plt.savefig(self.path_confusion_matrix)
            plt.close('all')
        


        
    def apprentissage_lstm(self) -> None:
        
        """ 
        lancer l'apprentissage du modèle rnn
        """
        
        self.call_backs()
        if self.chargement == 'keras':
            dataset_train, dataset_test = self.load_dataset_keras(mode='grayscale', tanh=True)
        else:
            X_train, X_test, y_train, y_test = self.load_dataset_cv2(three_channels=False, tanh=True)

        print("création du modèle")
        model = self.model_lstm(self.size, self.size)

        model.compile(optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.Recall(),tf.keras.metrics.Precision()])

        print("apprentissage")
        if self.chargement == 'keras':
            history = model.fit(dataset_train, epochs=self.epochs,batch_size=self.batch, validation_data=(dataset_test), callbacks=[self.save_best, self.callback_patience])
        else:
            history = model.fit(X_train, y_train, epochs=self.epochs,batch_size=self.batch, validation_data=(X_test, y_test), callbacks=[self.save_best, self.callback_patience])
        pd.DataFrame(history.history).to_csv(self.path_csv, index=False)

        if self.chargement !='keras':
            print("metrics")
            model = load_model(self.path_model)
            pred = self.pred_to_numpy(model.predict(X_test))
    
            plt.figure()
            plt.title='Matrice de confusion _ '+ self.path_model[:-3]
            sns.heatmap(confusion_matrix(y_test, pred) , annot=True)
            plt.savefig(self.path_confusion_matrix)
            plt.close('all')

        
        
    def apprentissage_vgg16(self) -> None:
        
        """ 
        lancer l'apprentissage du modèle vgg16 par transfert learning
        """
        
        self.call_backs()
        if self.chargement == 'keras':
            dataset_train, dataset_test = self.load_dataset_keras()
        else:
            X_train, X_test, y_train, y_test = self.load_dataset_cv2(three_channels=False)
    
        print("création du modèle")
        model = self.model_vgg16()
        
        model.compile(optimizer=Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.Recall(),tf.keras.metrics.Precision()])

        print("apprentissage")
        if self.chargement == 'keras':
            history = model.fit(dataset_train, epochs=self.epochs,batch_size=self.batch, validation_data=(dataset_test), callbacks=[self.save_best, self.callback_patience])
        else:
            history = model.fit(X_train, y_train, epochs=self.epochs,batch_size=self.batch, validation_data=(X_test, y_test), callbacks=[self.save_best, self.callback_patience])

        pd.DataFrame(history.history).to_csv(self.path_csv, index=False)
        
        if self.chargement !='keras':
            print("metrics")
            model = load_model(self.path_model)
            pred = self.pred_to_numpy(model.predict(X_test))
    
            plt.figure()
            plt.title='Matrice de confusion _ '+ self.path_model[:-3]
            sns.heatmap(confusion_matrix(y_test, pred) , annot=True)
            plt.savefig(self.path_confusion_matrix)
            plt.close('all')
        

    
    
    def call_backs(self) -> None:
        
        """ 
            fonctions callbacks pour :
                - stopper le modèle d'apprentissage si il n'évolue plus
                - sauvegarder le modèle en cas d'évolution
        """
        
        self.callback_patience = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=100)
        self.save_best = tf.keras.callbacks.ModelCheckpoint(
            filepath=self.path_model,
            save_weights_only=False,
            monitor='val_precision',
            mode='max',   
            save_best_only=True,verbose=1)
        
        
        
    def pred_to_numpy(self, pred:np.ndarray) -> np.ndarray:
        
        """ 
            convertir le tableau de prédictions en 0 (song) ou 1 (instru)
        """
        
        pred_l = []
        for i in range(len(pred)):
            if pred[i][0]<0.5:
                pred_l.append(0)
            else:
                pred_l.append(1)
        return np.array(pred_l)
    
    
    
    def to_json(self) -> None:
        """enregistre le dataframe au format json pour récupérer les résultats en front-end"""
        df = pd.read_csv(self.path_csv)
        
        df[['recall', 'val_recall', 'precision', 'val_precision']] = df[['recall', 'val_recall', 'precision', 'val_precision']].fillna(0)
        
        my_json = {
            'title': self.path_csv.split("/")[-1].replace('.csv', ''),
            'nom': str(self.timestamp),
            'index': list(df.index +1),
            'loss': list(df['loss']),
            'val_loss': list(df['val_loss']),
            'recall': list((df['recall']*100).astype(int)),
            'val_recall': list((df['val_recall']*100).astype(int)),
            'precision': list((df['precision']*100).astype(int)),
            'val_precision': list((df['val_precision']*100).astype(int)),
        }

        Mg().insert(my_json)
      
    

    
    def main(self, architecture:str = 'cnn', chargement:str = 'keras') -> None:
        
        """  
            lancement du programme
        """
         
        
        self.chargement = chargement
        self.path_model = './models/'+architecture+'_'+self.timest+'.h5'
        self.path_csv = './metrics/'+architecture+'_'+self.timest+'.csv'
        self.path_confusion_matrix =  './metrics/'+architecture+'_'+self.timest+'_matrice_de_confusion.png'
        
        if architecture=='cnn':
            self.size=100
            self.apprentissage_cnn()
        elif architecture =='lstm':
            self.size=100
            self.apprentissage_lstm()
        elif architecture=='vgg16':
            self.size = 224
            self.apprentissage_vgg16()
       
        
        self.to_json()

    
    
if __name__== '__main__':
    cl = Train(epochs=150)
    cl.main('vgg16')
    
    