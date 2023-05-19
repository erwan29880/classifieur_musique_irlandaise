from pymongo import MongoClient 

class Conn:
    
    """connexion à mongo"""
    
    def __init__(self) -> None:
        self.col = None
        self.conn = None 


    def connect(self) -> None:
        self.conn = MongoClient(host = "mongo_musique",
                                port = 27017,
                                username = "root",
                                password = "root",
                                )
        self.col = self.conn['musique']['irish']
        
        
    def close(self) -> None:
        self.cursor = None
        self.conn = None
        
        
    def test(self) -> list:
        self.connect()
        cursor = self.col.find({})
        ls = []
        for i in cursor:
            ls.append(i)
        self.close()
        return ls
        
        
    def delete(self, my_dict) -> None:
        self.connect()
        self.col.delete_one(my_dict)
        self.close()
        
        
    def fetch(self) -> list:
        self.connect()
        cursor = self.col.find({})
        ls = []
        for i in cursor:
            ls.append(i)
        self.close()
        return ls
        
        
    def fetch_one(self, myDict) -> dict:
        self.connect()
        cursor = self.col.find(myDict)
        self.close()
        data = cursor[0]
        data.pop("_id")
        return data
    
    
    def get_ids(self) -> list:
        self.connect()
        cursor = self.col.distinct("nom")
        ls = []
        for i in cursor:
            ls.append(i)
        ls = [int(x) for x in ls]
        ls = sorted(ls, reverse=True)
        self.close()
        return ls
    
    
    def get_data(self) -> dict:
        idx = str(self.get_ids()[-1])
        data = self.fetch_one({"nom" : idx})
        return data


    def insert(self, my_dict) -> None:        
        self.connect()
        self.col.insert_one(my_dict)
        self.close()