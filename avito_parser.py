from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import pandas as pd
#from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')
import time
import re

options = webdriver.ChromeOptions()

options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
url = 'https://www.avito.ru/kazan/kvartiry/prodam/novostroyka-ASgBAgICAkSSA8YQ5geOUg?context=H4sIAAAAAAAA_wEtANL_YToxOntzOjg6ImZyb21QYWdlIjtzOjE2OiJzZWFyY2hGb3JtV2lkZ2V0Ijt9F_yIfi0AAAA'

str = 'https://geocode-maps.yandex.ru/1.x/?apikey=8a764659-98c0-4eb9-8683-ef1591e7db86&geocode=Дубай, бульвар Мухаммед Бин Рашид, дом 1&format=json'

driver.get(url)

resTable = pd.DataFrame({
    'Цена за м2' : [],
    'Координаты' : []
})

#ads_count = driver.find_element(By.XPATH, "//span[@data-marker='page-title/count']").text.replace(' ','') # количество объявлений

page_count = driver.find_elements(By.XPATH, "//nav[@aria-label='Пагинация']/ul/li")[7]

for page in range(1, 2):
    driver.get(f'{url}&p{page}')
    driver.implicitly_wait(3)    
    ads_elements = driver.find_elements(by=By.XPATH, 
                                        value='//div[@data-marker="item"]')

    for ad in ads_elements:
        #resTable.add(ad.text.split('\n'))
        print(ad.text)
        


driver.close()
