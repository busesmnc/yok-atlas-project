import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('yokatlas.db')

# Get the list of all tables
cur = conn.cursor()
cur.execute("SELECT DISTINCT city_name FROM cities")
cities = cur.fetchall()

select_columns = []
for city in cities:
    city_name = city[0]
    select_columns.append(f"MAX(CASE WHEN c.city_name = '{city_name}' THEN sc.student_number ELSE 0 END) AS {city_name}")

# SQL sorgusunu dinamik olarak oluştur
query = f"""
    CREATE TABLE department_city_student_counts AS 
    SELECT 
        sc.year, 
        f.faculty_name, 
        d.department_name, 
        {', '.join(select_columns)}
    FROM 
        student_cities sc
    JOIN 
        cities c ON sc.city = c.id  -- cities tablosunu join ederek city_name alıyoruz
    JOIN 
        departments d ON sc.department_id = d.id
    JOIN 
        faculties f ON d.faculty_id = f.id
    GROUP BY 
        sc.year, f.faculty_name, d.department_name
    ORDER BY 
        sc.year, f.faculty_name, d.department_name;
"""


# Sorguyu çalıştır
cur.execute(query)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
cur.close()
# Close the connection
conn.close()
print(select_columns)