import sqlite3
import pandas as pd
import folium
from folium.plugins import HeatMap
from folium import Marker


department_id=input("""Select a department
1.Bilgisayar Mühendisliği
2.Bilgisayar ve Öğretim Teknolojileri Öğretmenliği
3.Biyomedikal Mühendisliği (İngilizce)
4.Biyomühendislik
5.Biyomühendislik (İngilizce)
6.Çevre Mühendisliği
7.Elektrik Mühendisliği
8.Elektronik ve Haberleşme Mühendisliği
9.Endüstri Mühendisliği
10.Endüstri Mühendisliği (İngilizce)
11.Fen Bilgisi Öğretmenliği
12.Fizik
13.Fotoğraf ve Video
14.Fransızca Mütercim ve Tercümanlık
15.Gemi İnşaatı ve Gemi Makineleri Mühendisliği
16.Gemi Makineleri İşletme Mühendisliği
17.Gıda Mühendisliği
18.Harita Mühendisliği
19.İktisat
20.İktisat (İngilizce)
21.İletişim ve Tasarımı
22.İlköğretim Matematik Öğretmenliği
23.İngilizce Öğretmenliği
24.İnşaat Mühendisliği
25.İnşaat Mühendisliği (İngilizce)
26.İstatistik
27.İşletme
28.İşletme (İngilizce)
29.Kimya
30.Kimya (İngilizce)
31.Kimya Mühendisliği
32.Kimya Mühendisliği (İngilizce)
33.Kontrol ve Otomasyon Mühendisliği
34.Kontrol ve Otomasyon Mühendisliği (İngilizce)
35.Kültür Varlıklarını Koruma ve Onarım
36.Kültür Varlıklarını Koruma ve Onarım (KKTC Uyruklu)
37.Makine Mühendisliği
38.Matematik
39.Matematik Mühendisliği
40.Matematik Mühendisliği (İngilizce)
41.Matematik Mühendisliği (KKTC Uyruklu)
42.Mekatronik Mühendisliği
43.Mekatronik Mühendisliği (İngilizce)
44.Mekatronik Mühendisliği (İngilizce) (KKTC Uyruklu)
45.Metalurji ve Malzeme Mühendisliği
46.Metalurji ve Malzeme Mühendisliği (İngilizce)
47.Mimarlık
48.Mimarlık (İngilizce)
49.Moleküler Biyoloji ve Genetik
50.Okul Öncesi Öğretmenliği
51.Rehberlik ve Psikolojik Danışmanlık
52.Sanat ve Kültür Yönetimi
53.Sınıf Öğretmenliği
54.Siyaset Bilimi ve Uluslararası İlişkiler
55.Sosyal Bilgiler Öğretmenliği
56.Şehir ve Bölge Planlama
57.Türk Dili ve Edebiyatı
58.Türkçe Öğretmenliği
""")
department_id=int(department_id)
year=input("""Select a year (2024,2023,2022,2021)""")
year=int(year)
conn = sqlite3.connect("yokatlas.db")

query = """
select city_name as city ,lat,lon,student_number as students from student_cities 
left join Cities on student_cities.city=Cities.id left join departments on departments.id=student_cities.department_id 
where department_id={} and year={};
""".format(department_id,year)
data = pd.read_sql_query(query, conn)
conn.close()
m = folium.Map(location=[38.9637, 35.2433], zoom_start=6) 
heat_data = [[row['lat'], row['lon'], row['students']] for index, row in data.iterrows()]

HeatMap(heat_data).add_to(m)
for index, row in data.iterrows():
    # Marker (işaretçi) ekleyin ve öğrenci sayısını etiket olarak gösterin
    Marker([row['lat'], row['lon']], 
           popup=f"{row['city']}: {row['students']} students").add_to(m)
file_path="heatmaps/department_{}_year_{}_heatmap.html".format(department_id,year)
m.save(file_path) 
print("Heatmap is created...")
