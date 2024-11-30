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
        self.browser = webdriver.Chrome()
        self.index = 0
        self.index2=0
        self.index3=0
        self.f_data = []
        self.faculties = []
        self.departments = []
        self.genders = []
        self.total_student_number=[]
        self.general_info = []
        self.academicians=[]
        self.exchange_program=[]
        self.create_database()
        self.get_departments_and_faculties()
        self.browser.close()  # İşlemler bittiğinde tarayıcıyı kapatıyoruz

    def create_database(self):
        db = "yok-atlas-project/yokatlas.db"
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Cities (id INTEGER PRIMARY KEY, city_name TEXT NOT NULL)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Regions (id INTEGER PRIMARY KEY, region_name TEXT NOT NULL)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS faculties (id INTEGER PRIMARY KEY, faculty_name VARCHAR(250))""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS departments (id INTEGER PRIMARY KEY, department_name VARCHAR(250),faculty_id INTEGER, url VARCHAR(10000))""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS genders (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, male INTEGER, female INTEGER)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS correct_answers_for_say (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, tyt_fen FLOAT, tyt_sosyal FLOAT, tyt_matematik FLOAT, tyt_turkce FLOAT, ayt_biyoloji FLOAT, ayt_fizik FLOAT, ayt_kimya FLOAT, ayt_matematik FLOAT)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS correct_answers_for_ea (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, tyt_fen FLOAT, tyt_sosyal FLOAT, tyt_matematik FLOAT, tyt_turkce FLOAT, ayt_cografya1 FLOAT, ayt_matematik FLOAT, ayt_tarih1 FLOAT, ayt_edebiyat FLOAT)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS correct_answers_for_soz (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, tyt_fen FLOAT, tyt_sosyal FLOAT, tyt_matematik FLOAT, tyt_turkce FLOAT, ayt_cografya1 FLOAT, ayt_cografya2 FLOAT, ayt_din FLOAT, ayt_felsefe FLOAT, ayt_tarih1 FLOAT, ayt_tarih2 FLOAT, ayt_edebiyat FLOAT)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS correct_answers_for_dil (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, tyt_fen FLOAT, tyt_sosyal FLOAT, tyt_matematik FLOAT, tyt_turkce FLOAT, ydt_yabanci_dil FLOAT)""")
        self.conn.commit() 
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS student_cities (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, city varchar(50), student_number integer)""")
        self.conn.commit() 
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS student_regions (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, region varchar(50), student_number integer)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS base_points (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, base_point REAL)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS success_orders (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, success_order INTEGER)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS general_infos (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, prefered INTEGER, quota INTEGER, s_number INTEGER)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS total_student_number (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, male INTEGER, female INTEGER, total_number INTEGER)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS academicians (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, proffesor INTEGER, assoc_prof INTEGER, phd INTEGER)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS exchange_program (id INTEGER PRIMARY KEY, department_id INTEGER, year INTEGER, leaving INTEGER, incoming INTEGER)""")
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
            self.generate_data_for_years(d[0],d[4])

    def check_existance(self):
        data = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1000_1"]/table[2]/tbody/tr[6]/td[2]"""))).text
        if data == "---":
            return False
        else:
            return True

    def generate_data_for_years(self, department_id,department_type):
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div[1]/div[4]/span/span/a[1]"""))).click()
        # d_type=WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1000_1"]/table[1]/tbody/tr[5]/td[2]"""))).text
        # self.cursor.execute(''' UPDATE departments SET d_type = ? WHERE id = ?;''', (d_type, department_id))
        # self.conn.commit()
        print(department_id)
        existance=self.check_existance()
        self.genders = []
        self.base_points = []
        self.success_orders = []
        self.general_info = []
        self.total_student_number=[]
        self.academicians=[]
        self.exchange_program=[]
        if existance:
            self.get_gender(2024, department_id)
            self.get_points_and_orders(2024,department_id)
            self.get_cities(2024,department_id)
            self.get_regions(2024,department_id)
        else:
            self.genders.append([department_id,2024,0,0])
            self.base_points.append([department_id,2024,0])
            self.success_orders.append([department_id,2024,0])
        self.get_correct_answers(2024,department_id,department_type)
        self.get_general_info(2024,department_id)
        self.get_total_student_number(2024,department_id)
        self.get_academicians(2024,department_id)
        self.get_exchange_program(2024,department_id)
        self.index+=1
        # if existance:
        #     self.get_gender(2023, department_id)
        #     self.get_points_and_orders(2023,department_id)
        #     self.get_cities(2023,department_id)
        #     self.get_regions(2023,department_id)
        # else:
        #     self.genders.append([self.index,department_id,2023,0,0])
        #     self.base_points.append([self.index,department_id,2023,0])
        #     self.success_orders.append([self.index,department_id,2023,0])
        # self.get_correct_answers(2023,department_id,department_type)
        # self.get_general_info(2023,department_id)
        # self.get_total_student_number(2023,department_id)
        # self.get_academicians(2023,department_id)
        # self.get_exchange_program(2023,department_id)

        # # Diğer yıllar için sırayla veriyi çekiyoruz
        # for year, xpath in [(2022, "/html/body/div[2]/div[1]/div[6]/div[2]/h2/strong/a[2]"),
        #                     (2021, "/html/body/div[2]/div[1]/div[6]/div[2]/h2/strong/a[1]")]:
        #     WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        #     invalid_urls=["https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php","https://yokatlas.yok.gov.tr/lisans.php"]
        #     if self.browser.current_url not in invalid_urls:
        #         self.close_pop_up()
        #         WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div[1]/div[4]/span/span/a[1]"""))).click()
        #         existance=self.check_existance()
        #         self.index+=1
        #         if existance:
        #             self.get_gender(year, department_id)
        #             self.get_points_and_orders(year,department_id)
        #             self.get_cities(year,department_id)
        #             self.get_regions(year,department_id)
        #         else:
        #             self.genders.append([self.index,department_id,year,0,0])
        #             self.base_points.append([self.index,department_id,year,0])
        #             self.success_orders.append([self.index,department_id,year,0])
        #         self.get_correct_answers(year,department_id,department_type)
        #         self.get_general_info(year,department_id)
        #         self.get_total_student_number(year,department_id)
        #         self.get_academicians(year,department_id)
        #         self.get_exchange_program(year,department_id)
        #     else:
        #         self.browser.back()
        #         break
        self.insert_datas()

    def insert_datas(self):
        if self.genders:
            self.cursor.executemany("INSERT INTO genders (department_id, year, male, female) VALUES (?, ?, ?, ?)", self.genders)
            self.conn.commit()
        if self.base_points:
            self.cursor.executemany("INSERT INTO base_points (department_id, year, base_point) VALUES (?, ?, ?)", self.base_points)
            self.conn.commit()
        if self.success_orders:
            self.cursor.executemany("INSERT INTO success_orders (department_id, year, success_order) VALUES (?, ?, ?)", self.success_orders)
            self.conn.commit()
        if self.general_info:
            self.cursor.executemany("INSERT INTO general_infos (department_id, year, prefered ,quota,s_number) VALUES (?, ?, ?,?,?)", self.general_info)
            self.conn.commit()
        if self.total_student_number:
            self.cursor.executemany("INSERT INTO total_student_number (department_id, year, male ,female,total_number) VALUES (?, ?, ?,?,?)", self.total_student_number)
            self.conn.commit()
        if self.academicians:
            self.cursor.executemany("INSERT INTO academicians (department_id, year, proffesor, assoc_prof, phd) VALUES (?, ?, ?,?,?)", self.academicians)
            self.conn.commit()
        if self.exchange_program:
            self.cursor.executemany("INSERT INTO exchange_program (department_id, year, leaving, incoming) VALUES (?, ?, ?,?)", self.exchange_program)
            self.conn.commit()
        # pass
        

    def get_gender(self, year, department_id):
   
        female = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1010"]/table/tbody/tr[1]/td[2]"""))).text  # Kadın öğrenci sayısı
        male = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1010"]/table/tbody/tr[2]/td[2]"""))).text    # Erkek öğrenci sayısı

        self.genders.append([department_id, year, male, female])

    def get_points_and_orders(self,year,department_id):
        base_point = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1000_3"]/table[1]/tbody/tr[1]/td[4]"""))).text
        base_point=base_point.replace(",",".")
        success_order = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1000_3"]/table[2]/tbody/tr[1]/td[4]"""))).text
        success_order=success_order.replace(".","")
        self.base_points.append([department_id,year,base_point])
        self.success_orders.append([department_id,year,success_order])

    def get_general_info(self,year,department_id):
        quota= WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1000_2"]/table/tbody/tr[5]/td[2]"""))).text
        prefered= WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1080"]/table[1]/tbody/tr[1]/td[2]"""))).text
        prefered=prefered.replace(".","")
        student_number= WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_1000_2"]/table/tbody/tr[5]/td[3]"""))).text
        if student_number=="---":
            student_number=0
        self.general_info.append([department_id,year,prefered,quota,student_number])

    def get_total_student_number(self,year,department_id):
        male=0
        female=0
        total=0
        page_source = self.browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('div', {'id': 'icerik_2010'})
        rows=table.find_all('tr')
        if len(rows)>1:
            rows=rows[1:]
            for row in rows:
                gender=row.find_all('td')[0].text.split('(')[0].strip()
                data=row.find_all('td')[1].text
                if gender=="Erkek":
                    male=data
                elif gender=="Kız":
                    female=data
                elif gender=="Toplam":
                    total=data
        self.total_student_number.append([department_id,year,male,female,total])

    def get_academicians(self,year,department_id):
        prof=WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_2050"]/table/tbody/tr[1]/td[2]"""))).text
        assoc=WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_2050"]/table/tbody/tr[2]/td[2]"""))).text
        phd=WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="icerik_2050"]/table/tbody/tr[3]/td[2]"""))).text
        if prof=="---":
            prof=0
        if assoc=="---":
            assoc=0
        if phd=="---":
            phd=0
        self.academicians.append([department_id,year,prof,assoc,phd])

    def get_exchange_program(self,year,department_id):
        page_source = self.browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('div', {'id': 'icerik_2040'})
        rows=table.find_all('tr')
        leaving=0
        incoming=0
        if len(rows)>0:
            rows=rows[1:]
            for row in rows:
                leaving+=int(row.find_all('td')[1].text)
                incoming+=int(row.find_all('td')[2].text)
        self.exchange_program.append([department_id,year,leaving,incoming])

    def get_correct_answers(self,year,department_id,department_type):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="icerik_1210a"]/table""")))
        correct_answers=[department_id,year]
        page_source = self.browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('div', {'id': 'icerik_1210a'})
        rows=table.find_all('tr')
        tyt_fen = None
        tyt_sosyal = None
        tyt_matematik = None
        tyt_turkce = None
        ayt_cografya1 = None
        ayt_cografya2 = None
        ayt_din = None
        ayt_felsefe = None
        ayt_tarih1 = None
        ayt_tarih2 = None
        ayt_edebiyat = None
        ayt_matematik = None
        ayt_kimya = None
        ayt_fizik = None
        ayt_biyoloji = None
        ydt_yabanci_dil = None
        if len(rows)>1:
            rows=rows[3:]
            for row in rows:
                subject=row.find_all('td')[0].text.split('(')[0].strip()
                data=row.find_all('td')[1].text
                data = data.replace(',', '.')
                if data!="---":
                    data=float(data)
                if subject=="TYT Fen Bilimleri":
                    tyt_fen=tyt_fen or data
                elif subject=="TYT Sosyal Bilimler":
                    tyt_sosyal=tyt_sosyal or data
                elif subject=="TYT Temel Matematik":
                    tyt_matematik= tyt_matematik or data
                elif subject =="TYT Türkçe":
                    tyt_turkce =tyt_turkce or data
                elif subject =="AYT Coğrafya-1":
                    ayt_cografya1=ayt_cografya1 or data
                elif subject == "AYT Coğrafya-2":
                    ayt_cografya2= ayt_cografya2 or data
                elif subject == "AYT Din Kültürü ve Ahlak Bilgisi":
                    ayt_din= ayt_din or data
                elif subject== "AYT Felsefe Grubu":
                    ayt_felsefe=ayt_felsefe or data
                elif subject == "AYT Tarih-1":
                    ayt_tarih1=ayt_tarih1 or data
                elif subject == "AYT Tarih-2":
                    ayt_tarih2=ayt_tarih2 or data
                elif subject=="AYT Türk Dili ve Edebiyatı":
                    ayt_edebiyat=ayt_edebiyat or data
                elif subject=="AYT Matematik":
                    ayt_matematik=ayt_matematik or data
                elif subject =="AYT Kimya":
                    ayt_kimya=ayt_kimya or data
                elif subject == "AYT Fizik":
                    ayt_fizik=ayt_fizik or data
                elif subject == "AYT Biyoloji":
                    ayt_biyoloji=ayt_biyoloji or data
                elif subject =="YDT Yabancı Dil":
                    ydt_yabanci_dil=ydt_yabanci_dil or data
            if department_type=="SAY":
                correct_answers+=[tyt_fen,tyt_sosyal,tyt_matematik,tyt_turkce,ayt_biyoloji,ayt_fizik,ayt_kimya,ayt_matematik]
            elif department_type=="EA":
                correct_answers+=[tyt_fen,tyt_sosyal,tyt_matematik,tyt_turkce,ayt_cografya1,ayt_matematik,ayt_tarih1,ayt_edebiyat]
            elif department_type=="SÖZ":
                correct_answers+=[tyt_fen,tyt_sosyal,tyt_matematik,tyt_turkce,ayt_cografya1,ayt_cografya2,ayt_din,ayt_felsefe,ayt_tarih1,ayt_tarih2,ayt_edebiyat]
            elif department_type=="DİL":
                correct_answers+=[tyt_fen,tyt_sosyal,tyt_matematik,tyt_turkce,ydt_yabanci_dil]       
        else:
            if department_type=="SAY" or department_type=="EA":
                correct_answers+=[0,0,0,0,0,0,0,0]
            elif department_type=="SÖZ":
                correct_answers+=[0,0,0,0,0,0,0,0,0,0,0]
            elif department_type=="DİL":
                correct_answers+=[0,0,0,0,0]
        correct_answers=tuple(correct_answers)
        if department_type=="SAY":
            self.cursor.execute("INSERT INTO correct_answers_for_say(department_id, year, tyt_fen,tyt_sosyal,tyt_matematik,tyt_turkce,ayt_biyoloji,ayt_fizik,ayt_kimya,ayt_matematik) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", correct_answers)
            self.conn.commit()
        elif department_type=="EA":
            self.cursor.execute("INSERT INTO correct_answers_for_ea(department_id, year,tyt_fen,tyt_sosyal,tyt_matematik,tyt_turkce,ayt_cografya1,ayt_matematik,ayt_tarih1,ayt_edebiyat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", correct_answers)
            self.conn.commit()
        elif department_type=="SÖZ":
            self.cursor.execute("INSERT INTO correct_answers_for_soz(department_id, year, tyt_fen,tyt_sosyal,tyt_matematik,tyt_turkce,ayt_cografya1,ayt_cografya2,ayt_din,ayt_felsefe,ayt_tarih1,ayt_tarih2,ayt_edebiyat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", correct_answers)
            self.conn.commit()
        elif department_type=="DİL":
            self.cursor.execute("INSERT INTO correct_answers_for_dil(department_id, year,tyt_fen,tyt_sosyal,tyt_matematik,tyt_turkce,ydt_yabanci_dil) VALUES (?, ?, ?, ?, ?, ?, ?)", correct_answers)
            self.conn.commit()
        
    def get_cities(self,year,department_id):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="icerik_1020c"]/table""")))
        page_source = self.browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('div', {'id': 'icerik_1020c'})
        rows=rows = table.find_all('tr', attrs={'height': '20'})
        if len(rows)>1:
            rows=rows[1:]
            for row in rows:
                city=row.find_all('td')[0].text.strip()
                student_number=row.find_all('td')[1].text
                self.cursor.execute("select id from cities where city_name=?",(city,))
                city_id=self.cursor.fetchone()
                if city_id:
                    city_id=city_id[0]
                    self.index2+=1
                    city_students=[department_id,year,city_id,student_number]
                    city_students=tuple(city_students)
                    self.cursor.execute("INSERT INTO student_cities(department_id,year,city,student_number) VALUES (?, ?, ?, ?)", city_students)
                    self.conn.commit()

    def get_regions(self,year,department_id):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="icerik_1020ab"]/table""")))
        page_source = self.browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = self.browser.find_element(By.XPATH,"""//*[@id="icerik_1020ab"]/table[2]""").get_attribute('outerHTML')
        table = BeautifulSoup(table, 'html.parser')
        rows = table.find_all('tr')
        rows=rows[2:]
        for row in rows:
            region=row.find_all('td')[0].text.strip()
            student_number=row.find_all('td')[1].text
            self.cursor.execute("select id from Regions where region_name=?",(region,))
            region_id=self.cursor.fetchone()
            if region_id:
                region_id=region_id[0]
                self.index3+=1
                region_students=[department_id,year,region_id,student_number]
                region_students=tuple(region_students)
                self.cursor.execute("INSERT INTO student_regions(department_id,year,region,student_number) VALUES (?, ?, ?, ?)", region_students)
                self.conn.commit()

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
