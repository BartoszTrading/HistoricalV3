import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from pymongo import MongoClient

import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

path = os.path.join("C:\\Users\\tosze\\seleniumm\\phantomjs-2.1.1-windows\\bin\\phantomjs")
print(path)


class Download:

    def __init__(self,link):
        self.link = link
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
        
        self.link_list = []

        self.cookie = {
            'UID':'180PUE14MJWYEUG69A8D5Ig1633880287',
            'GUC':'AQABBAFhZFhiO0Ih_wSi',
            'GUCS':'AXfG-rnH',
            'EuConsent':'CPN3ljKPN3ljKAOACBPLBtCoAP_AAH_AACiQIJNf_X__bX9n-_59__t0eY1f9_r_v-Qzjhfdt-8F2L_W_L0H_2E7NB36pq4KuR4ku3bBIQNtHMnUTUmxaolVrzHsak2MryNKJ7LkmnsZe2dYGHtPn91T-ZKZ7_78__f73z___9_-39z3_______9____-___V_993________9nd____BBIAkw1LyALsSxwJNo0qhRAjCsJDoBQAUUAwtE1gAwOCnZWAR6ghYAITUBGBECDEFGDAIABAIAkIiAkALBAIgCIBAACAFSAhAARMAgsALAwCAAUA0LECKAIQJCDI4KjlMCAiRaKCWysASi72NMIQyywAoFH9FRgIlCCBYGQkLBzHAEgJYAYaADAAEEEhEAGAAIIJCoAMAAQQSA',
            'APID':'UP15af4a1e-7ebd-11eb-bc23-02ae808367ac',
            'B':'api6lnpgm626u&b=3&s=lg',
            'A3':'d=AQABBOEIY2ECEL95gIqdSJrKg8NU9QzBwFAFEgABBAFYZGE7Yu-bb2UB9iMAAAcI3ghjYb7VyKw&S=AQAAArsgwMIazPx3SifShplC-cs',
            'A1':'d=AQABBOEIY2ECEL95gIqdSJrKg8NU9QzBwFAFEgABBAFYZGE7Yu-bb2UB9iMAAAcI3ghjYb7VyKw&S=AQAAArsgwMIazPx3SifShplC-cs',
            'A1S':'d=AQABBOEIY2ECEL95gIqdSJrKg8NU9QzBwFAFEgABBAFYZGE7Yu-bb2UB9iMAAAcI3ghjYb7VyKw&S=AQAAArsgwMIazPx3SifShplC-cs&j=GDPR',
            'cmp':'v=21&t=1633880342&j=1'
        }

    def download(self):
        response = requests.get(self.link,headers=self.headers,cookies=self.cookie)
        soup = BeautifulSoup(response.text,'html.parser')
        return soup
    
    def parse(self):
        soup = self.download() 
        article_section = soup.find_all('div',{"id":'latestQuoteNewsStream-0-Stream-Proxy'})
        #articles = soup.find_all('li', {"class":'js-stream-content Pos(r)'})
        for article in article_section:
            links = article.find_all('a')
            for a in links:
                if 'news' in a['href']:
                    self.link_list.append(a['href'])
                    print('x')
        return self.link_list

    
    def home_page(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        driver = webdriver.Firefox(executable_path= r'c:/Users/tosze/Desktop/geckodriver.exe',options=options)
        driver.get("https://finance.yahoo.com/topic/stock-market-news")

        print(1)
        driver.execute_script("document.getElementsByClassName('btn primary')[0].click()")
        #driver.find_element_by_css_selector('.btn').click()
        #driver.find_element_by_css_selector('.btn.primary').click()
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 0.2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 3
        start = time.time()
        while True:
            # scroll one screen height each time
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            #scroll_height = driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            # if (screen_height) * i > scroll_height:
            #     break 
            if time.time() - start > 15:
                break

        ##### Extract Reddit URLs #####
        urls = []
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for parent in soup.find_all('li',{'class':"js-stream-content Pos(r)"}):
            #a_tag = parent.find("a", class_="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE")
            hrefs =  parent.find('a')
            if 'news' in hrefs['href']:
                # print(hrefs['href'])
                urls.append(hrefs['href'])
        # print(len(urls))
        driver.close()
        driver.quit()
        return urls


class get_article:

    def __init__(self,link):
        self.link = link
        self.dict_ = {}
        #self.link_list = Download(link).parse()
        self.link_list = Download('gowno').home_page()
        self.new_link_list = []

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
        
        self.cookie = {
            'UID':'180PUE14MJWYEUG69A8D5Ig1633880287',
            'GUC':'AQABBAFhZFhiO0Ih_wSi',
            'GUCS':'AXfG-rnH',
            'EuConsent':'CPN3ljKPN3ljKAOACBPLBtCoAP_AAH_AACiQIJNf_X__bX9n-_59__t0eY1f9_r_v-Qzjhfdt-8F2L_W_L0H_2E7NB36pq4KuR4ku3bBIQNtHMnUTUmxaolVrzHsak2MryNKJ7LkmnsZe2dYGHtPn91T-ZKZ7_78__f73z___9_-39z3_______9____-___V_993________9nd____BBIAkw1LyALsSxwJNo0qhRAjCsJDoBQAUUAwtE1gAwOCnZWAR6ghYAITUBGBECDEFGDAIABAIAkIiAkALBAIgCIBAACAFSAhAARMAgsALAwCAAUA0LECKAIQJCDI4KjlMCAiRaKCWysASi72NMIQyywAoFH9FRgIlCCBYGQkLBzHAEgJYAYaADAAEEEhEAGAAIIJCoAMAAQQSA',
            'APID':'UP15af4a1e-7ebd-11eb-bc23-02ae808367ac',
            'B':'api6lnpgm626u&b=3&s=lg',
            'A3':'d=AQABBOEIY2ECEL95gIqdSJrKg8NU9QzBwFAFEgABBAFYZGE7Yu-bb2UB9iMAAAcI3ghjYb7VyKw&S=AQAAArsgwMIazPx3SifShplC-cs',
            'A1':'d=AQABBOEIY2ECEL95gIqdSJrKg8NU9QzBwFAFEgABBAFYZGE7Yu-bb2UB9iMAAAcI3ghjYb7VyKw&S=AQAAArsgwMIazPx3SifShplC-cs',
            'A1S':'d=AQABBOEIY2ECEL95gIqdSJrKg8NU9QzBwFAFEgABBAFYZGE7Yu-bb2UB9iMAAAcI3ghjYb7VyKw&S=AQAAArsgwMIazPx3SifShplC-cs&j=GDPR',
            'cmp':'v=21&t=1633880342&j=1'
        }

        self.main_dict = {}

    def main(self):
        self.new_link_list = ['https://finance.yahoo.com/' + x for x in self.link_list]
        print(4)
        self.request()

        return self.dict_
    
    def connect_to_mongodb(self,db):
        URL = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

        client = MongoClient(URL)
        return client[db]

    def request(self):
        df = pd.read_csv('links.csv')
        links_csv = df['0'].to_list()
        for linka in self.new_link_list:
            if linka in links_csv:
                print('yes')
                continue
            else:
                print(linka)
                print('definietly not')
                links_csv.append(linka)
            response = requests.get(linka,headers=self.headers,cookies = self.cookie)
            soup = BeautifulSoup(response.text,'html.parser')
            x =self.parse(soup)
            self.main_dict[linka] = x
        # col = self.connect_to_mongodb('YF_Fin8')
        # for key,value in self.dict_.items():
        #     keys = str(key).replace('.',',')
        #     colection = col[keys]
        #     colection.insert(self.dict_[str(key)])
        df_new = pd.DataFrame(links_csv)
        df_new.to_csv('links.csv')

    def parse(self, soup):
        master_dict = {}
        mentioned_stocks = []
        text = []
        str1 = ' '
        
        soup = soup.find_all('article')[0]
        
        title = soup.find('h1').text
        timedate = soup.find('time')
        article = soup.find('div',{'class':'caas-body'})
        mentions = soup.find_all('a',{'class':"xray-entity-title-link link rapid-noclick-resp caas-link-no-track"})
        for m in mentions:
            mentioned_stocks.append(m.text)
        mentioned_stocks = sorted(set(mentioned_stocks))
        if len(mentioned_stocks) != 0:
            if mentioned_stocks[0] == '':
                mentioned_stocks.pop(0)
        btn = soup.find('a',{'class':'link rapid-noclick-resp caas-button'})
        # print(title)
        # print(btn)
        if btn != None:
            link = soup.find('a',{'class':'link rapid-noclick-resp caas-button'})
            text.append(link['href'])
            print('yeahhhh')
        else:
            tekst = article.find_all('p')
            for tek in tekst:
                text.append(tek.text)

        info = [str1.join(text),str(timedate['datetime']),title]
        print(timedate['datetime'][:10])
        if timedate['datetime'][:10] not in self.dict_.keys():
            self.dict_[str(timedate['datetime'][:10])] = {}
        try:
            self.dict_[str(timedate['datetime'][:10])][str(mentioned_stocks).replace('.',',')].append(info)
        except KeyError:
            self.dict_[str(timedate['datetime'][:10])][str(mentioned_stocks).replace('.',',')] = [info]

        master_dict[title] = info
        print(self.dict_)
# start =time.time()
# x = get_article('https://finance.yahoo.com/quote/AAPL/news?p=AAPL').main()
# print(x)
# # Download('https://finance.yahoo.com/quote/AAPL/news?p=AAPL').parse()
# print(time.time() -start)