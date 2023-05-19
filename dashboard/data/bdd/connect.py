import psycopg2 
from bdd import param
import pandas as pd


class Conn:

    """effectuer les requêtes à la base de données"""

    def __init__(self) -> None:
        self.__host = param.HOST
        self.__user = param.USER
        self.__password = param.PASSWORD
        self.__port = param.PORT
        self.__db = param.BDD 
        self.__cur = None 
        self.__conn = None 


    def __ouvrir(self) -> None:
        """connexion à la bdd"""

        self.__conn = psycopg2.connect(host=self.__host,
                                       user = self.__user,
                                       password=self.__password,
                                       database=self.__db,
                                       port=self.__port) 
        self.__cur = self.__conn.cursor()


    def __fermer(self) -> None:
        """fermer la connexion"""
        self.__cur.close()
        self.__conn.close()


    def insert(self, sql) -> None:
        """
        insertion de données en bdd avec une liste de requêtes ou une seule requête
        """

        self.__ouvrir()
        try:
            if isinstance(sql, list) :
                [self.__cur.execute(x) for x in sql]
            else:
                self.__cur.execute(sql)
            self.__conn.commit()
        except:
            print('an error occured while executing requests')

        self.__fermer()


    def fetch(self, sql, multi=False) -> list:

        """requête à la base de données"""

        self.__ouvrir()
        res=None
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if multi==False:
                res = [x[0] for x in res]
        except:
            print('an error occured while executing requests')

        self.__fermer()
        if res is not None:
            return res


    def procedure(self, sql) -> list:
        self.__ouvrir()
        self.__cur.callproc(sql)
        res = self.__cur.fetchall()
        self.__fermer()
        return res


    def to_df(self, sql) -> pd.DataFrame:
        self.__ouvrir()
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        cols = [desc[0] for desc in self.__cur.description]
        lis=[]
        for i in res:
            lis_child=[]
            for j in i:
                lis_child.append(j)
            lis.append(lis_child)            
        self.__fermer()
        return pd.DataFrame(lis, columns=cols)