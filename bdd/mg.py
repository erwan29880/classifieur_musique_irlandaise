from pymongo import MongoClient 

class Conn:
    
    def __init__(self) -> None:
        self.col = None
        self.conn = None 


    def connect(self) -> None:
        self.conn = MongoClient(host = "localhost",
                                port = 27018,
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
        
        
    def fetch(self) -> None:
        self.connect()
        cursor = self.col.find({})
        for i in cursor:
            print(i)
        self.close()
        
        
    def insert(self, my_dict) -> None:        
        self.connect()
        self.col.insert_one(my_dict)
        self.close()