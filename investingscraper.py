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


class investing:

    def __init__(self,number_pages):
        self.number_pages = number_pages
        self.base_url = 'https://www.investing.com/news/stock-market-news/{}'
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

    def get_page(self):
        
        link_list = []
        
        for x in range(1,self.number_pages):
            

            options = Options()
            
            options.add_argument("--headless")
            
            options.add_argument("--disable-gpu")

            driver = webdriver.Firefox(executable_path= r'c:/Users/tosze/Desktop/geckodriver.exe',options=options)

            driver.get(self.base_url.format(x))

            sleep(2)

            driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()

            soup = BeautifulSoup(driver.page_source)

            driver.close()

            articles = soup.find_all('article',{'class':'js-article-item articleItem'})

            for article in articles:

                href = article.find('a')['href']

                link_list.append(href)

        return link_list
    
    def get_articles(self):

        links = self.get_page()

        options = Options()
        
        options.add_argument("--headless")
        
        options.add_argument("--disable-gpu")

        driver = webdriver.Firefox(executable_path= r'c:/Users/tosze/Desktop/geckodriver.exe',options=options)

        article_list = {}

        i=0

        for link in links:

            article = ''

            i+=1

            driver.get('https://www.investing.com/'+link)

            sleep(1)

            try:
                driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            except:
                pass
            try:
                driver.find_element_by_xpath('/html/body/div[6]/div[2]/i').click()
            except:
                pass

            soup = BeautifulSoup(driver.page_source)

            div = soup.find('div',{'class':'WYSIWYG articlePage'})

            time_ = soup.find('div',{'class':'contentSectionDetails'})
            time_ = time_.find('span')
            try:
                print(time_)
                time_ = time_.text.split('(')
                time_ = time_[1].split(')')
                time_date = time_[0]
                print(time_date)
            except IndexError:
                time_date = str(i)

            p = div.find_all('p')

            for paragraph in p:
                article += ' '+paragraph.text+' '


            article_list[time_date] = article

        driver.close()
        return article_list

# x = investing(3).get_articles()
# print(x)
    
