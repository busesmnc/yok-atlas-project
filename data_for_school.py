import sqlite3
from prettytable import PrettyTable
from colorama import Fore, Back, Style, init

init(autoreset=True)
conn=sqlite3.connect("yokatlas.db")
cursor=conn.cursor()
order=int(input(Fore.CYAN +"""
1.Genders for school
2.Prefered for school
3.Quota for school
4.Student Number for school
5.Total Student for school
6.Total Gender Percentages for school
7.Exchange Program for school
8.Academicians for school
9.Settlement for school
10.Quota Occupancy for school
11.Cities for school
12.Regions for school
"""))

def genders_for_school(years):
    for year in years:
        year=int(year)
        table = PrettyTable()

        cursor.execute("""
        select round(CAST(SUM(male) AS FLOAT) / (CAST(SUM(male) AS FLOAT) + CAST(SUM(female) AS FLOAT)) * 100,2) as male_percentage,
        round(CAST(SUM(female) AS FLOAT) / (CAST(SUM(male) AS FLOAT) + CAST(SUM(female) AS FLOAT)) * 100,2) as female_percentage from genders where year=?;
        """, (year,))
        table.field_names = ["Male Percentage","Female Percentage"]

        output=cursor.fetchone()
    
            
        table.add_row(list(output))
        print(Fore.GREEN+Style.BRIGHT+"\n\nMale and Female Percentage in {}".format(year))
        print(table)
        print("\n\n")


def prefered_for_school(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select sum(prefered) as total_prefered from general_infos where year=?;
        """, (year,))

        output=cursor.fetchone()
        table = PrettyTable()
        table.field_names = ["Prefered"]
        table.add_row(list(output))
        print(Fore.GREEN+Style.BRIGHT+"\n\nPrefered in {}".format(year))
        print(table)
        print("\n\n")

def quota_for_school(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select sum(quota) as total_quota from general_infos where year=?;
        """, (year,))

        output=cursor.fetchone()
        table = PrettyTable()
        table.field_names = ["Quota"]
        table.add_row(list(output))
        print(Fore.GREEN+Style.BRIGHT+"\n\nQuota in {}".format(year))
        print(table)
        print("\n\n")

def student_number_for_school(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select sum(s_number) as total_student from general_infos where year=?;
        """, (year,))

        output=cursor.fetchone()
        table = PrettyTable()
        table.field_names = ["Student Number"]
        table.add_row(list(output))
        print(Fore.GREEN+Style.BRIGHT+"\n\nStudent Number in {}".format(year))
        print(table)
        print("\n\n")

def total_student_number_for_school(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select sum(total_number) as total_student from total_student_number where year=?;
        """, (year,))

        output=cursor.fetchone()
        table = PrettyTable()
        table.field_names = ["Total Student Number"]
        table.add_row(list(output))
        print(Fore.GREEN+Style.BRIGHT+"\n\nTotal Student in {}".format(year))
        print(table)
        print("\n\n")

def total_genders_for_school(years):
    for year in years:
        year=int(year)
        table = PrettyTable()

        cursor.execute("""
        select round(cast(sum(male) as float)/(cast(sum(total_number) as float))*100,2) as male_percentage,
        round(cast(sum(female) as float)/(cast(sum(total_number) as float))*100,2) as female_percentage  from total_student_number where year=?;
        """, (year,))
        table.field_names = ["Male Percentage","Female Percentage"]

        output=cursor.fetchone()
    
            
        table.add_row(list(output))
        print(Fore.GREEN+Style.BRIGHT+"\n\nMale and Female Percentage in {}".format(year))
        print(table)
        print("\n\n")

def exchange_program_for_school(years):
    for year in years:
        year=int(year)
        table = PrettyTable()

        cursor.execute("""
        select sum(incoming) as total_incoming, sum(leaving) as total_leaving from exchange_program where year=?;
        """, (year,))
        table.field_names = ["Incoming Student","Leaving Student"]

        output=cursor.fetchone()
    
            
        table.add_row(list(output))
        print(Fore.GREEN+Style.BRIGHT+"\n\nExchange Program in {}".format(year))
        print(table)
        print("\n\n")

