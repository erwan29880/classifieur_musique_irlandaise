import os
import pandas as pd
import numpy as np
import glob
import shutil
from bdd import connect

###-------->
### ne pas utiliser cette classe si la base de données est déjà créée
###-------->


class Entree_bdd:

    """
    rentrer les chemins d'accès des fichiers sons en base de données, leur attribuer un id 
    déplacer les fichiers sons et les nommer en fonction de l'id
    """


    def __init__(self) -> None:
        self.conn = connect.Conn()
        self.path_dossier_son_glob = '/home/erwan/Musique/IRISH/*.mp3'
        self.path_dossier_son = '/home/erwan/Musique/sonid/'


    def insert(self) -> None:
        """
        rentrer les airs du dossier irish en bdd
        problème du caractère ' --> remplacementpar @
        """

        # parcourir l'arboresence des fichiers
        lis = [name for name in glob.glob(self.path_dossier_son_glob, recursive=True)]
        lis = [x.replace("'", "@") for x in lis]

        # enregistrer les requêtes en liste
        lis_requetes = []
        for i in range(len(lis)):
            sql = """insert into irish_path_sons(id_irish, path_son)values({},'{}');""".format(i, lis[i])
            lis_requetes.append(sql)
        
        self.conn.insert(lis_requetes)
          

    def create_table(self) -> None:
        """créer les tables et insérer les chemins de fichier"""

        self.conn.insert("""drop table if exists irish_path_sons;""")
        self.conn.insert("""create table irish_path_sons(id_irish int, path_son text);""")


    def move_files(self) -> None:
        """
        déplacer les fichiers et les nommer selon l'id
        """

        sql = """select id_irish, path_son from irish2 where path_son is not null;"""
        data = self.conn.fetch(sql, multi=True)
        data = pd.DataFrame(data, columns=['id', 'path'])
        data['path'] = data['path'].apply(lambda x: x.replace("@", "'"))
        data['id'] = data['id'].apply(lambda x: self.path_dossier_son + str(x) + '.mp3' )

        for i in range(data.shape[0]):
            try:
                shutil.move(data.loc[i, 'path'], data.loc[i, 'id'])
            except:
                continue



    def main(self):
        self.create_table()
        self.insert()
        self.move_files()


if __name__=='__main__':
    cl=Entree_bdd()
    cl.main()