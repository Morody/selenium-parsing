from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')
import time


options = webdriver.ChromeOptions()

options.add_argument("--start-maximized")


driver = webdriver.Chrome(options=options)
driver.get("https://mnp.economy.gov.ru/geo/geomnp/viewapp/?user_id=undefined&uin=9270100002020302202406211")



time.sleep(5)

searchButton = driver.find_element(By.CSS_SELECTOR, 'span#button-1006-btnWrap')

ActionChains(driver).click(searchButton).perform()

time.sleep(5)

searchBoxBottom = driver.find_element(By.CSS_SELECTOR, 'div#tool-1310-toolEl')
ActionChains(driver).click(searchBoxBottom).perform()

time.sleep(15)


#searchToolBar = driver.find_element(By.CSS_SELECTOR, 'a#ShowUnplugLayersListBtn')
#ActionChains(driver).click(searchToolBar).perform()

#time.sleep(15)

searchCheckBox = driver.find_elements(By.CSS_SELECTOR, 'div.x-grid-cell-inner ')[8]
ActionChains(driver).double_click(searchCheckBox).perform()

time.sleep(5)

searchListObj = driver.find_element(By.CSS_SELECTOR, 'a#BuildRListForPlugLayerBtn')
ActionChains(driver).click(searchListObj).perform()

time.sleep(20)

firstObj = driver.find_element(By.XPATH, "//table[@id='tableview-1175-record-44113']") # id записей постоянно обновляются, нужно менять
ActionChains(driver).click(firstObj).perform()

time.sleep(5)

focusOnMap = driver.find_element(By.CSS_SELECTOR, 'a#PanMapByCurrRpGrListObjBtn')
ActionChains(driver).click(focusOnMap).perform()

time.sleep(5)

ActionChains(driver).move_to_element_with_offset(focusOnMap,-423,15).perform() # в зависимости от экрана нужно менять координаты

time.sleep(5)

searchCoordinate = driver.find_element(By.CSS_SELECTOR, 'div.custom-mouse-position')

print(searchCoordinate.text)

time.sleep(5)

firstObjId = driver.find_element(By.XPATH, "//table[@id='tableview-1175-record-44113']/tbody/tr/td") # id записей постоянно обновляются, нужно менять

print(firstObjId.text)

time.sleep(5)

driver.close()