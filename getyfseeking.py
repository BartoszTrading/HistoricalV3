from pymongo import MongoClient
import ast
import time
from datetime import datetime

class get_d:

    def __init__(self,date,ticker,sen=False):
        self.date = date
        self.ticker = ticker
        self.sen = sen
    
    def connect_to_mongodb(self,db):
        URL = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

        client = MongoClient(URL)
        return client[db]

    def get_data_yf(self,second_try=1):
            
        for try_p in range(0,7):
            col = self.connect_to_mongodb('YF_Fin7')
            if self.date == 'Newest':
                collections_list = col.list_collection_names()
                col_list_dates = [datetime.strptime(x,'%Y-%m-%d') for x in collections_list]
                if col_list_dates == 'NoneType':
                    return None
                try:
                    self.date = sorted(col_list_dates)[try_p]
                except IndexError:
                    return None
                print(self.date)
            collection = col[str(self.date)[:10]]
            obj = collection.find()
            # print(obj[0])
            list_keys = []
            for key, value in obj[0].items():
                key_ = key.replace('^','')
                try:
                    key_ = ast.literal_eval(key_)
                except ValueError:
                    #print('VALUE ERROR AT KEY: ',key_)
                    continue

                for elem in key_:
                    if elem == self.ticker:
                        return obj[0][key]
                    else:
                        continue
    
    def get_fundamental(self,cik):
        master_dict = {}
        col = self.connect_to_mongodb('Stocks_Final9')
        collections_list = col.list_collection_names()
        col_list = []
        for cik_list in collections_list:
            if cik in cik_list:
                col_list.append(cik_list)
        for cik_ in col_list:
            g = col[cik_].find()
            counter = 0
            tem_list = []
            for i in g:
                counter+=1
                tem_list.append(i)
            if counter < 5:
                master_dict[cik_[-10:]] = tem_list
                print(len(master_dict[cik_[-10:]]))
        return master_dict

    def get_data_seeking(self,ticker,before=0,after=0,day=0):
        
        #cant use day function at the same time as before and after

        if isinstance(before,str) :
            before = datetime.strptime(before,'%Y-%m-%d %H:%M:%S')
        if isinstance(after,str):
            after = datetime.strptime(after,'%Y-%m-%d %H:%M:%S')
        if isinstance(day,str):
            day = datetime.strptime(day,'%Y-%m-%d')


        col = self.connect_to_mongodb('SEEKING5')
        
        collection_list = col.list_collection_names()

        if ticker not in collection_list:
            print('{} not found'.format(ticker))
            return 0
        
        collection = col[ticker]
        data = list(collection.find())
        dates = []
        dates_filter = []

        for g in data:
            dates_ = list(g.keys())#.pop(0) #removing '_id'
            del dates_[0]
            dates_ = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in dates_]
            for x in dates_:
                dates.append(x)
        
        if day != 0:
            dates_filter = [x for x in dates if str(x.date()) == str(day.date())]
            return_data = [data[0][str(x)] for x in dates_filter]
            return return_data

        if before != 0:
            dates_filter = [x for x in dates if x<before]
        if after != 0:
            dates_filter = [x for x in dates if x>after]
        return_data = [data[0][str(x)] for x in dates_filter]
        print(dates_filter)
        return return_data[0]