def academician_for_school(years):
    for year in years:
        year=int(year)
        table = PrettyTable()

        cursor.execute("""
        select round(CAST(SUM(proffesor) AS FLOAT) / (CAST(SUM(proffesor) AS FLOAT) + CAST(SUM(assoc_prof) AS FLOAT)+ CAST(SUM(phd) AS FLOAT)) * 100,2) as professor_percentage,
        round(CAST(SUM(assoc_prof) AS FLOAT) / (CAST(SUM(proffesor) AS FLOAT) + CAST(SUM(assoc_prof) AS FLOAT)+ CAST(SUM(phd) AS FLOAT)) * 100,2) as assoc_professor_percentage,
        round(CAST(SUM(phd) AS FLOAT) / (CAST(SUM(proffesor) AS FLOAT) + CAST(SUM(assoc_prof) AS FLOAT)+ CAST(SUM(phd) AS FLOAT)) * 100,2) as phd_percentage 
        from academicians where year=?;
        """, (year,))
        table.field_names = ["Professor Percentage","Associate Professor Percentage","PHD Percentage"]

        output=cursor.fetchone()
    
            
        table.add_row(list(output))
        print(Fore.GREEN+Style.BRIGHT+"\n\nAcademician Percentages in {}".format(year))
        print(table)
        print("\n\n")

def settlement_for_school(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select round(cast(sum(s_number) as float)/(cast(sum(prefered) as float))*100,2) as settlement_percentage from general_infos where year=?;
        """, (year,))

        output=cursor.fetchone()
        table = PrettyTable()
        table.field_names = ["Settlement Percentage"]
        table.add_row(list(output))
        print(Fore.GREEN+Style.BRIGHT+"\n\nSettlement Percentage in {}".format(year))
        print(table)
        print("\n\n")

def quota_occupancy_for_school(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select round(cast(sum(s_number) as float)/(cast(sum(quota) as float))*100,2) as quota_percentage from general_infos where year=?;
        """, (year,))

        output=cursor.fetchone()
        table = PrettyTable()
        table.field_names = ["Quota Occupancy"]
        table.add_row(list(output))
        print(Fore.GREEN+Style.BRIGHT+"\n\nQuota Occupancy in {}".format(year))
        print(table)
        print("\n\n")

def prefered_percentage_for_faculties(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        SELECT faculty_name, ROUND(
        CAST(SUM(prefered) AS FLOAT) / (
            SELECT SUM(prefered) 
            FROM general_infos 
            WHERE year = ?
        ) * 100, 2) AS prefered_percentage
        FROM general_infos LEFT JOIN departments ON departments.id = department_id
        LEFT JOIN faculties ON faculties.id = faculty_id
        WHERE year = ? GROUP BY faculty_name ORDER BY prefered_percentage DESC;
        """, (year,year))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["No","Faculty Name", "Prefered Percentage in School"]
        for index, row in enumerate(output, start=1):
            table.add_row([index] + list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nPrefered Percentage in School in {}".format(year))
        print(table)
        print("\n\n")

def cities_for_school(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select city_name,sum(student_number) as total_student from student_cities left join Cities on Cities.id=city 
        where year=? group by city_name order by total_student desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["City","Student Number"]
        for row in output:
            table.add_row(list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nStudent Number in Each City in {}".format(year))
        print(table)
        print("\n\n")

def regions_for_school(years):
    for year in years:
        year=int(year)
        cursor.execute("""
        select region_name_en,sum(student_number) as total_student from student_regions left join Regions on Regions.id=region 
        where year=? group by region_name_en order by total_student desc;
        """, (year,))

        output=cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Region","Student Number"]
        for row in output:
            table.add_row(list(row))
        print(Fore.GREEN+Style.BRIGHT+"\n\nStudent Number in Each Region in {}".format(year))
        print(table)
        print("\n\n")

years=input(Fore.YELLOW+"\nSelect a year(2024,2023,2022,2021)\nNote:You can choose more than one value, split with ','\n").split(",")
if order==1: 
    genders_for_school(years)
elif order==2:
    prefered_for_school(years)
elif order==3:
    quota_for_school(years)
elif order==4:
    student_number_for_school(years)
elif order==5:
    total_student_number_for_school(years)
elif order==6:
    total_genders_for_school(years)
elif order==7:
    exchange_program_for_school(years)
elif order==8:
    academician_for_school(years)
elif order==9:
    settlement_for_school(years)
elif order==10:
    quota_occupancy_for_school(years)
elif order==11:
    cities_for_school(years)
elif order==12:
    regions_for_school(years)

conn.close()