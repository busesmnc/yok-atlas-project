import requests
from bs4 import BeautifulSoup
import ssl
from selenium import webdriver
import time
import os
# import pyodbc
import sqlite3

from selenium.webdriver.common.by import By

import urllib3
def create_tables(conn,cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS faculties (id INTEGER PRIMARY KEY, faculty_name VARCHAR(250))""")
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS departments (id INTEGER PRIMARY KEY, department_name VARCHAR(250),faculty_id INTEGER, url VARCHAR(10000))""")
    conn.commit()

def get_gender(browser,year,department_id):
    browser.find_element(By.XPATH,"""//*[@id="h1010"]/a""").click()
    time.sleep(5)
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table=soup.find_all("td",{"class": "text-center vert-align"})
    print(soup)
    genders = [g.text.strip() for g in table]
    female=genders[0]
    male=genders[2]
    print(department_id,year,male,female)
    time.sleep(15)

def generate_data_for_years(browser,department_id):
    year=2023
    get_gender(browser,year,department_id)
    year=2022
    browser.find_element(By.XPATH,"""/html/body/div[2]/div[1]/div[6]/div[2]/h2/strong/a[2]""").click()
    close_pop_up(browser)
    get_gender(browser,year,department_id)
    year=2021
    browser.find_element(By.XPATH,"""/html/body/div[2]/div[1]/div[6]/div[2]/h2/strong/a[1]""").click()
    close_pop_up(browser)
    get_gender(browser,year,department_id)


def close_pop_up(browser):
    try:
        browser.find_element(By.XPATH,"/html/body/div[3]/div/span").click()
    except:
        pass
    


# SSL uyarılarını bastırma
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
db="yok-atlas-project/yokatlas.db"
if os.path.exists(db):
    os.remove(db)
conn=sqlite3.connect(db)
cursor=conn.cursor()
create_tables(conn,cursor)
cursor.executemany('''
    INSERT INTO faculties (id, faculty_name) VALUES (?, ?)
''', fakult)
conn.commit()
i=1
for l in last:
    cursor.execute("select id from faculties where faculty_name=?",(l[1],))
    faculty_id=cursor.fetchall()[0][0]
    cursor.execute("insert into departments (id,department_name,faculty_id,url) values(?,?,?,?)",(i,l[0],faculty_id,l[2]))
    conn.commit()
    i+=1

cursor.execute("select * from departments")
departments=cursor.fetchall()
for d in departments:
    url=d[3]
    browser=webdriver.Chrome()
    browser.get(url)
    close_pop_up(browser)
    generate_data_for_years(browser,d[0])
    browser.close()

# cursor.execute("SELECT * FROM departments")
# data=cursor.fetchall()
# for d in data:
#     print(d)
# Bağlantıyı kapat
conn.close()
