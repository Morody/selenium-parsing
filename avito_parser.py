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
import ischedule
from datetime import datetime

def myFunc():
    options = webdriver.ChromeOptions()
    
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    
    
    driver = webdriver.Chrome(options=options)
    url = '''https://www.avito.ru/kazan/kvartiry/prodam/novostroyka-ASgBAgICAkSSA8YQ5geOUg?
                context=H4sIAAAAAAAA_wEtANL_YToxOntzOjg6ImZyb21QYWdlIjtzOjE2OiJzZWFyY2hGb3JtV2lkZ2V0Ijt9F_yIfi0AAAA'''
    
    
    driver.get(url)
    
    res_table = pd.DataFrame({
        'Цена за м2' : [],
        'Координаты' : []
    })
    
    ads_count = driver.find_element(By.XPATH, "//span[@data-marker='page-title/count']").text.replace(' ','') # текущее количество страниц с объявлениями по новостройкам на Авито
    
    page_count = driver.find_elements(By.XPATH, "//nav[@aria-label='Пагинация']/ul/li")[7]



    excel_reader = pd.ExcelFile('tables/data.xlsx')

    df_dict = {}

    for sheet_name in excel_reader.sheet_names:
	    df_dict[sheet_name] = excel_reader.parse(sheet_name)

    sheet_name = str(datetime.now().date()) # представляем в виде строки дату на данный момент - это будет название листа, в который мы запишем актуальные данные на сегодня

    num_curr_recs = 0 # количество записей уже существующих в таблице

    for i in df_dict.keys():
    	num_curr_recs += df_dict[i].shape[0]

    start_page = math.ceil(num_curr_recs / 50) if (num_curr_recs // 50) != 0 else 1 # количество объявлений уже записанных в таблице делим на 50 тем самым определяем стартовую страницу для сбора данных на текущей итерации
    
    for page in range(start_page, start_page + 20): # увеличивать на 20, т.к есть ограничение на запросы ~1000, 1 страница с Авито = 50 объявлений, 20 стр. = ~1000
        count = 0 # счетчик количества собранных объявлений со страницы
        driver.get(f'{url}&p{page}')
        driver.implicitly_wait(3)    
        ads_elements = driver.find_elements(by=By.XPATH, 
                                            value='//div[@data-marker="item"]')
        for ad in ads_elements:
            
            priceSquare = re.search(r'[ \d]+ ₽ за м²', ad.text)
            address = re.search(r'(?:ул. [А-Яа-яёЁ0-9,.\-\/ ]+|пр-т [А-Яа-яёЁ0-9,.\-\/ ]+)', ad.text)
            if (address is None):
                pass
            else:
                response = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey=8a764659-98c0-4eb9-8683-ef1591e7db86&geocode=Казань, {address[0]}, &format=json')
                count += 1
                InBetweenRes = re.search(r'pos[\d\"\.\: ]+}', response.text)
                ListPos = re.search(r'[\d\. ]+', InBetweenRes[0])[0].split(' ')
    
                temp_data = pd.DataFrame({
                'Цена за м2' : [priceSquare[0]],
                'Координаты' : [f'{ListPos[1]} {ListPos[0]}']
                })
    
                res_table = res_table._append(temp_data)
    
    
        print(f"Страница {page} готова, количество собранных объявлений:{count}")
     
    if (sheet_name in df_dict.keys()):
    	fin_data = pd.concat([
    		df_dict[sheet_name],
    		res_table
    	])
    	df_dict[sheet_name] = fin_data
    else:
    	df_dict[sheet_name] = res_table
    
    
    with pd.ExcelWriter(
    					'tables/data.xlsx',
    					engine='xlsxwriter',
    					mode='w') as excel_writer:
    						for sheet_name in df_dict.keys():
    							df_dict[sheet_name].to_excel(excel_writer, sheet_name=sheet_name, index=False)
         
    driver.close()

ischedule.schedule(myFunc, interval=60*60*24) # сутки в секундах 60*60*24
ischedule.run_loop()