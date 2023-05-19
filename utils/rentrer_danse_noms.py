import os
import pandas as pd
from bdd import connect


class Danse_noms:

    """
    cette classe :

        fonction insert : 
            - traite les noms d'airs, associés à une danse, webscrappés depuis le site https://thesession.org/, et initialement rentrés dans des fichiers texte dans le dossier tunes
            - filtre les noms d'airs si ils sont trop courts, filtre le mot 'gan ainm' qui signifie air inconnu
            - supprime les noms d'airs dupliqués
            - rentre les données en base de données
        
        fonction traitement :
            - procédure stockée afin de créer une matrice de comptage du nombre d'occurence de noms de danses par piste audio, par danse ; en postgresql 14

    """


    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.dossier_tunes = os.path.join(self.path, 'tunes')
        self.conn = connect.Conn()


    def insert(self) -> None:
        """
        - traite les noms d'airs, associés à une danse, webscrappés depuis le site https://thesession.org/, et initialement rentrés dans des fichiers texte dans le dossier tunes
        - filtre les noms d'airs si ils sont trop courts, filtre le mot 'gan ainm' qui signifie air inconnu
        - supprime les noms d'airs dupliqués
        - rentre les données en base de données
        """
        
        dico = dict()
        requetes_sql = []       
        inc = 0

        self.conn.insert("""DROP TABLE IF EXISTS danse_noms;""")
        self.conn.insert("""CREATE TABLE danse_noms(danse VARCHAR(20), nom text);""")

        for name in os.listdir(self.dossier_tunes):
            file= os.path.join(self.dossier_tunes, name)
    
            danse = name.split('.')[0]

            with open(file, 'r') as f:
                res = f.readlines()
                res = [x for x in res if not 'ainm' in x.lower()]
                res = [x.replace("\n", '') for x in res]
                res = [x for x in res if len(x)>6]                 

            # rentrer les données dans un dictionnaire avec clé incrémentable
            for i in res:
                dico[inc]=[danse, i]
                inc = inc+1
            
        # utiliser la fonction qui supprime les entrées dupliquées de la librairie pandas
        df = pd.DataFrame(dico).T.copy()
        df.columns = ['danse', 'nom']
        df = df.drop_duplicates(subset="nom").reset_index(drop=True)
        
        # mettre les requêtes dans une liste
        for i in range(df.shape[0]):
            sql = """insert into danse_noms (nom, danse) values ('{}', '{}');""".format(df.loc[i, 'nom'], df.loc[i, 'danse']) 
            requetes_sql.append(sql)

        # insérer les données
        self.conn.insert(requetes_sql)




    def traitement(self) -> None:

        sqlFunction = """
            CREATE OR REPLACE FUNCTION classe_music_by_name()
            RETURNS void
            AS $total$
            BEGIN

                drop table if exists irish_music_classification_by_name;
                create table irish_music_classification_by_name (id_irish int,  path_son text, hornpipe int, strathspey int, waltz int, slipjig int, mazurka int, jig int, marche int, barndance int, polka int, reel int, slide int, song int); 
                insert into irish_music_classification_by_name (id_irish, path_son) select id_irish, path_son from irish2;
                update irish_music_classification_by_name set hornpipe=0, strathspey=0, waltz=0, slipjig=0, mazurka=0, jig=0, marche=0, barndance=0, polka=0, reel=0, slide=0, song=0;

                do
                $$
                declare r record;
                begin
                    for r in 
                    select danse, nom from danse_noms
                    loop
                    
                        if r.danse='reel' then update irish_music_classification_by_name set reel=reel+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='jig' then update irish_music_classification_by_name set jig=jig+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='hornpipe' then update irish_music_classification_by_name set hornpipe=hornpipe+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='marche' then update irish_music_classification_by_name set marche=marche+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='waltz' then update irish_music_classification_by_name set waltz=waltz+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='starthspey' then update irish_music_classification_by_name set strathspey=strathspey+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='slipjig' then update irish_music_classification_by_name set slipjig=slipjig+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='slide' then update irish_music_classification_by_name set slide=slide+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='polka' then update irish_music_classification_by_name set polka=polka+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='mazurka' then update irish_music_classification_by_name set mazurka=mazurka+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='barndance' then update irish_music_classification_by_name set barndance=barndance+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='song' then update irish_music_classification_by_name set song=song+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        else raise notice '%', r.danse;
                        end if;

                    raise notice '% %', upper(r.danse), upper(r.nom);
                    end loop;
                end;
                $$;

            END;
            $total$ LANGUAGE plpgsql;
        """

        self.conn.insert(sqlFunction)
        self.conn.insert("""select * from classe_music_by_name();""")



    def main(self):
        print('------>')
        print('traitement des fichiers')
        self.insert()
        print('fichiers traités')
        print('Création et exécution de la procédure stockée, temps estimé : 7 minutes')
        self.traitement()
        print('done')
        


if __name__=='__main__':
    cl = Danse_noms()
    cl.main()