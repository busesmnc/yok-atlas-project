import requests
from bs4 import BeautifulSoup
import ssl
from selenium import webdriver
import time
import os
import sqlite3
from selenium.webdriver.common.by import By
import urllib3
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
class Database_Creator():
    def __init__(self):
        self.cursor = ""
        self.conn = ""
        self.browser = webdriver.Chrome()  # Tarayıcıyı sadece bir kez başlatıyoruz
        self.index = 0
        self.f_data = []
        self.faculties = []
        self.departments = []
        self.genders = []
        self.create_database()
        self.get_departments_and_faculties()
        self.browser.close()  # İşlemler bittiğinde tarayıcıyı kapatıyoruz

    def create_database(self):
        db = "yok-atlas-project/yokatlas.db"
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS faculties (id INTEGER PRIMARY KEY, faculty_name VARCHAR(250))""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS departments (id INTEGER PRIMARY KEY, department_name VARCHAR(250),faculty_id INTEGER, url VARCHAR(10000))""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS genders (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, male INTEGER, female INTEGER)""")
        self.conn.commit()

    def close_pop_up(self):
        try:
            self.browser.find_element(By.XPATH,"/html/body/div[3]/div/span").click()
        except Exception as e:
            pass

    def get_faculty_details(self):
        self.cursor.execute("SELECT * FROM departments")
        deps = self.cursor.fetchall()
        for d in deps:
            url = d[3]
            self.browser.get(url)
            self.close_pop_up()
            self.generate_data_for_years(d[0])

    def check_existance(self):
        data = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1000_1"]/table[2]/tbody/tr[6]/td[2]"""))).text
        if data == "---":
            return False
        else:
            return True

    def generate_data_for_years(self, department_id):
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div[1]/div[4]/span/span/a[1]"""))).click()
        existance=self.check_existance()
        self.genders = []
        if existance:
            self.get_gender(2023, department_id)
        else:
            self.index+=1
            self.genders.append([self.index,department_id,2023,0,0])

        # Diğer yıllar için sırayla veriyi çekiyoruz
        for year, xpath in [(2022, "/html/body/div[2]/div[1]/div[6]/div[2]/h2/strong/a[2]"),
                            (2021, "/html/body/div[2]/div[1]/div[6]/div[2]/h2/strong/a[1]")]:
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            invalid_urls=["https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php","https://yokatlas.yok.gov.tr/lisans.php"]
            if self.browser.current_url not in invalid_urls:
                self.close_pop_up()
                WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div[1]/div[4]/span/span/a[1]"""))).click()
                existance=self.check_existance()
                if existance:
                    self.get_gender(year, department_id)
                else:
                    self.index+=1
                    self.genders.append([self.index,department_id,year,0,0])
            else:
                self.browser.back()
                break
        self.insert_datas()

    def insert_datas(self):
        if self.genders:
            self.cursor.executemany("INSERT INTO genders (id, department_id, year, male, female) VALUES (?, ?, ?, ?, ?)", self.genders)
            self.conn.commit()
        

    def get_gender(self, year, department_id):
        self.index += 1
        
        # # Tablo elemanını bulana kadar bekliyoruz
        # WebDriverWait(self.browser, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.text-center.vert-align")))

        # # Sayfa kaynağını çekiyoruz
        # page_source = self.browser.page_source
        # soup = BeautifulSoup(page_source, 'html.parser')

        # # Tablo verilerini alıyoruz
        # table = soup.find_all("td", {"class": "text-center vert-align"})
        # gnd = [g.text.strip() for g in table]
        
        female = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1010"]/table/tbody/tr[1]/td[2]"""))).text  # Kadın öğrenci sayısı
        male = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1010"]/table/tbody/tr[2]/td[2]"""))).text    # Erkek öğrenci sayısı

        # Veriyi listede tutuyoruz
        self.genders.append([self.index, department_id, year, male, female])

    def get_departments_and_faculties(self):
        url = 'https://yokatlas.yok.gov.tr/lisans-univ.php?u=1101'
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all("h4", {"class": "panel-title"})
        for i in data:
            url = "https://yokatlas.yok.gov.tr/" + i.find("a").get("href")
            department = i.find("div").text
            self.departments.append(department)
            faculty = i.find("font").text.rstrip(")").lstrip("(")
            if faculty not in self.faculties:
                self.faculties.append(faculty)
            merged_data = [department, faculty, url]
            self.f_data.append(merged_data)

        self.faculties.sort()
        self.faculties = list(enumerate(self.faculties, 1))
        # self.cursor.executemany('''INSERT INTO faculties (id, faculty_name) VALUES (?, ?)''', self.faculties)
        # self.conn.commit()
        
        i = 1
        for fd in self.f_data:
            self.cursor.execute("SELECT id FROM faculties WHERE faculty_name=?", (fd[1],))
            faculty_id = self.cursor.fetchone()[0]
            # self.cursor.execute("INSERT INTO departments (id, department_name, faculty_id, url) VALUES (?, ?, ?, ?)", (i, fd[0], faculty_id, fd[2]))
            # self.conn.commit()
            i += 1
        
        self.get_faculty_details()

Database_Creator()
