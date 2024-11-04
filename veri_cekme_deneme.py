import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser=webdriver.Chrome()
url="https://yokatlas.yok.gov.tr/lisans.php?y=110190112"
browser.get(url)
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div[1]/div[4]/span/span/a[1]"""))).click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="icerik_2040"]""")))
page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')
table = soup.find('div', {'id': 'icerik_2040'})
rows = table.find_all('tr')
leaving=0
incoming=0
if len(rows)>0:
    rows=rows[1:]
    for row in rows:
        leaving+=int(row.find_all('td')[1].text)
        incoming+=int(row.find_all('td')[2].text)

print(incoming)
print(leaving)
browser.close()