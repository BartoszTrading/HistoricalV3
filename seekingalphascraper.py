import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from requests.structures import CaseInsensitiveDict
from selenium import webdriver
from datetime import datetime
from pymongo import MongoClient
from insert_tomongo import Mongo

class Scraper:

    def __init__(self,range):   
        self.dict_ ={}
        self.range = range
        self.link = 'https://seekingalpha.com/market-news?page='
        self.headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "accept-encoding": "gzip, deflate, br",
                        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
                        "cache-control": "max-age=0",
                        "dnt": "1",
                        "sec-fetch-dest": "document",
                        "sec-fetch-mode": "navigate",
                        "sec-fetch-site": "none",
                        "sec-fetch-user": "?1",
                        'Cookie':'CONSENT=YES+cb.20210418-17-p0.it+FX+917; ',
                        "upgrade-insecure-requests": "1",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}
        
    def main(self):
        master_list = []
        for page_num in range(1,self.range):
            result = self.get_info2(page_num)
            list_ = self.scrape(result)
            master_list.append(list_)
        col = self.connect_to_mongodb('SEEKING5')
        return self.dict_
        # for key,value in self.dict_.items():
        #     collection = col[key]
        #     #ollection.insert(self.dict_[key])
    def get_info(self,page_num):
        master_list = []
        response = requests.get(self.link+str(page_num),headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        li_class = soup.find_all('li',{'class':'mc'})
        
        tickers = []

        for li in li_class:
            list_ = []
            ticker = li.find('a',{'sasource':'ticker_mc_quote'})
            if ticker is None:
                continue
            link_n = li.find('div',{'class':'title'})
            link = link_n.find('a')['href']
            list_.append(link)
            list_.append(ticker.text)
            tickers.append(ticker)
            master_list.append(list_)
        return master_list
    def get_info2(self,page_num):
        master_list = []
        link_list = []
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path= r'c:/Users/tosze/Desktop/geckodriver.exe',options=options)
        driver.get(self.link+str(page_num))
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for art in soup.find_all('article',{'data-test-id':'post-list-item'}):
            for a in art.find_all('a'):
                if a['href'][:5] == '/news':
                    link_list.append(a['href'])
                    list_ = []
                    list_.append(a['href'])
                    tic = art.find('footer',{'data-test-id':'post-footer'})
                    
                    #find ticker 
                    ticke = 'None'
                    tickg = None
                    if tic != None:

                        tick = tic.find('a')
                        if tick != None:
                            tickg = tick.find('span')
                        if tickg != None:
                            ticke = tickg.text
                    #append title of article
                    list_.append(a.text)
                    if a.text == '' or 'Comment' in a.text:
                        continue
                    list_.append(ticke)
                    master_list.append(list_)
        
        driver.close()
        return master_list
    def connect_to_mongodb(self,db):
        URL = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

        client = MongoClient(URL)
        return client[db]


    def scrape(self,list): #implement multithreadiing (Not important, but its worth a try     )
        master_list = []
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path= r'c:/Users/tosze/Desktop/geckodriver.exe',options=options)
        counter = 0

        start = time.time()
        for item in list:
            counter += 1
            #print('https://seekingalpha.com'+str(item[0]))
            driver.get('https://seekingalpha.com'+str(item[0]))
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            date = soup.find('span',{'data-test-id':'post-date'})
            try:
                dates = date.text
            except AttributeError:
                continue
            date_object = datetime.strptime(dates[:-6],'%b. %d, %Y %H:%M')
            # %b. %d, %Y
            try:
                hg = 0
                #print(date.text)
            except AttributeError:
                date = 0
            text = []
            texts = soup.find('div',{'data-test-id':'article-content'})
            if texts == None:
                continue
            for t in texts.find_all('li'):
                try:
                    if t.text != 'Press Release':
                        text.append(t.text)
                except AttributeError:
                    continue
            #print(text)
            try: 
                self.dict_[str(item[2])][str(date_object)].append(text)
            except KeyError:
                try:
                    self.dict_[str(item[2])][str(date_object)] = []
                except KeyError:
                    self.dict_[str(item[2])] = {}
                    self.dict_[str(item[2])][str(date_object)] = []
                self.dict_[str(item[2])][str(date_object)].append(text)
            #master_list.append([text,date_object.day+':'+date_object.month])
        # print(master_list)
        return master_list
# x = Scraper(2).main()
# print(x)
