import sqlite3
"""BUSE ŞUAN FAKÜLTELER, BÖLÜMLER VE CİNSİYETLER DATABASEDE VAR BU DOSYADA O DATALARI ÇEKİP GÖREBİLİRSİN
DATABASEİ DEĞİŞTİRMENE GEREK YOK NASIL YAPICAĞINI DA ÖRNEKTE GÖSTERDİM Bİ DE İŞİN İÇİNE WHERE FALAN GİRİNCE
BUNUN KOMUTLARI NORMAL SQLDEN FARKLI DİĞER CREATOR KISMI BİRAZ FARKLI İSTİYOSAN BURDAN SELECT * LA DATABASEDEN
ÇEKER ÖYLE CSV OLUŞTUTURSUN DAHA KOLAY OLUR SENİN İÇİNDE"""

db = "yok-atlas-project/yokatlas.db"
conn=sqlite3.connect(db)
cursor=conn.cursor()

cursor.execute("select * from departments")
deps=cursor.fetchall()
# print(deps)
cursor.execute("select * from faculties")
faculties=cursor.fetchall()
# print(faculties)
cursor.execute("select * from genders")
genders=cursor.fetchall()
# print(genders)


