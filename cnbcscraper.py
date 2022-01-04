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
from time import sleep
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class cnbc:

    def __init__(self,number):
        self.number = number
        self.link_base = 'https://www.cnbc.com/stocks/?page={}'
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
        


    def load_page(self):

        options = Options()
        
        options.add_argument("--headless")
        
        options.add_argument("--disable-gpu")

        driver = webdriver.Firefox(executable_path= r'c:/Users/tosze/Desktop/geckodriver.exe',options=options)
        
        #accept cookies
        driver.get(self.link_base.format(1))

        sleep(4)
        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
        
        for x in range(1,self.number): #iterate thourgh 5 pages

            
            driver.get(self.link_base.format(x))
            
            start = time.time()
            
            scroll_pause_time = 0.2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
            
            screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web

            i=3

            while True:
                driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  

                time.sleep(scroll_pause_time)

                i+=1

                if time.time() - start > 3:
                    break
                
            links = self.parse_page(driver.page_source)
            
            ar = self.download_articles(links)

        driver.close()

        return ar

    def parse_page(self,source):

        link_list = []

        soup = BeautifulSoup(source)

        divs = soup.find_all('div',{'class':'Layout-layout'})

        for div in divs:
            
            news_ = div.find_all('div',{'data-test':'Column'})
            news_2 = div.find_all('div',{'data-test':'Card'})
            for x in news_2:
                news_.append(x)

            for news in news_:

                if news.find('div',{'class':'Card-pro'}) != None:
                    continue

                href = news.find('a')['href']
                
                link_list.append(href)

        return link_list

    def download_articles(self,links):

        article_list = {}

        for link in links:
            response = requests.get(link,headers=self.headers)
            
            article = ''

            soup = BeautifulSoup(response.text)

            divs = soup.find_all('div',{'class':'group'})

            title = soup.find('h1').text

            try:
                time_date = soup.find('time',{'data-testid':'published-timestamp'})['datetime']
            except:
                print(link)
                continue

            for div in divs:

                p = div.find_all('p')
                for paragraph in p:
                    article += ' '+paragraph.text+' '
            
            article_list[time_date] = article
        
        return article_list

# x = cnbc(2).load_page()
# for key,value in x.items():
#     print(key)

