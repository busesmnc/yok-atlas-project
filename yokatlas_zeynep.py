import requests
from bs4 import BeautifulSoup
import ssl
from selenium import webdriver
import time
# import pyodbc
import sqlite3

from selenium.webdriver.common.by import By

# SSL bağlamını oluşturuyoruz
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# URL'yi çekiyoruz
url = 'https://yokatlas.yok.gov.tr/lisans-univ.php?u=1101'
response = requests.get(url, verify=False)  # SSL doğrulamasını kapatıyoruz
soup = BeautifulSoup(response.text, 'html.parser')
s=soup.find_all("h4",{"class": "panel-title"})
bolumler=[]
fakulteler=[]
linkler=[]
for i in s:
    link="https://yokatlas.yok.gov.tr/" +i.find("a").get("href")
    linkler.append(link)
    bolumler.append(i.find("div").text)
    fakulteler.append(i.find("font").text.rstrip(")").lstrip("("))
last=zip(bolumler,fakulteler,linkler)

fakult=[]
for fak in fakulteler:
    if fak not in fakult:
        fakult.append(fak)
fakult.sort()
fakult=list(enumerate(fakult,1))
print(fakult)

conn=sqlite3.connect("yokatlas.db")
cursor=conn.cursor()

# for i in last:
#     browser=webdriver.Chrome()
#     url=i[2]
#     browser.get(url)
#     try:
#         kapa=browser.find_element(By.XPATH,"/html/body/div[3]/div/span").click()
#     except:
#         print("x")
#     ac=browser.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[4]/span/span/a[1]").click()
#     time.sleep(10)
#     browser.close()
