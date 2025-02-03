from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import requests
import pandas as pd
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
    'Цена за м2' : [],
    'Координаты' : []
})

ads_count = driver.find_element(By.XPATH, "//span[@data-marker='page-title/count']").text.replace(' ','') # количество объявлений

page_count = driver.find_elements(By.XPATH, "//nav[@aria-label='Пагинация']/ul/li")[7]
current_data = pd.read_excel('data.xlsx', index_col=0)



for page in range(1, 2):
    driver.get(f'{url}&p{page}')
    driver.implicitly_wait(3)    
    ads_elements = driver.find_elements(by=By.XPATH, 
                                        value='//div[@data-marker="item"]')
    print(len(ads_elements))
    for ad in ads_elements:
        #resTable.add(ad.text.split('\n'), fill_value=0)


        priceSqaure = re.search(r'[ \d]+ ₽ за м²', ad.text)
        address = re.search(r'ул. [А-Яа-яёЁ0-9,.\-\/ ]+', ad.text)

        if (address is None):
            pass
        else:
            response = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey=8a764659-98c0-4eb9-8683-ef1591e7db86&geocode=Казань, {address[0]}, &format=json')

            InBetweenRes = re.search(r'pos[\d\"\.\: ]+}', response.text)
            ListPos = re.search(r'[\d\. ]+', InBetweenRes[0])[0].split(' ')

            tempData = pd.DataFrame({
            'Цена за м2' : [priceSqaure[0]],
            'Координаты' : [f'{ListPos[1]} {ListPos[0]}']
            })

            resTable = resTable._append(tempData)


    print(f"Страница {page} готова")
    resTable.to_excel('data.xlsx')


driver.close()