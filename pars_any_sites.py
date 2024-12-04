from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')
import time

driver = webdriver.Chrome()
driver.get("https://fgistp.economy.gov.ru/")

# Ищем раздел "Документы" и кликаем. Второй из списка с тэгом button
searchBox=driver.find_elements(By.CSS_SELECTOR, 'button.btn__card')[1]
ActionChains(driver).click(searchBox).perform()

time.sleep(3)
# Ищем поиск и набираем "Казань"
inputBox=driver.find_element(By.CSS_SELECTOR, 'input#__BVID__27').send_keys('Казань', Keys.ENTER)
time.sleep(5)

# Выбриаем первый генплан Казани от 21.06.24, второй из списка с тэгом li
searchString = driver.find_elements(By.CSS_SELECTOR, 'li.list-group-item')[1]

ActionChains(driver).click(searchString).perform()

time.sleep(7)

searchTitle = driver.find_element(By.CSS_SELECTOR, 'div#collapse-1733147156358')

ActionChains(driver).click(searchTitle).perform()

time.sleep(7)

driver.close()

