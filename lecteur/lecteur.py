import pygame
import os
import shutil
import requests
import requests
import json
from bdd.connect import Conn
from tkinter import *
from tkinter import filedialog
from typing import List
from config import *


class Lecteur:

    """
        programme pour labelliser des airs, effectuer une prédiction, lire de la musique
        réalisé avec TKinter
        le containeur docker de la base de données doit être démarré 
        le container de l'api de prédiction doit être démarré

    """


    def __init__(self) -> None:
        self.path = PATH
        self.url = URL
        self.token = TOKEN
        self.id_current = None
        self.conn = Conn()
        self.current_song_Length = 0
        self.button_width = 10
        self.button_padx=10
        self.button_pady = 4

        # initialisation de la fenêtre
        self.__root=Tk()
        self.__root.geometry('750x600')
        self.__root.title("lire - labelliser")
        self.song_box = 100000
        
        # initialisation de la fenêtre secondaire d'affichage prédiction
        self.__newWindow = None
        self.__res_list = None
        self.__close_secondary_window_button = None

        # frame des boutons supérieurs
        self.__requetes_frame = Frame(self.__root)
        self.__requetes_frame.pack()
        
        # boutons de sélection du mode : prédire, random songs ou instrus, labelliseur
        self.__pred_button = Button(self.__requetes_frame, text="prédire",  command=self.pred).grid(column=6, row=0, padx=self.button_padx)
        # self.__eval_button = Button(self.__requetes_frame, text="eval_dataset",  command=self.eval).grid(column=0, row=0, padx=self.button_padx)
        self.__updatefinal_button = Button(self.__requetes_frame, text="update",  command=self.enable_label_frame1).grid(column=5, row=0, padx=self.button_padx)
        self.__airs_random_slowairs = Button(self.__requetes_frame, text="slow airs",  command=self.requete_random_slowairs).grid(column=0, row=0, padx=self.button_padx)
        self.__airs_random_nonsongs = Button(self.__requetes_frame, text="danses",  command=self.requete_random_nonsongs).grid(column=1, row=0, padx=self.button_padx)
        self.__airs_random_songs = Button(self.__requetes_frame, text="songs",  command=self.requete_random_songs).grid(column=2, row=0, padx=self.button_padx)
        self.__labeliser_tunes = Button(self.__requetes_frame, text="labelliser", command = self.labeliseur_tunes).grid(column=3, row=0, padx=self.button_padx)
        # self.__eval_song = Button(self.__requetes_frame, text="song",  command=self.eval_update_song).grid(column=2, row=1, padx=self.button_padx)
        # self.__eval_nonsong = Button(self.__requetes_frame, text="nonsong", command = self.eval_update_nonsong).grid(column=1, row=1, padx=self.button_padx)
        
        # la frame qui va contenir les fichiers
        self.listbox_frame = Frame(self.__root)
        self.listbox_frame.pack(ipadx=20, pady=10)

        # la liste avec les tunes
        self.song_box = Listbox(self.listbox_frame, bg = 'black', fg = 'white', width=80, height=12)
        self.song_box.pack(ipady=20)

        # la barre de défilement de la list box
        self.__scrollbar = Scrollbar(self.listbox_frame)
        self.__scrollbar.pack(side = 'right', fill = 'both')
        self.song_box.config(yscrollcommand = self.__scrollbar.set)
        self.__scrollbar.config(command = self.song_box.yview)

        # conteneur pour les boutons labelliseur: 
        self.__controls_frame0 = Frame(self.__root)
        self.__controls_frame0.pack()
        self.__controls_frame = Frame(self.__root)
        self.__controls_frame.pack()
        self.id = StringVar(self.__controls_frame, "id tune")
        self.id.set("")

        # conteneur pour les boutons updater final: 
        self.__controls_frame1 = Frame(self.__root)
        self.__controls_frame1.pack()
        


        # les images des boutons de contrôle audio
        self.__play_btn_img = PhotoImage(file='media/play1.png')
        self.__stop_btn_img = PhotoImage(file='media/stop1.png')
        self.__forward_btn_img = PhotoImage(file='media/forward.png')
        self.__fastforward_btn_img = PhotoImage(file='media/forwardrapide.png')
        
        # les boutons de contrôle audio
        self.__play_btn = Button(self.__controls_frame0, image=self.__play_btn_img, command=self.play).grid(column=1, row=0, padx=self.button_padx)
        self.__stop_btn = Button(self.__controls_frame0, image=self.__stop_btn_img, command = self.stop).grid(column=2, row=0, padx=self.button_padx)
        self.__forward_btn = Button(self.__controls_frame0, image=self.__forward_btn_img, command = self.play_forward).grid(column=3, row=0, padx=self.button_padx)
        self.__fastforward_btn = Button(self.__controls_frame0, image=self.__fastforward_btn_img, command = self.play_fastforward).grid(column=4, row=0, padx=self.button_padx)
        
        # les boutons pour labelliser
        self.__label_id = Entry(self.__controls_frame0, textvariable=self.id, width=self.button_width).grid(column=0, row=1, padx=self.button_padx)
        self.__song = Button(self.__controls_frame, text='song', command=self.song, width=self.button_width).grid(column=0, row=2, padx=self.button_padx, pady=self.button_pady)
        self.__reel = Button(self.__controls_frame, text='reel', command=self.reel, width=self.button_width).grid(column=1, row=2, padx=self.button_padx, pady=self.button_pady)
        self.__jig = Button(self.__controls_frame, text='jig', command=self.jig, width=self.button_width).grid(column=2, row=2, padx=self.button_padx, pady=self.button_pady)
        self.__hornpipe = Button(self.__controls_frame, text='hornpipe', command=self.hornpipe, width=self.button_width).grid(column=3, row=2, padx=self.button_padx, pady=self.button_pady)
        self.__polka = Button(self.__controls_frame, text='polka', command=self.polka, width=self.button_width).grid(column=4, row=2, padx=self.button_padx, pady=self.button_pady)
        self.__marche = Button(self.__controls_frame, text='marche', command=self.marche, width=self.button_width).grid(column=0, row=3, padx=self.button_padx, pady=self.button_pady)
        self.__valse = Button(self.__controls_frame, text='valse', command=self.valse, width=self.button_width).grid(column=1, row=3, padx=self.button_padx, pady=self.button_pady)
        self.__mazurka = Button(self.__controls_frame, text='mazurka', command=self.mazurka, width=self.button_width).grid(column=2, row=3, padx=self.button_padx, pady=self.button_pady)
        self.__slide = Button(self.__controls_frame, text='slide', command=self.slide, width=self.button_width).grid(column=3, row=3, padx=self.button_padx, pady=self.button_pady)
        self.__slipjig = Button(self.__controls_frame, text='slip jig', command=self.slipjig, width=self.button_width).grid(column=4, row=3, padx=self.button_padx, pady=self.button_pady)
        self.__autre = Button(self.__controls_frame, text='autre', command=self.autre, width=self.button_width).grid(column=0, row=4, padx=self.button_padx, pady=self.button_pady)
        self.__slowair = Button(self.__controls_frame, text='slow air', command=self.slowair, width=self.button_width).grid(column=1, row=4, padx=self.button_padx, pady=self.button_pady)
        self.__carolan = Button(self.__controls_frame, text='o\'carolan', command=self.carolan, width=self.button_width).grid(column=2, row=4, padx=self.button_padx, pady=self.button_pady)

        for child in self.__controls_frame.winfo_children():
            child.configure(state='disable')    


        self.__song_final = Button(self.__controls_frame1, text='song', command=self.song_final, width=self.button_width).grid(column=0, row=2, padx=self.button_padx, pady=self.button_pady)
        self.__instru_final = Button(self.__controls_frame1, text='instru', command=self.instru_final, width=self.button_width).grid(column=1, row=2, padx=self.button_padx, pady=self.button_pady)
        self.__slowair_final = Button(self.__controls_frame1, text='slow air', command=self.slowair_final, width=self.button_width).grid(column=2, row=2, padx=self.button_padx, pady=self.button_pady)
        
        for child in self.__controls_frame1.winfo_children():
            child.configure(state='disable')    



        # menus
        self.__my_menu = Menu(self.__root)
        self.__root.config(menu = self.__my_menu)

        # sous-menu
        self.__sous_menu = Menu(self.__my_menu)
        self.__my_menu.add_cascade(label = 'fichier', menu=self.__sous_menu)
        self.__sous_menu.add_command(label='ouvrir un fichier', command=self.add_file)
        self.__sous_menu.add_command(label='supprimer la playlist', command=self.clear_playlist)
        self.__sous_menu.add_command(label='supprimer l\'élément', command=self.remove_item_playlist)
        self.__sous_menu.add_command(label='quitter', command=self.__root.quit)
  
        # initialisation du mixer pygame
        pygame.mixer.init()
    
    #-------------------------------------------------------------

    ########################################
    ########################################
    # lecture des fichiers sons et options #
    ########################################
    ########################################


    def add_file(self) -> None:
        song = filedialog.askopenfilenames(initialdir='/media/bob/media/sonid', title="choisissez un fichier", filetypes=[('mp3 Files','*.mp3'), ('wave Files', '*.wav')])
        print(song)
        self.clear_playlist()
        self.song_box.insert(END, song)


    def find_id(self, nom) -> int:
        # controler l'id de la piste jouée au cas où
        return(int(nom.split("/")[-1][:-4]))
        

    def play(self) -> None:
        song = self.song_box.get(ACTIVE)
        self.current_song_Length=0
        self.id.set(str(self.find_id(song)))
        self.id_current=self.find_id(song)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=-1)


    def stop(self) -> None:
        pygame.mixer.music.stop()


    def clear_playlist(self) -> None:
        self.song_box.delete(0, END)


    def remove_item_playlist(self) -> None:
        # supprime l'élément actif de la playlist
        song = self.song_box.get(ACTIVE)
        idx = self.song_box.get(0, END).index(song)
        self.song_box.delete(idx)


    def play_forward(self) -> None:
        # lire la piste suivante
        selection_indices = self.song_box.curselection()
        next_selection = 0
        if len(selection_indices) > 0:
            last_selection = int(selection_indices[-1])
            self.song_box.selection_clear(selection_indices)
            if last_selection < self.song_box.size() - 1:
                next_selection = last_selection + 1
        self.song_box.activate(next_selection)
        self.song_box.selection_set(next_selection)
        self.current_song_Length=0
        song = self.song_box.get(ACTIVE)
        self.id.set(str(self.find_id(song)))
        self.id_current=self.find_id(song)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=-1)


    def play_fastforward(self) -> None:
        # avance rapide
        self.current_song_Length = self.current_song_Length + pygame.mixer.music.get_pos()/1000
        f = self.current_song_Length + 20.0
        try:
            pygame.mixer.music.set_pos(f)
        except:
            pygame.mixer.music.set_pos(0)


    def import_fichier_playlist1(self) -> None:
        # playlist importée au démarrage du programme
        liste_mp3 = []
        self.disable_label_frame('disable')
        for i in (os.listdir(self.path)):
            if i.endswith('.mp3'):
                dossier = self.path+i
                liste_mp3.append(dossier)

        liste_mp3 = sorted(liste_mp3)
        
        for i in liste_mp3:
                self.song_box.insert(END, i)
    

    def delete(self) -> None:
        self.song_box.delete(0,END)


    def disable_label_frame(self,state) -> None:
        # éviter une labellisation anarchique en activant ou désactivant certains boutons
        for child in self.__controls_frame.winfo_children():
            child.configure(state=state)


    def disable_label_frame1(self,state) -> None:
        # éviter une labellisation anarchique en activant ou désactivant certains boutons
        for child in self.__controls_frame1.winfo_children():
            child.configure(state=state)
            
            
    def enable_label_frame1(self) -> None:
        # activer les boutons de labellisation finale
        self.disable_label_frame('disable')
        for child in self.__controls_frame1.winfo_children():
            child.configure(state="normal")


    def pred(self) -> None:
        # requête à l'api de prédiction 
        song = self.song_box.get(ACTIVE)
        nom_fichier = song.split('/')[-1]
        if os.path.exists('temp'):
            shutil.rmtree('temp')
        os.mkdir('temp')
        shutil.copy(song, f'temp/{nom_fichier}')
        shutil.make_archive('trans', 'zip', 'temp')
        
        url = 'http://localhost:5001/vgg'

        with open("trans.zip", 'rb') as wav:

            files = { "file": wav }
            d = { "body" : "Foo Bar" }

            req = requests.post(url, files=files, json=d)
        
        aff = req.text[1:-2]
        aff = aff.replace("'", '')
        self.openNewWindow(aff)
        shutil.rmtree('temp')
        os.remove('trans.zip')


    def requete_random_nonsongs(self) -> None:
        # importer une sélection aléatoire d'airs labellisés instrus de la base de données 
        self.delete()
        self.disable_label_frame('disable')
        self.disable_label_frame1('disable')
        for i in self.conn.get_random_nonsongs():
            self.song_box.insert(END, i)

    def requete_random_songs(self) -> None:
        # importer une sélection aléatoire d'airs labellisés chansons de la base de données 
        self.delete()
        self.disable_label_frame('disable')
        self.disable_label_frame1('disable')
        for i in self.conn.get_random_songs():
            self.song_box.insert(END, i)
            
    def requete_random_slowairs(self) -> None:
        # importer une sélection aléatoire d'airs labellisés chansons de la base de données 
        self.delete()
        self.disable_label_frame('disable')
        self.disable_label_frame1('disable')
        for i in self.conn.get_random_slowairs():
            self.song_box.insert(END, i)

    def labeliseur_tunes(self) -> None:
        # labeliser des airs
        self.delete()
        self.disable_label_frame('normal')
        self.disable_label_frame1('disable')
        for i in self.conn.get_songs():
            self.song_box.insert(END, i)

    def eval(self) -> None:
        # bouton à activer si besoin, utilisé pour labelliser un dataset d'évaluation
        self.delete()
        self.disable_label_frame('normal')
        for i in self.conn.eval():
            self.song_box.insert(END, i)


    def openNewWindow(self, texte) -> None:
        # afficher le résultat de la prédiction
        self.__newWindow = Toplevel(self.__root)
        self.__newWindow.title("New Window")
        self.__newWindow.geometry("200x133")
        self.__res_list = Label(self.__newWindow, text=texte)
        self.__res_list.pack(ipady=10)
        self.__close_secondary_window_button = Button(self.__newWindow, text='close', command=self.__newWindow.destroy).pack()


    # ---------------------------------------------------------------

    ##########################
    ##########################
    # updates base de donnée #
    ##########################
    ##########################


    def reel(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='reel'), labelised2=1 where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def song(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='song'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def jig(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='jig'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def hornpipe(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='hornpipe'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def polka(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='polka'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def slipjig(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='slipjig'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def slide(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='slide'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def marche(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='marche'), labelised2=1 where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def slowair(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='slowair'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def autre(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='autre'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def valse(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='valse'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def mazurka(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='mazurka'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def carolan(self) -> None:
        sql = """update irish2 set id_iter2=(select id_nom_danses from nom_danses where danse='carolan'), labelised2=1  where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
        
        
    # updates finaux
    def instru_final(self) -> None:
        sql = """update irish2 set vgg_11_14=1.0, vgg2=0 where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql) 
        params = {
            "token":self.token,
            "val":str(self.id_current),
            "classi":"instru"
        }
        req = requests.get(self.url, params=params)
        print(req.json())
                
    
    def song_final(self) -> None:
        sql = """update irish2 set cnn=1.0 where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql) 
        params = {
            "token":self.token,
            "val":str(self.id_current),
            "classi":"song"
        }
        req = requests.get(self.url, params=params)
        print(req.json())
        
        
    def slowair_final(self) -> None:
        sql = """update irish2 set cnn2=1.0, vgg_11_14=0.4 where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql) 
        params = {
            "token":self.token,
            "val":str(self.id_current),
            "classi":"slowair"
        }
        req = requests.get(self.url, params=params)
        print(req.json())
        
        
    
    def eval_update_song(self) -> None:
        sql = """update rand_classes set confirmation_classe='song' where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
    def eval_update_nonsong(self):
        sql = """update rand_classes set confirmation_classe='nonsong' where id_irish={};""".format(int(self.id_current))
        self.conn.exec_and_commit(sql)
        

    def demarrer_le_programme(self) -> None:
        # désactiver les boutons du labelliseur, importer une playlist
        self.disable_label_frame('disable')
        self.disable_label_frame1('disable')
        self.import_fichier_playlist1()     
        self.__root.mainloop()
    
    
    
    
    
if __name__ == "__main__":

    fen = Lecteur()
    fen.demarrer_le_programme()
    
    
    
    
    






    