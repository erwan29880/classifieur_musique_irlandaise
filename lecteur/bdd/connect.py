from bdd import param
import psycopg2

class Conn:
    
    """
    classe de connexion à la base de données pour tkinter
    sélectionner des songs, tunes, ou labelliser des airs
    
    """

    
    def __init__(self) -> None:
    
        self.__host = param.HOST 
        self.__user = param.USER
        self.__password = param.PASSWORD
        self.__database = param.DATABASE
        self.cur = None
        self.conn = None
        self.path = '/media/bob/media/sonid/'


    def ouvrir(self) -> None:
        """ 
            ouverture de la connection
        """
        self.conn = psycopg2.connect(host=self.__host,
                                    database=self.__database,
                                    user=self.__user,
                                    password=self.__password)
        self.cur = self.conn.cursor()


    def get_songs(self) -> list:
        """ 
            importer des airs pour labellisation
        """
        
        self.ouvrir()
        self.cur.execute("select id_irish from irish2 where labelised!=1 order by id_irish;")
        res = self.cur.fetchall()
        res = [self.path+str(x[0])+'.mp3' for x in res]
        self.fermer()
        return res


    def eval(self) -> list:
        """
            importer le dataset d'évaluation pour labellisation
        """
        
        self.ouvrir()
        self.cur.execute("""select id_irish from irish2 where lower(path_son) like '%harpe%' and labelised2 is null ;""")
        res = self.cur.fetchall()
        res = [self.path+str(x[0])+'.mp3' for x in res]
        self.fermer()
        return res


    def get_random_nonsongs(self) -> list:
        """  
            importer des airs instrumentaux
        """
        
        self.ouvrir()
        self.cur.execute("select id_irish from irish2 where vgg2<0.5 and vgg_11_14>0.5 and id_iter2!=(select id_nom_danses from nom_danses where danse='song') and id_iter2!=(select id_nom_danses from nom_danses where danse='slowair') order by random() limit 100;")
        res = self.cur.fetchall()
        res = [self.path+str(x[0])+'.mp3' for x in res]
        self.fermer()
        return res


    def get_random_songs(self) ->list:
        """  
            importer des chansons
        """
        
        self.ouvrir()
        self.cur.execute("with agg as(select id_irish, case when vgg_11_14<0.5 then 'song' else 'nonsong' end as classe from irish2) select * from agg where classe='song' order by random() limit 100;")
        res = self.cur.fetchall()
        res = [self.path+str(x[0])+'.mp3' for x in res]
        self.fermer()
        return res

   
    def get_random_slowairs(self) -> list:
        """  
            importer des chansons
        """
        
        self.ouvrir()
        self.cur.execute("select id_irish from irish2 where cnn2>0.5 and vgg_11_14>0.3 order by random() limit 100;")
        res = self.cur.fetchall()
        res = [self.path+str(x[0])+'.mp3' for x in res]
        self.fermer()
        return res   
   
   
    def exec_and_commit(self, sql) -> None:
        """  
            exécution des requètes de labellisation
        """
        self.ouvrir()
        self.cur.execute(sql)
        self.conn.commit()
        self.fermer()
         
       
    def fermer(self) -> None:
        """ 
            fermeture de la connection
        """
        
        self.cur.close()
        self.conn.close()