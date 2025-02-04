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
import math

options = webdriver.ChromeOptions()

options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
url = 'https://www.avito.ru/kazan/kvartiry/prodam/novostroyka-ASgBAgICAkSSA8YQ5geOUg?context=H4sIAAAAAAAA_wEtANL_YToxOntzOjg6ImZyb21QYWdlIjtzOjE2OiJzZWFyY2hGb3JtV2lkZ2V0Ijt9F_yIfi0AAAA'

str = 'https://geocode-maps.yandex.ru/1.x/?apikey=8a764659-98c0-4eb9-8683-ef1591e7db86&geocode=Дубай, бульвар Мухаммед Бин Рашид, дом 1&format=json'

driver.get(url)

res_table = pd.DataFrame({
    'Цена за м2' : [],
    'Координаты' : []
})

ads_count = driver.find_element(By.XPATH, "//span[@data-marker='page-title/count']").text.replace(' ','') # количество объявлений

page_count = driver.find_elements(By.XPATH, "//nav[@aria-label='Пагинация']/ul/li")[7]
df = pd.read_excel('data.xlsx')

num_curr_recs = df.shape[0]
start_page = math.ceil(num_curr_recs / 50) if (num_curr_recs // 50) != 0 else 1

for page in range(start_page, start_page + 1): # увеличивать на 20
    driver.get(f'{url}&p{page}')
    driver.implicitly_wait(3)    
    ads_elements = driver.find_elements(by=By.XPATH, 
                                        value='//div[@data-marker="item"]')
    for ad in ads_elements:
        print(ad.text)
        priceSquare = re.search(r'[ \d]+ ₽ за м²', ad.text)
        address = re.search(r'ул. [А-Яа-яёЁ0-9,.\-\/ ]+', ad.text)

        if (address is None):
            pass
        else:
            response = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey=8a764659-98c0-4eb9-8683-ef1591e7db86&geocode=Казань, {address[0]}, &format=json')

            InBetweenRes = re.search(r'pos[\d\"\.\: ]+}', response.text)
            ListPos = re.search(r'[\d\. ]+', InBetweenRes[0])[0].split(' ')

            temp_data = pd.DataFrame({
            'Цена за м2' : [priceSquare[0]],
            'Координаты' : [f'{ListPos[1]} {ListPos[0]}']
            })

            res_table = res_table._append(temp_data)


    print(f"Страница {page} готова")

df_finally_res = pd.concat([
        df,
        res_table
])
df_finally_res.to_excel('data.xlsx', index=False)


driver.close()