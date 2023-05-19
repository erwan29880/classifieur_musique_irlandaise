import os
import pandas as pd
import sys 
sys.path.append('/home/erwan/Musique/')
from bdd import connect
import shutil



class Create_dataset:

    """
    Création d'un dataset d'images labellisées, selon l'architecture keras.utils.image_dataset_from_directory
    les ids sont associés aux noms d'images
    """


    def __init__(self):
        self.conn = connect.Conn()
        self.df = None
        self.path = '/home/erwan/Musique/data/images/'
        self.path_dataset = '/home/erwan/Musique/data/dataset/'

    def select(self) -> None:

        """
        créer un dataset d'entraînement : 
            - choix des airs en fonction du nombre d'air (cf la matrice créée avec rentrer_danse_noms.py) 
            - choix d'airs labellisés manuellement (deux derniers inserts de la procédure stockée ci-dessous)
        """

        sql = """
        create or replace function create_dataset()
        returns table(id int, clas VARCHAR(20))
        as $$
        BEGIN
            drop table if exists train_dataset;
            create table train_dataset(id_irish int, classe VARCHAR(20));
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where reel>=3;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where jig>=3;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where hornpipe>=2;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where polka>=3;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where marche>=2;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where slide>=2;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where slipjig>=2;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where strathspey>=2;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where waltz>=2;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where mazurka>=2;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish_music_classification_by_name where barndance>=2;
            insert into train_dataset select id_irish, 'song' as classe from irish2 where danse_nom='song';
            insert into train_dataset select id_irish, 'song' as classe from irish2 where song1609='song' and id_irish<=3104;
            insert into train_dataset select id_irish, 'nonsong' as classe from irish2 where song1609!='song' and id_irish<=3104;
            
            return query select id_irish, classe from train_dataset;
        --	drop table if exists train_dataset;
            
        END;
        $$ LANGUAGE plpgsql;
        """

        self.conn.insert(sql)
        res = self.conn.procedure('create_dataset')
        self.df = pd.DataFrame(res, columns=['id_irish', 'classe'])
        self.df = self.df.drop_duplicates(subset='id_irish').reset_index(drop=True)
        


    def make_source(self, id:int) -> str:
        file = str(id) + '.png'
        return os.path.join(self.path, file)


    def make_dest(self, id:int, label:int) -> str:
        file = str(id) + '.png'
        if label==0: # nonsong
            return os.path.join(self.path_dataset,'0',file)
        else:
            return os.path.join(self.path_dataset,'1',file)


    def make_dirs(self) -> None:
        """
        créé les dossiers du dataset de train, selon l'architecture préconisée par keras.utils.image_dataset_from_directory
        """
        if os.path.exists(self.path_dataset):
            shutil.rmtree(self.path_dataset)
        os.mkdir(self.path_dataset)
        os.mkdir(os.path.join(self.path_dataset, '0'))
        os.mkdir(os.path.join(self.path_dataset, '1'))


    def copy(self) -> None:

        """
        récupère id et classe du dataset créé, et copie les images (liées à l'id) dans le dossier dataset en vue de l'entraînement du modèle
        """

        for i in range(self.df.shape[0]):
            id = self.df.loc[i,'id_irish']
            label = 0 if self.df.loc[i, 'classe']=='song' else 'nonsong'

            source = self.make_source(id)
            destination = self.make_dest(id, label)

            shutil.copy(source, destination)



    def main(self) -> None:
        self.select()
        self.make_dirs()
        self.copy()


if __name__=="__main__":
    cl=Create_dataset()
    cl.main()