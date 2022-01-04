from cnbcscraper import cnbc
from investingscraper import investing
from seekingalphascraper import Scraper
from yahoofinancescraper import get_article
from pymongo import MongoClient
import pandas as pd

class scheduler:

    def __init__(self,number,ticker):
        self.number = number
        self.ticker = ticker

    def cnbc(self):
        x = cnbc(self.number).load_page()
        return x
    
    def connect_to_mongodb(self,db):
        URL = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

        client = MongoClient(URL)
        return client[db]
    
    def investing(self):
        x = investing(self.number).get_articles()
        return x
    
    def seekingalpha(self):
        x = Scraper(self.number).main()
        return x

    def yahoofinance(self):
        x = get_article('https://finance.yahoo.com/quote/AAPL/news?p='+self.ticker).main()
        return x

    def main(self):

        cnbc = self.cnbc()
        investing = self.investing()
        seekingalpha = self.seekingalpha()
        yahoofinance = self.yahoofinance()

        seekingalpha_db = self.connect_to_mongodb('seekingalpha24')
        seekingalpha_cl = seekingalpha_db['test01']
        seekingalpha_cl.insert_one(seekingalpha)

        investing_db = self.connect_to_mongodb('investing')
        investing_cl = investing_db['test01']
        investing_cl.insert_one(investing)

        cnbc_db = self.connect_to_mongodb('cnbc')
        cnbc_cl = cnbc_db['test01']
        cnbc_cl.insert_one(cnbc)

        yf_db = self.connect_to_mongodb('yfk')
        yf_cl = yf_db['test01']
        yf_cl.insert_one(yahoofinance)


scheduler(2,'AAPL').main()