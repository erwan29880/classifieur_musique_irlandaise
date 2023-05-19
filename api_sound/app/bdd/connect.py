import psycopg2 
from bdd import param
import pandas as pd

class Conn:

    """effectuer les requêtes à la base de données"""

    def __init__(self):
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


    def df(self) -> pd.DataFrame:
        self.__ouvrir()
        data = pd.read_sql("select * from irish2;", self.__conn)
        self.__fermer()
        return data
        

    def find_cols(self) -> list:
        sql = """SELECT distinct COLUMN_NAME as col FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='irish2' 
        and COLUMN_NAME like 'lstm%' 
        or COLUMN_NAME like 'cnn%'
        or COLUMN_NAME like 'vgg%';"""
        return self.fetch(sql)
    
    
    def col_count_dict(self) -> list:
        dico = []
        for col in self.find_cols():
            x = self.fetch(f"select count(*) from irish2 where {col} is not null;")[0]
            if x > 15000:
                dico.append(col)
        return dico