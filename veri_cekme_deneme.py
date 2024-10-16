import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

browser=webdriver.Chrome()
url="https://yokatlas.yok.gov.tr/lisans.php?y=110110385"
browser.get(url)
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div[1]/div[4]/span/span/a[1]"""))).click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="icerik_1020ab"]/table[2]""")))
page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')
table = browser.find_element(By.XPATH,"""//*[@id="icerik_1020ab"]/table[2]""").get_attribute('outerHTML')
table = BeautifulSoup(table, 'html.parser')
rows = table.find_all('tr')
rows=rows[2:]
for row in rows:
    region=row.find_all('td')[0].text
    student_number=row.find_all('td')[1].text
    print(region,student_number)

browser.close()