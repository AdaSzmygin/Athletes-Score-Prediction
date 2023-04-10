from bs4 import BeautifulSoup as BS
from selenium import webdriver
from functools import reduce
import pandas as pd
import time

#Strona ładuje zawartość z opóźnieniem, poniższa metoda włącza sterownik chrome i oczekuje na zawartość
def render_page(url):
    driver = webdriver.Chrome('path_to/chromedriver')
    driver.get(url)
    time.sleep(3)
    r = driver.page_source
    driver.quit()
    return r

def scraper(page, dates):
    
    for d in dates:
        url = str(str(page) + str(d))
        r = render_page(url)
        soup = BS(r, "html.parser")
        container = soup.find('lib-city-history-observation')
        check = container.find('tbody')

        data = []

        for c in check.find_all('tr', class_='ng-star-inserted'):
            for i in c.find_all('td', class_='ng-star-inserted'):
                trial = i.text
                trial = trial.strip('  ')
                data.append(trial)
        print(data)
        Time=[]
        Temperature=[]
        #Dew_Point=[]
        Humidity=[]
        #Wind=[]
        #Wind_Speed=[]
        #Wind_Gust=[]
        Pressure=[]
        Precipitation=[]
        #Condition=[]
        if(len(data)>9 & len(data)<241):
            for i in range(0,len(data),10):
                Time=data[i]
                Temperature=data[i+1]
                Humidity=data[i+3]
                Pressure=data[i+7]
                Precipitation=data[i+8]
            return Time, Temperature,  Humidity,  Pressure, Precipitation
        else:
            print('No data found!')

    return None


#dates = ['2019-4-12']
#page = 'https://www.wunderground.com/history/daily/pt/lisbon/date/'

#df = scraper(page, dates)
#print(df)