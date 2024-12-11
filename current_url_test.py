from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import pandas as pd
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

ButClose = driver.find_element(By.XPATH, "//div[@data-componentid='tool-1307']")
ActionChains(driver).click(ButClose).perform()

time.sleep(5)

searchListObj = driver.find_element(By.CSS_SELECTOR, 'a#BuildRListForPlugLayerBtn')
ActionChains(driver).click(searchListObj).perform()

time.sleep(20)

resTable = pd.DataFrame({
    'Name and ID': [],
    'Coordinates': []
})


for i in range(0, 5):


    OnetObj = driver.find_elements(By.XPATH, f"//div[@id='mwRightPanelGrid-body']//table[@data-recordindex='{i}']//td")[0]

    ActionChains(driver).click(OnetObj).perform()

    time.sleep(2)

    focusOnMap = driver.find_element(By.CSS_SELECTOR, 'a#PanMapByCurrRpGrListObjBtn')
    ActionChains(driver).click(focusOnMap).perform()

    time.sleep(5)

    ActionChains(driver).move_to_element_with_offset(focusOnMap,-423,15).perform() # в зависимости от экрана нужно менять координаты

    time.sleep(5)

    searchCoordinate = driver.find_element(By.CSS_SELECTOR, 'div.custom-mouse-position')
    
    tempData = pd.DataFrame({
        "Name and ID": [OnetObj.text],
        "Coordinates": [searchCoordinate.text]
    })

    resTable = resTable._append(tempData)

    ActionChains(driver).click(OnetObj).send_keys(Keys.PAGE_DOWN).perform()

    time.sleep(5)

driver.close()

resTable.to_excel('data.xlsx')