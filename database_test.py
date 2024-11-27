import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('yokatlas.db')

# Get the list of all tables
cursor = conn.cursor()
cursor.execute("select faculties.id as faculty_id , faculties.faculty_name as faculty_name ,"
               " departments.id as department_id, departments.department_name, "
               "departments.d_type as department_type, genders.year as year, "
               "genders.male, genders.female, total_student_number.male as total_male_number, "
               "total_student_number.female as total_female_number, "
               "total_student_number.total_number as total_sdt_number from departments"
               " LEFT JOIN genders on departments.id = genders.department_id"
               " LEFT JOIN faculties on departments.faculty_id = faculties.id"
               " LEFT JOIN total_student_number on departments.id = total_student_number.department_id"
               " GROUP by departments.department_name, genders.year;")
gender_table = cursor.fetchall()
# for row in gender_table:
#     print(row)


# Close the connection
conn.close()
