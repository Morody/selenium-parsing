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
driver.get(url)

resTable = pd.DataFrame({
    'Комнаты': [],
    'Площадь': [],
    'Этаж': [],
    'Цена': [],
    'Цена за м2': [],
    'Акции': [],
    'Продавец': [],
    'Нежилая площадь': [],
    'Улица': [],
    'Район': [],
    'Близость к станции метро': [],
    'Описание': [],
    'Застройщик': [],
    'Объявления': [],
    'Реквизиты': []
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
        print(len(ad.text.split('\n')))
        


driver.close()
