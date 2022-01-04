# importing libraries and packages
import snscrape.modules.twitter as sntwitter
import pandas as pd
import time
from pymongo import MongoClient



class get_tweets:

    def __init__(self,query,count,since='',until=''):
        self.query = query
        self.count = count
        self.since = since
        self.until = until
        self.tweets_list2 = []
        self.search_query_date = '{} since:{} until:{}'
        self.file_name = '{}_{}_{}_{}'
    
    def connect_to_mongodb(self,db):
        URL = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

        client = MongoClient(URL)
        return client[db]
        
    def get_tweets(self):
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(self.search_query_date.format(self.query,self.since,self.until)).get_items()):
            print(i)
            if i>self.count:
                break
            self.tweets_list2.append([tweet.date, tweet.id, tweet.content])
        #self.debug()
        tweets_df1 = pd.DataFrame(self.tweets_list2, columns=['Datetime', 'Tweet Id', 'Text'])
        tweets_df1.to_csv(self.filename.format(self.query,self.count,self.since,self.until))
    def debug(self):
        print(self.tweets_list2)
        print(self.search_query_date.format(self.query,self.since,self.until))

get_tweets('AAPL',5,since='2012-02-02',until='2013-02-02').get_tweets()