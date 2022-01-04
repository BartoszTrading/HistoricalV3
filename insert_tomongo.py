from pymongo import MongoClient
import pandas as pd
import os
import json
import numpy as np
class Mongo:

    def __init__(self,folder,dir,date_from,date_to):
        self.folder = folder
        self.dir = dir
        self.files = os.listdir(folder+'/'+dir+'_label_sentiment')
        self.date_from = date_from
        self.date_to = date_to    

    def connect_to_mongodb(self,db):
        URL = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

        client = MongoClient(URL)
        return client[db]

    def upload_to_mongo(self):
        col = self.connect_to_mongodb(self.date_from+'-'+self.date_to)
        for file in self.files:
            collection = col[file+self.folder]
            df = pd.read_csv(self.folder+'/'+self.dir+'_label_sentiment/'+file)
            columns = list(df.columns)
            columns_del = [x for x in columns if 'Unnamed' in x]
            for dell in columns_del:
                del df[dell]
            
            columns_upd = list(df.columns)
            dict_save = {}

            for column in range(len(df)):
                list_t = []
                for y in columns_upd:
                    list_t.append(df[y][column])
                dict_save[str(column)] = list_t
            
            dict_save_c = dict_save.copy()
            
            for key, value in dict_save_c.items():
                for x in value:
                    #print(type(x))
                    if isinstance(x, np.int64):
                        value[value.index(x)] = int(x)
                    if isinstance(x, np.int64):
                        #print('CRICITAL ERROR')
                        pass
                        

            collection.insert_one(dict_save)



#So i think, that every documnet in the collection, should represent one day or two for example, we can download data in format like this 28-29 29-30 etc