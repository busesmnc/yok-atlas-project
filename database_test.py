import sqlite3
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import time
"""BUSE ŞUAN FAKÜLTELER, BÖLÜMLER VE CİNSİYETLER DATABASEDE VAR BU DOSYADA O DATALARI ÇEKİP GÖREBİLİRSİN
DATABASEİ DEĞİŞTİRMENE GEREK YOK NASIL YAPICAĞINI DA ÖRNEKTE GÖSTERDİM Bİ DE İŞİN İÇİNE WHERE FALAN GİRİNCE
BUNUN KOMUTLARI NORMAL SQLDEN FARKLI DİĞER CREATOR KISMI BİRAZ FARKLI İSTİYOSAN BURDAN SELECT * LA DATABASEDEN
ÇEKER ÖYLE CSV OLUŞTUTURSUN DAHA KOLAY OLUR SENİN İÇİNDE"""

db = "yok-atlas-project/yokatlas.db"
conn=sqlite3.connect(db)
cursor=conn.cursor()

cursor.execute("select id,department_name from departments")
deps=cursor.fetchall()
# print(deps)
cursor.execute("select * from faculties")
faculties=cursor.fetchall()
# print(faculties)
cursor.execute("drop table genders")
conn.commit()
cursor.execute("select * from genders")
genders=cursor.fetchall()
# print(genders)
# for dep in deps:
#     d_id=dep[0]
#     d_name=dep[1]
#     print(d_id)
#     cursor.execute("select male from genders where department_id=?",(d_id,))
#     data=cursor.fetchall()
#     males=[d[0] for d in data if isinstance(d[0],int)]
#     males.reverse()
#     cursor.execute("select female from genders where department_id=?",(d_id,))
#     data=cursor.fetchall()
#     females=[d[0] for d in data]
#     females.reverse()
#     cursor.execute("select year from genders where department_id=?",(d_id,))
#     data=cursor.fetchall()
#     years=[int(d[0]) for d in data]
#     years.reverse()
#     # y_axis=males+females
#     # y_axis.sort()
#     plt.subplot(1,2,1)
#     plt.plot(years, males, label='Males', marker='o', color='blue')  # Line for males
#     plt.xlabel('Years')
#     plt.ylabel('Number of Students')
#     plt.title("MALES")
#     plt.xticks(years)
#     plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

#     plt.subplot(1,2,2)
#     plt.plot(years, females, label='Females', marker='o', color='red')  # Line for females
#     plt.title("FEMALES")
#     plt.xlabel('Years')
#     # plt.legend()
#     # plt.yticks(y_axis)
#     plt.xticks(years) 
#     plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
#     plt.suptitle(d_name)
#     plt.show()


